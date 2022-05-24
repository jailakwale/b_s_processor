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
  
def clean_format(x):
    x = x.upper()
    mapping = {
         "RE V":"REV",
         "R EV":"REV",
         "MO B":"MOB",
         "M OB":"MOB",
        "N IBSS":"NIBSS"
        }
    
    for k, v in mapping.items():
        x = x.replace(k, v)
    return x

def check_transact(l_key_words):
    tr_list = l_key_words
    def is_transaction(x,transact_list=tr_list):
        return any( el in x for el in transact_list) 
    return is_transaction
  
loan_transact = ["LOAN",'INTEREST','REPAYMENT',"LIQ","FUND HELD"]
reversal_transact = ["REV","REFUND","REVERSAL"]
charges_transact = ["CHARGE","FEE"]
cash_transact = ["AWR@", "CASHBACK","CASH"]



def is_salary(x):
    return (("SALARY" in x or "SAL" in x or "OTHERPYMT" in x) and "SALES" not in x and "FIP:MB:" not in x)

def is_transfert(x):
    return(("TO:" in x or "TRF" in x or "TNF" in x  or "TRANSFER" in x  or "/TO" in x or "TO:" in x)\
       and "VAT" not in x\
       and "FEE" not in x\
       and "REFUND" not in x\
       and "COMMISSION" not in x\
       and "REV" not in x)


def is_payment(x):
    if any([not(is_loan(x)),
        not(is_reversal(x)),
        not(is_charges(x)),
        not(is_transfert(x)),
        not(is_salary(x))]):
        return  True
      

is_loan = check_transact(loan_transact)
is_reversal = check_transact(reversal_transact)
is_charges = check_transact(charges_transact)
is_cash = check_transact(cash_transact)

def check_transaction(x):
    tr_id = ["LOAN","REVERSAL","CHARGES","CASH","SALARY","TRANSFERT"]
    tr = [is_loan, is_reversal, is_charges, is_cash, is_salary, is_transfert]
    res = None
    for idx,t in enumerate(tr):
        if t(x):
            res=tr_id[idx]
            break
    if res ==None:
        res="PAYMENT"
    
    return res

  
def classify_liberta_leasing_convert_handler(event, context):
    '''
    function whose responsibility is to classify
    '''
    OUTPUT_FILE_NAME = os.environ["output_file_name"]
    OUTPUT_BUCKET_NAME = os.environ["output_bucket_name"]
    
    if 'body' in list(event.keys()):
        event = json.loads(event['body'])
        
    input_file_url = event["url"]
    output_format = event["format"]
    model_Doc2Vec_path = event["model_Doc2Vec_path"]
    model_NLP_path = event["model_NLP_path"]
    
    f_path = download_url(input_file_url, "xlsx")
    
    try:
        # when no error :process and returns json
        dest_file = f_path
        dataframe_file = pd.read_excel(dest_file)
        # the narration columns varies from 1 bank to another
        bank_columns = { "WEMA_BANK": "Narration",
                         "UBA_BANK":"Narration",
                         "STANDARD_CHARTERED_BANK": "Transaction",
                         "POLARIS_BANK":"Details",
                         "ACCESS_BANK":"Description"}
        
        column_name = bank_columns[output_format]        
        
        # upper
        dataframe_file["UPPER"] = dataframe_file[column_name].apply(lambda x: clean_format(x))
        # classe
        dataframe_file["CLASSE"] = dataframe_file["UPPER"].apply(lambda x: check_transaction(x))
        # id
        dataframe_file["BANK_ID"] = output_format
        
        # s3 save file
        s3_client = boto3.client('s3')
        
        # save to local file excel
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
