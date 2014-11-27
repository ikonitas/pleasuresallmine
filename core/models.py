from django.db import models


class HomeScreen(models.Model):
    help_text_home = "This Image is showing on home page please use exactly" \
                     "the same width 900px height 371px"

    image = models.ImageField(null=True,
                              blank=True,
                              upload_to="uploads/%Y/%m/%d",
                              help_text=help_text_home)
    is_active = models.NullBooleanField(blank=True, default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.image.url
