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


class Dataset_Bank():
    def __init__(self, Data, a_list_of_keywords):
        # save data inside the object
        self._data = Data
        self.to_excel = True
        self.a_list_of_keywords = a_list_of_keywords
        self.filename = Data['FILE_NAME'].unique()[0]
        self.account_type = Data['ACCOUNT_TYPE'].unique()[0]
        self.bank_id = Data['BANK_ID'].unique()[0]
        self.pipeline()
        
    def pipeline(self):
        '''
        chain the operations to generate the analytics reports
        '''

        self.features_engineering()
        self.filter_text()
        self.filter_dest()  
        self.clean_data()
        self.save2csv(out="./first_data.csv")
        self.subset_dataframe()
        self.impute_class()
        self.export_datasets()

    def features_engineering(self):
        '''
        features builder: iterate given a list of keywords (criterias used to build new features)
        '''

        for key_word in tqdm(self.a_list_of_keywords):
            self.check_keyword(key_word)
    
    def check_keyword(self, keyword):
        '''
        feature builder: check against a criteria and create a feature in the main dataframe (_data)
        '''
    
        self._data["IS_A_"+ keyword] =  self._data.loc[:,"Remarks_processed"].str.contains(keyword, case=False).astype('int')
    
    def filter_text(self):
        '''
        feature builder: filter description to return text only
        '''
        
        self._data["filtered_description"] = self._data.loc[:,"Remarks_processed"].str.findall('[^\d\W]+').str.join(sep =' ')
    
    def filter_dest(self):
        '''
        feature builder: filtered benificiary
        '''
        
        self._data["filtered_dest"] = self._data["filtered_description"].str.upper()
        self._data["filtered_dest"] = self._data["filtered_dest"].str.split("TO").str[-1]
        
    def clean_data(self):
        '''
        fix data problems
        # the "date format" problem inside timestamp cell
        # problem found : 02-Apr-2021.1
        '''

        self.csv_to_annotate = self._data
        for c in self.csv_to_annotate.columns[:2]:
            self.csv_to_annotate[c] = self.csv_to_annotate[c].apply(lambda x : str(x).split(".")[0])
            
        # problem found : \r inside the dataframe
        self.csv_to_annotate[c] = self.csv_to_annotate[c].astype('str').str.replace("\r"," ")
        
    def save2csv(self, out):
        '''
        clean save (remove the last line with dummy timestamp (9999))
        '''
        self.df = self.csv_to_annotate.iloc[:-1,:]
        self.df.to_csv(out, index= None, sep = ";",encoding='utf-8-sig')
        print(self.df.columns)
             
    def subset_dataframe(self):
        '''
        creates subset dataframes with key information (loan, salary, cheque,commission,tax)
        '''

        # create subsets: (salary, salary_advance, transfer, loan, tax, commission, cheque, cash, others)
        self.salary = self.df[self.df["Remarks_processed"].str.contains("SALARY|OCT|NOV|DEC|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP",regex=True, case=False).values]
        self.reversal = self.df[self.df["Remarks_processed"].str.contains("REVERSAL",regex=True, case=False).values]
        self.salary_advance = self.df[self.df["Remarks_processed"].str.contains("SALARY ADVANCE", case=False).values]
        self.transfer = self.df[self.df["Remarks_processed"].str.contains("TRANSFER", case=False).values]
        self.loan = self.df[self.df["Remarks_processed"].str.contains("LOAN", case=False).values]
        self.tax = self.df[self.df["Remarks_processed"].str.contains("TAX|VAT", case=False).values]
        self.commission = self.df[self.df["Remarks_processed"].str.contains("COMM", case=False).values]
        self.cheque = self.df[self.df["Remarks_processed"].str.contains("CHEQUE",case=False).values]
        self.cash_withdrawal = self.df[self.df["Remarks_processed"].str.contains("WITHDRAWAL|CASH",case=False).values]
        self.others = self.df[self.df["Remarks_processed"].str.contains("OTHER",case=False).values]
        self.utility = self.df[self.df["Remarks_processed"].str.contains("SMS|AIRTIME",case=False).values]
        self.web = self.df[self.df["Remarks_processed"].str.contains("WEB",regex=True, case=False).values]
        self.food = self.df[self.df["Remarks_processed"].str.contains("FOOD",regex=True, case=False).values]
        self.instant_payment = self.df[self.df["Remarks_processed"].str.contains("INSTANT PAYMENT",regex=True, case=False).values]
        self.maintenance = self.df[self.df["Remarks_processed"].str.contains("MAINTENANCE",case=False).values]

    def impute_class(self):

        '''
        classify transactions based on keywords present in remarks
        '''
        
        self.subset_dataframe()
        # store the indexes: (salary, salary_advance, transfer, loan, tax, commission, cheque, cash, others)
        transfer_index = self.transfer.index
        salary_advance_index = self.salary_advance.index
        cash_withdrawal_index = self.cash_withdrawal.index
        comm_index = self.commission.index
        tax_index = self.tax.index
        salary_index = self.salary.index
        loan_index = self.loan.index
        other_index = self.others.index
        cheque_index = self.cheque.index
        utility_index = self.utility.index
        reversal_index = self.reversal.index
        web_index = self.web.index
        food_index = self.food.index
        instant_payment_index = self.instant_payment.index
        maintenance_index = self.maintenance.index

        # classify expenses
        impute_list = [
                    [other_index,"OTHER"],
                    [transfer_index,"TRANSFER"],
                    [salary_advance_index,"ADVANCE"],
                    [cash_withdrawal_index,"CASH"],
                    [comm_index, "COMM"],
                    [tax_index,"TAX"],
                    [salary_index,"SALARY"],
                    [reversal_index,"REVERSAL"],
                    [loan_index,"LOAN"],
                    [cheque_index, "CHEQUE"],
                    [utility_index, "UTILITY"], 
                    [web_index, "WEB"],
                    [food_index, "FOOD"],
                    [instant_payment_index, "INSTANT PAYMENT"],
                    [maintenance_index, "MAINTENANCE"],
                    ]

        self.df_class = self.df.copy()
        for element in impute_list:
            self.df_class.loc[element[0],"Class"] = element[1]

        self.df_class["Trans. Date"] = self.df_class["Trans. Date"].apply(lambda x : str(x).split(".")[0])
        self.df_class["Value. Date"] = self.df_class["Value. Date"].apply(lambda x : str(x).split(".")[0])
        # dataframe with class information
        return self.df_class

    def export_datasets(self):
        '''
        
        '''
        self.prefix = self.filename.split(".pdf")[0].split("/")[-1]
        self.folder = "./data"
        os.makedirs(f'{self.folder}/{self.prefix}/engineered/', exist_ok=True)

        if not self.to_excel:
            self.salary.to_csv(f"{self.folder}/{self.prefix}/engineered/salary.csv", sep=';')
            self.salary_advance.to_csv(f"{self.folder}/{self.prefix}/engineered/salary_advance.csv", sep=';')
            self.transfer.to_csv(f"{self.folder}/{self.prefix}/engineered/transfer.csv", sep=';')
            self.loan.to_csv(f"{self.folder}/{self.prefix}/engineered/loan.csv", sep=';')
            self.tax.to_csv(f"{self.folder}/{self.prefix}/engineered/tax.csv", sep=';')
            self.commission.to_csv(f"{self.folder}/{self.prefix}/engineered/commission.csv", sep=';')
            self.cheque.to_csv(f"{self.folder}/{self.prefix}/engineered/cheque.csv", sep=';')
            self.cash_withdrawal.to_csv(f"{self.folder}/{self.prefix}/engineered/cash_withdrawal.csv", sep=';')
            self.others.to_csv(f"{self.folder}/{self.prefix}/engineered/others.csv", sep=';')
            self.df_class.to_csv(f"{self.folder}/{self.prefix}/engineered/df_class.csv", sep=';', index=None)
        else:
            self.salary.to_excel(f"{self.folder}/{self.prefix}/engineered/salary.xlsx",sheet_name='salary')
            self.salary_advance.to_excel(f"{self.folder}/{self.prefix}/engineered/salary_advance.xlsx",sheet_name='salary_advance')
            self.transfer.to_excel(f"{self.folder}/{self.prefix}/engineered/transfer.xlsx",sheet_name='transfer')
            self.loan.to_excel(f"{self.folder}/{self.prefix}/engineered/loan.xlsx",sheet_name='loan')
            self.tax.to_excel(f"{self.folder}/{self.prefix}/engineered/tax.xlsx",sheet_name='tax')
            self.commission.to_excel(f"{self.folder}/{self.prefix}/engineered/commission.xlsx",sheet_name='commission')
            self.cheque.to_excel(f"{self.folder}/{self.prefix}/engineered/cheque.xlsx",sheet_name='cheque')
            self.cash_withdrawal.to_excel(f"{self.folder}/{self.prefix}/engineered/cash_withdrawal.xlsx",sheet_name='cash_withdrawal')
            self.others.to_excel(f"{self.folder}/{self.prefix}/engineered/others.xlsx",sheet_name='others')
            self.df_class.to_excel(f"{self.folder}/{self.prefix}/engineered/df_class.xlsx",sheet_name='df_class')