import pandas as pd
from sqlalchemy import create_engine


class DBconnect:
    __cnx = None  # Do not modify
    __user = 'admin'
    __password = # TODO fill in db password
    # __host = os.environ.get("DATABASE_ENDPOINT",
    #                         default=False)  # 'cct-db.caeczgelrws8.us-east-1.rds.amazonaws.com'
    __host = # TODO fill in db host
    __port = '3306'
    __database = 'main'

    def get_connection_string(self):
        return 'mysql+pymysql://' + self.__user + ':' + self.__password + '@' + self.__host + '/' + self.__database

    def connect(self):
        connection_string = 'mysql+pymysql://' + self.__user + ':' + self.__password + '@' + self.__host + '/' + self.__database
        cnx = create_engine(connection_string).connect()
        return cnx


def get_df(cnx, table_name):
    df = pd.read_sql_table(table_name, cnx)
    return df
