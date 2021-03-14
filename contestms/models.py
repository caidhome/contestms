from django.db import models
from certms.models import Cert
from userms.models import Admin, Student
# Create your models here.
class Contest(models.Model):
    con_id = models.AutoField(primary_key=True)
    con_name = models.CharField(max_length=255)
    con_time = models.DateTimeField()
    con_signtime = models.DateTimeField()
    con_endtime = models.DateTimeField()
    con_place = models.CharField(max_length=255)
    con_rule = models.TextField(max_length=255)
    con_environ = models.CharField(max_length=255, blank=True, null=True)
    con_lang = models.CharField(max_length=255, blank=True, null=True)
    con_level = models.IntegerField()
    con_signlink = models.CharField(max_length=255, blank=True, null=True)
    con_certid = models.ForeignKey(Cert, models.DO_NOTHING, db_column='con_certid')
    con_createrid = models.ForeignKey(Admin, models.DO_NOTHING, db_column='con_createrid')

    class Meta:
        managed = True
        db_table = 'tt_contest'

class Group(models.Model):
    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=20)
    group_conid = models.ForeignKey(Contest, models.DO_NOTHING, db_column='group_conid')

    class Meta:
        managed = True
        db_table = 'tt_group'


class Sign(models.Model):
    sign_id = models.IntegerField(primary_key=True)
    sign_lang = models.CharField(max_length=255, blank=True, null=True)
    sign_state = models.IntegerField()
    sign_certpath = models.CharField(max_length=255, blank=True, null=True)
    sign_total = models.IntegerField(blank=True, null=True)
    sign_detial = models.CharField(max_length=255, blank=True, null=True)
    sign_level = models.CharField(max_length=255, blank=True, null=True)
    sign_teach = models.CharField(max_length=50, blank=True, null=True)
    sign_conid = models.ForeignKey(Contest, models.DO_NOTHING, db_column='sign_conid')
    sign_stuid = models.ForeignKey(Student, models.DO_NOTHING, db_column='sign_stuid')
    sign_groupid = models.ForeignKey(Group, models.DO_NOTHING, db_column='sign_groupid', blank=True)

    class Meta:
        managed = True
        db_table = 'tt_sign'