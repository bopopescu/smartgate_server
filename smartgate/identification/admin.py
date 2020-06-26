from django.contrib import admin
from .models import TestUserInfo, Userinfo, Booklist, Roominfo

# Register your models here.

class TestUserInfoAdmin(admin.ModelAdmin):
        list_display = ['test_num' ,'test_id', 'test_name'] 
        list_filter = ('test_id', 'test_name',)
        ordering = ['test_num']
        search_fields = ['test_id', 'test_name']
        #test_num.short_description = "인원수"

        actions = ['test_method']

        def test_method(self, request, queryset):
                update_count = queryset.update(test_name="hi")
                self.message_user(request, '{}건의 사용자의 이름을 hi로 변경'.format(update_count))
        test_method.short_description = '선택한 사용자의 정보 변경'

class UserInfoAdmin(admin.ModelAdmin):
        list_display = ['uid', 'upw', 'uname', 'utel', 'umail']
        search_fields = ['uname']

class RoomInfoAdmin(admin.ModelAdmin):
        list_display = ['rnum','rmac','rpw','rcheck','rgrade']
        list_filter = ('rcheck','rgrade',)
        search_fields = ['rnum']

        actions = ['room_checkout', 'room_checkin']

        def room_checkout(self, request, queryset):
                update_count = queryset.update(rcheck=0)
                self.message_user(request, '{}건의 방을 체크아웃 상태로 변경'.format(update_count))
        room_checkout.short_description = '선택한 방을 체크아웃'

        def room_checkin(self, request, queryset):
                update_count = queryset.update(rcheck=1)
                self.message_user(request, '{}건의 방을 체크인 상태로 변경'.format(update_count))
        room_checkin.short_description = '선택한 방을 체크인'

class BookInfoAdmin(admin.ModelAdmin):
        list_display = ['bid','bnum','bdate','btel', 'bcin', 'bcout', 'bstel', 'bttel', 'bftel']
        search_fields = ['bnum', 'btel']
        list_filter = ('bnum','bcin',)

admin.site.site_header = '호텔 관리'
admin.site.register(TestUserInfo, TestUserInfoAdmin)
admin.site.register(Userinfo, UserInfoAdmin)
admin.site.register(Roominfo, RoomInfoAdmin)
admin.site.register(Booklist, BookInfoAdmin)
