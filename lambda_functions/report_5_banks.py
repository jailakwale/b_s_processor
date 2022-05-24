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

def create_salary_bracket(salary_dollars):
    '''
    rules to define the salary bracket
    '''
    bracket = ''
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



def try_convert(x):
    try :
        if x != None:
            x = float(x)
        else:
            x = 0
    except Exception as e:   
        x = 0
    return x


def liberta_leasing_convert_handler(event, context):
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
  
  col1 = "Withdrawal"
  col2 = "Deposit"
        
  df = pd.read_excel(url)      

  cols = [col1,col2] 
  
  for c in cols:
      df[c]= df[c].astype('str').str.strip().str.replace(",","").str.replace("NaN","")
  
  
  df[cols[0]] = df[cols[0]].apply(lambda x: try_convert(x)).fillna(0).astype('float')
  df[cols[1]] = df[cols[1]].apply(lambda x: try_convert(x)).fillna(0).astype('float')
  df["Total"] = df[cols[0]] + df[cols[1]] 
  result_aggregated = df.groupby("CLASSE").aggregate('sum')["Total"]
  
  
  # date
  df["Tran date"] = df["Tran date"].apply(lambda x: pd.to_datetime(x))
  monthly_transactions = df.set_index("Tran date").groupby("CLASSE").resample('M').sum()["Total"]
  final_df = pd.DataFrame(monthly_transactions).reset_index()
  

        
  # df_cash
  DF_CASH = final_df[final_df["CLASSE"]=="CASH"].copy()
  DF_CASH["Tran date"] = DF_CASH["Tran date"].dt.strftime('%Y-%m')
  
  # df_transfert
  DF_TRANSFERT = final_df[final_df["CLASSE"]=="TRANSFERT"].copy()
  DF_TRANSFERT["Tran date"] = DF_TRANSFERT["Tran date"].dt.strftime('%Y-%m')
  
  # df_charges
  DF_CHARGES = final_df[final_df["CLASSE"]=="CHARGES"].copy()
  DF_CHARGES["Tran date"] = DF_CHARGES["Tran date"].dt.strftime('%Y-%m')
  
  # df_payment
  DF_PAYMENT = final_df[final_df["CLASSE"]=="PAYMENT"].copy()
  DF_PAYMENT["Tran date"] = DF_PAYMENT["Tran date"].dt.strftime('%Y-%m')

  # df_reversal
  DF_REVERSAL = final_df[final_df["CLASSE"]=="REVERSAL"].copy()
  DF_REVERSAL["Tran date"] = DF_REVERSAL["Tran date"].dt.strftime('%Y-%m')
  
  # df_salary
  DF_SALARY = final_df[final_df["CLASSE"]=="SALARY"].copy()
  DF_SALARY["Tran date"] = DF_SALARY["Tran date"].dt.strftime('%Y-%m')
  
  # successive joins (cash + transfert)
  cash_transfert = DF_CASH.merge(DF_TRANSFERT, on="Tran date", how="outer")
  classe_pair = ["CASH","TRANSFERT"]
  cash_transfert.columns  = [f"CLASSE_{classe_pair[0]}",
                             "Tran date",
                             f"TOTAL_{classe_pair[0]}",
                             f"CLASSE_{classe_pair[1]}",
                             f"TOTAL_{classe_pair[1]}"]

  cash_transfert_df = cash_transfert[["Tran date", f"TOTAL_{classe_pair[0]}",f"TOTAL_{classe_pair[1]}"]]

  
  # successive joins (charges + payment)
  charges_payment = DF_CHARGES.merge(DF_PAYMENT, on="Tran date", how="outer")
  classe_pair = ["CHARGES","PAYMENT"]
  charges_payment.columns  = [f"CLASSE_{classe_pair[0]}",
                             "Tran date",
                             f"TOTAL_{classe_pair[0]}",
                             f"CLASSE_{classe_pair[1]}",
                             f"TOTAL_{classe_pair[1]}"]

  charges_payment_df = charges_payment[["Tran date", f"TOTAL_{classe_pair[0]}",f"TOTAL_{classe_pair[1]}"]]
  
  
  # successive joins (reversal + salary)
  reversal_salary = DF_REVERSAL.merge(DF_SALARY, on="Tran date", how="outer")
  classe_pair = ["REVERSAL","SALARY"]
  reversal_salary.columns  = [f"CLASSE_{classe_pair[0]}",
                             "Tran date",
                             f"TOTAL_{classe_pair[0]}",
                             f"CLASSE_{classe_pair[1]}",
                             f"TOTAL_{classe_pair[1]}"]
  reversal_salary_df = reversal_salary[["Tran date", f"TOTAL_{classe_pair[0]}",f"TOTAL_{classe_pair[1]}"]]

  # final join
  summary_df = charges_payment_df.\
  merge(reversal_salary_df, on="Tran date", how="outer").\
  merge(cash_transfert_df, on="Tran date", how="outer")


  

    # df_loan

  DF_LOAN = final_df[final_df["CLASSE"]=="LOAN"].copy()
  DF_LOAN["Tran date"] = DF_LOAN["Tran date"].dt.strftime('%Y-%m')
  DF_LOAN.columns =["CLASSE_LOAN", "Tran date", "TOTAL_LOAN"]
  DF_LOAN.drop(["CLASSE_LOAN"], axis=1, inplace=True)

  summary_df = summary_df.\
  merge(DF_LOAN, on="Tran date", how="outer")
  summary_df.fillna(0, inplace=True)

  eps=1e-6
  summary_df["TOTAL_LOAN/TOTAL_SALARY"] = summary_df["TOTAL_LOAN"]/(summary_df["TOTAL_SALARY"]+eps)
  mean_salary = summary_df[summary_df["TOTAL_SALARY"] !=0]["TOTAL_SALARY"].mean()
  bracket_salary = create_salary_bracket(mean_salary)
  
        
        
    
  
  return {'statusCode' : 200,
         'body': json.dumps({"beacker_salary":bracket_salary})
         }
