#!/usr/bin/env python

import glob2
import os
import shutil
import tabula
import argparse
from tqdm import tqdm
import pandas as pd
import numpy as np
import requests
import json
import base64

__author__ = "Assan Sanogo"
__copyright__ = "Copyright 2007, Liberta Leasing"
__credits__ = ["Liberta Leasing", "Assan Sanogo"]
__license__ = "private"
__version__ = "0.1"
__maintainer__ = "Assan Sanogo"
__email__ = "predicteev@gmail.com"
__status__ = "Production"


GT_HEADER = ["Trans. Date","Value. Date","Reference","Debits","Credits","Balance","Originating Branch","Remarks"]

def extract_list_dataframes(dataframes_list, out_path):
    
    for i,d in enumerate(dataframes_list):
        try:
            # set the header to each sub dataframe
            d.columns = GT_HEADER
            # save locally for debug purposes (each extracted dataframe has a positional suffix (=index))
            d.to_csv(out_path.replace(".csv",f"{str(i)}.csv"), sep=';')
        except Exception as e:
            # if the dataframe is malformed remove it from the list of processable dataframes
            print(i)
            dataframes_list.remove(d)
    return dataframes_list

def simple_df_clean(m_df):
    '''
    function which cleans non informative data ("Remarks and Trans.date")
    ocurring while tabula extraction
    '''
    m_df = m_df[m_df['Remarks']!= 'Remarks']
    m_df = m_df[m_df['Remarks']!= 'Balance as at Last Transaction.']
    m_df = m_df[m_df["Trans. Date"] != 'Trans. Date']
    return m_df

def transactions(m_df):
    '''
    function which keeps transactions index, the last transaction idx and adds an artificial last transaction
    '''
    transactions_df = m_df[~m_df["Trans. Date"].isna()].copy()
    transactions_idx = list(transactions_df.index)
    max_transactions_idx = max(transactions_idx)
    transactions_df.loc[max_transactions_idx + 1,'Trans. Date'] = '99-Apr-9999'
    return  transactions_df,transactions_idx,max_transactions_idx
                           
                           
def postprocess(m_df, transaction_not_null_df):
    '''
    reconstruct the financial operations which overflow to the next line in 1 single text
    '''

    # all the indexes of the transaction with dates
    index_with_dates = transaction_not_null_df.index

    operation_descr = {}
    for step_date in index_with_dates:
        operation_descr[str(step_date)] = []
    
    # safety check : index is not nan                       
    if not np.isnan(index_with_dates.values[0]):

        for idx, step in enumerate(index_with_dates):
            # iteration until we reach the last recorded transaction (excluded)
            if idx < len(index_with_dates)-1:
                for ind in range(index_with_dates[idx], index_with_dates[idx+1], 1):
                    if str(m_df.loc[ind, 'Remarks']) != 'nan':
                        operation_descr[str(step)] += [str(m_df.loc[ind, 'Remarks'])]
                           
            # last iteration: after reaching the last recorded transaction until the artificial last operation
            else:
                for ind in range(index_with_dates[idx], m_df.shape[0], 1):
                    if str(m_df.loc[ind, 'Remarks']) != 'nan':
                        operation_descr[str(step)] += [str(m_df.loc[ind, 'Remarks'])]
        # final cleanup (remove carriage to prevent csv malformation)
        for key in operation_descr.keys():
            operation_descr[key] = (''.join(operation_descr[key])).replace('\r',' ')

    return operation_descr         


def recombine_dataframe(operations_description_dict, transaction_not_null, account_type, bank_id):
    '''
    reconstruct the final dataset with all original transaction information plus the annotations
    '''
    # Dataframe of the transactions
    if  not 'nan' in operations_description_dict.keys():
        annotations = pd.DataFrame.from_dict(operations_description_dict,  orient='index', columns=['Remarks_processed'])
        dataset_recombined = pd.concat([transaction_not_null.reset_index(drop=True), annotations.reset_index(drop=True)], axis=1)
        dataset_recombined['ACCOUNT_TYPE'] = account_type
        dataset_recombined['BANK_ID'] = bank_id

        dataset_recombined = dataset_recombined[['Trans. Date','Reference','Value. Date','Debits','Credits','Balance','Remarks_processed','ACCOUNT_TYPE','BANK_ID']]
    return dataset_recombined

                           
def process_bank_statements(b_statement, out_format ='csv',ll_bank_id = "GTBANK", ll_account_type="savings"):
    '''
    Method to transform a list of Bank statements paths into a list of .CSV
    '''
    response = {}
    # check the type of b_statements_gt_bank
    if isinstance(b_statement, str):
        b_statement = [b_statement]
    n_statements = len(b_statement)
    assert n_statements !=0
                           
    #loop over the list of bank statements 
    for idx, bk_st in tqdm(enumerate(b_statement)):
        # input filename
        inp = bk_st
        local_inp = inp.split("/")[-1]
        #shutil.copy(inp, local_inp)
        os.chdir("/tmp")
        
        # output filename
        out = bk_st.replace(".pdf","_output.csv")
        
        # 1. convert to csv by default
        df_list = tabula.read_pdf(local_inp, multiple_tables=True, lattice= True, pages='all')
        header_shape = df_list[1].shape[1]
        df_list = [datafram for datafram in df_list if (header_shape !=2 and datafram.shape[0]!=0) ]
                           
        # 2. extract dataframes (& save to disk for debug)                 
        df_list = extract_list_dataframes(df_list, out)
        
        # 3. concat each dataframe into 1
        master_df = pd.concat(df_list).reset_index(drop=True)
                           
        # 4. clean non informative cells
        master_df = simple_df_clean(master_df).reset_index(drop=True)
        
        # 5. store informations about the transactions
        tr_df, tr_idx, max_tr_idx = transactions(master_df)
                     
        # 6. postprocessing of transactions 
        operations = postprocess(master_df, tr_df)
        
        # 7. cleaned dataframe with aligned transactions
        final_dataframe = recombine_dataframe(operations, tr_df, ll_account_type, bank_id=ll_bank_id)
        
        # 8. save to disk for debug
        final_dataframe.to_csv(out, 
                               sep=';', 
                               index = False, header=True)
        
        # json response
        response[str(idx)] = {"name":bk_st, 
                              "body":final_dataframe.to_json(orient="records")}
                           
        return response                  
                            
def download_url(url):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if ".pdf" in el][0]
    # open a file to dump the stream in
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    return f'/tmp/{file_name}'

def lliberta_leasing_convert_handler(event, context):
    '''
    formatting of the lambda handler to be compatible with by AWS
    '''
    # information extracted from the event payload

    # when no error :process and returns json

    return({ 'statusCode': 200,
            'body': json.dumps(base64.b64decode(event['body']).decode('utf-8'))})

def liberta_leasing_convert_handler(event, context):
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
        processed_dataframe = process_bank_statements(f_name, output_format)
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(processed_dataframe)}
       
    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
                
    #return process_bank_statements(f_name, output_format)


def http_liberta_leasing_convert_handler(event, context):
    '''
    formatting of the lambda handler to be compatible with by AWS
    '''
    # information extracted from the event payload
    event = json.loads(base64.b64decode(event['body']).decode('utf-8'))
    input_file_url = event["url"]
    output_format = event["format"]
    
    # download file locally and keep the filename
    f_name = download_url(input_file_url)
    
    try:
        # when no error :process and returns json
        processed_dataframe = process_bank_statements(f_name, output_format)
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 200,
                'body': json.dumps(processed_dataframe)}
       
    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
                'statusCode': 400,
                'body': json.dumps(str(e))}
                
    #return process_bank_statements(f_name, output_format)
        
if __name__ =='__main__':
    
    liberta_leasing_parser = argparse.ArgumentParser()
    liberta_leasing_parser.add_argument('--input_file', action='store', type=str, required=True)
    liberta_leasing_parser.add_argument('--output_format', action='store', type=str, required=True, default='csv')
    
    args = liberta_leasing_parser.parse_args()
    f_name = args.input_file
    output_format = args.output_format
    print(process_bank_statements(f_name, output_format))
