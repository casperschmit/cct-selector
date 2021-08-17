# ------------------------------------------------------------- #
# Import database through google API
# ------------------------------------------------------------- #
import gspread
import socket
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import pathlib

database_url = "https://docs.google.com/spreadsheets/d/1LWuYPcuovqe97nsCe8JG22mdVJERhEE06S5f_qH9OBg/edit#gid=0"
api_key = str(pathlib.Path(__file__).parent.resolve()) + "/database-api-key.json"

def get_database():
    socket.setdefaulttimeout(180)
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(api_key, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_url(database_url)
    database = sh.worksheet("database").get_all_values()
    df = pandas.DataFrame(data=database)
    return df

