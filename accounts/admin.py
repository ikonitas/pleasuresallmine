from django.contrib import admin
from django.conf.urls import patterns

from .models import UserProfile
from .views import edit_customer

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date_of_birth', 'phone', 'user', 'terms',
                    'user_email', 'modified_at', 'created_at',)
    readonly_fields = ('user',)

    def get_urls(self):
        urls = super(UserProfileAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'(\d+)/$', edit_customer)
                           )
        return my_urls + urls


admin.site.register(UserProfile, UserProfileAdmin)
