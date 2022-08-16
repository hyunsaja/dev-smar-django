from django.db import models
from machine.models import Machine

# Create your models here.
class CamMaster(models.Model):
    id = models.AutoField(primary_key=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE)  # 장비ID
    origin_image = models.ImageField(upload_to='plate_chamfer_origin/%y/%m/%d')
    result_image = models.ImageField(upload_to='plate_chamfer_result/%y/%m/%d', blank=True, null=True)
    ncfile = models.FileField(upload_to='plate_chamfer_ncfile/%Y/%m/%d/', blank=True, null=True)
    sim_point = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.machine_id} :: {self.origin_image} :: {self.result_image} :: {self.ncfile}'


    class Meta:
        # managed = False
        db_table = "tb_cam_master"
        verbose_name_plural = "1. Cam Master"
        ordering = ["machine_id", ]