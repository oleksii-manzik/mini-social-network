from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, null=False)
    last_name = models.CharField(_('last name'), max_length=150, null=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')
    date_of_birth = models.DateField(_('date of birth'), null=False)
    country = models.CharField(_('country'), max_length=255, null=False)
    city = models.CharField(_('city'), max_length=255, null=False)


class Post(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='posts')
    text = models.TextField(_('text'), max_length=5000)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='likes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='likes')
    created = models.DateTimeField(_('like date'), auto_now_add=True)
    is_liked = models.BooleanField(_('is liked'))
