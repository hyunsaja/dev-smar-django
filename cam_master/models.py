from django.db import models
from machine.models import Machine

# Create your models here.
class PlateChamferMachine(models.Model):
    id = models.AutoField(primary_key=True)
    cam_name = models.CharField(max_length=20)
    origin_image = models.ImageField(upload_to='plate_chamfer_origin/%y/%m/%d')
    result_image = models.ImageField(upload_to='plate_chamfer_result/%y/%m/%d', blank=True, null=True)
    ncfile = models.FileField(upload_to='plate_chamfer_ncfile/%Y/%m/%d/', blank=True, null=True)
    sim_point = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] :: {self.result_image} :: {self.ncfile}'

    class Meta:
        # managed = False
        db_table = "tb_plate_chamfer_cam"
        verbose_name_plural = "1. Plate Chamfer Machine"
        ordering = ["id", ]


class RpcmS300Machine(models.Model):
    id = models.AutoField(primary_key=True)
    cam_name = models.CharField(max_length=20)
    origin_image = models.ImageField(upload_to='rpcm_s300_origin/%y/%m/%d')
    result_image = models.ImageField(upload_to='rpcm_s300_result/%y/%m/%d', blank=True, null=True)
    ncfile = models.FileField(upload_to='rpcm_s300_ncfile/%Y/%m/%d/', blank=True, null=True)
    sim_point = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] :: {self.result_image} :: {self.ncfile}'

    class Meta:
        # managed = False
        db_table = "tb_rpcm_s300_cam"
        verbose_name_plural = "2. Rpcm S300 Machine"
        ordering = ["id", ]


class RpcmAgcutMachine(models.Model):
    id = models.AutoField(primary_key=True)
    cam_name = models.CharField(max_length=20)
    origin_image = models.ImageField(upload_to='rpcm_agcut_origin/%y/%m/%d')
    result_image = models.ImageField(upload_to='rpcm_agcut_result/%y/%m/%d', blank=True, null=True)
    ncfile = models.FileField(upload_to='rpcm_agcut_ncfile/%Y/%m/%d/', blank=True, null=True)
    sim_point = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] :: {self.result_image} :: {self.ncfile}'

    class Meta:
        # managed = False
        db_table = "tb_rpcm_agcut_cam"
        verbose_name_plural = "3. Rpcm Agcut Machine"
        ordering = ["id", ]


class CoamingMachine(models.Model):
    id = models.AutoField(primary_key=True)
    origin_image = models.ImageField(upload_to='coamming_origin/%y/%m/%d')
    result_image = models.ImageField(upload_to='coamming_result/%y/%m/%d', blank=True, null=True)
    ncfile = models.FileField(upload_to='coamming_ncfile/%Y/%m/%d/', blank=True, null=True)
    sim_point = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] :: {self.result_image} :: {self.ncfile}'

    class Meta:
        # managed = False
        db_table = "tb_coamming_cam"
        verbose_name_plural = "4. Coamming Machine"
        ordering = ["id", ]


class MijuRobotWeldingMachine(models.Model):
    id = models.AutoField(primary_key=True)
    origin_image = models.ImageField(upload_to='miju_robot_welding_origin/%y/%m/%d')
    result_image = models.ImageField(upload_to='miju_robot_welding_result/%y/%m/%d', blank=True, null=True)
    ncfile = models.FileField(upload_to='miju_robot_welding_ncfile/%Y/%m/%d/', blank=True, null=True)
    sim_point = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] :: {self.result_image} :: {self.ncfile}'

    class Meta:
        # managed = False
        db_table = "tb_miju_robot_welding_cam"
        verbose_name_plural = "5. Miju Robot Welding Machine"
        ordering = ["id", ]