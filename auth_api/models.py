from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


@python_2_unicode_compatible
class Entry(models.Model):
    title = models.CharField(max_length=256)

    # there's been two other options to make this field set automatically:
    # - default=timezone.now()
    # or
    # - just use 'auto_now_add=True'
    # but the option I used allows to edit the entry without editing this field
    create_date = models.DateField()
    show = models.BooleanField(default=False)
    user = models.ForeignKey(User, models.CASCADE, related_name="entry_id")

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_date = timezone.now()
        return super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

