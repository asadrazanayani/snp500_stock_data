# snp500_stock_data
stock closing and financial information

# Listing Information
- Listing information for SnP500 can be found at https://en.wikipedia.org/wiki/List_of_S%26P_500_companies

# How to use this repository
0. Clone the repository to a directory on your local computer.
1. Change the `[database]` in `config.json` to reflect the SQL database of your choice running either locally or on a dedicated server
2. The `[ingestion][run_ddl]` option `Y` runs the `ddl.sql` before the data ingestions and therefore, it is the default option.
3. Create a virtual python enviornment.
    - 3a. Install python on your local computer.
        - i. create a virual env and activate  
            ```bash
            python -m venv venv
            <!-- create virtual env -->
            ```
            ```bash
            source venv/bin/activate
            <!-- activates the virtual env -->
            ```
        - ii. Install the `requirements.txt`
            ```bash
            pip install -r requirements.txt
            ```
        - iii. Run the main.py script
            ```bash
            python main.py
            ```
