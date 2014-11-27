from django.db import models


class Category(models.Model):
    page_title_help = '''This title to be shown at the top of your browser window.'''
    meta_description_help = '''This should be a comma separated list of keywords/keyphrases
                               that are relevant to this page'''
    meta_keywords_help = '''This should be a brief description of the content of this page.'''
    is_active_help = '''Should this category show in subcategories?'''

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text=is_active_help)
    sort_order = models.IntegerField(null=True, blank=True)
    page_title = models.CharField(max_length=200, null=True,
                                  blank=True, help_text=page_title_help)
    meta_description = models.CharField(max_length=250, null=True,
                                        blank=True, help_text=meta_description_help)
    meta_keywords = models.CharField(max_length=300, null=True, blank=True,
                                     help_text=meta_keywords_help)

    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('sort_order',)
        verbose_name_plural = 'categories'

    def __unicode__(self):
        if self.parent:
            return u'{0} ({1})'.format(self.name, self.parent)
        else:
            return self.name

    def get_children(self):
        children = Category.objects.filter(parent=self)
        return children

    def _get_random_image(self):
        try:
            return self.product_set.order_by('?')[0].productimage_set.all()[0].image
        except:
            return None
    get_random_image = property(_get_random_image)

    def get_absolute_url(self):
        if self.parent:
            slug = "{0}/{1}".format(self.parent.slug, self.slug)
        else:
            slug = self.slug
        return slug

