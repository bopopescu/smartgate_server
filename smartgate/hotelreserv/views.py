from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from identification.models import Userinfo
import pymysql
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import json
from . import condb as db
from django.utils import timezone

# Create your views here.

@csrf_exempt
def user_login(request):

    user_id = request.POST.get('UserID','')
    user_pw = request.POST.get('UserPW', '')

    userInfo = get_object_or_404(Userinfo, uid= 'hello')

    userinfo = userInfo.uid + '/' + userInfo.upw
    return HttpResponse(userinfo)

@csrf_exempt
def dup_check_id(request):

    check_id = request.POST.get('UserID','')

    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'select UID from UserInfo where UID = %s'
        curs.execute(sql, (check_id))

        datas = curs.fetchone()
        print_datas = datas
        errornum = 1

    except con.Error as error:
        con.rollback()
        print('error has occur when finding duplicate ID')
        print(error)
        errornum = 0

    finally:
        con.close()

    if print_datas == None:
        return HttpResponse(0)
    else:
        print(print_datas)
        print(type(print_datas))
        return HttpResponse(print_datas)

@csrf_exempt
def dup_check_email(request):

    check_email = request.POST.get('UserEmail','')

    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'select UMail from UserInfo where UMail = %s'
        curs.execute(sql, (check_email))

        datas = curs.fetchone()
        print_datas = datas
        errornum = 1

    except con.Error as error:
        con.rollback()
        print('error has occur when finding duplicate EMAIL')
        print(error)
        errornum = 0

    finally:
        con.close()

    if print_datas == None :
        return HttpResponse(0)
    else:
        return HttpResponse(print_datas)

@csrf_exempt
def dup_check_phone(request):

    check_phone = request.POST.get('UserTel','')

    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'select UTel from UserInfo where UTel = %s'
        curs.execute(sql, (check_phone))

        datas = curs.fetchone()
        print_datas = datas
        errornum = 1
    
    except con.Error as error:
        con.rollback()
        print('error has occur when finding duplicated UTel')
        print(error)
        errornum = 0

    finally:
        con.close()

    if print_datas == None :
        return HttpResponse(0)
    else:
        return HttpResponse(print_datas)

@csrf_exempt
def add_user(request):

    input_id = request.POST.get('UserID','')
    input_pw = request.POST.get('UserPW','')
    input_name = request.POST.get('UserName','')
    input_tel = request.POST.get('UserTel','')
    input_mail = request.POST.get('UserEmail','')

    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'insert into UserInfo values(%s, %s, %s, %s, %s)'
        curs.execute(sql, (input_id, input_pw, input_name, input_tel, input_mail))
        con.commit()
        errornum = 1

    except con.Error as error:
        con.rollback()
        print('error during insert user informations')
        print(error)
        errornum = 0

    finally:
        con.close()

    if(errornum ==1):
        return HttpResponse(1)
    else:
        return HttpResponse(0)

@csrf_exempt
def log_in(request):
    
    input_id = request.POST.get('UserID','')
    input_pw = request.POST.get('UserPW','')
    login_success = 0 # default 0 means login fail

    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'select UID from UserInfo where UID = %s'
        curs.execute(sql, (input_id))
        id_data = curs.fetchone()

        if id_data is None:
            print('it is not exist in DB. Please Sign in')
        
        else:
            print('id is in DB')
            sql = 'select UPW from UserInfo where UID = %s'
            curs.execute(sql, (input_id))
            compare_pw = curs.fetchone()

            if compare_pw is None:
                print('id is same but pw is uncorrect')
                login_success = 1
            elif compare_pw[0] == input_pw:
                print('login success!')
                login_success = 2
            else:
                print('pw is uncorrect')
                login_success = 1

    finally:
        con.close()

        if login_success == 2:
            print('login success')
            return HttpResponse(2)

        else:
            print('login fail')

            if login_success == 1:
                print('pw is not same')
                return HttpResponse (1)

            else:
                print('cannot find id')
                return HttpResponse(0)

@csrf_exempt
def my_book_list(request):

    userID = request.POST.get('UserID','')
    userID = 'hoi'

    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor(pymysql.cursors.DictCursor)
        sql = 'select * from BookList where BID = %s and date(BCin)>=date(now()) or ( BCin < now() and BCout>now())'
        curs.execute(sql, (userID))
        datas = curs.fetchall()

        print(datas)
        return HttpResponse(datas)

        if datas is None:
            print('This user is not booked our hotel')
            return HttpResponse(0)

        elif len(datas) == 0:
            print('This user is not booked our hotel')
            return HttpResponse(0)

    finally:
        con.close()

    return HttpResponse(2)

@csrf_exempt
def insert_booked_info(request):

    userID = request.POST.get('UserID','')
    a = 0
    now = timezone.localtime(timezone.now()).strftime('%Y-%m-%d-%H:%M:%S')
    tomorrow = timezone.localtime(timezone.now()+timezone.timedelta(days=a)).strftime('%Y-%m-%d-%H:%M:%S')

    result = make_check_in_out(now, tomorrow)

    return HttpResponse(result)

def make_check_in_out(start,end):
    start = ''.join(str(e) for e in start)
    checkin = start[:11]+"14:00:00"
    end = ''.join(str(e) for e in end)
    checkout = end[:11]+"11:00:00"

    return checkin+"/"+checkout

def print_time_now(request):
    return HttpResponse(timezone.now())
   






