import pymysql
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import json

class Dbcon:

    def __init__(self, sql, control):
        con = pymysql.connect(host='localhost', user='sungmin_lim', password='qwerty', db='', charset='utf8')
        
        this.sql = sql
        this.control = control
        curs = None
        print('success')

    def db_define():

        # result by dict
        if control == 1 or control == 2:
            curs = con.cursor(pymysql.cursors.DictCursor)
            db_activity(control)

        # input or delete data to db
        else:
            curs = con.cursor()
            db_activity(control)

        return curs

    def db_activity(control):

        if control == 1:
            curs.execute(sql)

            except con.Error as error:
                con.rollback()
                datas = curs.fet


                print('error')

    def db_errors



