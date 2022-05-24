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
from utils import bank_logger
from bank_exceptions import errors
from utils import bank_logger,io
import dataconf

class Metrics2():
    def __init__(self, imputed_Dataset):
        self.DTI = dataconf.data_config.DTI_EARNERS
        self.Ds = copy.deepcopy(imputed_Dataset)
        self.data = imputed_Dataset.df_class
        self.filename = imputed_Dataset.filename
        self.pipeline()
           

    def pipeline(self):
        '''
        chain the operations to generate the analytics reports
        '''
        self.create_loan_summary()
        self.create_others_summary()
        self.create_cash_summary()
        self.create_salary_summary()
        self.create_transfer_between_summary()
        self.loan_to_salary_ratio()  
        self.abnormal_transactions()
        self.advance = self.create_salary_advance_summary()
        self.access_to_ddebt = self.access_to_direct_debt()
        self.export_datasets()


    def create_salary_advance_summary(self):
        '''
        returns boolean evaluation about receiving an advance on salary 
        '''
        return self.Ds.salary_advance.shape[0] > 0
 
    
    def access_to_direct_debt(self):
        '''
        depending on certain banks the acceptance of direct debt access is not allowed
        '''
        return self.Ds.bank_id.lower() not in ["standard charter", "first bank", "stanbic"]
       

    def create_others_summary(self): 
        '''
        creates the dataframe for the loan info
        '''
        # convert entries to date format
        # self.data.loc[:]["Trans. Date"] = pd.to_datetime(self.Ds.loan["Trans. Date"], errors='coerce')
        
        # create a summary limiting ourselves to some columns
        other_summary = self.Ds.others.loc[:,["Trans. Date", "Credits", "Debits"]].copy()
        
        # use the colum ( just transformed to date format as index)
        other_summary.set_index('Trans. Date', inplace=True)
        
        
        # make sure thzat the index is @ the right format (date)
        other_summary.index = pd.to_datetime(other_summary.index)
        
        
        # remove the missing value and replace them by 0
        for cat in ["Credits", "Debits"]:
            other_summary[cat].fillna("0", inplace=True)

        
        # remove the thousands separator
        for cat in ["Credits", "Debits"]:
            other_summary[cat]= other_summary[cat].str.replace(",","").astype('float')
            
            
        # "effective" number of loans
        self.df_other_summary = other_summary.groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
        
        credits = self.df_other_summary.copy()
        debits = self.df_other_summary.copy()

        credits[credits['Credits']>0]=1
        debits[debits['Debits']>0]=-1
        
        credits['Credits'].fillna(0,inplace=True)
        debits['Debits'].fillna(0,inplace=True)

        df_credits = credits['Credits'].astype(str).str.replace(",","").astype('float')
        df_debits = debits['Debits'].astype(str).str.replace(",","").astype('float')
        
        
        # dataframe storing the current number of loans
        self.total_n_other_summary = pd.DataFrame(pd.concat([df_debits,df_credits], axis = 1).sum(axis=1))
        self.total_n_other_summary.columns = ['#n loans']
        self.total_n_other_summary['#n loans'] = self.total_n_other_summary['#n loans'].apply(lambda x: np.abs(x))
        
        self.df_other_summary["effective"] = -1*self.df_other_summary["Debits"].astype('float')+self.df_other_summary["Credits"].astype('float')
        
        self.other_dict = {
            "other_summary" : self.df_other_summary, 
            "n_other_summary": self.total_n_other_summary
        }
        return self.other_dict
    
    
    def create_loan_summary(self):
        '''
        creates the dataframe for the loan info
        '''
        # convert entries to date format
        #self.data.loc[:]["Trans. Date"] = pd.to_datetime(self.Ds.loan["Trans. Date"], errors='coerce')
        
        # create a summary limiting ourselves to some columns
        loan_summary = self.Ds.loan.loc[:,["Trans. Date", "Credits", "Debits"]].copy()
        
        # use the colum ( just transformed to date format as index)
        loan_summary.set_index('Trans. Date', inplace=True)
        
        
        # make sure thzat the index is @ the right format (date)
        loan_summary.index = pd.to_datetime(loan_summary.index)
        
        
        # remove the missing value and replace them by 0
        for cat in ["Credits", "Debits"]:
            loan_summary[cat].fillna("0", inplace=True)

        
        # remove the thousands separator
        for cat in ["Credits", "Debits"]:
            loan_summary[cat]= loan_summary[cat].str.replace(",","").astype('float')
            
            
        # "effective" number of loans
        self.df_loan_summary = loan_summary.groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
        
        credits = self.df_loan_summary.copy()
        debits = self.df_loan_summary.copy()

        credits[credits['Credits']>0]=1
        debits[debits['Debits']>0]=-1
        
        credits['Credits'].fillna(0,inplace=True)
        debits['Debits'].fillna(0,inplace=True)

        df_credits = credits['Credits'].astype(str).str.replace(",","").astype('float')
        df_debits = debits['Debits'].astype(str).str.replace(",","").astype('float')
        
        
        
        self.total_n_loans_summary = pd.DataFrame(pd.concat([df_debits,df_credits], axis = 1).sum(axis=1))
        self.total_n_loans_summary.columns = ['#n loans']
        self.total_n_loans_summary['#n loans'] = self.total_n_loans_summary['#n loans'].apply(lambda x: np.abs(x))
        
        self.df_loan_summary["effective"] = -1*self.df_loan_summary["Debits"].astype('float')+self.df_loan_summary["Credits"].astype('float')
        
        self.loan_dict = {
            "loan_summary" : self.df_loan_summary, 
            "n_loans_summary": self.total_n_loans_summary
        }
        return self.loan_dict
    
     
    def create_cash_summary(self):
        '''
        creates the dataframe for the cash info
        '''
        self.Ds.cash_withdrawal.loc[:]["Trans. Date"] = pd.to_datetime(self.Ds.cash_withdrawal["Trans. Date"], errors='coerce')
        self.Ds.cash_withdrawal.set_index('Trans. Date', inplace=True)
        self.Ds.cash_withdrawal.index = pd.to_datetime(self.Ds.cash_withdrawal.index)
        
        number_of_payments = len(set(list(self.Ds.cash_withdrawal.index)))
        cash_info = np.array([[el.month,el.day] for el in set(list(self.Ds.cash_withdrawal.index))])


        self.cash_numeric = self.Ds.cash_withdrawal.loc[:,["Debits","Credits"]]
        
        for cat in ["Debits","Credits"] :
            self.cash_numeric[cat].fillna(0, inplace=True)
        
        for cat in ["Debits","Credits"] :
            self.cash_numeric[cat] = self.cash_numeric[cat].astype(str).str.replace(",","")
        
        self.cash_numeric["effective"] = self.cash_numeric["Credits"].astype('float') - self.cash_numeric["Debits"].astype('float')
        
        
        #aggregation - monthly income
        self.df_cash_summary = self.cash_numeric[["effective"]].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
        

        self.cash_dict = {
            "all_transactions": self.cash_numeric,
            "number_of_payments": number_of_payments,
            "cash_summary": self.df_cash_summary,
         
        }
    
        return self.cash_dict
    
 
    def create_salary_summary(self):
        '''
        creates the dataframe for the salary info - when the salary is recorded as a Remark
        '''
        self.Ds.salary.loc[:]["Trans. Date"] = pd.to_datetime(self.Ds.salary["Trans. Date"], errors='coerce')
        self.Ds.salary.set_index('Trans. Date', inplace=True)
        self.Ds.salary.index = pd.to_datetime(self.Ds.salary.index)
        
        number_of_payments = len(set(list(self.Ds.salary.index)))
        paid_info = np.array([[el.month,el.day] for el in set(list(self.Ds.salary.index))])
        
        
        self.salary_dict = {
        "all_transactions": None,
        "number_of_payments": None,
        "paid_month": None,
        "paid_days": None,
        "paid_day_mean": None,
        "paid_day_variance": None,
        "salary_summary": pd.DataFrame(),
        "paid_to_employees": None
        }
    
        
        
        try:
            paid_month, paid_day = paid_info[:,0],paid_info[:,1]

            # common metrics to evaluate the paid date stability
            paid_day_mean, paid_day_variance = np.mean(paid_day), np.std(paid_day) 


            # create a dataframe with no missing values and format the numbers to be numeric
            salary_numeric = self.Ds.salary.loc[:,["Debits","Credits"]]
            salary_numeric[["Debits","Credits"]].fillna(0, inplace=True)

            for cat in ["Debits","Credits"] :
                salary_numeric[cat] = salary_numeric[cat].astype(str).str.replace(",","")

            salary_numeric["effective"] = salary_numeric["Credits"].astype('float') - salary_numeric["Debits"].astype('float')


            # aggregation - monthly income
            self.df_salary_summary = salary_numeric[["effective"]].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()

            # check if the salary info describes income or paid salary
            salary_paid_to_employees = self.df_salary_summary["effective"].sum() <0

            self.salary_dict = {
                "all_transactions": salary_numeric,
                "number_of_payments": number_of_payments,
                "paid_month": paid_month,
                "paid_days": paid_day,
                "paid_day_mean": paid_day_mean,
                "paid_day_variance": paid_day_variance,
                "salary_summary": self.df_salary_summary,
                "paid_to_employees": salary_paid_to_employees
            }
        except IndexError as e:
            bank_logger.log_info('ANALYTICS',self.Ds.account_type, self.Ds.bank_id, self.Ds.filename, e)
            self.df_salary_summary = pd.DataFrame()
            
        return self.salary_dict

         
    def create_transfer_between_summary(self):
        '''
        creates the dataframe for the transfer info - can be used as a proxy for salary
        '''
        self.Ds.transfer.loc[:]["Trans. Date"] = pd.to_datetime(self.Ds.transfer["Trans. Date"], errors='coerce')
        self.Ds.transfer.set_index('Trans. Date', inplace=True)
        self.Ds.transfer.index = pd.to_datetime(self.Ds.transfer.index)
        
        self.number_of_transfer = len(set(list(self.Ds.transfer.index)))
        paid_info = np.array([[el.month,el.day] for el in set(list(self.Ds.transfer.index))])
        paid_month, paid_day = paid_info[:,0],paid_info[:,1]

        paid_day_mean, paid_day_variance = np.mean(paid_day), np.std(paid_day) 


        self.transfer_numeric = self.Ds.transfer.loc[:,["Debits","Credits"]]
        
        for cat in ["Debits","Credits"] :
            self.transfer_numeric[cat].fillna(0, inplace=True)
        
        for cat in ["Debits","Credits"] :
            self.transfer_numeric[cat] = self.transfer_numeric[cat].astype(str).str.replace(",","")
        
        self.transfer_numeric["effective"] = self.transfer_numeric["Credits"].astype('float') - self.transfer_numeric["Debits"].astype('float')
        
        
        #aggregation - monthly income
        self.df_transfer_summary = self.transfer_numeric[["effective"]].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
        
        # check if the salary info describes income or paid salary
        self.total_transfer = self.df_transfer_summary["effective"].sum()
        
        self.transfer_between_summary_dict = {
            "all_transactions": self.transfer_numeric,
            "number_of_payments": self.number_of_transfer,
            "transfer_summary": self.df_transfer_summary,
            "total_transfer": self.total_transfer   
        }
        return self.transfer_between_summary_dict
    
    
    def create_salary_bracket(self, salary_dollars):
        '''
        DTI leasing brackets for salary classification
        '''
        self.bracket = ''
        if salary_dollars > 50000 and salary_dollars < 200000:
            self.bracket = "LOW_EARNER"
        elif salary_dollars > 210000 and salary_dollars < 500000:
            self.bracket = "LOW_MED_EARNER"
        elif salary_dollars > 500000 and salary_dollars < 1000000:  
            self.bracket = "MED_EARNER"
        elif salary_dollars > 1000000 and salary_dollars < 3000000: 
            self.bracket = "HIGH_MED_EARNER"
        elif salary_dollars > 3000000 and salary_dollars < 5000000:
            self.bracket = "HIGH_EARNER"
        elif salary_dollars > 5000000:
            self.bracket = "TOP_EARNER"
 
          
    def loan_to_salary_ratio(self):
        '''
        compute the loan to salary ratio (checks whether the salary is computed directly or indirectly)
        '''
        self.df_loan = self.loan_dict['loan_summary']
        
        df_transfer_summary = self.transfer_between_summary_dict['transfer_summary']
        df_salary_summary = self.salary_dict['salary_summary']
        
        
        if (df_salary_summary.empty) or (df_salary_summary["effective"].sum() <0):
            df_salary = df_transfer_summary    
            bank_logger.log_info('ANALYTICS_LOAN_TO_SALARY_RATIO',self.Ds.account_type, self.Ds.bank_id, self.Ds.filename, 'NO_SALARY')
                
        else:
            df_salary = df_salary_summary
        
        df_salary_recomputed_mean = max(df_salary["effective"].mean(),df_transfer_summary['effective'].mean())
        df_salary_recomputed_sum = max(df_salary["effective"].sum(),df_transfer_summary['effective'].sum())
        self.salary_bracket = self.create_salary_bracket(df_salary_recomputed_mean)
        
        self.loan_to_salary = pd.merge(self.df_loan['effective'],
                                df_salary['effective'], 
                                left_index=True,
                                right_index=True,
                                how='outer')

        self.loan_to_salary.columns = ['effective_loan', 'salary']
        
        self.loan_to_salary['ratio'] = (self.loan_to_salary['effective_loan'])/self.loan_to_salary['salary']
        self.loan_to_salary['ratio'] = self.loan_to_salary['ratio'].clip(0,None)
        self.loan_to_salary['ratio_total'] = (self.df_loan['effective'].sum() + self.df_other_summary['effective'].sum())/ df_transfer_summary['effective'].sum()
        self.loan_to_salary['ratio_total'] = self.loan_to_salary['ratio_total'].clip(0,None)

        return self.loan_to_salary, self.salary_bracket
    

    def abnormal_transactions(self):

        # salary can be computed either from salary info when available
        # net transfers can be used to estimate the salary
        self.Ds.transfer.loc[:,'F_Credits'] = self.Ds.transfer['Credits'].fillna(0).astype('str').str.replace(",","").astype('float').copy()
        
        self.Ds.salary.loc[:,'F_Credits'] = self.Ds.salary['Credits'].fillna(0).astype('str').str.replace(",","").astype('float').copy()

        
        self.Ds.transfer.loc[:,'F_Debits'] = self.Ds.transfer['Debits'].fillna(0).astype('str').str.replace(",","").astype('float').copy()
        
        df_salary_summary = self.salary_dict['salary_summary']
        
        if (df_salary_summary.empty) or (df_salary_summary["effective"].sum() <0):
            history_transaction_pos = self.Ds.transfer.loc[self.Ds.transfer['F_Credits']>0].copy()
        else:
            history_transaction_pos = self.Ds.salary.loc[self.Ds.salary['F_Credits']>0].copy()
            
        history_transaction_neg = self.Ds.transfer.loc[self.Ds.transfer['F_Debits']>0].copy()
        

        # transfer summary where the positive & negative operations are recorded for a given day
        transfer_pos = history_transaction_pos.loc[:,["F_Credits"]].groupby("Trans. Date").agg(sum)
        transfer_neg = history_transaction_neg.loc[:,["F_Debits"]].groupby("Trans. Date").agg(sum)


        self.transfer_anomaly = pd.merge(transfer_pos,transfer_neg,left_index=True,right_index=True, how='outer').fillna(0)

        self.transfer_anomaly["daily_delta"] = 1-(self.transfer_anomaly["F_Credits"] - self.transfer_anomaly["F_Debits"])/(self.transfer_anomaly["F_Credits"])
        self.transfer_anomaly["abnormality"] = self.transfer_anomaly["daily_delta"].apply(lambda x: x >0.8 and x!= np.inf).astype('int')
        
        self.transfer_anomaly.index = pd.to_datetime(self.transfer_anomaly.index)
        self.monthly_anomaly = self.transfer_anomaly[['abnormality']].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
        self.daily_anomaly = self.transfer_anomaly[['abnormality']].groupby(pd.Grouper(level='Trans. Date',freq='D')).sum()
        return self.transfer_anomaly, self.daily_anomaly, self.monthly_anomaly

    
    def export_datasets(self):
        '''
        
        '''
        self.prefix = self.filename.split(".pdf")[0].split("/")[-1]
        os.makedirs(f'./data/{self.prefix}/analytix/', exist_ok=True)

        ratio_total = self.loan_to_salary['ratio_total'].unique()[0]
        self.oneline_info = pd.DataFrame([[self.advance, self.access_to_ddebt, self.bracket, ratio_total]], 
                            columns=["IOU","DDEBT","BRACKET","LOAN_TO_INCOME"])

        self.oneline_info.to_csv(f"./data/{self.prefix}/analytix/one_line_info.csv", sep=';', index=None)


        self.transfer_numeric.to_csv(f"./data/{self.prefix}/analytix/transfer_all_operations.csv", sep=';')
        self.df_transfer_summary.to_csv(f"./data/{self.prefix}/analytix/monthly_transfer.csv", sep=';')

        self.df_salary_summary.to_csv(f"./data/{self.prefix}/analytix/monthly_salary.csv", sep=';')

        self.cash_numeric.to_csv(f"./data/{self.prefix}/analytix/cash_all_operations.csv", sep=';')
        self.df_cash_summary.to_csv(f"./data/{self.prefix}/analytix/monthly_cash.csv", sep=';')
        
        self.df_loan.to_csv(f"./data/{self.prefix}/analytix/loan.csv", sep=';')

        self.loan_to_salary.to_csv(f"./data/{self.prefix}/analytix/loan_to_salary.csv", sep=';')
        self.df_other_summary.to_csv(f"./data/{self.prefix}/analytix/monthly_other.csv", sep=';')
        self.monthly_anomaly.to_csv(f"./data/{self.prefix}/analytix/monthly_anomaly.csv", sep=';')
        self.daily_anomaly.to_csv(f"./data/{self.prefix}/analytix/daily_anomaly.csv", sep=';')
