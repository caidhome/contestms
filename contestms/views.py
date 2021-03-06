import datetime
import os
import zipfile
import qrcode
import xlrd as xlrd
from PIL import Image, ImageDraw, ImageFont
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django_redis import get_redis_connection
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from contestms.models import Contest, Sign, Cert, Group
from userms.models import Admin, Student
from django.http import JsonResponse
from TiantiMS import settings
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class ListView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        login_user_sess = request.session.get('login_user')
        if not is_login or not login_user_sess or is_login == 3:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请登录后重试。', 'next': '/contest/list'})
        login_id = login_user_sess['admin_id']
        try:
            loginUser = Admin.objects.get(admin_id=login_id)
        except Exception as ex:
            print(ex)
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请登录后重试。', 'next': '/contest/list'})
        pIndex = request.GET.get('cpage')
        search_dict = dict()
        search_dict['con_createrid__admin_id'] = loginUser.admin_id
        # 如果有这个值 就写入到字典中去
        start = request.GET.get('start')
        end = request.GET.get('end')
        con_level = request.GET.get('con_level')
        con_id = request.GET.get('con_id')
        if con_level:
            search_dict['con_level'] = con_level
        else:
            con_level = ''
        if con_id:
            search_dict['con_id'] = con_id
        else:
            con_id = ''
        if start:
            search_dict['con_time__gte'] = start
        else:
            start = ''
        if end:
            search_dict['con_time__lte'] = end
        else:
            end = ''
        res = Contest.objects.filter(**search_dict).order_by('con_id')

        paginator = Paginator(res, 10)
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
            'res': list_page,
            'tpage': len(totol_page),
            'cpage': pIndex,
            'filt': {
                'con_level': con_level,
                'con_id': con_id,
                'start': start,
                'end': end
            }
        }
        return render(request, 'admin/contest/contest_list.html', rep_data)

    def post(self, request):
        pass


class AddView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请重新登录！', 'next': '/contest/add'})
        cert_list = Cert.objects.all()
        con_id = request.GET.get('con_id')
        contest = None
        if con_id:
            try:
                contest = Contest.objects.get(con_id=con_id)
            except Exception as ex:
                pass
        return render(request, 'admin/contest/contest_add.html', {'certs': cert_list, 'con': contest})

    @xframe_options_sameorigin
    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        code = 6
        msg = '添加成功'
        is_login = request.session.get('is_login')
        if is_login == None or is_login is 3:
            return JsonResponse({
                "code": 4
                , "msg": '当前权限不够，请以管理员身份登录后重试'
            })
        login_id = request.session.get('login_user')['admin_id']
        try:
            loginUser = Admin.objects.get(admin_id=login_id)
        except Exception as ex:
            print(ex)
            return JsonResponse({
                "code": 4
                , "msg": '你还未登录，请登录后重试'
            })
        con_name = request.POST.get('con_name')
        con_time = request.POST.get('con_time')
        con_signtime = request.POST.get('con_signtime')
        con_endtime = request.POST.get('con_endtime')
        con_place = request.POST.get('con_place')
        con_rule = request.POST.get('con_rule')
        con_environ = request.POST.get('con_environ')
        con_lang_list = request.POST.getlist('con_lang')
        con_lang = ''
        for lang_item in con_lang_list:
            con_lang += lang_item + ';'
        con_level = request.POST.get('con_level')
        con_signlink = request.POST.get('con_signlink')

        con_id = request.POST.get('con_id')
        contest = Contest()
        if con_id:
            contest = Contest.objects.get(con_id=con_id)
            msg = '修改成功'
        contest.con_name = con_name
        contest.con_time = con_time
        contest.con_signtime = con_signtime
        contest.con_endtime = con_endtime
        contest.con_place = con_place
        contest.con_rule = con_rule
        contest.con_environ = con_environ
        contest.con_lang = con_lang[:-1]
        contest.con_level = con_level
        contest.con_signlink = con_signlink
        contest.con_createrid = loginUser
        cert_id = request.POST.get('cert_id')
        try:
            con_cert = Cert.objects.get(cert_id=cert_id)
            contest.con_certid = con_cert
        except Exception:
            pass
        contest.save()
        return JsonResponse({
            "code": code
            , "msg": msg
        })


class DelView(View):

    def get(self, request):
        pass

    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        cid = request.POST.get('cid')
        try:
            contest = Contest.objects.get(con_id=cid)
            contest.delete()
            code = 6
            msg = '删除成功'
        except Exception as ex:
            code = 1
            msg = '删除失败'
        response_data = {
            "code": code
            , "msg": msg
        }
        return JsonResponse(response_data)


class DetialView(View):

    @xframe_options_sameorigin
    def get(self, request, cid):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        contest = None
        try:
            contest = Contest.objects.get(con_id=cid)
            contest.today = datetime.datetime.now()
            lang_str = ''
            for lang in contest.con_lang.split(';'):
                lang_str = lang_str + lang + ', '
            contest.con_lang = lang_str[:-2]
        except Exception as ex:
            print(ex)
        cur_sign = None
        if is_login and is_login in [1, 2]:
            groups = Group.objects.filter(group_conid__con_id=contest.con_id)
            group_dict = dict()
            for group in groups:
                sign_list = Sign.objects.filter(sign_groupid__group_id=group.group_id)
                stu_list = list()
                for sign in sign_list:
                    stu_list.append(Student.objects.get(stu_id=sign.sign_stuid_id))
                group_dict[group] = stu_list
            return render(request, 'admin/contest/contest_detial.html', {'con': contest, 'group_dict': group_dict})
        else:
            stu = None
            login_user = request.session.get('login_user')
            if login_user:
                try:
                    stu = Student.objects.get(stu_id=login_user['stu_id'])
                    sign = Sign.objects.filter(sign_stuid=stu, sign_conid=contest)
                    if sign and len(sign) > 0:
                        cur_sign = sign[0]
                except Exception as ex:
                    print(ex)
        return render(request, 'student/contest_detial.html', {'con': contest, 'sign': cur_sign})

    @xframe_options_sameorigin
    def post(self, request, cid):
        pass


class HeadView(View):

    @xframe_options_sameorigin
    def get(self, request):
        return render(request, 'student/head.html')

    @xframe_options_sameorigin
    def post(self, request):
        pass


class Sign_Person_View(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        if not is_login or is_login != 3 or not login_user:
            return render(request, 'student/login.html',
                          {'err_msg': '您当前还未登录，请登录后重试。', 'next': '/contest/sign/person'})
        sign_list = Sign.objects.filter(sign_stuid_id=login_user['stu_id']).values('sign_conid_id')
        cons = list()
        for sign_item in sign_list:
            cons.append(Contest.objects.get(con_id=sign_item['sign_conid_id']))
        return render(request, 'student/person_scores.html', {'cons': cons})

    @xframe_options_sameorigin
    def post(self, request):
        pass


class SignView(View):

    @xframe_options_sameorigin
    def get(self, request, cid):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        if not is_login or not login_user:
            return render(request, 'student/login.html',
                          {'err_msg': '您当前还未登录，请先登录！', 'next': '/contest/sign/%s/' % cid})
        contest = None
        try:
            contest = Contest.objects.get(con_id=cid)
            lang_str = [lang for lang in contest.con_lang.split(';')]
            contest.con_lang = lang_str
        except Exception as ex:
            print('查询异常')
            print(ex)
        return render(request, 'student/contest_sign.html', {'con': contest})

    def post(self, request, cid):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        if not is_login or not login_user:
            return JsonResponse({"code": 2, "msg": '您还未登录！'})

        sign_lang = request.POST.get('sign_lang')
        stu_no = request.POST.get('stu_no')
        sign_teach = request.POST.get('sign_teach')
        code = 6
        msg = '报名成功'
        stu = None
        con = None
        try:
            stu = Student.objects.filter(stu_no=stu_no)
            con = Contest.objects.get(con_id=cid)
        except Exception as ex:
            print(ex)
            code = 2
            msg = '报名失败，暂无该学生或竞赛信息！'
        if not con or not stu or len(stu) <= 0:
            code = 2
            msg = '报名失败，暂无该学生或竞赛信息！'
        cur_stu = stu[0]
        sign_list = Sign.objects.filter(sign_conid_id=con.con_id, sign_stuid_id=cur_stu.stu_id)
        if sign_list and len(sign_list) > 0:
            return JsonResponse({'code': 2, 'msg': '您已报名！'})

        sign = Sign(sign_lang=sign_lang, sign_state=0, sign_conid_id=con.con_id, sign_teach=sign_teach,
                    sign_stuid=cur_stu)
        sign.save()

        # 发邮件
        from_email = settings.EMAIL_FROM
        subject = '竞赛管理系统-报名成功'
        text_content = '这是一封重要的邮件.'
        html_content = '<p style="font-size: 18px;"><strong>%s</strong> 同学, 恭喜你：<br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;你报名的 <strong><a href="%s/contest/detial/%s/">%s</a></strong> 报名成功' \
                       '具体报名信息请查看<a href="%s/user/student/%s/">个人主页</a>。</p>' % (
                       cur_stu.stu_name, settings.PRO_HOST_URL, con.con_id, con.con_name, settings.PRO_HOST_URL,
                       cur_stu.stu_id)
        send_msg = EmailMultiAlternatives(subject, text_content, from_email, [stu[0].stu_email])
        send_msg.attach_alternative(html_content, "text/html")
        send_msg.send()

        response_data = {
            "code": code
            , "msg": msg
        }
        return JsonResponse(response_data)


# 报名状态：0 报名成功，1 弃赛（未审核） 2 弃赛  3 上传成绩 4 证书生成
class UploadScoreView(View):

    def get(self, request, con_id):
        pass

    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        file = request.FILES.get('file')
        con_id_str = request.POST.get('con_id')
        errorlist = list()
        if not con_id_str:
            return JsonResponse({'msg': '暂无查询到竞赛信息！', 'code': 2, 'errorlist': errorlist})
        con_id = int(con_id_str)
        file_path = settings.UPLOAD_ROOT + '\\contest\\score_file'
        rand_name = 'con_%s_%s' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17], con_id)
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
        try:
            file = xlrd.open_workbook(file_full_path)
            sheet_1 = file.sheet_by_index(0)
            # report_name = sheet_1.row_values(2)  # 获取报表名称行数据

            row_num = sheet_1.nrows  # 获取行数
            head_cols = sheet_1.row_values(0)
            head_dict = {col_index: "".join(str(head_cols[col_index]).split()) for col_index in
                         range(5, len(head_cols))}
            report_num = sheet_1.ncols  # 获取列数
            print(report_num)
            if report_num != 10:
                return JsonResponse({"code": 2, "msg": '上传失败，模板错误，请先下载模板并按模板指定内容格式上传！', 'errorlist': None})
            cur_con = Contest.objects.get(con_id=con_id)

            for i in range(1, row_num):  # 循环每一行数据
                row = sheet_1.row_values(i)  # 获取行数据
                stu_no = int(row[0])
                print(stu_no)
                stu_name = "".join(str(row[1]).split())
                stu_depart = "".join(str(row[2]).split())
                stu_major = "".join(str(row[3]).split())
                stu_teach = "".join(str(row[4]).split())
                # print('no:', stu_no, 'name: ', stu_name, 'depart: ', stu_depart, 'major: ', stu_major)
                cur_stu_list = Student.objects.filter(stu_no=stu_no, stu_name=stu_name, stu_depart=stu_depart,
                                                      stu_major=stu_major)
                # print(cur_stu_list)
                # print(cur_stu_list.query.__str__())
                # print(len(cur_stu_list))
                score_str = "".join(str(row[5]).split())
                score_level = "".join(str(row[6]).split())
                if not cur_stu_list or len(cur_stu_list) <= 0:
                    errorlist.append("%d:%s,总分：%s (数据库无此人）<br/>" % (stu_no, stu_name, score_str))
                    continue
                cur_stu = cur_stu_list[0]
                sign_list = Sign.objects.filter(sign_stuid=cur_stu, sign_conid=cur_con)
                # 缺考为：-1， 上传失败为：-2，
                if len(sign_list) > 0:
                    total_score = -5
                    cur_sign = sign_list[0]
                    try:
                        if score_str == '缺考':
                            total_score = -1
                        else:
                            total_score = float(score_str)
                    except Exception as ex:
                        total_score = -2
                        print(ex)
                        errorlist.append("%d:%s,总分数据为：%s（数据格式错误）<br/>" % (stu_no, stu_name, score_str))
                    detial = ''
                    for item in range(7, len(row)):
                        itemstr = head_dict[item] + '=' + "".join(str(row[item]).split()) + '&'
                        detial = detial + itemstr
                    cur_sign.sign_detial = detial[:-1]
                    cur_sign.sign_total = total_score
                    cur_sign.sign_state = 3
                    if stu_teach:
                        cur_sign.sign_teach = stu_teach
                    if score_level:
                        cur_sign.sign_level = score_level
                    cur_sign.save()
                else:
                    errorlist.append("%d:%s,总分：%s (该学生未报名该竞赛）<br/>" % (stu_no, stu_name, score_str))
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": 2, "msg": '上传失败，服务器错误！', 'errorlist': None})
        response_data = {
            "code": 6
            , "msg": '上传成功！'
            , 'errorlist': errorlist
        }
        return JsonResponse(response_data)


class Sign_List_View(View):

    @xframe_options_sameorigin
    def get(self, request, cid):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        try:
            cur_con = Contest.objects.get(con_id=cid)
            msg = '查询成功'
            code = 6
        except Exception as ex:
            msg = '查询异常'
            code = 2
            print(ex)
            response_data = {
                "code": code
                , "msg": msg
            }
            return JsonResponse(response_data)
        sign_list = Sign.objects.filter(sign_conid=cur_con).order_by('sign_groupid')

        data = list(sign_list.values())

        s_index = 1
        for s_item in data:
            temp_obj = dict(s_item)
            s_item['s_index'] = s_index
            s_index = s_index+1
            sign_state = temp_obj['sign_state']
            if sign_state == 1:
                s_item[
                    'sign_state'] = '<a style="color: red" href="javascript:void(0);" onclick=checkState(%s)>待审核</a>' % \
                                    s_item['sign_id']
            elif sign_state == 2:
                s_item['sign_state'] = '弃赛'
            else:
                s_item['sign_state'] = '正常'

            group_name = '未分组'
            sign_group_motto = '无'
            if s_item['sign_groupid_id']:
                group = Group.objects.get(group_id=s_item['sign_groupid_id'])
                group_name = group.group_name
                sign_group_motto = group.group_motto
            s_item['sign_group'] = group_name
            s_item['sign_group_motto'] = sign_group_motto

            sex_dict = {'F': '男', 'M': '女'}
            try:
                # s_item['sign_conname'] = Contest.objects.get(con_id=temp_obj['sign_conid_id'])
                student = Student.objects.get(stu_id=temp_obj['sign_stuid_id'])
                s_item['sign_stuname'] = student.stu_name
                s_item['sign_sex'] = sex_dict[student.stu_sex]
                s_item['sign_major'] = student.stu_major
                s_item['sign_motto'] = student.stu_motto
                s_item['sign_tel'] = student.stu_tel + '\t'
                s_item['sign_card'] = student.stu_card + '\t'
                s_item['sign_email'] = student.stu_email
            except Exception as ex:
                print(ex)
            if temp_obj['sign_detial']:
                detial_arr = temp_obj['sign_detial'].split('&')
                detial = dict()
                for d_item in detial_arr:
                    d_title = d_item.split('=')[0]
                    d_score = d_item.split('=')[1]
                    detial[d_title] = d_score
                s_item['sign_detial'] = str(detial)

        response_data = {
            "code": 0
            , "msg": ""
            , "count": len(sign_list)
            , "data": data
        }

        return JsonResponse(response_data)

    def post(self, request, cid):
        pass


class Sign_Check_View(View):

    @xframe_options_sameorigin
    def get(self, request, cid):
        pass

    def post(self, request, sid):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        state = request.POST.get('state')
        if not state or not is_login or not login_user:
            return JsonResponse({"code": 2, "msg": '当前权限不够或参数不合法！'})
        if state == '1':
            if is_login is not 3:
                return JsonResponse({"code": 2, "msg": '您还未登录！'})
        else:
            if is_login not in [1, 2]:
                return JsonResponse({"code": 2, "msg": '当前权限不够！'})
        try:
            sign = Sign.objects.get(sign_id=sid)
            if state and state in ['0', '1', '2']:
                sign.sign_state = state
                sign.save()
                msg = '审批成功'
                code = 6
            else:
                msg = '审批失败，状态值不合法！'
                code = 2
        except Exception as ex:
            msg = '暂无当前报名信息'
            code = 2
            print(ex)
        response_data = {
            "code": code
            , "msg": msg
        }
        return JsonResponse(response_data)


class Sign_Score_View(View):

    def get(self, request, cid):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        msg = '查询失败，请先登录后再试'
        code = 2
        if not is_login or is_login != 3 or not login_user:
            return JsonResponse({"code": code, "msg": msg})
        sign_list = Sign.objects.filter(sign_stuid_id=login_user['stu_id'], sign_conid_id=cid)
        data = dict()
        if sign_list and len(sign_list) > 0:
            sign_obj = sign_list[0]
            if sign_obj.sign_state != 3:
                return JsonResponse({"code": code, "msg": '您参加的该竞赛还未录入成绩'})
            detial_str = sign_obj.sign_detial
            if detial_str:
                detial = dict()
                detial_res = ''
                num = 0
                for d_item in detial_str.split('&'):
                    num = num + 1
                    d_title = d_item.split('=')[0]
                    d_score = d_item.split('=')[1]
                    detial_res = detial_res + d_title + ': ' + d_score
                    if num % 2 != 0:
                        detial_res = detial_res + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                    else:
                        detial_res = detial_res + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
                    detial[d_title] = d_score
                data['detial'] = detial_res
            data['score'] = sign_obj.sign_total
            data['level'] = sign_obj.sign_level
            data['teach'] = sign_obj.sign_teach
            data['sign_id'] = sign_obj.sign_id
            data['sign_lang'] = sign_obj.sign_lang
            if sign_obj.sign_certpath:
                data['sign_certpath'] = sign_obj.sign_certpath
            else:
                data['sign_certpath'] = ''
            msg = '查询成功'
            code = 6
        else:
            msg = '暂无该竞赛对应的成绩信息！'
            code = 2
        response_data = {
            "code": code
            , "msg": msg
            , "data": data
        }
        return JsonResponse(response_data)

    def post(self, request, sid):
        pass


class Sign_GenCert_View(View):

    def get(self, request, cid, sid):
        pass

    def post(self, request, cid, sid):
        host_url = '%s://%s' % (request.META['wsgi.url_scheme'], request.META['HTTP_HOST'])
        # 批量生成
        msg = "生成成功！"
        response_data = {
            "code": 6
            , "msg": msg
            , 'url': ''
        }
        if sid == '0':
            sign_list = Sign.objects.filter(sign_conid_id=cid).values('sign_id', 'sign_conid_id', 'sign_stuid_id',
                                                                      'sign_level', 'sign_total')
            # err_list = list()
            err_list = ''
            for sign in sign_list:
                if not sign['sign_level'] or sign['sign_total'] < 0:
                    continue
                response_data = self.gen_single(host_url, sign['sign_conid_id'], sign['sign_stuid_id'])
                if response_data['code'] == 3:
                    err_list = err_list + str(response_data['err_sid']) + ','
                    response_data['msg'] = '部分学生暂无成绩或等级信息，请上传后再试！无证书数据学生ID：%s' % err_list[:-1]
                    response_data['code'] = 2
        else:
            response_data = self.gen_single(host_url, cid, sid)
        return JsonResponse(response_data)

    def gen_single(self, host_url, cid, sid):
        msg = '生成成功'
        code = 6
        sign_list = Sign.objects.filter(sign_conid_id=cid, sign_stuid_id=sid)
        try:
            contest = Contest.objects.get(con_id=cid)
            stu = Student.objects.get(stu_id=sid)
        except Exception as ex:
            print(ex)
            return {"msg": '暂无当前学生或竞赛信息<br>生成失败，学生ID：%d' % sid, "code": 2}
        if sign_list and len(sign_list) > 0:
            sign_obj = sign_list[0]
            if sign_obj.sign_state != 3 or not sign_obj.sign_level or sign_obj.sign_total < 0:
                return {"msg": '当前学生暂无证书数据<br>生成失败，学生ID：%d' % sid, "code": 3, 'url': "", 'err_sid': stu.stu_id}
        else:
            return {"msg": '暂无当前报名信息，生成失败学生名称：' + stu.stu_name, "code": 2, 'url': ""}

        cert_obj = contest.con_certid
        cert_dir = '%s/cert/generate/%s/' % (settings.DOWNLOAD_ROOT, contest.con_id)
        temp_dir = '%s/cert/temp' % (settings.DOWNLOAD_ROOT)

        img_png_path = '%spng/cert_%s_%d.png' % (cert_dir, stu.stu_no, contest.con_id)
        img_pdf_path = '%spdf/cert_%s_%d.pdf' % (cert_dir, stu.stu_no, contest.con_id)
        if not os.path.exists('%spng' % (cert_dir)):
            os.makedirs('%spng' % (cert_dir))
        if not os.path.exists('%spdf' % (cert_dir)):
            os.makedirs('%spdf' % (cert_dir))
        if not os.path.exists(cert_dir):
            os.makedirs(cert_dir)

        cert_url = '%s/static/download/cert/generate/%s/png/cert_%s_%d.png' % (
        host_url, contest.con_id, stu.stu_no, contest.con_id)
        # 生成图片
        if not os.path.exists(img_png_path):
            old_img = Image.open("%s%s" % (os.path.join(settings.BASE_DIR, 'static'), cert_obj.cert_imgurl))
            draw = ImageDraw.Draw(old_img)
            # 设置图片文字，字体类型，以及字体大小，颜色
            newfont = ImageFont.truetype('%s/simhei.ttf' % temp_dir, 75)
            simsun = ImageFont.truetype('%s/simsun.ttf' % temp_dir, 75)
            # 写学生信息
            draw.text((cert_obj.cert_userx, cert_obj.cert_usery), stu.stu_name, font=newfont, fill="black")
            # 写证书等级
            simsun_level = ImageFont.truetype('%s/simhei.ttf' % temp_dir, 110)
            draw.text((cert_obj.cert_levelx, cert_obj.cert_levely), sign_obj.sign_level, font=simsun_level,
                      fill="black")
            # 写指导教师
            if sign_obj.sign_teach:
                simsun_teach = ImageFont.truetype('%s/simhei.ttf' % temp_dir, 80)
                draw.text((cert_obj.cert_teachx, cert_obj.cert_teachy), '指导教师：%s' % (sign_obj.sign_teach),
                          font=simsun_teach, fill="black")
            # 转pdf  1代表比赛id  我默认将ccf比赛的id置为1
            # 生成二维码
            qr = qrcode.QRCode(box_size=10, border=0)
            # 添加二维码的显示信息
            qr.add_data(cert_url)
            qr.make(fit=True)
            qr_img = qr.make_image()
            # 粘贴二维码
            # myQR_w, myQR_h = qr_img.size
            # base_img_w, base_img_h = old_img.size
            paste_location = (cert_obj.cert_qrcodex, cert_obj.cert_qrcodey)
            old_img.paste(qr_img, paste_location)
            old_img = old_img.transpose(Image.ROTATE_90)
            old_img.save(img_png_path)
        else:
            old_img = (Image.open(img_png_path))
        if not sign_obj.sign_certpath:
            sign_obj.sign_certpath = '/download/cert/generate/%s/png/cert_%s_%d.png' % (
            contest.con_id, stu.stu_no, contest.con_id)
            sign_obj.save()
        # 生成pdf
        if not os.path.exists(img_pdf_path):
            (w, h) = old_img.size
            pdf_obj = canvas.Canvas(img_pdf_path, pagesize=portrait((w, h)))
            pdf_obj.setTitle('荣誉证书_' + stu.stu_name)
            pdf_obj.drawImage(img_png_path, 0, 0, w, h)
            # pdf_obj.showPage()
            pdf_obj.save()
            old_img = old_img.transpose(Image.ROTATE_270)
            old_img.save(img_png_path)
            sign_obj.sign_certpath = img_png_path
        response_data = {
            "code": code
            , "msg": msg
            , 'url': cert_url
        }
        return response_data


class Cert_download_View(View):

    def get(self, request, sid):
        try:
            sign = Sign.objects.get(sign_id=sid)
            sign_png = sign.sign_certpath.replace('png', 'pdf')
            # /download/cert/generate/1/png/cert_2016001_1.png
            file = open("%s/static%s" % (settings.BASE_DIR, sign_png), 'rb')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
            rand_name = 'cert_%s' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17])
            response['Content-Disposition'] = 'attachment;filename="%s.pdf"' % rand_name
            return response
        except Exception as ex:
            print(ex)
        return HttpResponse('下载错误！')

    def post(self, request):
        pass


class Template_download_View(View):

    def get(self, request):
        file_name = request.GET.get('fname')
        try:
            file = open("%s/static%s" % (settings.BASE_DIR, '/download/common/template/%s' % file_name), 'rb')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
            response['Content-Disposition'] = 'attachment;filename="%s"' % file_name
            return response
        except Exception as ex:
            print(ex)
        return HttpResponse('下载错误！')

    def post(self, request):
        pass


class Downzip_Certs_View(View):

    def get(self, request, cid):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        if not is_login or is_login not in [1, 2] or not login_user:
            return JsonResponse({"code": 2, "msg": '当前权限不够！'})
        absDir = os.path.join('%s/cert/generate' % (settings.DOWNLOAD_ROOT), cid)
        if not os.path.exists(absDir):
            return HttpResponse("证书尚未生成！")

        cert_zip_dir = '%s/cert/generate/zip' % (settings.DOWNLOAD_ROOT)
        if not os.path.exists(cert_zip_dir):
            os.makedirs(cert_zip_dir)
        zipFilePath = os.path.join(cert_zip_dir, "cert_%s.zip" % cid)
        zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)
        os.chdir(absDir)
        for f in os.listdir(absDir):
            absFile = os.path.join(absDir, f)  # 子文件的绝对路径
            if os.path.isdir(absFile):  # 判断是文件夹，继续深度读取。
                relFile = absFile[len(absDir) + 1:]  # 改成相对路径，否则解压zip是/User/xxx开头的文件。
                zipFile.write(relFile)  # 在zip文件中创建文件夹
                self.writeAllFileToZip(absFile, zipFile)  # 递归操作
            else:  # 判断是普通文件，直接写到zip文件中。
                relFile = absFile[len(absDir) + 1:]  # 改成相对路径
                zipFile.write(relFile)
        zipFile.close()
        try:
            file = open(zipFilePath, 'rb')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/zip'  # 设置头信息，告诉浏览器这是个文件
            rand_name = 'cert_%s' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17])
            response['Content-Disposition'] = 'attachment;filename="%s.zip"' % rand_name
            return response
        except Exception as ex:
            print(ex)
        return HttpResponse('下载错误！')

    # 定义一个函数，递归读取absDir文件夹中所有文件，并塞进zipFile文件中。参数absDir表示文件夹的绝对路径。
    def writeAllFileToZip(self, absDir, zipFile):
        for f in os.listdir(absDir):
            absFile = os.path.join(absDir, f)  # 子文件的绝对路径
            if os.path.isdir(absFile):  # 判断是文件夹，继续深度读取。
                relFile = absFile[len(os.getcwd()) + 1:]  # 改成相对路径，否则解压zip是/User/xxx开头的文件。
                zipFile.write(relFile)  # 在zip文件中创建文件夹
                self.writeAllFileToZip(absFile, zipFile)  # 递归操作
            else:  # 判断是普通文件，直接写到zip文件中。
                relFile = absFile[len(os.getcwd()) + 1:]  # 改成相对路径
                zipFile.write(relFile)
        return

    def post(self, request):
        pass


class SendNoticeView(View):

    def get(self, request):
        pass

    def post(self, request, cid):
        redis_client = get_redis_connection('code')
        code = 6
        msg = '通知群发成功！'
        email_list = list()
        con = None
        try:
            con = Contest.objects.get(con_id=cid)
            if con.con_endtime < datetime.datetime.now():
                return JsonResponse({'code': 2, 'msg': '该竞赛报名已结束！'})
        except Exception as ex:
            print(ex)
            return JsonResponse({'code': 2, 'msg': '暂无该竞赛！'})
        try:
            stu_list = Student.objects.all()
            if stu_list and len(stu_list) > 0:
                for stu_item in stu_list:
                    if stu_item.stu_email:
                        email_list.append(stu_item.stu_email)
        except Exception as ex:
            print(ex)
            code = 2
            msg = '服务器错误！'
        from_email = settings.EMAIL_FROM
        subject = '竞赛管理系统-报名通知'
        text_content = ''
        html_content = '<p style="font-size: 18px;"><strong></strong> 同学, 你好：<br><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;天梯赛管理系统刚刚发布了 <strong><a href="%s/contest/detial/%s/">%s</a></strong>' \
                       '，赶紧去报名吧！<br/>具体报名信息请查看<a href="%s/contest/detial/%s/">竞赛详情</a>吧。</p>' % (
                           settings.PRO_HOST_URL, cid, con.con_name, settings.PRO_HOST_URL,
                           cid)
        send_msg = EmailMultiAlternatives(subject, text_content, from_email, email_list)
        send_msg.attach_alternative(html_content, "text/html")
        send_msg.send()
        redis_client.setex('tts_con_sendnotice_state_' + cid, 60 * 60 * 24 * 30, 1)
        response_data = {
            "code": code
            , "msg": msg
        }
        return JsonResponse(response_data)


# group 管理
class GroupListView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        if not is_login or not login_user or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前还未登录或登录权限不够，请重先登录！', 'next': '/contest/group/list'})
        res = Group.objects.all().order_by('group_conid__con_id')
        pIndex = request.GET.get('cpage')
        if not pIndex:
            pIndex = 1
        paginator = Paginator(res, 10)
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
            'res': list_page,
            'tpage': len(totol_page),
            'cpage': pIndex,
            'filt': {
            }
        }
        return render(request, 'admin/group/group_list.html', rep_data)

    def post(self, request):
        pass


class GroupAddView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请重新登录！', 'next': '/contest/group/add'})
        group_id = request.GET.get("group_id")
        group = None
        if group_id:
            group = Group.objects.get(group_id=group_id)
        con_list = Contest.objects.all()
        return render(request, 'admin/group/group_add.html', {'con_list': con_list, 'group': group})

    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        msg = '添加成功！'
        group_id = request.POST.get("group_id")
        group_name = request.POST.get("group_name")
        group_motto = request.POST.get("group_motto")
        group_conid = request.POST.get('group_conid')
        group = Group(group_name=group_name, group_motto=group_motto, group_conid_id=group_conid)
        if group_id:
            group.group_id = group_id
            msg = '更新成功！'
        group.save()
        return JsonResponse({'code': 6, 'msg': msg})


class GroupDelView(View):

    def get(self, request):
        pass

    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        gid = request.POST.get('group_id')
        try:
            group = Group.objects.get(group_id=gid)
            group.delete()
            code = 6
            msg = '删除成功'
        except Exception as ex:
            code = 2
            print(ex)
            msg = '删除失败'
        response_data = {
            "code": code
            , "msg": msg
        }
        return JsonResponse(response_data)


class GroupManageView(View):

    @xframe_options_sameorigin
    def get(self, request, gid):
        is_login = request.session.get('is_login')
        login_user_sess = request.session.get('login_user')
        if not is_login or not login_user_sess or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请登录后重试。', 'next': '/contest/group/manage/%s/' % gid})
        group = Group.objects.get(group_id=gid)
        con = Contest.objects.get(con_id=group.group_conid_id)
        sign_list = Sign.objects.filter(sign_conid_id=con.con_id)
        # sign_list = Sign.objects.filter(sign_groupid_id=gid)
        stu_list = list()
        stu_grouped = list()
        for sign in sign_list:
            s_stu = Student.objects.get(stu_id=sign.sign_stuid_id)
            if sign.sign_groupid_id == None or sign.sign_groupid_id == int(gid):
                stu_list.append(s_stu)
            if sign.sign_groupid_id == int(gid):
                stu_grouped.append(s_stu.stu_id)
        return render(request, 'admin/group/group_manage.html',
                      {'group': group, 'stu_list': stu_list, 'grouped': stu_grouped})

    def post(self, request):
        pass


class GroupPartView(View):

    def get(self, request):
        pass

    def post(self, request):
        is_login = request.session.get('is_login')
        login_user_sess = request.session.get('login_user')
        if not is_login or not login_user_sess or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请登录后重试。', 'next': '/contest/group/part'})
        code = 6
        msg = '分组成功！'
        gid = request.POST.get('gid')
        group = Group.objects.get(group_id=gid)
        add_list = request.POST.getlist('add')
        del_list = request.POST.getlist('del')
        for stu_add in add_list:
            sign_list = Sign.objects.filter(sign_conid_id=group.group_conid.con_id, sign_stuid_id=stu_add)
            if sign_list and len(sign_list) > 0:
                cur_sign = sign_list[0]
                cur_sign.sign_groupid_id = int(gid)
                cur_sign.save()
        for stu_del in del_list:
            sign_list_del = Sign.objects.filter(sign_groupid_id=group.group_id, sign_stuid_id=stu_del)
            if sign_list_del and len(sign_list_del) > 0:
                cur_sign_del = sign_list_del[0]
                cur_sign_del.sign_groupid = None
                cur_sign_del.save()
                msg = '删除成功'
        response_data = {
            "code": code
            , "msg": msg
        }
        return JsonResponse(response_data)


class Downzip_Avator_View(View):

    @xframe_options_sameorigin
    def get(self, request, export_type, cid):
        is_login = request.session.get('is_login')
        login_user = request.session.get('login_user')
        if not is_login or is_login not in [1, 2] or not login_user:
            return JsonResponse({"code": 2, "msg": '当前权限不够！'})

        type_str = ['common', 'part']

        # con = Contest.objects.get(con_id=cid)
        cert_zip_dir = '%s/contest/avator_export/zip/%s/%s' % (settings.DOWNLOAD_ROOT, type_str[int(export_type)], cid)
        if not os.path.exists(cert_zip_dir):
            os.makedirs(cert_zip_dir)

        absDir = '%s/user/avator/student/' % (settings.UPLOAD_ROOT)
        zipFilePath = os.path.join(cert_zip_dir, "avator_%s.zip" % cid)
        zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)
        if not os.path.exists(absDir):
            return HttpResponse("暂无头像信息！")
        os.chdir(absDir)

        has_custom_avator = True
        if export_type == '0':
            sign_list = Sign.objects.filter(sign_conid_id=cid)
            for sign in sign_list:
                stu = Student.objects.get(stu_id=sign.sign_stuid_id)
                if stu.stu_avator != '/upload/user/avator/student/default_avator.jpg':
                    has_custom_avator = False
                    # avator_file_list.append(stu.stu_avator)
                    absFile = os.path.join(settings.BASE_DIR, 'static', stu.stu_avator[1:])
                    print(absFile)
                    # if not os.path.isdir():
                    relFile = absFile[len(absDir):]  # 改成相对路径
                    zipFile.write(relFile)
        else:
            group_list = Group.objects.filter(group_conid_id=cid)
            avator_part_dir = '%s/contest/avator_export/file/%s/%s' % (
            settings.DOWNLOAD_ROOT, type_str[int(export_type)], cid)
            for group in group_list:
                sign_group_list = Sign.objects.filter(sign_conid_id=cid, sign_groupid_id=group.group_id)
                if not os.path.exists(os.path.join(avator_part_dir, group.group_name)):
                    os.makedirs(os.path.join(avator_part_dir, group.group_name))
                if sign_group_list and len(sign_group_list) > 0:
                    for sign_group in sign_group_list:
                        stu_group = Student.objects.get(stu_id=sign_group.sign_stuid_id)
                        if not stu_group.stu_avator or not os.path.exists(os.path.join(settings.BASE_DIR, 'static',
                                                                                       stu_group.stu_avator[
                                                                                       1:])) or stu_group.stu_avator == '/upload/user/avator/student/default_avator.jpg':
                            continue
                        has_custom_avator = False
                        with open(os.path.join(settings.BASE_DIR, 'static', stu_group.stu_avator[1:]), 'rb') as f_r:
                            content = f_r.read()
                        with open(os.path.join(avator_part_dir, group.group_name, '%s_%s%s' % (
                        stu_group.stu_no, stu_group.stu_name,
                        os.path.splitext(os.path.basename(stu_group.stu_avator))[1])), 'wb') as f_w:
                            f_w.write(content)
            sign_ungroup_list = Sign.objects.filter(sign_conid_id=cid, sign_groupid_id__isnull=True)
            if sign_ungroup_list and len(sign_ungroup_list) > 0:
                if not os.path.exists(os.path.join(avator_part_dir, '未分组')):
                    os.makedirs(os.path.join(avator_part_dir, '未分组'))
                for ungroup in sign_ungroup_list:
                    stu_group = Student.objects.get(stu_id=ungroup.sign_stuid_id)
                    with open(os.path.join(settings.BASE_DIR, 'static', stu_group.stu_avator[1:]), 'rb') as f_r:
                        content = f_r.read()
                    with open(os.path.join(avator_part_dir, '未分组', '%s_%s%s' % (
                            stu_group.stu_no, stu_group.stu_name,
                            os.path.splitext(os.path.basename(stu_group.stu_avator))[1])),
                              'wb') as f_w:
                        f_w.write(content)

            os.chdir(avator_part_dir)
            Downzip_Certs_View().writeAllFileToZip(avator_part_dir, zipFile)  # 递归操作

        zipFile.close()

        if has_custom_avator:
            return HttpResponse("暂无头像信息！")

        try:
            # /download/cert/generate/1/png/cert_2016001_1.png
            file = open(zipFilePath, 'rb')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/zip'  # 设置头信息，告诉浏览器这是个文件
            rand_name = 'avator_%s_%s' % (
            type_str[int(export_type)], datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:17])
            response['Content-Disposition'] = 'attachment;filename="%s.zip"' % rand_name
            return response
        except Exception as ex:
            print(ex)
        return HttpResponse('下载错误！')

    def post(self, request):
        pass


class Sign_DelList_View(View):

    def get(self, request):
        pass

    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})

        ids = request.POST.getlist('ids')
        code = 6
        msg = '删除成功！'
        error_list = ""
        for id in ids:
            try:
                sign = Sign(sign_id=id)
                sign.delete()
            except Exception as ex:
                print(ex)
                error_list = error_list + id + ','
        if len(error_list) > 0:
            code = 2
            msg = '删除失败，失败学生ID：' + error_list[:-1]
        return JsonResponse({'code': code, 'msg': msg})
