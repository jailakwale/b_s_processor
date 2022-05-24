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

    corrected_dataframe = corrected_dataframe[corrected_dataframe["CLASSE"]=="transfer"]
    corrected_dataframe.loc[:]["Trans. Date"] = pd.to_datetime(corrected_dataframe["Trans. Date"], errors='coerce')
    corrected_dataframe.set_index('Trans. Date', inplace=True)
    corrected_dataframe.index = pd.to_datetime(corrected_dataframe.index)
    
    number_of_transfer = len(set(list(corrected_dataframe.index)))
    #paid_info = np.array([[el.month,el.day] for el in set(list(corrected_dataframe.index))])
    #paid_month, paid_day = paid_info[:,0],paid_info[:,1]

    #paid_day_mean, paid_day_variance = np.mean(paid_day), np.std(paid_day) 

    transfer_numeric = corrected_dataframe.loc[:,["Debits","Credits"]]
    
    for cat in ["Debits","Credits"] :
        transfer_numeric[cat].fillna(0, inplace=True)
    
    for cat in ["Debits","Credits"] :
        transfer_numeric[cat] = transfer_numeric[cat].astype(str).str.replace(",","")
    
    transfer_numeric["effective"] = transfer_numeric["Credits"].astype('float') - transfer_numeric["Debits"].astype('float')
    
    
    #aggregation - monthly income
    df_transfer_summary = transfer_numeric[["effective"]].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()
    
    # check if the salary info describes income or paid salary
    total_transfer = df_transfer_summary["effective"].sum()
    
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
    print(salary.shape)
    salary.loc[:]["Trans. Date"] = pd.to_datetime(salary["Trans. Date"], errors='coerce')
    salary.set_index('Trans. Date', inplace=True)
    salary.index = pd.to_datetime(salary.index)
    
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
    

    paid_month, paid_day = paid_info[:,0],paid_info[:,1]

    paid_day_mean, paid_day_variance = np.mean(paid_day), np.std(paid_day) 

    salary_numeric = salary.loc[:,["Debits","Credits"]]

    for cat in ["Debits","Credits"] :
        salary_numeric[cat].fillna(0, inplace=True)

    for cat in ["Debits","Credits"] :
        salary_numeric[cat] = salary_numeric[cat].astype(str).str.replace(",","")

    salary_numeric["effective"] = salary_numeric["Credits"].astype('float') - salary_numeric["Debits"].astype('float')

    #aggregation - monthly income
    df_salary_summary = salary_numeric[["effective"]].groupby(pd.Grouper(level='Trans. Date',freq='M')).sum()

    # check if the salary info describes if it is really a received income or rather a paid salary
    salary_paid_to_employees = df_salary_summary["effective"].sum() <0

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



def loan_analysis(amount, n_months, data_path):
    '''
    function which returns the amount borrowable per month
    '''
    df = pd.read_csv(data_path, sep=';')
    df["CLASSE"] = df["preds"]
    df_loan = df[df["CLASSE"]=='loan']
    df_transfer = df[df["CLASSE"]=='transfer']
    df_salary = df[df["CLASSE"]=='salary']

    result_loan = create_loan_summary(df)['loan_summary']

    result_salary = create_salary_summary(df)['salary_summary']

    result_loan_to_summary, salary_bracket = loan_to_salary_ratio(df)

    result_no_access_to_debt = no_access_to_direct_debit_criteria(df)
    

    original_ratio_to_borrow =  (np.abs(result_loan["effective"]) / result_salary["effective"]).mean()
    
    if  original_ratio_to_borrow < DTI[salary_bracket]:
        ratio_to_borrow = ((amount/n_months) + np.abs(result_loan["effective"])) / result_salary["effective"]
        borrow_as_is=True
        monthly_allowed_amount_to_borrow = DTI[salary_bracket] * result_salary["effective"] - np.abs(result_loan["effective"])
        monthly_allowed_amount_to_borrow = monthly_allowed_amount_to_borrow.apply(lambda x :max(0,x)).mean()
        tenure = np.abs(amount/monthly_allowed_amount_to_borrow)
    else:
        ratio_to_borrow = 0
        monthly_allowed_amount_to_borrow = pd.DataFrame([0], columns=["monthly_allowed"]).mean()
        borrow_as_is = False
        tenure = pd.DataFrame([0], columns=["monthly_allowed"])
    return tenure, monthly_allowed_amount_to_borrow, amount,n_months,salary_bracket, borrow_as_is, original_ratio_to_borrow




def full_analysis(data_path):
    '''
    perform all steps to extract metrics to deny of accept loans
    '''
    df = pd.read_csv(data_path, sep=',')
    print(df.shape)
    df_loan = df[df["CLASSE"]=='loan']
    df_transfer = df[df["CLASSE"]=='transfer']
    df_salary = df[df["CLASSE"]=='salary']

    result_loan = create_loan_summary(df)

    #result_transfer = create_transfer_between_summary(df)

    result_salary = create_salary_summary(df)

    result_loan_to_summary, salary_bracket = loan_to_salary_ratio(df)

    result_no_access_to_debt= no_access_to_direct_debit_criteria(df)


    n_payments = result_salary["number_of_payments"]
    paid_months = (" ").join([str(m) for m in result_salary["paid_month"]])
    paid_days = (" ").join([str(m) for m in result_salary["paid_days"]])
    mean_day_salary = result_salary["paid_day_mean"]
    var_salary = result_salary["paid_day_variance"]
    no_access_to_debt = result_no_access_to_debt

    return(result_loan["n_loans_summary"], 
            result_loan["loan_summary"],
            result_salary["number_of_payments"],
            result_salary["paid_month"],
            result_salary["paid_days"],
            result_salary["paid_day_mean"],
            result_salary["paid_day_variance"],
            result_salary["salary_summary"],
            result_no_access_to_debt,
            result_loan_to_summary,
            salary_bracket)


def liberta_leasing_analyze_handler(event, context):
    amount = event["amount"]
    n_months = event["n_months"]
    url = event["url"]

    LL_tenure, LL_monthly_allowed_amount_to_borrow, LL_amount, LL_n_months, LL_salary_bracket, LL_borrow_as_is, LL_original_ratio_to_borrow = loan_analysis(amount, n_months, url)
    return {'statusCode' : 200,
           'body': json.dumps({
                   "tenure": json.dumps(LL_tenure),
                   "monthly_allowed_amount_to_borrow": json.dumps(LL_monthly_allowed_amount_to_borrow),
                   "amount_requested": json.dumps(LL_amount),
                   "tenure_requested": json.dumps(LL_n_months),
                   "loan_request": json.dumps(LL_borrow_as_is),
                   "original_loan_ratio_salary": json.dumps(LL_original_ratio_to_borrow),
                   "salary_bracket": json.dumps(LL_salary_bracket),
                   "authorized_ratio": json.dumps(DTI[LL_salary_bracket])
                   })
           }
