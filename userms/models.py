from django.db import models

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_account = models.CharField(max_length=255)
    admin_pwd = models.CharField(max_length=255)
    admin_name = models.CharField(max_length=50)
    admin_role = models.IntegerField()
    admin_logtime = models.DateTimeField()
    admin_avator = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'tt_admin'
class Student(models.Model):
    stu_id = models.AutoField(primary_key=True)
    stu_no = models.CharField(max_length=20)
    stu_name = models.CharField(max_length=50)
    stu_pwd = models.CharField(max_length=50)
    stu_tel = models.CharField(max_length=20)
    stu_email = models.CharField(max_length=50)
    stu_major = models.CharField(max_length=50)
    stu_depart = models.CharField(max_length=50)
    stu_avator = models.CharField(max_length=255, blank=True, null=True)
    stu_sex = models.CharField(max_length=2)
    stu_motto = models.CharField(max_length=30)
    stu_card = models.CharField(max_length=18)
    class Meta:
        managed = True
        db_table = 'tt_student'
