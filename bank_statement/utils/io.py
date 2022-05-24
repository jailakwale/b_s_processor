import os
import glob2
import tabula
import pandas as pd
import numpy as np
import tqdm
import shutil


def produce_output_files(file_signature):
    '''
    save the processed files for Ayo's team
    '''
    list_of_output_files = glob2.glob(f"./data/*/engineered/{file_signature}")

    out = "./out"
    os.makedirs(out, exist_ok=True)
    for el in tqdm.tqdm(list_of_output_files):
        bank_user = (el.split("/")[2])
        f_name = (el.split("/")[-1])
        shutil.copyfile(el, os.path.join(out, bank_user + "_" + f_name))

def process_bank_statements(b_statements_gt_bank, out_format ='csv'):
    '''
    Method to transform a list of Bank statements paths into a list of .CSV
    '''
    
    n_statements = len(b_statements_gt_bank)
    for bk_st in tqdm(b_statements_gt_bank):
        inp = bk_st
        out = bk_st.replace(".pdf","output.csv")
        tabula.convert_into(inp, out, output_format=out_format)
        
    print( f"{n_statements} bank_statements processed!")

def bank_statement_to_dataframe(b_statement_gt_bank, mult=True, pages_all='all'):
    '''
    Function to transform to dataframe a Bank statement pdf
    
    b_statement_gt_bank: a statement path of a Bank statement pdf
    mult: consider various tables in the document
    pages_all: keep all pages if 'all'
    '''
    df = tabula.read_pdf(b_statement_gt_bank,
                         multiple_tables=mult,
                         pages=pages_all)
    return df

def bank_statement_to_dataframe_plus(b_statement_gt_bank, mult=True, pages_all='all'):
    '''
    Function to transform to dataframe a Bank statement pdf
    
    b_statement_gt_bank: a statement path of a Bank statement pdf
    mult: consider various tables in the document
    pages_all: keep all pages if 'all'
    '''
    df = tabula.read_pdf(b_statement_gt_bank,
                         multiple_tables=mult,
                         lattice= True,
                         pages=pages_all)
    return df

def process_bank_statements(b_statements_gt_bank, out_format ='csv'):
    '''
    Method to transform to csv a list of Bank statements paths
    '''
    
    n_statements = len(b_statements_gt_bank)
    for bk_st in tqdm(b_statements_gt_bank):
        inp = bk_st
        out = bk_st.replace(".pdf","output.csv")
        tabula.convert_into(inp, out, output_format=out_format)
        
    print( f"{n_statements} bank_statements processed!")


if __name__=='__main__':
    f_signature = "df_class.xlsx"
    produce_output_files(f_signature)