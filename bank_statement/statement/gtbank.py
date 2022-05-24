import os
import glob2
import tabula
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
#import cv2
import matplotlib.pyplot as plt
import re
import logging
import copy
from utils import bank_logger,io
from bank_exceptions import errors


class GT_BankStatement_no_header():
    
    def __init__(self, b_statement_gt_bank, bank_id='GT_Bank', template_version='NO_HEADER'):
        '''
        initializes the Gt_bank statement class
        '''
        # a bankstatement has 2 input attributes (for now)
        # bank_id & statement pdf path
        
        self.bank_id = bank_id
        self.filename = b_statement_gt_bank
        self.allowed_extensions =["pdf"]
        self.template_version = template_version
        
                
        self.mapping = {
            "GT_Bank": {
                "NO_HEADER":8,
                "HEADER":7
                }
        }
        
        self.log_check_bank_statement_extension()
        self.log_check_bank_statement_path()
        self.customer_bank_statement = io.bank_statement_to_dataframe(b_statement_gt_bank, mult=True, pages_all='all')
        self.pipeline()

    def pipeline(self):
        '''
        chain operations to generate the final dataframe
        '''
        self.df = self.customer_bank_statement.copy()
        self.describe_accounts_types()
        self.log_check_account_type()
        self.log_check_bank_statement_extension()
        self.black_list_narrow_tables()
        self.log_check_table()
        self.combine_dataframes()
        self.clean_dataframe()
        self.clean_transactions()
        self.postprocess()
        self.recombine_dataframe()
              
    def describe_accounts_types(self):
        '''
        returns the account type (savings or current)
        '''
        
        self.accounts_info = [df for df in self.df if len(df.columns) == 2]
        account_type_list= []
        for account in self.accounts_info:
            account.index = account["Print. Date"]
            acc_tr = account.transpose()
            account_type_list.append(acc_tr["Account Type"][-1])
        return account_type_list
                       
    def log_check_bank_statement_extension(self):
        extension = os.path.splitext(self.filename)[1][1:]
        if extension not in self.allowed_extensions:
            account_type = 'NA'
            bank_logger.log_info('PRELOAD',account_type, self.bank_id, self.filename,'BankStatementFormatError')
            raise errors.BankStatementFormatError
                      
    def log_check_bank_statement_path(self):
        file_exists = os.path.exists(self.filename)
        if not file_exists:
            account_type = 'NA'
            bank_logger.log_info('PRELOAD',account_type, self.bank_id, self.filename,'BankStatementPathError')
            raise errors.BankStatementPathError 
             
    def log_check_account_type(self):
        '''
        checks the bank_type and logs the operation
        '''
        
        account_type = self.describe_accounts_types()
        if len(account_type) != 1:
            bank_logger.log_info('LOAD',account_type, self.bank_id, self.filename,'BankAccountTypeError')
            raise errors.BankAccountTypeError(account_type)
        else:
            self.account_type = account_type[0]
            bank_logger.log_info('LOAD',self.account_type, self.bank_id, self.filename,None)
                    
    def log_check_table(self):
        '''
        Store the list of columns names of all extracted dataframes
        '''
        # store the columns names for debug
        self.df_cols = [b_statement_dataframe.columns for b_statement_dataframe in self.df]
        
        max_ncols = self.mapping[self.bank_id][self.template_version]
        print(max_ncols)
        print(max([len(el) for el in self.df_cols]))
        
        if max([len(el) for el in self.df_cols]) < max_ncols:
            raise errors.BankStatementColumnsError(self.template_version, self.bank_id, self.mapping)
            log_info('PDF-TABLES',self.account_type, self.bank_id, self.filename,'BankStatementColumnsError')   
        
        elif max([len(el) for el in self.df_cols]) > max_ncols:
            bank_logger.log_info('PDF-TABLES',self.account_type, self.bank_id, self.filename,'BankStatementColumnsWarning')
            self.passed_df_cols_idx = [ind for ind, ex in enumerate(self.df_cols) if len(ex) == 8]
            failed_idx = list(set(list(range(len(self.df_cols))))- set(self.passed_df_cols_idx))
            failed_idx.sort()
            self.not_passed_df_cols_idx = failed_idx
            
        return self.df_cols
    
    def black_list_narrow_tables(self, verbose = False):
        '''
        removes the tables that do not contain transaction data
        '''
        
        # each pdf can extract tables
        # (some tables will be without headers)
        # We want to recreate the header (which matches table 1)
        
        
        self.finalized_dfs = []
        self.blacklisted_tables_idxs = []
        
        # all dataframes with statement operations is reformatted
        self.reformatted_dfs = [self.df[k].T.reset_index().T for k in range(1,len(self.df),1)]
        
        
        for idx,r_df in enumerate(self.reformatted_dfs): 
            try:
                # the first dataframe with the right header is the dataframe id = 1
                r_df.columns = self.df[1].columns
                r_df.index = range(r_df.shape[0])
                r_df = r_df.replace(regex=[r'^Unnamed:..$'], value=np.nan)
                
                # store  the cleaned data frame in a placeholder list
                self.finalized_dfs.append(r_df)
                
            except Exception as e:
                if verbose : print(e)
                bank_logger.log_info('DATAFRAME-CLEANING',self.account_type, self.bank_id, self.filename,e) 
                # if it fails, it is because it is a table of another type
                # they will be blacklisted and kept for potential processing
                self.blacklisted_tables_idxs.append(idx)
  
    def combine_dataframes(self):
        '''
        combines dataframes that contain financial data
        '''
        # combine all whitelisted dataframes (=transactions)
        try:
            self.master_df = pd.concat(self.finalized_dfs[:]).reset_index(drop=True)
            bank_logger.log_info('DATAFRAME-COMBINATION',self.account_type, self.bank_id, self.filename, None)
            
            assert (self.master_df.columns == self.df[1].columns), "the columns names do not match the top header"
            assert (self.shape[0] != 0), "the dataframe is empty - no rows"
            
        except Exception as e:
            bank_logger.log_info('DATAFRAME-COMBINATION', self.account_type, self.bank_id, self.filename, e) 
     
    def clean_dataframe(self):
        '''
        simple data cleaning to remove non informative cells
        '''
        # extra cleaning due to columns concatenation
        self.master_df = self.master_df[self.master_df['Remarks']!= 'Remarks']
        self.master_df = self.master_df[self.master_df['Remarks']!= 'Balance as at Last Transaction.']
        self.master_df = self.master_df[self.master_df["Trans. Date"] != 'Trans. Date']
        self.master_df = self.master_df.reset_index(drop=True)
        bank_logger.log_info('CLEAN-DATFRAME', self.account_type, self.bank_id, self.filename, None)

    def clean_transactions(self):
        '''
        keep only the transactions with dates and add one fictious date for easier processing
        
        '''
        try:
            self.clean_dataframe()
            self.transaction_not_null = self.master_df[~self.master_df["Trans. Date"].isna()].copy()
            # we must append 1 record to the last non null transaction
            max_idx = self.transaction_not_null.index.max()
            self.index_list_of_transaction = list(self.transaction_not_null.index)
            self.transaction_not_null.loc[max_idx + 1,'Trans. Date'] = '99-Apr-9999'
            
            bank_logger.log_info('CLEAN-TRANSACTIONS', self.account_type, self.bank_id, self.filename, None) 

            assert (self.transaction_not_null.loc[max_idx + 1,'Trans. Date'] == '99-Apr-9999'),"the additional row (99-Apr-9999) was not properly added"

        except Exception as e:
            bank_logger.log_info('CLEAN-TRANSACTIONS', self.account_type, self.bank_id, self.filename, e) 

    def postprocess(self, verbose = False):
        '''
        reconstruct the financial operations which overflow to the next line in 1 single text
        '''
        
        # all the indexes of the transaction with dates
        self.index_with_dates = self.transaction_not_null.index
        
        self.descr = {}
        for step_date in self.index_with_dates:
            self.descr[str(step_date)] = []

        print(self.index_with_dates.values)

        for idx, step in enumerate(self.index_with_dates):
            if idx < len(self.index_with_dates)-1:
                for ind in range(self.index_with_dates[idx], self.index_with_dates[idx+1], 1):
                    if ind < self.index_with_dates[idx+1]: 
                        if str(self.master_df.loc[ind, 'Remarks']) != 'nan':
                            self.descr[str(step)] += [str(self.master_df.loc[ind, 'Remarks'])]
            else:
                for ind in range(self.index_with_dates[idx], self.master_df.shape[0], 1):
                    if str(self.master_df.loc[ind, 'Remarks']) != 'nan':
                        self.descr[str(step)] += [str(self.master_df.loc[ind, 'Remarks'])]
                        
        for key in self.descr.keys():
            self.descr[key] = (''.join(self.descr[key])).replace('\r',' ')
        if verbose:
            return self.descr
    
    def recombine_dataframe(self, verbose= False):
        '''
        reconstruct the final dataset with all original transaction information plus the annotations
        '''
        # Dataframe of the transactions
        annotations = pd.DataFrame.from_dict(self.descr,  orient='index', columns=['Remarks_processed'])
        self.dataset_recombined = pd.concat([self.transaction_not_null.reset_index(drop=True), annotations.reset_index(drop=True)], axis=1)
        self.dataset_recombined['ACCOUNT_TYPE'] = self.account_type
        self.dataset_recombined['BANK_ID'] = self.bank_id
        self.dataset_recombined['FILE_NAME'] = self.filename
        
        if verbose:
            return self.dataset_recombined
        
        self.dataset_recombined = self.dataset_recombined[['Trans. Date','Reference','Value. Date','Debits','Credits','Balance','Remarks_processed','ACCOUNT_TYPE','BANK_ID', 'FILE_NAME']]