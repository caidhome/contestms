from django.db import models

# Create your models here.

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



"""
class Student(models.Model):
    stu_no = models.IntegerField(primary_key=True, verbose_name='学号')
    stu_name = models.CharField(max_length=50, verbose_name='姓名')
    stu_tel = models.CharField(max_length=20, verbose_name='电话')
    stu_email = models.CharField(max_length=50, verbose_name='邮箱')
    stu_depart = models.CharField(max_length=50, verbose_name='院系')
    stu_major = models.CharField(max_length=50, verbose_name='专业')
    stu_level = models.CharField(max_length=50, verbose_name='等级')
    class Meta:
        db_table = 'student'
        verbose_name = '学生信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.stu_name """