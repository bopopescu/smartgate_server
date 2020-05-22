from django.contrib import admin
from .models import TestUserInfo

# Register your models here.

class TestUserInfoAdmin(admin.ModelAdmin):
        list_display = ['test_num' ,'test_id', 'test_name'] 
        list_filter = ('test_id', 'test_name',)
        ordering = ['test_num']
        search_fields = ['test_id', 'test_name']
        #test_num.short_description = "인원수"

        actions = ['test_method']

        def test_method(self, request, queryset):
                queryset.update()
        test_method.short_description = '선택한 방의 예약 설정 변경'



admin.site.site_header = '호텔 관리'
admin.site.register(TestUserInfo, TestUserInfoAdmin)
