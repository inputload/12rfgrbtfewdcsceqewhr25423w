from django.db import models
import random
import string


class Url(models.Model):
    short_code = models.CharField(max_length=15, default='')
    long_url = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        self.short_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return super().save(*args, **kwargs)
