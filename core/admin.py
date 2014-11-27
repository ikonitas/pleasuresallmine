from sorl.thumbnail import default
from django.contrib import admin

from core.models import HomeScreen


ADMIN_THUMBS_SIZE = "600x300"

class HomeScreenAdmin(admin.ModelAdmin):
    list_display = ('image', 'admin_thumbnail', 'is_active', 'modified_at',
                    'created_at',)

    def admin_thumbnail(self, obj):
        if obj.image:
            thumb = default.backend.get_thumbnail(obj.image.file, ADMIN_THUMBS_SIZE)
            return "<a class='fancybox' href='{0}' /><img width='{1}'src='{2}' /></a>".format(obj.image.url, thumb.width, thumb.url)
        else:
            return "No Image"
    admin_thumbnail.allow_tags = True
    admin_thumbnail.short_description = "Thumb"




    class Media:
        css = {
                'all': ('css/products_admin/jquery.fancybox.css',)
              }
        js = ('js/lib/jquery-1.8.0.min.js',
              'js/products/jquery.fancybox.js',
              'js/products/zoom_image.js',)

admin.site.register(HomeScreen, HomeScreenAdmin)
