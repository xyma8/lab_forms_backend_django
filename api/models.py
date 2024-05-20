from django.db import models
import uuid
from django.contrib.auth.hashers import make_password


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, null=False)
    surname = models.CharField(max_length=15, null=False)
    email = models.CharField(max_length=254, null=False)
    login = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=255, null=False)
    gender = models.IntegerField(null=False)
    darktheme = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=False)


    def generate_token(self):
        return str(uuid.uuid4())


    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

