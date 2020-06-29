import pymysql.cursors
import pymysql
import array
import json
from datetime import datetime
import pandas as pd

class db:
    def __init__(self):
        connection = pymysql.connect(host='localhost', user='pi', password='raspberry', db='carnavigation', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.connector = connection

    def getAll(self):
        try:
            df = pd.read_sql('SELECT * FROM car', con=self.connector)
        finally:
            self.connector.close()
        return df

    def insertTable(self, table_name, inserted_array ):
        inserted = False;
        insert_val = responce = []
        timestamp = datetime.now().strftime('%Y-%m-%d')

        if table_name :
            sql = "INSERT INTO "+table_name+" ("
            for key, value in inserted_array.items():
                sql += " `"+key+"`, ";
            sql = sql[:-2]
            sql += ") values ( "
            for key, value in inserted_array.items():
                sql += "%s, "
                insert_val.append(value)
            sql = sql[:-2]
            sql += " ) "
            sql += "on duplicate key update"
            sql += " `date` = current_timestamp, ";
            sql += " `latitude_old` = latitude, ";
            sql += " `longitude_old` = longitude, ";
            for key, value in inserted_array.items():
                sql += " `"+key+"` = " + value + ", ";
            sql = sql[:-2]

            try:
                with self.connector.cursor() as cursor:
                    cursor.execute(sql, insert_val)
                    self.connector.commit()
                    inserted = True
            finally:
                #self.connector.close()
                print()

            if inserted:
                responce = {"message": "inserted succesfully"}
            else:
                responce = {"message": "problem occured"}

            return responce;

    def fetchRow(self, table_name, collum_name, where_arr = []):
        where_cond = ' WHERE 1'
        insert_val = result = responce = []
        try:
            with self.connector.cursor() as cursor:
                sql = "SELECT "

                for collums in collum_name:
                    sql += "`"+collums+"`, ";
                sql = sql[:-2]
                sql += " FROM "+table_name
                if where_arr:
                    for key, value in where_arr.items():
                        where_cond += ' and `'+key+'`= %s'

                    for key, value in where_arr.items():
                        insert_val.append(value)

                sql = sql+where_cond
                cursor.execute(sql, (insert_val))
                result = cursor.fetchone()
                responce = {"data" : result}
        finally:
            self.connector.close()

        return responce

    def fetchAll(self, table_name, collum_name, where_arr = []):
        where_cond = ' WHERE 1'
        insert_val = result = responce = []
        try:
            with self.connector.cursor() as cursor:
                sql = "SELECT "

                for collums in collum_name:
                    sql += "`"+collums+"`, ";
                sql = sql[:-2]
                sql += " FROM "+table_name
                if where_arr:
                    for key, value in where_arr.items():
                        where_cond += ' and `'+key+'`= %s'

                    for key, value in where_arr.items():
                        insert_val.append(value)

                sql = sql+where_cond
                cursor.execute(sql, (insert_val))
                result = cursor.fetchall()
                responce = {"data" : result}
        finally:
            self.connector.close()

        return responce

    def updateTable(self, table_name = '', updated_val = [], where_arr = []):
        responce = where_final_arr = [];
        sql = collum_str = where_str = ""
        try:
            with self.connector.cursor() as cursor:
                if table_name :
                    for key,value in updated_val.items():
                        collum_str = '`'+key+'` = "'+value+'", '

                    collum_str = collum_str[:-2]
                    for key, value in where_arr.items():
                        where_str = ' and `'+key+'` = %s'
                        where_final_arr.append(value)

                    sql = "update "+table_name+" set "+collum_str+" where 1 "+where_str
                    cursor.execute(sql, (where_final_arr))
                    self.connector.commit()
                    responce = {"message": "updated succesfully" }
                else:
                    responce = {"type":False, "message": "Provide valid table name" }
        finally:
            self.connector.close()
        return responce;

    def deleteTable(self, table_name = '', where_arr = []):
        responce = where_final_arr = []
        sql = where_str = '';

        for key, value in where_arr.items():
            where_str = ' and `'+key+'` = %s'
            where_final_arr.append(value)
        if table_name:
            sql = "DELETE FROM `"+table_name+"` "
            try:
                with self.connector.cursor() as cursor:
                    sql = sql+" where 1 "+where_str;
                    cursor.execute(sql, (where_final_arr))
                    self.connector.commit()
                    responce = {"message": "deleted succesfully" }
            finally:
                self.connector.close()
        else:
            responce = {"message" : "Provide valid table name" }

        return responce
