# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Booklist(models.Model):
    bid = models.OneToOneField('Userinfo', models.DO_NOTHING, db_column='BID', primary_key=True)  # Field name made lowercase.
    bnum = models.ForeignKey('Roominfo', models.DO_NOTHING, db_column='BNum')  # Field name made lowercase.
    bdate = models.DateTimeField(db_column='BDate')  # Field name made lowercase.
    btel = models.CharField(db_column='BTel', max_length=13)  # Field name made lowercase.
    bcin = models.DateTimeField(db_column='BCin', blank=True, null=True)  # Field name made lowercase.
    bcout = models.DateTimeField(db_column='BCout', blank=True, null=True)  # Field name made lowercase.
    bstel = models.CharField(db_column='BSTel', max_length=13, blank=True, null=True)  # Field name made lowercase.
    bttel = models.CharField(db_column='BTTel', max_length=13, blank=True, null=True)  # Field name made lowercase.
    bftel = models.CharField(db_column='BFTel', max_length=13, blank=True, null=True)  # Field name made lowercase.

    bid.verbose_name = "예약자 아이디"
    bnum.verbose_name = "방번호"
    bdate.verbose_name = "예약한 날짜"
    btel.verbose_name = "예약자 번호"
    bcin.verbose_name = "체크인"
    bcout.verbose_name = "체크아웃"
    bstel.verbose_name = "동반예약자(2인)"
    bttel.verbose_name = "동반예약자(3인)"
    bftel.verbose_name = "동반예약자(4인)"

    class Meta:
        managed = False
        db_table = 'BookList'
        unique_together = (('bid', 'bnum', 'bdate'),)


class Roominfo(models.Model):
    rnum = models.CharField(db_column='RNum', primary_key=True, max_length=6)  # Field name made lowercase.
    rmac = models.CharField(db_column='RMac', unique=True, max_length=17)  # Field name made lowercase.
    rpw = models.IntegerField(db_column='RPW')  # Field name made lowercase.
    rcheck = models.IntegerField(db_column='RCheck')  # Field name made lowercase.
    rgrade = models.IntegerField(db_column='RGrade')  # Field name made lowercase.

    rnum.verbose_name = "방번호"
    rmac.verbose_name = "맥주소"
    rpw.verbose_name = "비밀번호"
    rcheck.verbose_name = "예약여부"
    rgrade.verbose_name = "등급"

    def __str__(self):
        return self.rnum

    class Meta:
        managed = False
        db_table = 'RoomInfo'


class Userinfo(models.Model):
    uid = models.CharField(db_column='UID', primary_key=True, max_length=20)  # Field name made lowercase.
    upw = models.CharField(db_column='UPW', max_length=30)  # Field name made lowercase.
    uname = models.CharField(db_column='UName', max_length=30)  # Field name made lowercase.
    utel = models.CharField(db_column='UTel', unique=True, max_length=13, blank=True, null=True)  # Field name made lowercase.
    umail = models.CharField(db_column='UMail', max_length=40)  # Field name made lowercase.

    uid.verbose_name = "아이디"
    upw.verbose_name = "비밀번호"
    uname.verbose_name = "이름"
    utel.verbose_name = "전화번호"
    umail.verbose_name = "이메일"

    def __str__(self):
        return self.uid

    class Meta:
        managed = False
        db_table = 'UserInfo'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TestUserInfo(models.Model):
    test_num = models.AutoField(primary_key=True)
    test_id = models.CharField(unique=True, max_length=32, blank=True, null=True)
    test_name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'test_user_info'
