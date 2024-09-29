import yfinance as yf
import datetime
import pandas as pd
import json
from postgres_client import PostgresSingleton

with open('config.json', 'r') as file:
    config = json.load(file)
    
ddl_flag = config['ingestion']['run_ddl']
db_user = config['database']['user']
db_password = config['database']['password']
db_host = config['database']['host']
db_port = config['database']['port']
db_name = config['database']['db_name']
period = config['timeperiod']
db = PostgresSingleton(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
connection = db.get_connection()
connection.autocommit = True

if ddl_flag == 'Y':
    try:
        ddl_file = open('ddl.sql', 'r')
        ddl_script = ddl_file.read()
        for script in ddl_script.split(';'):
            print(f'ingesting ddl {script}')
            try:
                connection.cursor().execute(script)
            except Exception as e:
                print(e)    
        print('ddl ingested')
    except Exception as e:
        print(e)
        

df_snp500 = pd.read_csv('snp_500.csv')
all_tickers = df_snp500['Symbol'].unique()

for ele in all_tickers:
    ticker = f'{ele.strip()}'
    print(f'ingesting ele {ticker}')
    try:
        msft = yf.Ticker(ticker)
        hist = msft.history(period=period)
        financials = msft.financials.T.reset_index()
        balance_sheet = msft.balance_sheet.T.reset_index()
        cash_flow = msft.cashflow.T.reset_index()
    except Exception as e:
        print(e)
    
    try:
        print(f'historical trade data ingesting for {ticker}')
        hist = hist.reset_index()
        hist['Date'] =  hist['Date'].dt.tz_localize(None)
        hist['Date'] =  hist['Date'].astype('str')
        hist['stock_symbol'] = ticker
        hist = hist[['Date', 'stock_symbol', 'Close', 'Volume']]
        data_hist = hist.to_records(index=False).tolist()
        insert_query_hist = """
        INSERT INTO stock_closing (trade_datetime, stock_symbol, closing_price, volume) VALUES (%s, %s, %s, %s)
        """
        connection.cursor().executemany(insert_query_hist, data_hist)
        print(f'historical trade data ingested for {ticker}')
    except Exception as e:
        print(e)
        
    try:
        print(f'historical income data ingesting for {ticker}')
        financials['index'] = financials['index'].astype('str')
        financials['stock_symbol'] = ticker
        insert_financial_data = financials[['index','stock_symbol','EBITDA','EBIT','Diluted EPS','Basic EPS','Net Income','Tax Provision','Pretax Income','Operating Income','Operating Expense','Gross Profit','Total Revenue','Operating Revenue']].to_records(index=False).tolist()
        insert_query_financial = """
        INSERT INTO financial_data (period, stock_symbol, ebitda, ebit, diluted_eps, basic_eps, net_income, tax_provision, pretax_income, operating_income, operating_expense, gross_profit, total_revenue, operating_revenue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        connection.cursor().executemany(insert_query_financial, insert_financial_data)
        print(f'historical income data ingested for {ticker}')
    except Exception as e:
        print(e)

    try:
        print(f'historical balance sheet data ingesting for {ticker}')
        balance_sheet['index'] = balance_sheet['index'].astype('str')
        balance_sheet['stock_symbol'] = ticker
        insert_query_balance_sheet = """
        INSERT INTO balance_sheet (period, stock_symbol, ordinary_shares_number, share_issued, total_debt, cash_and_cash_equivalents) VALUES (%s, %s, %s, %s, %s, %s)
        """
        insert_balance_sheet_data = balance_sheet[['index','stock_symbol','Ordinary Shares Number','Share Issued','Total Debt','Cash And Cash Equivalents']].to_records(index=False).tolist()
        connection.cursor().executemany(insert_query_balance_sheet, insert_balance_sheet_data)
        print(f'historical balance sheet data ingested for {ticker}')
    except Exception as e:
        print(e)

    try:
        
        print(f'historical cash flow data ingesting for {ticker}')
        cash_flow['index'] = cash_flow['index'].astype('str')
        cash_flow['stock_symbol'] = ticker
        insert_query_cash_flow = """
        INSERT INTO cash_flow (period, stock_symbol, free_cash_flow, end_cash_position, begin_cash_position, changes_in_cash, operating_cashflow, cashflow_from_cont_operation) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """
        insert_cashflow_data = cash_flow[['index','stock_symbol','Free Cash Flow','End Cash Position','Beginning Cash Position','Changes In Cash','Operating Cash Flow','Cash Flow From Continuing Operating Activities']].to_records(index=False).tolist()
        connection.cursor().executemany(insert_query_cash_flow, insert_cashflow_data)
        print(f'historical cash flow data in ingested for {ticker}')
    except Exception as e:
        print(e)
