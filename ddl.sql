CREATE TABLE stock_closing (
    trade_datetime Timestamp NOT NULL,
    stock_symbol VARCHAR(10) NOT NULL,   
    closing_price DECIMAL(10, 2) NOT NULL, 
    volume BIGINT NOT NULL,              
    PRIMARY KEY (trade_datetime, stock_symbol) 
);

CREATE TABLE financial_data (
    period Timestamp,
    stock_symbol VARCHAR(10),
    ebitda DECIMAL(15, 2),
    ebit DECIMAL(15, 2),
    diluted_eps DECIMAL(10, 4),
    basic_eps DECIMAL(10, 4),
    net_income DECIMAL(15, 2),
    tax_provision DECIMAL(15, 2),
    pretax_income DECIMAL(15, 2),
    operating_income DECIMAL(15, 2),
    operating_expense DECIMAL(15, 2),
    gross_profit DECIMAL(15, 2),
    total_revenue DECIMAL(15, 2),
    operating_revenue DECIMAL(15, 2),
    PRIMARY KEY (period, stock_symbol) 
);

CREATE TABLE balance_sheet (
    period Timestamp,  
    stock_symbol VARCHAR(10),  
    ordinary_shares_number DECIMAL(15, 2),  
    share_issued DECIMAL(15, 2),  
    total_debt DECIMAL(15, 2),  
    cash_and_cash_equivalents DECIMAL(15, 2),  
    PRIMARY KEY (period, stock_symbol)  
);

CREATE TABLE cash_flow (
    period timestamp,
    stock_symbol VARCHAR(10),
    free_cash_flow DECIMAL(15, 2),
    end_cash_position DECIMAL(15, 2),
    begin_cash_position DECIMAL(15, 2),
    changes_in_cash DECIMAL(15, 2),
    operating_cashflow DECIMAL(15, 2),
    cashflow_from_cont_operation DECIMAL(15, 2),
    PRIMARY key (period, stock_symbol)
);