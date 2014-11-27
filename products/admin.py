from sorl.thumbnail import default
from django.contrib import admin

from products.models import Size, Color, Product, ProductImage
from products.forms import ProductForm

ADMIN_THUMBS_SIZE = "60x60"
ADMIN_THUMBS_SIZE_INLINE = "120x120"


class SizeAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Size, SizeAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Color, ColorAdmin)


class ProductImageInline(admin.TabularInline):
    readonly_fields = ('admin_thumbnail', )
    model = ProductImage
    extra = 5
    max_num = 5

    def admin_thumbnail(self, obj):
        try:
            if obj.image:
                thumb = default.backend.get_thumbnail(
                        obj.image.file,
                        ADMIN_THUMBS_SIZE_INLINE
                )
                return "<a class='fancybox' href='{0}' /> \
                        <img width='{1}'src='{2}' /></a>".format(
                                obj.image.url,
                                thumb.width,
                                thumb.url
                        )
        except IOError:
            return "No Image"

    admin_thumbnail.allow_tags = True
    admin_thumbnail.short_description = "Thumb"


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline,]
    list_display = ('name', 'description', 'admin_thumb', 'category',
                    'is_in_stock', 'special_offer', 'price', 'margin',
                    'total_price', 'product_number', 'slug', 'page_title',
                    'meta_description', 'meta_keywords', 'is_active',
                    'created_at', 'modified_at' )

    list_per_page = 50
    list_filter = ('category',)
    search_fields = ('name', 'description', 'product_number',)
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
            (
                'Product', {
                    'fields' : (
                        'name', 'description', 'category', 'size', 'color',
                        'is_in_stock', 'special_offer', 'price', 'margin',
                        'total_price', 'product_number', 'is_active', 'slug',
                        )
                    }
            ),
            (
                'SEO fields', {
                    'description' : 'These fields are for the purpose of ' \
                            'search engine optimisation.',
                    'classes': ('collapse',),
                    'fields':(
                        'page_title', 'meta_keywords', 'meta_description',
                        )
                    }
                ),
            )

    class Media:
        css = {
                'all': ('css/products_admin/jquery.fancybox.css',)
              }
        js = ('js/lib/jquery-1.8.0.min.js',
              'js/products/jquery.fancybox.js',
              'js/products/zoom_image.js',
              'js/products/total_price.js')

    def admin_thumb(self, obj):
        try:
            if obj.get_image():
                thumb = default.backend.get_thumbnail(
                        obj.get_image().file,
                        ADMIN_THUMBS_SIZE_INLINE
                )
                return "<a class='fancybox' href='{0}' /> \
                        <img width='{1}'src='{2}' /></a>".format(
                                obj.get_image().url,
                                thumb.width,
                                thumb.url
                        )
        except IOError:
            return "No Image"

    admin_thumb.allow_tags = True

    def total_price(self, obj):
        total_price = (obj.price * obj.margin) / 100
        total_price = obj.price + total_price
        return "%.2f" % total_price

admin.site.register(Product, ProductAdmin)
