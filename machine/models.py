from django.db import models


# Create your models here.

class MachineGroup(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128, null=True)

    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        # managed = False
        db_table = "tb_machine_group"
        verbose_name_plural = "1. MACHINE GROUP"
        ordering = ["name", ]

from core.models import Company

class Machine(models.Model):
    id = models.AutoField(primary_key=True)

    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    machine_group_id = models.ForeignKey(MachineGroup, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128, null=True)

    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        # managed = False
        db_table = "tb_machine"
        verbose_name_plural = "2. MACHINE"
        ordering = ["name", ]


class MachineInit(models.Model):
    id = models.AutoField(primary_key=True)

    machine_id = models.OneToOneField(Machine, on_delete=models.CASCADE)
    # name = models.CharField(max_length=32)

    set_value_1 = models.CharField(max_length=32)
    set_value_2 = models.CharField(max_length=32)
    set_value_3 = models.CharField(max_length=32)
    set_value_4 = models.CharField(max_length=32)

    description = models.CharField(max_length=128, null=True)

    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)

    def __str__(self):
        return self.description

    class Meta:
        # managed = False
        db_table = "tb_machine_init"
        verbose_name_plural = "3. MACHINE INIT INFO"
        ordering = ["machine_id", ]


from django.contrib.auth.models import Group, User
class MachineOperator(models.Model):
    id = models.AutoField(primary_key=True)

    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.CharField(max_length=128, null=True)

    astatus = models.IntegerField(null=True)
    adate = models.DateTimeField(null=True)

    def __str__(self):
        return self.description

    class Meta:
        # managed = False
        db_table = "tb_machine_operator"
        verbose_name_plural = "4. MACHINE OPERATOR"
        ordering = ["id", ]
