from django.contrib import admin
from categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'slug', 'parent', 'is_active',
            'sort_order' )
    list_filter = ('parent', 'is_active', )
    list_editable = ('sort_order',)
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
            (
                'Category', {
                    'fields' : (
                        'name', 'parent', 'is_active',
                        )
                    }
            ),
            (
                'SEO fields', {
                    'description': 'These fields are for the purpose of search engine oiptimisation.',
                    'classes' : ('collapse',),
                    'fields' : ('slug', 'page_title', 'meta_description', 'meta_keywords',)
                    }
            ),
    )

admin.site.register(Category, CategoryAdmin)
