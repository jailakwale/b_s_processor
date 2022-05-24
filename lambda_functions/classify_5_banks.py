import os
import json
import shutil
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import glob2
import requests
import base64
from zipfile import ZipFile
from tqdm import tqdm
import gensim
import joblib
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

import numpy as np


def download_url(url, ext):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if (f".{ext}" in el)][0]
    os.makedirs('/tmp', exist_ok=True)
    
    # open a file to dump the stream in
    print(r)
    print(file_name)
    
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(os.stat(f'/tmp/{file_name}').st_size)

    return f'/tmp/{file_name}'
  

def import_model(model_path):
    model_Doc2vec = gensim.models.Doc2Vec.load(model_path)
    return model_Doc2vec


  # problem with pngs
    
    
def simple_preprocess(df, col_name):
    """
    simple data preprocessing step for NLP embeddings
    """
    df[col_name] = df[col_name].str.replace("/"," ")
    df_new = df.copy()
    temp_df = df_new[col_name].str.extractall(r'([a-zA-Z]+)')
    df_new.loc[:, col_name]  = temp_df.groupby(level=0).apply(lambda x: (' ').join(x[0].values).upper()).copy()
    return df_new

def doc2vec_transformer(x, model):
    ''' returns doc2vec embedding(sentence-based)''' 
    return model.infer_vector(x)


def doc_2_vec_transformer(df, col_name="Description", model_d2vec=None):
    df['Vect_D2V'] = df[col_name].apply(lambda x : doc2vec_transformer(str(x).split(" "), model_d2vec))
    return df


def define_model_keys(model):
    '''returns  the lookup dictionary following the structure: {key : vector}
    ''' 
    
    my_dict = {}
    for k in model.wv.key_to_index.keys():
        my_dict[k] = model.wv.get_vector(key=k)
    return my_dict
    
    
    
    
  
def classify_liberta_leasing_convert_handler(event, context):
    '''
    function whose responsibility is to classify
    '''

    if 'body' in list(event.keys()):
        event = json.loads(event['body'])
    
    OUTPUT_FILE_NAME = event["output_file_name"]
    OUTPUT_BUCKET_NAME = event["output_bucket_name"]
    input_file_url = event["url"]
    output_format = event["format"]
    model_Doc2Vec_path = event["model_Doc2Vec_path"]
    model_NLP_path = event["model_NLP_path"]
    
    # download models (doc2vec) from their respective urls
    
    local_model_Doc2Vec_path = download_url(model_Doc2Vec_path, "model")
    #model_Doc2Vec = import_model(local_model_Doc2Vec_path) 
    
    # download models (classifier) from their respective urls
    local_model_NLP_path = download_url(model_NLP_path,"pkl")
    #model_NLP = joblib.load(local_model_NLP_path)
    
    f_path = download_url(input_file_url, "xlsx")
    

    try:
        # when no error :process and returns json
        dest_file = f_path
        dataframe_file = pd.read_excel(dest_file, engine="openpyxl")
        # the narration columns varies from 1 bank to another
        bank_columns = { "WEMA_BANK": "Narration",
                         "UBA_BANK":"Narration",
                         "STANDARD_CHARTERED_BANK": "Transaction",
                         "POLARIS_BANK":"Details",
                         "ACCESS_BANK":"Description"}
        
        # define the column name based on the bank type
        column_name = bank_columns[output_format]  
        
        # we load the downloaded model_path
        model_doc2vec = Doc2Vec.load("/tmp/other_gensim_doc_2_vec.model")
        
        #transform the description column
        res_doc2vec = doc_2_vec_transformer(dataframe_file, 
                                    col_name="Description", 
                                    model_d2vec=model_doc2vec).reset_index(drop=True)
        
        # load the model
        sklearn_model_filename = '/tmp/other_rf_classifier.pkl'
        loaded_model = joblib.load(sklearn_model_filename)
        additional_columns = ["Debit","Credit"]
        # replace special characters in Debit & Credit column
        for col in ["Debit","Credit"]:
            res_doc2vec[col] = res_doc2vec[col].str.replace(",|-","").fillna("0")
            res_doc2vec[col] = res_doc2vec[col].str.replace("","0").astype('float')
            
        
        # process the "Vect_D2V"
        to_pred = pd.DataFrame(list([list(el) for el in res_doc2vec["Vect_D2V"].values]))
        vect_data = pd.concat([res_doc2vec[additional_columns].fillna(0), to_pred], axis=1)
        
        # store in both columns data (predictions + bank_id)
        dataframe_file["PREDICTION"] = loaded_model.predict(vect_data)
        dataframe_file["BANK_ID"] = output_format
        
        # create a boto3 client
        try:
            s3_client = boto3.client('s3', region_name='eu-west-1')
            location = {'LocationConstraint':'eu-west-1'}
            s3_client.create_bucket(Bucket=OUTPUT_BUCKET_NAME, CreateBucketConfiguration=location)
        except Exception as e:
            print("the bucket already exists")
            pass

        # save file locally
        local_file_name = '/tmp/classified_file.xlsx'
        dataframe_file.to_excel(local_file_name, index=None)
        
        response = s3_client.upload_file(local_file_name, OUTPUT_BUCKET_NAME, OUTPUT_FILE_NAME)
        upload_details = s3_client.generate_presigned_url('get_object', Params={"Bucket":OUTPUT_BUCKET_NAME, "Key":OUTPUT_FILE_NAME}, ExpiresIn = 100)
        
        
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(str(upload_details))}

    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
