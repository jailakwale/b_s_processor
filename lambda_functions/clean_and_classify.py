#!/usr/bin/env python

import os
import shutil
import sklearn
from tqdm import tqdm
import pandas as pd
import numpy as np
import math
import requests
import json
import base64
import re
import gensim.models
from joblib import dump, load

__author__ = "Assan Sanogo"
__copyright__ = "Copyright 2007, Liberta Leasing"
__credits__ = ["Liberta Leasing", "Assan Sanogo"]
__license__ = "private"
__version__ = "0.1"
__maintainer__ = "Assan Sanogo"
__email__ = "predicteev@gmail.com"
__status__ = "Production"



CATEGORIES = ['bank_charges', 'cash', 'commission', 'loan', 'maintenance',
       'reversal', 'salary', 'tax', 'transfert', 'utility']


def download_url(url):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    # the pdf filename is extracted from the presigned url

    file_name = url.split("/")[-1]
    # open a file to dump the stream in
    
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    return f'/tmp/{file_name}'

def process_descriptions(sentences):
    sentences_from = [re.sub("([\w]+) ([f|F]rom)([\w\W\s]+)", r"\1 from \3", str(el)) for el in sentences]
    sentences_from = [re.sub("([\w]+) ([f|F]rom)([\w\W]+)", r"\1 from \3", str(el)) for el in sentences_from]
    sentences_from = [re.sub("([\w]+) ([v|V]ia)([\w\W\s]+)", r"\1 via \3", str(el)) for el in sentences_from]
    sentences_from = [re.sub("(\s\w{1}\s)","", str(el)) for el in sentences_from]
    sentences_from_no_underscore = [el.replace("_","") for el in sentences_from]
    sentences_from_no_underscore = [(" ").join([et.strip() for et in el.split() if len(et) >1]) for el in sentences_from_no_underscore if not len(el.strip()) <1]
    return sentences_from_no_underscore


def clean_tokens(model, tokenized_text_l):
    toks = [[k if k in model.wv.key_to_index.keys() else 'UNK' for k in tokenized_text] for tokenized_text in tokenized_text_l ]
    return toks


def clean_na_symbols(sentences):
    res = []
    for el in sentences :
        try:
            # if number only
            if not math.isnan(float(el)):
                 res.append(el)
                    
            # replace nan values by empty space
            else:
                res.append(" ")
             # the exception clause is the clause for "normal sentences ( just with potential special characters)
        except Exception as e:
            sd = (" ").join([el.replace("_","").replace("(","").replace(")","") for el in el.split(" ") if len(el) >1])
            res.append(sd)
            
    # limit sentences to 10 tokens MAX        
    res_sentences = [el.split(" ")[:10] + ['UNK'] * (10 - len(el.split(" "))) for el in res]
    
    res_sen = [(" ").join(el) for el in res_sentences]
    
    # list of stop words/forbidden words
    forbidden_words = pd.read_csv("./forbidden_words_cs.txt", sep=',', names =["word"]).values
    
    # replace unauthorized words by UNK token
    tokenized_text_l = [[elt if elt not in forbidden_words else "UNK" for elt in el.split() ] for el in res_sen ]
    
    # clean tokens ( out of dictionary tokens)
    model = load(download_url(url='https://assansanogos3.s3.eu-west-1.amazonaws.com/word2vec_1.joblib'))
    toks = clean_tokens(model, tokenized_text_l)
    
    classifier_model = load(download_url(url='https://assansanogos3.s3.eu-west-1.amazonaws.com/classifier_1.joblib'))
    
    # embedding transformation
    df_vect = pd.DataFrame(np.array([np.array([model.wv[el] for el in tok]).mean(axis = 0) for tok in toks ]))

    # class prediction
    preds = classifier_model.predict(df_vect)
    
    return preds
  
    
def clean_bank_statements(file_name, out_format):
    dtf = pd.read_csv(file_name.replace("\"",""), sep=';')
    dtf["filtered_description"] = dtf["Remarks_processed"].str.upper()
    sentences = list(dtf["filtered_description"].values)
    sentences = process_descriptions(sentences)
    dtf["preds"] = clean_na_symbols(sentences)

    df = dtf.copy()
    
    df["Debits"] = df["Debits"].str.replace(",","").astype('float').fillna(0)
    df["Credits"] = df["Credits"].str.replace(",","").astype('float').fillna(0)
    for c in CATEGORIES:
        df[f'category_{str(c)}'] = (df["preds"] == c).astype('float') * (-1*df["Debits"] + df["Credits"])
    df = df.iloc[:-1]
    df.index = pd.to_datetime(df["Trans. Date"])
    l_columns = [f'category_{str(c)}' for c in CATEGORIES]

    summary_decision = df[l_columns].groupby(pd.Grouper(level="Trans. Date",freq='M')).sum()
    summations = pd.DataFrame(summary_decision.sum()).transpose()
    summations.index = ["Total"]
    decision_df = pd.concat([summary_decision, summations], axis=0)
    return (dtf.to_json( orient='records'), decision_df.to_json( orient='records'))
    #return str(sentences)
    

def liberta_leasing_classify_handler(event, context):
    '''
    formatting of the lambda handler to be compatible with by AWS
    '''
    # information extracted from the event payload
    input_file_url = event["url"]
    output_format = event["format"]
    
    # download file locally and keep the filename
    f_name = download_url(input_file_url)
    
    try:
        # when no error :process and returns json
        processed_dataframe_json, decision_json = clean_bank_statements(f_name, output_format)
        
        return {
              "headers": {
                     "Content-Type": "application/json"
              },
              "statusCode": 200,
              "body": {
                     "classified": json.dumps(processed_dataframe_json),
                     "decision": json.dumps(decision_json)
              }
       }

       
    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
                
    #return process_bank_statements(f_name, output_format)


