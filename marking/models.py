from django.db import models
from django.contrib.auth.models import User
from datetime import date
class Mark(models.Model):
    score = models.SmallIntegerField(verbose_name="分数",default=0)
    score_num = models.SmallIntegerField(default=0)
    ave_score = models.CharField(max_length=64, verbose_name="平均分", default=0)
    # month = models.DateField(u'评分月份', default=date.today)
    month = models.CharField(u'评分月份',max_length=32, blank=True, null=True)

    name = models.ForeignKey('UserProfile',blank=True, null=True, verbose_name="姓名", on_delete=models.SET_NULL)
    class Meto:
        unique_together = 'name'
    def __str__(self):
        return '<%s-%s-%s>' % (self.name.email,self.month, self.score)
##
class IsMark(models.Model):
    is_grade = models.BooleanField(default=False)
    name = models.ManyToManyField('UserProfile', blank=True)
    mark = models.ManyToManyField('Mark', blank=True)
    def __str__(self):
        return self.id

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    job_title = models.CharField(max_length=64)
    # month_id = models.ForeignKey('Months',blank=True, null=True, on_delete=models.SET_NULL)
    #is_grade = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'       #定义用户名的字段
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
