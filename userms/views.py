import datetime
import os
import re

import xlrd
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponseRedirect
from django_redis import get_redis_connection

from TiantiMS import settings
from certms.models import Cert
from userms import models
from userms.models import Admin, Student
from contestms.models import Contest, Sign
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from random import randint
import hashlib

# Create your views here.
class Admin_LoginView(View):

    def get(self, request):
        return render(request, 'admin/user/login.html')

    def post(self, request):
        admin_account = request.POST.get('admin_account')
        admin_pwd = request.POST.get('admin_pwd')
        next = request.POST.get('next')
        user=Admin.objects.filter(admin_account=admin_account,admin_pwd=admin_pwd)
        if user:
            admin = user[0]
            admin_dict = {'admin_id': admin.admin_id, 'admin_role': admin.admin_role, 'admin_account': admin.admin_account, 'admin_name': admin.admin_name,
                   'admin_avator': admin.admin_avator, 'admin_logtime': admin.admin_logtime.strftime('%Y-%m-%d %H:%M:%S')}
            request.session['is_login'] = admin.admin_role  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            request.session['login_user'] = admin_dict
            admin.admin_logtime = datetime.datetime.now()
            admin.save()
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/admin/index')
        return render(request, 'admin/user/login.html', {'err_msg': '账号或密码错误！'})

# Create your views here.
class Stu_LoginView(View):

    def get(self, request):
        next = request.GET.get('next')
        return render(request, 'student/login.html', {'next': next})

    def post(self, request):
        stu_no = request.POST.get('stu_no')
        stu_pwd = request.POST.get('stu_pwd')
        next = request.POST.get('next')
        user=Student.objects.filter(stu_no=stu_no,stu_pwd=stu_pwd)
        if user and len(user) > 0:
            stu = user[0]
            stu = {'stu_id': stu.stu_id, 'stu_name': stu.stu_name, 'stu_tel': stu.stu_tel, 'stu_email': stu.stu_email,
                   'stu_major': stu.stu_major, 'stu_depart': stu.stu_depart, 'stu_no': stu.stu_no,
                   'stu_avator': stu.stu_avator, 'stu_sex': stu.stu_sex, 'stu_card': stu.stu_card, 'stu_motto': stu.stu_motto}
            request.session['is_login'] = 3  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            request.session['login_user'] = stu
            # print(next)
            if next and next != 'None':
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/')
        return render(request, 'student/login.html', {'err_msg': '账号或密码错误！'})

class Stu_IndexView(View):

    def get(self, request):
        login_user = None
        is_login = request.session.get('is_login')
        # if not is_login or is_login != 3:
        #     return render(request, 'student/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/'})
        login_user_sess = request.session.get('login_user')
        if login_user_sess and is_login == 3:
            login_id = login_user_sess['stu_id']
            try:
                login_user = Student.objects.get(stu_id=login_id)
            except Exception as ex:
                print('查询异常')
                print(ex)
                # return render(request, 'student/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/'})
        pIndex = request.GET.get('cpage')
        res = Contest.objects.filter().order_by('con_time')
        paginator = Paginator(res, 8)
        try:
            # page对象
            list_page = paginator.page(pIndex)
        except PageNotAnInteger:
            list_page = paginator.page(1)
        except EmptyPage:
            list_page = paginator.page(paginator.num_pages)
        p = Paginator(res, 10)
        if not pIndex:
            pIndex = '1'
        pIndex = int(pIndex)

        totol_page = p.page_range
        rep_data = {
            'res': list_page,
            'tpage': len(totol_page),
            'cpage': pIndex,
            'login_user': login_user
        }
        return render(request, 'student/index.html', rep_data)
        # return render(request, 'student/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/'})

    def post(self, request):
        pass

class Admin_IndexView(View):

    def get(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1,2]:
            return render(request, 'admin/user/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/admin/index'})
        login_user_sess = request.session.get('login_user')
        print(is_login, login_user_sess)
        if login_user_sess:
            login_id = login_user_sess['admin_id']
            try:
                login_user = Admin.objects.get(admin_id=login_id)
                return render(request, 'admin/index.html', {'login_user': login_user})
            except Exception as ex:
                print('查询异常')
        return render(request, 'admin/user/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/admin/index'})


    def post(self, request):
        pass

class WelcomeView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': 'welcome'})
        stu_num = 0
        admin_num = 0
        contest_num = 0
        cert_num = 0
        try:
            stu_num = len(Student.objects.all())
            admin_num = len(Admin.objects.all())
            contest_num = len(Contest.objects.all())
            cert_num = len(Cert.objects.all())
        except Exception as ex:
            print(ex)
        data_dict = {
            'stu_num': stu_num,
            'admin_num': admin_num,
            'contest_num': contest_num,
            'cert_num': cert_num
        }
        return render(request, 'admin/welcome.html', data_dict)

    def post(self, request):
        pass

class LogoutView(View):

    def get(self, request):
        is_login = request.session.get('is_login')
        target = 'student/login.html'
        if is_login == 2 or is_login == 1:
            target = 'admin/user/login.html'
        request.session['is_login'] = 0  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
        request.session['login_user'] = None
        return render(request, target, {'err_msg': '注销成功！'})

    def post(self, request):
        pass


class ListView(View):

    @xframe_options_sameorigin
    def get(self, request, role):
        """
        :param request:
        :param type: 查询的角色类别：1为管理员，2为学生
        :return:
        """
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html', {'err_msg': '您当前权限不够，请重新登录！', 'next': '/user/list/%s/' % role})

        pIndex = request.GET.get('cpage')
        search_dict = dict()
        # 如果有这个值 就写入到字典中去
        target = 'admin/user/admin_list.html'
        if role == '1':
            res = Admin.objects.filter().order_by('admin_id')
        else:
            res = Student.objects.filter().order_by('stu_id')
            target = 'admin/user/stu_list.html'

        paginator = Paginator(res, 10)
        if not pIndex:
            pIndex = '1'
        pIndex = int(pIndex)
        try:
            # page对象
            list_page = paginator.page(pIndex)
        except PageNotAnInteger:
            list_page = paginator.page(1)
        except EmptyPage:
            list_page = paginator.page(paginator.num_pages)
        p = Paginator(res, 10)
        totol_page = p.page_range
        rep_data = {
            'res': list_page,
            'tpage': len(totol_page),
            'cpage': pIndex
            # 'filt': {
            #     'con_level': con_level,
            #     'con_id': con_id,
            #     'start': start,
            #     'end': end
            # }
        }
        return render(request, target, rep_data)

    def post(self, request):
        pass


class AddView(View):

    @xframe_options_sameorigin
    def get(self, request, role):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请重新登录！', 'next': '/user/add/%s/' % role})
        user_id = request.GET.get('user_id')
        user = None
        if role == '1':
            if user_id:
                try:
                    user = Admin.objects.get(admin_id=user_id)
                except Exception as ex:
                    print(ex)
            return render(request, 'admin/user/admin_add.html', {'user': user})
        else:
            if user_id:
                try:
                    user = Student.objects.get(stu_id=user_id)
                except Exception as ex:
                    print(ex)
            return render(request, 'admin/user/stu_add.html', {'user': user})

    @xframe_options_sameorigin
    def post(self, request, role):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请重新登录！', 'next': '/user/list/%s/' % role})
        if role == '1':
            admin_account = request.POST.get('admin_account')
            admin_name = request.POST.get('admin_name')
            admin_pwd = request.POST.get('admin_pwd')
            admin_role = request.POST.get('admin_role')
            admin_avator = request.POST.get('admin_avator')
            admin_id = request.POST.get("admin_id")
            admin = None
            if admin_id:
                try:
                    admin = Admin.objects.get(admin_id=admin_id)
                    msg = '更新成功'
                except Exception as ex:
                    print(ex)
                    msg = '更新失败，暂无此管理员信息'
            else:
                admin = Admin()
                admin.admin_logtime = datetime.datetime.now()
                msg = '添加成功'
            if admin_pwd:
                admin.admin_pwd = admin_pwd
            admin.admin_role = admin_role
            admin.admin_name = admin_name
            admin.admin_avator = admin_avator
            admin.admin_account = admin_account
            admin.save()
            res_data = {"code": 6, "msg": msg}
        else:
            stu_no = request.POST.get('stu_no')
            stu_name = request.POST.get('stu_name')
            stu_pwd = request.POST.get('stu_pwd')
            stu_depart = request.POST.get('stu_depart')
            stu_major = request.POST.get('stu_major')
            stu_tel = request.POST.get("stu_tel")
            stu_email = request.POST.get("stu_email")
            stu_avator = request.POST.get("stu_avator")
            stu_sex = request.POST.get("stu_sex")
            stu_motto = request.POST.get("stu_motto")
            stu_card = request.POST.get("stu_card")
            stu_id = request.POST.get("stu_id")
            stu = Student()
            if stu_id:
                try:
                    stu = Student.objects.get(stu_id=stu_id)
                    msg = '更新成功'
                except Exception as ex:
                    print(ex)
                    msg = '更新失败，暂无此管理员信息'
            else:
                msg = '添加成功'
            if stu_pwd:
                stu.stu_pwd = stu_pwd
            if stu_no:
                stu.stu_no = stu_no
            if stu_name:
                stu.stu_name = stu_name
            if stu_avator:
                stu.stu_avator = stu_avator
            if stu_depart:
                stu.stu_depart = stu_depart
            if stu_major:
                stu.stu_major = stu_major
            if stu_tel:
                stu.stu_tel = stu_tel
            if stu_email:
                stu.stu_email = stu_email
            if stu_sex:
                stu.stu_sex = stu_sex
            if stu_motto:
                stu.stu_motto = stu_motto
            if stu_card:
                stu.stu_card = stu_card
            stu.save()
            res_data = {"code": 6, "msg": msg}
        return JsonResponse(res_data)


@method_decorator(csrf_exempt, name='dispatch')
class UploadAvatorView(View):

    @xframe_options_sameorigin
    def get(self, request):

        return render(request, 'admin/user/admin_add.html')

    @csrf_exempt
    def post(self, request):
        """
        头像上传(管理员和学生)
        证书上传
        layui富文本编辑器 图片上传
        :param request:
        :return:
        """
        code = 2
        msg = '上传失败'
        url = ''
        pre = ''
        flag = False

        file = request.FILES.get('file')
        fpath = request.POST.get('fpath')
        # print(fpath)
        if not fpath:
            flag = True
            fpath = '/temp/%s'%os.path.splitext(file.name)[1][1:]
            pre = '/static'
        rand_name = 'temp_%s' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17])
        file_path = '%s/%s' % (settings.UPLOAD_ROOT, fpath)
        file_full_path = '%s/%s%s'%(file_path, rand_name, os.path.splitext(file.name)[1])
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        try:
            if file is None:
                code = 2
                msg = '请选择文件后再上传！'
            # 循环二进制写入
            with open(file_full_path, 'wb') as f:
                for i in file.readlines():
                    f.write(i)
            code = 6
            msg = '上传成功'
            url='/upload%s/%s%s'%(fpath, rand_name, os.path.splitext(file.name)[1])
            # url='/upload/%s'%(cur_str, rand_name, os.path.splitext(file.name)[1])
        except Exception as e:
            print(e)
            msg = '上传失败'
        if flag:
            code = 0
        res_data = {
            "code": code,
            "msg": msg,
            'url': url,
            "data": {
                "src": pre+url
                , "title": "%s%s"%(rand_name, os.path.splitext(file.name)[1])
            }
        }
        return JsonResponse(res_data)


class ResetpwdView(View):

    def get(self, request, role):
        pass

    def post(self, request, role):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        user_id = request.POST.get('user_id')
        try:
            if role == '1':
                user = Admin.objects.get(admin_id=user_id)
                user.admin_pwd = '123456'
            else:
                user = Student.objects.get(stu_id=user_id)
                user.stu_pwd = '123456'
            user.save()
            res_data = {"code": 6, "msg": "密码重置成功，重置后的密码为:123456"}
        except Exception as ex:
            print(ex)
            res_data = {"code": 2, "msg": "密码重置失败"}
        return JsonResponse(res_data)


class Admin_PersonView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请重新登录！', 'next': '/user/person'})
        login_id = request.session.get('login_user')['admin_id']
        try:
            login_user = Admin.objects.get(admin_id=login_id)
            return render(request, 'admin/user/admin_person.html', {'user': login_user})
        except Exception as ex:
            print(ex)
        return render(request, 'admin/user/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/user/person'})

    @xframe_options_sameorigin
    def post(self, request):
        pass


class Stu_Query_PersonView(View):

    def get(self, request):
        # is_login = request.session.get('is_login')
        # if not is_login or is_login not in [1, 2]:
        #     return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！', 'stu':''})
        user_id = request.GET.get('user_id')
        try:
            stu = Student.objects.get(stu_no=user_id)
            stu = {'stu_id': stu.stu_id, 'stu_name': stu.stu_name, 'stu_tel': stu.stu_tel, 'stu_email': stu.stu_email,
                   'stu_major': stu.stu_major, 'stu_depart': stu.stu_depart, 'stu_no': stu.stu_no,
                   'stu_avator': stu.stu_avator, 'stu_sex': stu.stu_sex, 'stu_card': stu.stu_card, 'stu_motto': stu.stu_motto}
            res_data = {"code": 6, "msg": "查询成功", 'stu': stu}
        except Exception as ex:
            print(ex)
            res_data = {"code": 2, "msg": "查询失败,暂无此学号信息", 'stu':''}
        return JsonResponse(res_data)

    def post(self, request):
        pass


class DelView(View):

    def get(self, request, role):
        pass

    def post(self, request, role):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        user_id = request.POST.get('user_id')
        file_path = '%s\\user\\avator' % settings.UPLOAD_ROOT
        try:
            if role == '1':
                user = Admin.objects.get(admin_id=user_id)
                file_full_path = '%s\\admin\\%s' % (file_path, user.admin_avator.split('/')[-1])
                if user.admin_avator and user.admin_avator.split('/')[-1] != 'default_avator.jpg' and os.path.exists(
                        file_full_path):
                    os.remove(file_full_path)
            else:
                user = Student.objects.get(stu_id=user_id)
                file_full_path = '%s\\student\\%s' % (file_path, user.stu_avator.split('/')[-1])
                if user.stu_avator and user.stu_avator.split('/')[-1] != 'default_avator.jpg' and os.path.exists(file_full_path):
                    os.remove(file_full_path)
            user.delete()
            res_data = {"code": 6, "msg": "删除成功"}
            return JsonResponse(res_data)
        except Exception as ex:
            print(ex)
        res_data = {"code": 2, "msg": "删除失败"}
        return JsonResponse(res_data)

# 学生个人主页
class Stu_PersonView(View):

    def get(self, request, sid):
        login_user = request.session.get('login_user')
        is_login = request.session.get('is_login')
        if not login_user or not is_login:
            return render(request, 'student/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/user/student/%s/'%sid})
        stu = Student.objects.get(stu_id=login_user['stu_id'])
        con_sign = Sign.objects.filter(sign_stuid=stu)
        cons = list()
        pIndex = request.session.get('pIndex')
        for cs in con_sign:
            try:
                con_item = Contest.objects.get(con_id=cs.sign_conid.con_id)
                pattern = re.compile(r'<[^>]+>', re.S)
                con_rule_re = pattern.sub('', con_item.con_rule)
                con_item.con_rule = con_rule_re
                cons.append(con_item)
            except Exception as ex:
                print(ex)

        paginator = Paginator(cons, 10)
        try:
            # page对象
            list_page = paginator.page(pIndex)
        except PageNotAnInteger:
            list_page = paginator.page(1)
        except EmptyPage:
            list_page = paginator.page(paginator.num_pages)
        if not pIndex:
            pIndex = '1'
        pIndex = int(pIndex)

        totol_page = paginator.page_range
        rep_data = {
            'cons': list_page,
            'tpage': len(totol_page),
            'cpage': pIndex,
        }
        return render(request, 'student/person_base.html', rep_data)

    def post(self, request):
        pass


class Stu_InfoView(View):

    def get(self, request):
        login_user = request.session.get('login_user')
        is_login = request.session.get('is_login')
        if not login_user or not is_login:
            return render(request, 'student/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/user/stu_info'})
        try:
            stu = Student.objects.get(stu_id=login_user['stu_id'])
        except Exception as ex:
            print(ex)
            return render(request, 'student/login.html', {'err_msg': '暂无查到此账户信息，请重新登录！', 'next': '/user/stu_info'})
        return render(request, 'student/person_account.html', {'stu': stu})

    def post(self, request):
        pass


# 404
def page_not_found(request, exception):  # 注意点 ①
    return render(request, '404.html')

# 500
def page_error(request):
    return render(request, '500.html')





class StuUpdateInfo(View):
    def post(self, request):
        # try:
            # 从前端获取验证码
        login_user = request.session.get('login_user')
        is_login = request.session.get('is_login')
        if not login_user or not is_login:
            return render(request, 'student/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/user/stu_info'})
        try:
            stu = Student.objects.get(stu_id=login_user['stu_id'])
        except Exception as ex:
            print(ex)
            return render(request, 'student/login.html', {'err_msg': '暂无查到此账户信息，请重新登录！', 'next': '/user/stu_info'})
        email = stu.stu_email  # 获取前端邮箱
        code = request.POST.get('verif') #获取前段的验证码
        # 验证邮箱的格式
        re_email = r'(\w+)@(\w+)\.(\w+)'
        if not re.match(re_email, email):
            return JsonResponse({'code': 2, 'msg': '邮箱格式不正确'})
        #判断是否输入了验证码
        if not code:
            return JsonResponse({'code':2,'msg':'请输入验证码'})
        #获取验证码，并判断是否失效了

        key = 'tts_verfiy_code_' + email
        redis_client = get_redis_connection('code')
        code_ = str(redis_client.get(key), 'utf-8')
        # code_ = cache.get('tts_'+email)
        if not code_:
            return JsonResponse({'code':2,'msg':'验证码已失效'})
        #判断输入的验证码，和获取到的验证码是否一致
        if code == code_:
            stu_pwd = request.POST.get('stu_pwd')  # 获取前端邮箱
            stu_tel = request.POST.get('stu_tel')  # 获取前段的验证码
            stu_email = request.POST.get('stu_email')  # 获取前段的验证码
            stu_avator = request.POST.get('stu_avator')  # 获取前段的验证码
            if stu_avator and stu_avator != stu.stu_avator:
                file_full_path = '%s\\user\\avator\\student\\%s' % (settings.UPLOAD_ROOT, stu.stu_avator.split('/')[-1])
                if stu.stu_avator.split('/')[-1] != 'default_avator.jpg' and os.path.exists(file_full_path):
                    os.remove(file_full_path)
                stu.stu_avator= stu_avator
            if stu_pwd:
                stu.stu_pwd = stu_pwd
            if stu_tel:
                stu.stu_tel = stu_tel
            if stu_email:
                stu.stu_email = stu_email
            stu.save()

            login_user['stu_tel'] = stu_tel
            login_user['stu_email'] = stu_email
            login_user['stu_avator'] = stu_avator

            request.session['login_user'] = login_user
            return JsonResponse({'code':6 ,'msg':'修改成功！'})
        return JsonResponse({'code':2,'msg':'验证码错误'})
        #返回错误信息
        # except Exception as ex:
        #     print(ex)
        #     return JsonResponse({'code': 2, 'msg': '网络有些问题，请等一下再试'})


# post请求
# 获取到验证码，并存入redis
# 发生邮箱
class Email_code_APIView(View):
    def post(self, request):
        # try:
            # 从前端获取验证码
            login_user = request.session.get('login_user')
            is_login = request.session.get('is_login')
            if not login_user or not is_login:
                return render(request, 'student/login.html', {'err_msg': '您当前还未登录，请先登录！', 'next': '/user/stu_info'})
            try:
                stu = Student.objects.get(stu_id=login_user['stu_id'])
            except Exception as ex:
                print(ex)
                return render(request, 'student/login.html', {'err_msg': '暂无查到此账户信息，请重新登录！', 'next': '/user/stu_info'})
            # email = request.POST.get('email')
            email = stu.stu_email

            key = 'tts_verfiy_code_' + email
            redis_client = get_redis_connection('code')
            code_ = redis_client.get(key)
            # if not code_:
            # 生成随机的验证码
            code = self.Email_Code()
            # 给邮箱发送验证码
            # 发邮件
            from_email = settings.EMAIL_FROM
            subject = '竞赛管理系统-修改个人信息'
            text_content = ''
            html_content = '<p style="font-size: 18px;">[兰州理工大学竞赛管理系统] 验证码:<br><br><div style="text-align: center; font-size: 24px;"><strong><a href="">%s</a></strong></div>' \
                           '<br><br>该验证码仅用于身份验证，请勿泄露给他人使用。</p>' % code
            send_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            send_msg.attach_alternative(html_content, "text/html")
            send_msg.send()

            redis_client = get_redis_connection('code')
            redis_client.setex(key, 60 * 5, code)
            # cache.set(key, code, 30)  # 5分钟的有效时间
            ret = {
                'code': 6,
                'msg': "邮件发送成功"
            }
            return JsonResponse(ret)
        # 返回错误信息
        # except Exception as ex:
        #     print(ex)
        #     return JsonResponse({'code': 0, 'msg': '网络有些问题，请等一下再试'})

    def get(self, request):
        pass

    # 生成随机的验证码
    def Email_Code(self):
        code_ = ''
        code_str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ1234567890'
        for k in range(5):
            code_ += code_str[randint(0, 35)]
        return code_


class RegisterView(View):

    def get(self, request):
        return render(request, 'student/register.html')

    def post(self, request):
        stu_no = request.POST.get('stu_no')
        stu_name = request.POST.get('stu_name')
        stu_pwd =  request.POST.get('stu_pwd')
        stu_tel =  request.POST.get('stu_tel')
        stu_email =  request.POST.get('stu_email')
        stu_major =  request.POST.get('stu_major')
        stu_depart =  request.POST.get('stu_depart')
        stu_sex =  request.POST.get('stu_sex')
        stu_card =  request.POST.get('stu_card')
        stu_motto =  request.POST.get('stu_motto')
        stu = Student(stu_no=stu_no, stu_name=stu_name, stu_pwd = stu_pwd, stu_tel = stu_tel, stu_email = stu_email,
                      stu_major=stu_major, stu_depart=stu_depart, stu_avator='/upload/user/avator/student/default_avator.jpg',
                      stu_sex=stu_sex, stu_card=stu_card, stu_motto=stu_motto)
        stu.save()
        return render(request, 'student/login.html', {'err_msg': '注册成功，请登录！'})


class UploadStuView(View):

    def get(self, request):
        pass

    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        file = request.FILES.get('file')
        errorlist = list()
        file_path = settings.UPLOAD_ROOT + '\\user\\stu_info'
        rand_name = 'stu_%s' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17])
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_full_path = '%s\\%s%s' % (file_path, rand_name, os.path.splitext(file.name)[1])
        try:
            if file is None:
                return JsonResponse({"code": 2, "msg": '请选择文件后再上传！', 'errorlist': errorlist})
            # 循环二进制写入
            with open(file_full_path, 'wb') as f:
                for i in file.readlines():
                    f.write(i)
        except Exception as e:
            return HttpResponse(e)
        file = xlrd.open_workbook(file_full_path)
        sheet_1 = file.sheet_by_index(0)
        # report_name = sheet_1.row_values(2)  # 获取报表名称行数据
        row_num = sheet_1.nrows  # 获取行数
        # head_cols = sheet_1.row_values(0)
        # head_dict = {col_index: "".join(str(head_cols[col_index]).split()) for col_index in range(5, len(head_cols))}

        for i in range(1, row_num):  # 循环每一行数据
            row = sheet_1.row_values(i)  # 获取行数据
            if type(row[0]) is float:
                stu_no = repr(row[0]).split(".")[0]
            else:
                stu_no = "".join(str(row[0]).split())
            stu_name = "".join(str(row[1]).split())
            try:
                stu_list = Student.objects.filter(stu_no=stu_no)
                if stu_list and len(stu_list) > 0:
                    errorlist.append("%s: %s (已注册)<br/>" % (stu_no, stu_name))
                    continue
            except Exception as ex:
                print(ex)
                errorlist.append("%s: %s 服务器异常<br/>" % (stu_no, stu_name))
            if type(row[0]) is float:
                stu_pwd = repr(row[2]).split(".")[0]
            else:
                stu_pwd = "".join(str(row[2]).split())
            if not stu_pwd:
                stu_pwd = '123456'
            if type(row[0]) is float:
                stu_tel = repr(row[3]).split(".")[0]
            else:
                stu_tel = "".join(str(row[3]).split())
            stu_email = "".join(str(row[4]).split())
            stu_major = "".join(str(row[5]).split())
            stu_depart = "".join(str(row[6]).split())
            stu_avator = "/upload/user/avator/student/default_avator.jpg"
            stu_card = "".join(str(row[7]).split())
            stu_motto = "".join(str(row[8]).split())
            stu_sex = "".join(str(row[9]).split())

            stu_temp = Student(stu_no=stu_no, stu_name=stu_name, stu_pwd=stu_pwd, stu_tel=stu_tel, stu_email=stu_email,
                               stu_major=stu_major, stu_depart=stu_depart, stu_avator=stu_avator, stu_motto=stu_motto,
                               stu_card=stu_card, stu_sex=stu_sex)
            try:
                stu_temp.save()
            except Exception as ex:
                print(ex)
                errorlist.append("%s: %s 服务器异常<br/>" % (stu_no, stu_name))
        response_data = {
            "code": 6
            , "msg": '解析完成！'
            , 'errorlist': errorlist
        }
        return JsonResponse(response_data)


class CheckStunoView(View):

    def get(self, request):
        stu_no = request.GET.get('stu_no')
        if not stu_no:
            return JsonResponse({"code": 2, "msg": '请输入学号！'})
        try:
            stu = Student.objects.filter(stu_no=stu_no)
            if stu and len(stu) > 0:
                return JsonResponse({"code": 2, "msg": '当前学号已经注册，请选择其他学号！'})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": 2, "msg": '查询异常！'})
        return JsonResponse({"code": 6, "msg": '学号合法！'})



    def post(self, request):
        pass