from django.db import models

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
