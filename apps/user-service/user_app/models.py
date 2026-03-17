from django.db import models

class User(models.Model):
    auth_id = models.IntegerField()
    username = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username