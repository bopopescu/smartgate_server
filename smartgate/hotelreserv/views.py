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
from django.utils import timezone, dateformat
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
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
    book_start = request.POST.get('BStart','')
    a = 0
    now = dateformat.format(timezone.now(), 'Y-m-d-H:i:s')
    # now = timezone.localtime(timezone.now()).strftime('%Y-%m-%d-%H:%M:%S')
    # tomorrow = timezone.localtime(timezone.now()+timezone.timedelta(days=a)).strftime('%Y-%m-%d-%H:%M:%S')

    # result = make_check_in_out(now, tomorrow)

    return HttpResponse(now)

def make_check_in_out(start,end):
    start = ''.join(str(e) for e in start)
    checkin = start[:11]+"-14:00:00"
    end = ''.join(str(e) for e in end)
    checkout = end[:11]+"-11:00:00"

    return checkin+"/"+checkout

def print_time_now(request):
    return HttpResponse(timezone.now())
    
@csrf_exempt   
def test_date_send(request):

    test_start = request.POST.get('start','')
    test_end = request.POST.get('end','')

    print(test_start)
    print(type(test_start))

    print(test_end)
    print(type(test_end))

    start_end = make_check_in_out(test_start, test_end)
    print(start_end)
    date_list = start_end.split("/")
    print(date_list[0])
    print(date_list[1])
    
    try:

        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'insert into BookList values ("hoi", "SMR001", now(),"010-1234-4321", %s, %s)'
        curs.execute(sql, (date_list[0], date_list[1]))
        con.commit()

    except con.Error as error:
        con.rollback()
        print('error inserting user book list')
        print(error)

    finally:
        con.close()

    return HttpResponse(1)

@csrf_exempt
def remain_room_selected_date(request):

    start = request.POST.get('start','')
    end = request.POST.get('end','')

    print(start)
    
    try:

        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor(pymysql.cursors.DictCursor)

        sql = 'select RNum, RGrade from RoomInfo where RNum not in (select BNum from BookList where (BCin <= %s and %s <=BCout) or (%s<=BCin and %s>=BCout) )'

        curs.execute(sql, (start, start, start, end))

        datas = curs.fetchall()

    finally:
        con.close()

    if datas is None:
        print('there is no data mathcing conditions')
        return HttpResponse(0)

    elif len(datas) ==0:
        print('there is no data matching conditions')
        return HttpResponse(0)

    else:
        print(len(datas))
        print(datas)
        for i in range(len(datas)):
            if datas[i]['RGrade'] ==1:
                print(" RNum : {:s} | RGrade : {:d}".format(datas[i]['RNum'], datas[i]['RGrade']))

            if datas[i]['RGrade'] ==2:
                print(" RNum : {:s} | RGrade : {:d}".format(datas[i]['RNum'], datas[i]['RGrade']))
        
        return HttpResponse(json.dumps(datas))

def udp_module_code(request):

    from . import test as t

    data = 1

    t.udp_connection(data)

    return HttpResponse("1")

@csrf_exempt
def insert_booklist_reservation(request):

    userID = request.POST.get('UserID','')
    roomnum = request.POST.get('roomnum','')
    startDate = request.POST.get('StartDate','')
    endDate = request.POST.get('EndDate','')
    numOfPhone = request.POST.get('numofphone','')
    bookphone = request.POST.get('bookphone','')

    check_in_out = make_check_in_out(startDate, endDate)

    date_list = check_in_out.split('/')
    print(bookphone+' | '+numOfPhone)
    phone_list = bookphone.split('/')
    startDate = date_list[0]
    endDate = date_list[1]
    print(roomnum)
    if roomnum == "":
        print("your access is not available")
        return HttpResponse("2")
    print(startDate)
    print(endDate)
    
    try:

        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'select BNum from BookList where BNum = %s and ( (date(%s) <date(BCout) and BCout <=%s) or (BCin >=%s and date(BCin)<= %s) )'
        curs.execute(sql, (roomnum, startDate, endDate, startDate, endDate))
        datas = curs.fetchall()
        print(datas)
        if len(datas) ==0:
            print('ok go ahead')

            if numOfPhone == '1': 
                sql = 'insert into BookList(BID, BNum, BDate, BTel, BCin, BCout) values(%s, %s, now(), %s, %s, %s)'
                curs.execute(sql, (userID, roomnum, phone_list[0], startDate, endDate) )
            elif numOfPhone == '2':
                sql = 'insert into BookList(BID, BNum, BDate, BTel, BCin, BCout,BSTel) values(%s, %s, now(), %s, %s, %s, %s)'
                curs.execute(sql, (userID, roomnum, phone_list[0], startDate, endDate, phone_list[1]) )
            elif numOfPhone == '3':
                sql = 'insert into BookList(BID, BNum, BDate, BTel, BCin, BCout,BSTel,BTTel) values(%s, %s, now(), %s, %s, %s, %s, %s)'
                curs.execute(sql, (userID, roomnum, phone_list[0], startDate, endDate, phone_list[1], phone_list[2]) )
            elif numOfPhone == '4':
                sql = 'insert into BookList(BID, BNum, BDate, BTel, BCin, BCout,BSTel, BTTel, BFTel) values(%s, %s, now(), %s, %s, %s, %s, %s, %s)'
                curs.execute(sql, (userID, roomnum, phone_list[0], startDate, endDate, phone_list[1], phone_list[2], phone_list[3]) )
            else:
                print('phone number does not exist')
                return HttpResponse("3")

            con.commit()
            print('your book is success !')

        else:
            print("the room that you selected already booked")
            return HttpResponse(1)

    except con.Error as error:
        con.rollback()
        print('database error while during input data or executing query')
        print(error)
        return HttpResponse("4")

    finally:
        con.close()

    return HttpResponse("0")

@csrf_exempt
def get_user_booklists(request):
    userID = request.POST.get('UserID','')
    # now = timezone.localtime(timezone.now()).strftime('%Y-%m-%d-%H:%M:%S')
    now = dateformat.format(timezone.now(), 'Y-m-d-H:i:s')


    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor(pymysql.cursors.DictCursor)
        sql = 'select * from BookList where date(BCin) >= date(%s) and BID = %s'
        curs.execute(sql, (now, userID))
        bookdata = curs.fetchall()
        print(bookdata)

        if len(bookdata) == 0:
            print('there is no data in booklist')
            return HttpResponse('0')

        else:    
            room_num_list = []
            room_num_dict = {}
            temp = ()
            for i in bookdata:
                print(i['BNum'])
                room_num_dict[i['BNum']] = i['BNum']
                print('split')

            print(room_num_dict)
            room_num_list = list(room_num_dict.values())
            temp = tuple(list(room_num_dict.values()))
            print(room_num_list)
            print(temp)
            print(temp[0])
            print(len(room_num_list))

            sql = 'select RNum, RGrade from RoomInfo where RNum in %s'
            curs.execute(sql, [temp])
            grade_list = curs.fetchall()
            print(grade_list)
            print(grade_list[0])

            for i in range(len(bookdata)):
                for j in range(len(grade_list)):
                    if bookdata[i]['BNum'] == grade_list[j]['RNum']:
                        bookdata[i].update({'BGrade': grade_list[j]['RGrade']})
            print(bookdata)

        #print(bookdata)
        #print(type(bookdata))
        #print(bookdata[len(bookdata)-1].update({'hello':'world'}))
        #print(bookdata[len(bookdata)-1]['hello'])

        if bookdata is None:
            print('there is no matching data that users booked hotel')


    except con.Error as error:
        con.rollback()
        print('there is no matching data that users booked hotel')
        print(error)


    finally:
        con.close()
    
    if len(bookdata) != 0:
        
        print(json.dumps(bookdata, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
        return HttpResponse(json.dumps(bookdata, sort_keys=True, indent=1, cls=DjangoJSONEncoder))

    else:
        return HttpResponse("0")

@csrf_exempt
def cancel_reservations(request):

    userID = request.POST.get('UserID','')
    bookedNum = request.POST.get('BookedNum','')
    bookedDate = request.POST.get('BookedDate','')
    errornum = 0
    bookeddate = bookedDate.split('T')
    print(bookeddate)
    strfdate = bookeddate[0]+'-'+bookeddate[1]
    print(strfdate)
    try:
        con = pymysql.connect(host=db.INFO['host'], user= db.INFO['user'], password= db.INFO['password'], db=db.INFO['db'], charset='utf8')
        curs = con.cursor()
        sql = 'select * from BookList where BID = %s and BNum = %s and BDate = %s'
        curs.execute(sql, (userID, bookedNum, strfdate))
        datas = curs.fetchall()
        print(datas)
        print(len(datas))

        if len(datas) == 0:
            print('there is no matching booked data that you selected booked room')
        else:
            sql = 'delete from BookList where BID = %s and BNum = %s and BDate = %s'
            curs.execute(sql, (userID, bookedNum, strfdate))

        if curs.rowcount == 1:
            errornum =1
            con.commit()

    except con.Error as error:
        con.rollback()
        print(error)

    finally:
        con.close()
        
    if errornum == 1:
        return HttpResponse('0')

    else:
        return HttpResponse("1")
