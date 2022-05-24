import glob2
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")
data_csv_container =  st.beta_container()
cash_container =  st.beta_container()
loan_to_income_container =  st.beta_container()
#income_bracket_container = st.beta_container()
#other_container =  st.beta_container()
#wire_anomaly_container =  st.beta_container()
cash_container, income_bracket_container = st.beta_columns((2, 1))
other_container, wire_anomaly_container = st.beta_columns((2, 1))



BANK_OPERATIONS = [
    "TRANSFER", "TRANSFER COMMISSION","TRANSFER BETWEEN CUSTOMERS","CONTRIBUTION",
    "TAX","SALARY", "VAT", "WEB PURCHASE", "POS/WEB",
    "AIRTIME", "PURCHASE", "INSTANT PAYMENT",
    "CASH","WITHDRAWAL", "ATM", "SMS ALERT CHARGE",
    "FAILED", "FUNDS", "FAILED","FUNDS","LOAN","INTEREST",
    "GTWORLD", "LOANDISBURSEMENT","FOOD"
    ]

DTI_EARNERS = {
    "LOW_EARNER": 0.33,
    "LOW_MED_EARNER": 0.35,
    "MED_EARNER": 0.40,
    "HIGH_MED_EARNER": 0.45,
    "HIGH_EARNER": 0.5,
    "TOP_EARNER": 0.55
}

BRACKET_COLORS =  {
    "LOW_EARNER": "red",
    "LOW_MED_EARNER": "orange",
    "MED_EARNER": "yellow",
    "HIGH_MED_EARNER": "lightgreen",
    "HIGH_EARNER": "blue",
    "TOP_EARNER": "blue"
}


if __name__=='__main__':

    with st.form("my_form"):
        with data_csv_container:
            list_of_folders = [f for f in glob2.glob("./data/*") if os.path.isdir(f)]

            option = st.selectbox(
            'Which customer do you want to review?',
            list_of_folders
            )

        with other_container:
            
            chart_data = pd.read_csv(f"{option}/analytix/monthly_other.csv",sep=';')

            if chart_data['effective'].mean() <0:
                msg="Other type of expenditures:"
                ## 1f77b4 : muted blue
                st.markdown(f'<p style="color:black;font-size:18px;border-radius:2%;">{msg}</p>', unsafe_allow_html=True)
                
            else:
                msg="Risk of Hidden Loan"
                st.markdown(f'<p style="text-decoration:underline;color:red;font-size:18px;border-radius:2%;">{msg}</p>', unsafe_allow_html=True)
            
            chart_data["color"] = chart_data["effective"].astype('float').apply(lambda x: "lightcoral"  if x>0 else "lightblue" )
            
            fig = go.Figure(
                
                data=go.Bar(
                x=list(chart_data["Trans. Date"]), 
                y=list(chart_data["effective"]),
                #mode='lines+markers',
                #line_shape='spline'
                marker_color=list(chart_data["color"]),
                ))

            st.plotly_chart(fig, use_container_width=True)


        with wire_anomaly_container:
        
            msg="Money Transfert movement trough time:"
            st.markdown(f'<p style="color:rblack;font-size:18px;border-radius:2%;">{msg}</p>', unsafe_allow_html=True)

            chart_data = pd.read_csv(f"{option}/analytix/monthly_anomaly.csv",sep=';')
            fig = go.Figure(
                data = go.Table(
                    header=dict(values=chart_data.columns),
                    cells=dict(values=[chart_data[el].values for el in  chart_data.columns])
                    )
                )
            st.plotly_chart(fig, use_container_width=True)

    
        with cash_container:
            all_csv = glob2.glob(f"{option}/analytix/*.csv")
        
            msg = "Cash withdrawal trough time:"
            st.markdown(f'<p style="color:rblack;font-size:18px;border-radius:2%;">{msg}</p>', unsafe_allow_html=True)


            #st.write('csv files: ', all_csv)
            chart_data = pd.read_csv(f"{option}/analytix/cash_all_operations.csv",sep=';')
            
            chart_data["cash_operation"] = chart_data["effective"].astype('int').apply(lambda x: "debit" if x<0 else "credit")
            fig = px.bar(
                chart_data, 
                x="Trans. Date", 
                y="effective", 
                color="cash_operation",
                color_discrete_sequence=px.colors.qualitative.Pastel1
                )

            st.plotly_chart(fig, use_container_width=True)

        with income_bracket_container:
            chart_data = pd.read_csv(f"{option}/analytix/one_line_info.csv",sep=';')
            st.title(f"\n")

            print(chart_data["IOU"].values[0])
            iou = "lightblue" if chart_data["IOU"].values[0] == False else "lightcoral"
            ddebt = "lightblue" if chart_data["DDEBT"].values[0] == True else "lightcoral"

            bracket = chart_data["BRACKET"].values[0]
            bracket_col = BRACKET_COLORS[bracket]

            loan_to_income = chart_data["LOAN_TO_INCOME"].values[0]

            loan_to_income_col = "lightblue" if loan_to_income < DTI_EARNERS[bracket] else "lightcoral"

            st.title(f"\n")
            st.markdown(f"<h1 style='text-align: center; color: {iou};'>IOU</h1>", unsafe_allow_html=True)
            st.title(f"\n")
            st.markdown(f"<h1 style='text-align: center; color: {ddebt};'>DDEBT</h1>", unsafe_allow_html=True)
            st.title(f"\n")
            st.markdown(f"<h1 style='text-align: center; color: {bracket_col};'>{bracket}</h1>", unsafe_allow_html=True)
            st.title(f"\n")
            st.markdown(f"<h1 style='text-align: center; color: {loan_to_income_col};'>TOTAL LOAN TO INCOME</h1>", unsafe_allow_html=True)
            st.title(f"\n")
            st.title(f"\n")