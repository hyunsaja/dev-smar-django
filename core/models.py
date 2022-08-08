from django.db import models

# Create your models here.

from django.contrib.auth.models import Group, User


class Code(models.Model):
    gNumber = models.IntegerField()
    gSubNumber = models.IntegerField()
    gDeep = models.IntegerField()
    aNumber = models.AutoField(primary_key=True)

    aint = models.IntegerField(null=True)
    avarchar = models.CharField(null=True, max_length=255)
    atext = models.TextField(null=True)

    auser = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)


    def __str__(self):
        return self.avarchar

    class Meta:
        # managed = False
        db_table = "tb_code"
        verbose_name_plural = "1. Code"
        ordering = ["-gNumber", "gSubNumber", "aNumber"]



class Company(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=32)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)

    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)


    def __str__(self):
        return self.name

    class Meta:
        # managed = False
        db_table = "tb_company"
        verbose_name_plural = "2. Company"
        ordering = ["name", ]



class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    phone = models.CharField(max_length=32)
    department = models.IntegerField(choices=Code.objects.values_list('aint', 'avarchar').filter(gNumber=4).filter(aint__gt=-1))
    phone = models.CharField(max_length=100)

    class Meta:
        # managed = False
        db_table = "tb_UserDetail"
        verbose_name_plural = "3. UserDetail"
