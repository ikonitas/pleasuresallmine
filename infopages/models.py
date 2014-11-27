from django.db import models
from django.core.urlresolvers import reverse

class InfoPage(models.Model):
    page_title_help = 'The title to be shown at the top of your browser window.'
    meta_description_help = 'This should be a comma seperated list of keywords/keyphrases that are relevant to this page.'
    meta_keywords_help = 'This should be a brief description of the content of this page.'
    show_menu_help = 'It will shop in top navigation menu this infopage'

    title = models.CharField(max_length=200)
    url = models.CharField(max_length=100)
    content = models.TextField()
    show_menu = models.BooleanField(default=False, help_text=show_menu_help)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(null=True, blank=True)
    page_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=page_title_help
    )
    meta_description = models.CharField(
        'Description',
        max_length=250,
        blank=True,
        null=True,
        help_text=meta_description_help
    )
    meta_keywords = models.CharField(
        'Keywords',
        max_length=300,
        blank=True,
        null=True,
        help_text=meta_keywords_help
    )
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'information page'
        verbose_name_plural = 'information pages'
        ordering = ('url',)

    def get_absolute_url(self):
        return reverse('infopages.views.view_page', args=[self.url])

    def __unicode__(self):
        return u"%s - %s" % (self.url, self.title)
