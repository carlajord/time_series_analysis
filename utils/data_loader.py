import os, sys, json

from datetime import datetime, timedelta, time

import duckdb
from duckdb import DuckDBPyConnection

import pandas as pd
import logging

from dotenv import load_dotenv

from cognite.client import CogniteClient
from cognite.client.config import ClientConfig
from cognite.client.credentials import OAuthClientCredentials

import utils.constants as consts

load_dotenv()

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data")
DB_PATH = os.path.join(DATA_PATH, "database.duckdb")
VAR_MAP_PATH = os.path.join(DATA_PATH, "cdf_var_map.json")

def init_db() -> DuckDBPyConnection:

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        logging.error(f"{consts.ERROR}: Database file not found. Creating a new DuckDB database")
    conn = duckdb.connect(DB_PATH)

    return conn

def create_cdf_client():

    client_id = os.getenv("CDF_CLIENT_ID")
    client_secret = os.getenv("CDF_CLIENT_SECRET")
    tenant_id = os.getenv("CDF_TENANT_ID")
    base_url = os.getenv("CDF_URL")
    project = os.getenv("CDF_PROJECT")

    if not client_id or not client_secret:
        raise ValueError("Missing Cognite API credentials. CDF_CLIENT_ID and CDF_CLIENT_SECRET.")

    creds = OAuthClientCredentials(
      token_url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
      client_id=client_id,
      client_secret=client_secret,
      scopes=[f"{base_url}/.default"]
    )

    config = ClientConfig(
      client_name="my-special-client",
      base_url=base_url,
      project=project,
      credentials=creds
    )

    client = CogniteClient(config)

    return client


def get_data_info(table, data_type=None):

    with open(VAR_MAP_PATH, 'r') as file:
        var_map = json.load(file)

    data_info = consts.ALL_CDF_VARIABLES[table]
    if data_type in [consts.TAG, consts.PI_NUMBER]:
        data_info = [var_map[table][var_name][data_type] for var_name in consts.ALL_CDF_VARIABLES[table]]

    return data_info


def get_cognite_data(granularity, start_date, end_date, table):

    id_vals = get_data_info(table, data_type=consts.PI_NUMBER)
    client = create_cdf_client()
    datapoints_df = client.time_series.data.retrieve_dataframe(
        external_id=id_vals,
        aggregates=["average"],
        granularity=granularity,
        start=pd.to_datetime([start_date])[0],
        end=pd.to_datetime([end_date])[0],
    )
    datapoints_df.columns = consts.ALL_CDF_VARIABLES[table]
    datapoints_df = datapoints_df.reset_index(names=[consts.TIMESTAMP])

    return datapoints_df

def fetch_dataframe(table_name: str):
    conn = init_db()
    df = conn.execute(f'SELECT * FROM "{table_name}"').fetchdf()
    conn.close()
    return df

def fetch_data_from_cognite(table, timeframe: list = []) -> pd.DataFrame:

    if timeframe:
        start_date, end_date = timeframe
    else:
        end_date = datetime.today().strftime("%Y-%m-%d")
        start_date = datetime.today() - timedelta(days=366)
        start_date=start_date.strftime("%Y-%m-%d")

    print("\nFetching data from Cognite...")
    print("Start date:", start_date)
    print("End date:", end_date)

    df = get_cognite_data(
        table=table,
        granularity=consts.GRANULARITY,
        start_date=start_date,
        end_date=end_date)

    return df

def update_db(table_name:str, timeframe: list = []):

    try:
        conn = init_db()
        df = fetch_data_from_cognite(table_name, timeframe)
        print(f"Collected data from {table_name}")

    except Exception as e:
        logging.error(f"{consts.ERROR}: Failed to collect {table_name} data from Cognite {e}.\n")
        msg = f"{consts.ERROR}: Failed to collect {table_name} data from Cognite {e}.\n"
        return msg
    
    try:
        # update db
        query = f'DROP TABLE IF EXISTS "{table_name}"'
        conn.execute(query)
        query = f'CREATE TABLE "{table_name}" AS SELECT * FROM df'
        conn.query(query)
        msg = f"{consts.SUCCESS}: {table_name} data was successfully updated\n"

    except Exception as e:
        logging.error(f"{consts.ERROR}: Could not update DuckDB: {e}\n")
        msg = f"{consts.ERROR}: Could not update DuckDB: {e}\n"

    return msg


def get_table_names():
    conn = init_db()
    query = "SHOW TABLES;"
    existing_tables = list(conn.sql(query).df()['name'])
    return existing_tables


def load_data(required_tables: list):

    """
    Checks database schema and timeframe compliance and triggers update if needed
    """

    msg = ""
    for table_name in required_tables:
        msg = msg + update_db(table_name)

    return msg
