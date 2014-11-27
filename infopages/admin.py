from tinymce.widgets import TinyMCE

from django.core.urlresolvers import reverse
from django.contrib import admin

from infopages.models import InfoPage

class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'url', 'sort_order', 'show_menu',
                    'is_active', 'date_modified',)
    prepopulated_fields = {'url': ('title',),}
    fieldsets = (
            (
                'Infopage', {
                    'fields': (
                        'title', 'url', 'content', 'show_menu', 'sort_order',
                        'is_active',
                    )
                }
            ),
            (
                'SEO fields', {
                    'classes': ('collapse',),
                    'fields': ('page_title', 'meta_description', 'meta_keywords',)
                }
            )
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('content',):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 120, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(InfoPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(InfoPage, InfoPageAdmin)
