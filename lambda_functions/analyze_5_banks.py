import pandas as pd
import numpy as np
import glob2
import json

# set of criterias provided by Liberta leasing

DTI = {
        "LOW_EARNER": 0.33,
        "LOW_MED_EARNER":0.35,
        "MED_EARNER":0.40,
        "HIGH_MED_EARNER":0.45,
        "HIGH_EARNER": 0.5,
        "TOP_EARNER": 0.55
        }

def create_loan_summary(corrected_dataframe):
        '''
        creates the dataframe for the loan info
        '''
        # convert entries to date format
        #self.data.loc[:]["Trans. Date"] = pd.to_datetime(self.Ds.loan["Trans. Date"], errors='coerce')
        
        corrected_dataframe["CLASSE"] = corrected_dataframe["CLASSE"].str.lower()
        
        corrected_dataframe = corrected_dataframe[corrected_dataframe["CLASSE"]=="loan"]
        # create a summary limiting ourselves to some columns
        loan_summary = corrected_dataframe.loc[:,["Trans. Date", "Credits", "Debits"]].copy()
        
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
        df_loan_summary = loan_summary.groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
        
        credits = df_loan_summary.copy()
        debits = df_loan_summary.copy()

        credits[credits['Credits']>0]=1
        debits[debits['Debits']>0]=-1
        
        credits['Credits'].fillna(0,inplace=True)
        debits['Debits'].fillna(0,inplace=True)

        df_credits = credits['Credits'].astype(str).str.replace(",","").astype('float')
        df_debits = debits['Debits'].astype(str).str.replace(",","").astype('float')
            
        total_n_loans_summary = pd.DataFrame(pd.concat([df_debits,df_credits], axis = 1).sum(axis=1))
        total_n_loans_summary.columns = ['#n loans']
        total_n_loans_summary['#n loans'] = total_n_loans_summary['#n loans'].apply(lambda x: np.abs(x))
        
        df_loan_summary["effective"] = -1*df_loan_summary["Debits"].astype('float')+df_loan_summary["Credits"].astype('float')
        print(df_loan_summary)
        loan_dict = {
            "loan_summary" : df_loan_summary, 
            "n_loans_summary": total_n_loans_summary
        }
        return loan_dict
    
def create_salary_bracket(salary_dollars):
    '''
    rules to define the salary bracket
    '''
    if salary_dollars > 50000 and salary_dollars < 200000:
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

def create_transfer_between_summary(corrected_dataframe):
    '''
    summarizes the transferts
    '''
    corrected_dataframe = corrected_dataframe[corrected_dataframe["CLASSE"]=="transfert"]
    corrected_dataframe.loc[:]['Trans. Date'] = pd.to_datetime(corrected_dataframe['Trans. Date'], errors='coerce')
    corrected_dataframe.set_index('Trans. Date', inplace=True)
    corrected_dataframe.index = pd.to_datetime(corrected_dataframe.index)
    
    number_of_transfer = len(set(list(corrected_dataframe.index)))
    #paid_info = np.array([[el.month,el.day] for el in set(list(corrected_dataframe.index))])
    #paid_month, paid_day = paid_info[:,0],paid_info[:,1]

    #paid_day_mean, paid_day_variance = np.mean(paid_day), np.std(paid_day) 

    transfer_numeric = corrected_dataframe.loc[:,["Debits","Credits"]]
    
    # replace na by zeroes
    for cat in ["Debits","Credits"] :
        transfer_numeric[cat].fillna(0, inplace=True)
        
    # numbers  use "," for more readability
    for cat in ["Debits","Credits"] :
        transfer_numeric[cat] = transfer_numeric[cat].astype(str).str.replace(",","")
        
    # effective transferts are the algebric sum of "TO and FRO" transferts
    transfer_numeric["effective"] = transfer_numeric["Credits"].astype('float') - transfer_numeric["Debits"].astype('float')
    
    #aggregation - monthly income
    df_transfer_summary = transfer_numeric[["effective"]].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
    
    # check if the salary info describes income or paid salary
    total_transfer = df_transfer_summary["effective"].sum()
    
    # detailed summary of transferts
    transfer_between_summary_dict = {
        "all_transactions": transfer_numeric,
        "number_of_payments": number_of_transfer,
        "transfer_summary": df_transfer_summary,
        "total_transfer": total_transfer,
    }

    return transfer_between_summary_dict 

def no_access_to_direct_debit_criteria(corrected_dataframe):
    '''
    function which assesses the acces to direct debit
    '''
    bank_id = corrected_dataframe["BANK_ID"].values[0]
    return bank_id.lower() in ["standard charter", "first bank", "stanbic"]

def create_salary_summary(corrected_dataframe):
    '''
    function which creates  a salary report
    '''
    salary = corrected_dataframe[corrected_dataframe["CLASSE"]=="salary"]
        
    assert salary.shape[0] != 0
    
    # conversion of dates to timestamps
    salary.loc[:]["Trans. Date"] = pd.to_datetime(salary["Trans. Date"], errors='coerce')
    salary.set_index('Trans. Date', inplace=True)
    salary.index = pd.to_datetime(salary.index)
    
    # computes the number of salary paycheck have been received
    number_of_payments = len(set(list(salary.index)))
    paid_info = np.array([[el.month, el.day] for el in set(list(salary.index))])
    
    
    salary_dict = {
    "all_transactions": None,
    "number_of_payments": None,
    "paid_month": None,
    "paid_days": None,
    "paid_day_mean": None,
    "paid_day_variance": None,
    "salary_summary": pd.DataFrame(),
    "paid_to_employees": None
    }
    
    # info about paid_month and paid_day
    paid_month, paid_day = paid_info[:,0], paid_info[:,1]

    paid_day_mean, paid_day_variance = np.mean(paid_day), np.std(paid_day) 

    salary_numeric = salary.loc[:,["Debits","Credits"]]

    # replace NAs by zeroes
    for cat in ["Debits","Credits"] :
        salary_numeric[cat].fillna(0, inplace=True)

    # replace "," by "" (the commas are used for bookkeeping readability)
    for cat in ["Debits","Credits"] :
        salary_numeric[cat] = salary_numeric[cat].astype(str).str.replace(",","")
    # algebric sum
    salary_numeric["effective"] = salary_numeric["Credits"].astype('float') - salary_numeric["Debits"].astype('float')

    # aggregation - monthly income
    df_salary_summary = salary_numeric[["effective"]].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()

    # check if the salary info describes if it is really a received income or rather a paid salary
    salary_paid_to_employees = df_salary_summary["effective"].sum()<0

    salary_dict = {
        "all_transactions": salary_numeric,
        "number_of_payments": number_of_payments,
        "paid_month": paid_month,
        "paid_days": paid_day,
        "paid_day_mean": paid_day_mean,
        "paid_day_variance": paid_day_variance,
        "salary_summary": df_salary_summary,
        "paid_to_employees": salary_paid_to_employees
    }
        
    return salary_dict
    
    
def loan_to_salary_ratio(corrected_dataframe):
    '''
    function which creates the loan to salary ratio report 
    '''
    
    df_loan = create_loan_summary(corrected_dataframe)['loan_summary']
    
    df_salary = create_salary_summary(corrected_dataframe)['salary_summary']

    salary_bracket = create_salary_bracket(df_salary["effective"].mean())
    
    loan_to_salary = pd.merge(df_loan['effective'],df_salary['effective'], left_index=True,right_index=True )
    loan_to_salary.columns = ['effective_loan', 'salary']
    loan_to_salary['ratio'] = loan_to_salary['effective_loan']/loan_to_salary['salary']
    return loan_to_salary, salary_bracket

  
def salary_variance(corrected_dataframe):
    '''
    function which returns the salary variance
    '''
    return(create_salary_summary(corrected_dataframe)["salary_summary"].std())



def ETL_bank(raw_df, bank_name):
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
        
    
    return df_no_index
                  

def loan_analysis(amount, n_months, data_path, bank):
    '''
    function which returns the amount borrowable per month
    '''
    if data_path.endswith(".csv"): 
        df = pd.read_csv(data_path, sep=';')
    elif data_path.endswith(".xlsx"): 
        df = pd.read_excel(data_path)
        
    df["CLASSE"] = df["CLASSE"].str.lower()
    print(df.head(5))
    
    # depending on the banks some columns must be mapped
    df = ETL_bank(df, bank)
                
        
    #df["CLASSE"] = df["preds"]
    df_loan = df[df["CLASSE"]=='loan']
    df_transfer = df[df["CLASSE"]=='transfert']
    df_salary = df[df["CLASSE"]=='salary']
        
    print(f"the shape of df_salary is : {df_salary.shape}")
    print(f"the shape of df_transfer is : {df_transfer.shape}")
    print(f"the shape of df_loan is : {df_loan.shape}")

    # build the loan summary report
    result_loan = create_loan_summary(df)['loan_summary']

    #  build the salary report
    result_salary = create_salary_summary(df)['salary_summary']

    # build the loan to salary ratio (via the helper function)
    result_loan_to_summary, salary_bracket = loan_to_salary_ratio(df)

    # access to debt
    result_no_access_to_debt = no_access_to_direct_debit_criteria(df)
    
    # loan entries can be positive/negative - same goes for salary  ("effective" means algebric sum)
    original_ratio_to_borrow =  (np.abs(result_loan["effective"]) / result_salary["effective"]+ 1e-10).mean()
    
    # the ratio to borrow is supplied by LL
    # if the ratio is under the limit (the ratio is calculated based on LL formula) 
    print(result_loan)
    print(original_ratio_to_borrow)

    if  original_ratio_to_borrow < DTI[salary_bracket]:
        ratio_to_borrow = ((amount/n_months) + np.abs(result_loan["effective"])) / (result_salary["effective"]+ 1e-10)
        borrow_as_is=True
        # computes a series of monthly allowed amounts
        monthly_allowed_amount_to_borrow = DTI[salary_bracket] * result_salary["effective"] - np.abs(result_loan["effective"])
        # average the series of monthly allowed amounts
        monthly_allowed_amount_to_borrow = monthly_allowed_amount_to_borrow.apply(lambda x :max(0,x)).mean()
        
        # first calculation (to make sure that the lender does not default
        # number of months = total value divided by the average 
        tenure = np.abs(amount/monthly_allowed_amount_to_borrow)
        

    # if the ratio is under the limit : loan is denied
    #
    # monthly_allowed_amount_to_borrow,  ratio_to_borrow, tenure => 0
    # borrow_as_is = False
        
    else:
        ratio_to_borrow = 0
        monthly_allowed_amount_to_borrow = pd.DataFrame([0], columns=["monthly_allowed"]).mean()
        borrow_as_is = False
        tenure = pd.DataFrame([0], columns=["monthly_allowed"])
        
    return tenure, monthly_allowed_amount_to_borrow, amount,n_months,salary_bracket, borrow_as_is, original_ratio_to_borrow


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


        

  LL_tenure, LL_monthly_allowed_amount_to_borrow, LL_amount, LL_n_months, LL_salary_bracket, LL_borrow_as_is, LL_original_ratio_to_borrow = loan_analysis(amount, n_months, url, bank)
  print(LL_tenure)
  return {'statusCode' : 200,
         'body': json.dumps({
                 "tenure": json.dumps(str(LL_tenure.iloc[0])),
                 "monthly_allowed_amount_to_borrow": json.dumps(str(LL_monthly_allowed_amount_to_borrow.iloc[0])),
                 "amount_requested": json.dumps(LL_amount),
                 "tenure_requested": json.dumps(LL_n_months),
                 "loan_request": json.dumps(LL_borrow_as_is),
                 "original_loan_ratio_salary": json.dumps(LL_original_ratio_to_borrow),
                 "salary_bracket": json.dumps(LL_salary_bracket),
                 "authorized_ratio": json.dumps(DTI[LL_salary_bracket])
                 })
         }
