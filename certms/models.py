from django.db import models

# Create your models here.
class Cert(models.Model):
    cert_id = models.AutoField(primary_key=True)
    cert_imgurl = models.CharField(max_length=255)
    cert_name = models.CharField(max_length=50)
    cert_userx = models.IntegerField()
    cert_usery = models.IntegerField()
    cert_levelx = models.IntegerField()
    cert_levely = models.IntegerField()
    cert_qrcodex = models.IntegerField()
    cert_qrcodey = models.IntegerField()
    cert_teachx = models.IntegerField()
    cert_teachy = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tt_cert'
# from django.db import models
#
# # Create your models here.
# class Certms(models.Model):
#
#     # 证书主键
#     cert_id = models.AutoField(primary_key=True)
#     # 证书文件路径
#     cert_imgurl = models.CharField(max_length=255)
#     # 证书姓名坐标x
#     cert_userx = models.IntegerField()
#     # 证书姓名坐标y
#     cert_usery = models.IntegerField()
#     # 证书等级坐标x
#     cert_levelx = models.IntegerField()
#     # 证书等级坐标y
#     cert_levely = models.IntegerField()
#     # 证书名称
#     cert_name = models.TextField()
#     # 二维码坐标x
#     cert_qrcodex = models.IntegerField()
#     # 二维码坐标y
#     cert_qrcodey = models.IntegerField()
#     from django.db import models
#
#
#     class Meta:
#         managed = True
#         db_table = 'tt_cert'