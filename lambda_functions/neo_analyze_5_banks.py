import os
from datetime import datetime
import pandas as pd
import numpy as np
import json
import requests

# set of criterias provided by Liberta leasing

DTI = {
        "LOW_EARNER": 0.33,
        "LOW_MED_EARNER":0.35,
        "MED_EARNER":0.40,
        "HIGH_MED_EARNER":0.45,
        "HIGH_EARNER": 0.5,
        "TOP_EARNER": 0.55
        }

def download_url(url):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if (".xlsx" in el)][0]
    
    os.makedirs('/tmp', exist_ok=True)
    # open a file to dump the stream in
    # print whether the request worked or not 
    print(r)
    # check the filename we are dumping contents in 
    print(file_name)
    
    # open the temp filename to store the contents (zip file)
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(os.stat(f'/tmp/{file_name}').st_size)
    return file_name


def util_ETL_bank(raw_df, bank_name):
    '''
    this function performs ETL on the bank statements
    different bank statements have different header
    @param: raw_df DataFrame  initial dataframe
    @param: bank_name string bank of interest
    '''
    df_no_index = raw_df[[col for col in raw_df.columns if "Unnamed" not in col]]
    
    if bank_name == "STANDARD_CHARTERED_BANK":
        df_no_index['Trans. Date'] = df_no_index["Date"]
        df_no_index['Credits'] = df_no_index["Deposit"]
        df_no_index['Debits'] =  df_no_index["Withdraw"]
        df_no_index['Credits'].fillna(0, inplace=True)
        df_no_index['Debits'].fillna(0, inplace=True)
        
    elif bank_name == "WEMA_BANK":
        df_no_index['Trans. Date'] = df_no_index["Tran date"]
        df_no_index['Credits'] = df_no_index["Deposit"]
        df_no_index['Debits'] =  df_no_index["Withdrawal"]
        df_no_index['Credits'].fillna(0, inplace=True)
        df_no_index['Debits'].fillna(0, inplace=True)
        df_no_index['Credits'] = df_no_index['Credits'].apply(lambda x: str(x))
        df_no_index['Debits'] = df_no_index['Debits'].apply(lambda x: str(x))
        
    elif bank_name == "ACCESS_BANK":
        df_no_index['Trans. Date'] = df_no_index["Posted date"]
        df_no_index['Credits'] = df_no_index["Credit"]
        df_no_index['Debits'] =  df_no_index["Debit"]
        
    elif bank_name == "UBA_BANK":
        df_no_index['Trans. Date'] = df_no_index["TRANS DATE"]
        df_no_index['Credits'] = df_no_index["CREDIT"]
        df_no_index['Debits'] =  df_no_index["DEBIT"]
        
    else:
        df_no_index['Trans. Date'] = df_no_index["Posted Date"]
        df_no_index['Credits'] = df_no_index["Credit"]
        df_no_index['Debits'] =  df_no_index["Debit"]
        

    return df_no_index
  
  
def util_create_salary_bracket(salary_dollars):
    '''
    rules to define the salary bracket
    @param: salary_dollars float monthly salary
    '''
    if  salary_dollars < 200000:
        bracket = "LOW_EARNER"
    elif salary_dollars > 210000 and salary_dollars < 500000:
        bracket = "LOW_MED_EARNER"
    elif salary_dollars > 500000 and salary_dollars < 1000000:  
        bracket = "MED_EARNER"
    elif salary_dollars > 1000000 and salary_dollars < 3000000: 
        bracket = "HIGH_MED_EARNER"
    elif salary_dollars > 3000000 and salary_dollars < 5000000:
        bracket = "HIGH_EARNER"
    elif salary_dollars > 5000000:
        bracket = "TOP_EARNER"
    return bracket
  

def convert_col(x):
    '''
    converts a column with 1000 separator to float
    converts empty value into zero
    '''
    try :
        res = float(x.replace(",",""))
    except:
        res = 0
    return res


def sort_columns(transpose_kpi):
    '''
    return sorted dataframe based on months
    TODO : rewrite with sort based on datetime
    '''
    col_list = transpose_kpi.columns
    months_list = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    pos_list = list(range(12))

    # create a dictionary with the month as key and the # of the month
    month_mapping = dict(zip(months_list,pos_list))
    # revert the dictionary
    inverted_month_mapping = dict(zip(pos_list,months_list))

    #
    new_col_list =[]
    for el in list(col_list):
        new_col_list.append([month_mapping[el[0]],el[1]])

    # sort the months
    sorted_list =[]
    intermediate_cols  = sorted(new_col_list, key = lambda x: x[0])
    for el in list(intermediate_cols):
        sorted_list.append((inverted_month_mapping[el[0]],el[1]))

    sorted_kpi = transpose_kpi[sorted_list]

    return sorted_kpi
    
    
def add_empty_columns(t_kpi):
    '''
    add columns when they don't exist so that each month has the same number of categories of transactions
    '''
    _kpi = t_kpi.copy()

    month_summary =[]
    months_list = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    
    # iterate over all months
    # add for each month the type of transactions that is absent
    for m in months_list:
        try:
            c = set(['CASH','CHARGES','PURCHASE','SALARY','TRANSFERT',"REVERSAL"]) - set(list(_kpi[m].columns))
            if len(c)>0:
                month_summary.append({m:c})
        except Exception as e:
            print(e)
            pass
    # iterate over each month
    # set the empty type of transactions to zero
    for el in month_summary :
        for k in list(el.keys()):
            vals = el[k]
            for v in vals:
                t_kpi = t_kpi.copy()
                t_kpi.loc[0,(k,v)] = 0
    return t_kpi
  
def return_effective_money(transpose_kpi, month):
    effective_mon = \
    transpose_kpi.loc[0,(month,'CASH')]\
    + transpose_kpi.loc[0,(month,'CHARGES')]\
    + transpose_kpi.loc[0,(month,'PURCHASE')]\
    + transpose_kpi.loc[0,(month,'REVERSAL')]\
    + transpose_kpi.loc[0,(month,'SALARY')]\
    + transpose_kpi.loc[0,(month,'TRANSFERT')]
    
    return effective_mon

def return_effective_loan(transpose_kpi, month):
    print(transpose_kpi)
    effective_loan = \
    transpose_kpi.loc[0,(month,'LOAN')]
    
    
    return effective_loan

def return_effective_salary(transpose_kpi, month):
    effective_loan = \
    transpose_kpi.loc[0,(month,'SALARY')]
    
    return effective_loan


def create_report(df):
    '''
    function which buils analytics report
    '''

    # problems with dates (get cut/eaten)
    date_regex = "([\w\s]+)-([\w\s]+)-([\w\s]+)"
    df["Year"] = df["Posted Date"].str.extract(date_regex)[2]
    df["Month"] = df["Posted Date"].str.extract(date_regex)[1]
    df["Debit"] = df["Debit"].apply(lambda x: convert_col(x))
    df["Credit"] = df["Credit"].apply(lambda x: convert_col(x))

    final_df = df.groupby(["Month","PREDICTION"]).agg('sum')
    # debit - credit -> balance for each type of operation
    kpi = -final_df["Debit"] + final_df["Credit"]
    df_kpi = pd.DataFrame(kpi)
        
    # transposition of the matrix to read for business analytics
    transpose_kpi = pd.DataFrame(kpi).transpose()

    # columns of the transposed matrix
    col_list = transpose_kpi.columns

    sorted_analytics = sort_columns(transpose_kpi)
    clean_sorted_analytics = sort_columns(add_empty_columns(sorted_analytics))

    summary_totals =[]
    col_list = set([el[0] for el in clean_sorted_analytics.columns])
    months_sorted = sorted(col_list, key=lambda mo: datetime.strptime(mo, "%b"))

    salary_totals = []
    loan_totals = []

    for m in months_sorted:
        print(m)
        try:
            res_mon = return_effective_money(clean_sorted_analytics, m)
        except:
            pass
        try:
            res_loan = return_effective_loan(clean_sorted_analytics, m)
        except:
            pass
        try:
            res_sal = return_effective_salary(clean_sorted_analytics, m)
        except:
            pass
        #print(res)
        summary_totals.append(res_mon)
        loan_totals.append(res_loan)
        salary_totals.append(res_sal)
    
    # effective calculations (-debit + credit)
    effective_money_dict = dict(zip(months_sorted, summary_totals))
    effective_salary_dict = dict(zip(months_sorted, salary_totals))
    effective_loan_dict = dict(zip(months_sorted, loan_totals))

    # average metrics
    average_salary = np.mean(np.array(list(effective_salary_dict.values())))
    average_loan = np.mean(np.array(list(effective_loan_dict.values())))

    # brackets (loan & salary as ddefined by LLeasing)
    salary_bracket = util_create_salary_bracket(average_salary)
    loan_bracket = DTI[salary_bracket]

    # loan over effective (sal - exp) & loan over effective salary
    loan_over_effective_money = np.divide(np.array(list(effective_loan_dict.values())),np.array(list(effective_money_dict.values())))
    loan_over_effective_salary = np.divide(np.array(list(effective_loan_dict.values())),np.array(list(effective_salary_dict.values())))

    # dictionary "loan over effective ..."
    loan_over_effective_money_dict  = dict(zip(months_sorted, loan_over_effective_money))
    loan_over_effective_salary_dict = dict(zip(months_sorted, loan_over_effective_salary))

    # metric which grants loan or not
    can_take_loan_effective_based_on_money =  sum(effective_money_dict.values()) > 0
    can_take_loan_effective_based_on_salary =  (average_loan/average_salary) < loan_bracket

    return (effective_money_dict,
            effective_salary_dict,
            effective_loan_dict,
            average_salary,
            average_loan, 
            salary_bracket,
            loan_bracket,
            loan_over_effective_money_dict,
            loan_over_effective_salary_dict,
            can_take_loan_effective_based_on_money,
            can_take_loan_effective_based_on_salary)
   


def test():
    df = pd.read_excel("/Users/assansanogo/Downloads/processed_for_BERT.xlsx")
    
    df = util_ETL_bank(df, "OTHER")
    
    effective_money_dict,\
    effective_salary_dict,\
    effective_loan_dict,\
    average_salary,\
    average_loan,\
    salary_bracket,\
    loan_bracket,\
    loan_over_effective_money_dict,\
    loan_over_effective_salary_dict,\
    can_take_loan_effective_based_on_money,\
    can_take_loan_effective_based_on_salary = create_report(df)


    return {'statusCode' : 200,
            'body': json.dumps({"hello":"world"})
            }


def liberta_leasing_analyze_handler(event, context):
    '''
    lambda handler function
    '''
    # snippet necessary in case of integration with API GATEWAY (rest api)
    if "body" in event.keys():
        event = json.loads(event["body"])

    amount = event["amount"]
    n_months = event["n_months"]
    url = event["url"]
    bank = event["bank"]

    filename = download_url(url)
    
    df = pd.read_excel(f"/tmp/{filename}")
    
    df = util_ETL_bank(df, "OTHER")
    
    effective_money_dict,\
    effective_salary_dict,\
    effective_loan_dict,\
    average_salary,\
    average_loan,\
    salary_bracket,\
    loan_bracket,\
    loan_over_effective_money_dict,\
    loan_over_effective_salary_dict,\
    can_take_loan_effective_based_on_money,\
    can_take_loan_effective_based_on_salary = create_report(df)


    return {'statusCode' : 200,
            'body': json.dumps({"hello":"world"})
            }

if __name__ =='__main__':
    test()
  
