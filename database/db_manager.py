import sqlalchemy as db
import sqlalchemy
from sqlalchemy import create_engine, inspect
import os
import pandas as pd

from get_database import get_database


class DBconnect:
    __cnx = None  # Do not modify
    __user = 'admin'
    __password = 'Sigibaba123'
    # __host = os.environ.get("DATABASE_ENDPOINT",
    #                         default=False)  # 'cct-db.caeczgelrws8.us-east-1.rds.amazonaws.com'
    __host = 'cct-db.caeczgelrws8.us-east-1.rds.amazonaws.com'
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


if __name__ == '__main__':
    # c = DBconnect()
    # cn = c.connect()
    # inspector = inspect(cn.engine)
    #
    # df = get_database()
    # df.to_sql('cct', con=cn.engine, if_exists='append', index=False, chunksize=1000)
    #
    # print(get_df(cn, 'cct'))
    #
    # print(inspector.get_table_names())
    pass
