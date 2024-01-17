from django.contrib.auth.models import User
from django.db import models


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    home = models.URLField(blank=True)
    text = models.TextField()
    reply = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, related_name="replies")
