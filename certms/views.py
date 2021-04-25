# coding=utf-8
import datetime
import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.views.decorators.clickjacking import xframe_options_sameorigin
from certms.models import Cert
from django.http import JsonResponse
from TiantiMS import settings


class ListView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请重新登录！', 'next': '/cert/list'})
        pIndex = request.GET.get('cpage')
        search_dict = dict()
        # 如果有这个值 就写入到字典中去
        res = Cert.objects.filter().order_by('cert_id')
        paginator = Paginator(res, 10)
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
            'cpage': pIndex
        }
        return render(request, 'admin/cert/cert_list.html', rep_data)

    def post(self, request):
        pass


class AddView(View):

    @xframe_options_sameorigin
    def get(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return render(request, 'admin/user/login.html',
                          {'err_msg': '您当前权限不够，请重新登录！', 'next': '/cert/add'})
        cert_id = request.GET.get('cert_id')
        cert = None
        if cert_id:
            try:
                cert = Cert.objects.get(cert_id=cert_id)
            except Exception as ex:
                pass
        return render(request, 'admin/cert/cert_add.html', {'cert': cert})

    @xframe_options_sameorigin
    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        cert_name = request.POST.get('cert_name')
        cert_userx = request.POST.get('cert_userx')
        cert_usery = request.POST.get('cert_usery')
        cert_levelx = request.POST.get('cert_levelx')
        cert_levely = request.POST.get('cert_levely')
        cert_qrcodex = request.POST.get('cert_qrcodex')
        cert_qrcodey = request.POST.get('cert_qrcodey')
        cert_teachx = request.POST.get('cert_teachx')
        cert_teachy = request.POST.get('cert_teachy')
        cert_imgurl = request.POST.get('cert_imgurl')
        cert_id = request.POST.get('cert_id')
        cert = None

        cert = Cert(cert_name=cert_name, cert_userx=cert_userx, cert_usery=cert_usery, cert_levelx=cert_levelx,
                    cert_levely=cert_levely,
                    cert_qrcodex=cert_qrcodex, cert_qrcodey=cert_qrcodey, cert_teachx=cert_teachx,
                    cert_teachy=cert_teachy, cert_imgurl=cert_imgurl)
        if cert_id:
            try:
                cert_old = Cert.objects.get(cert_id=cert_id)
                cert.cert_id = cert_old.cert_id
                msg = '更新成功'
                code = 6
            except Exception as ex:
                print(ex)
                msg = '更新失败'
                code = 2
        else:
            msg = '添加成功'
            code = 6
        cert.save()
        return JsonResponse({
            "code": code
            , "msg": msg
        })


class DelView(View):

    def get(self, request):
        pass

    @xframe_options_sameorigin
    def post(self, request):
        is_login = request.session.get('is_login')
        if not is_login or is_login not in [1, 2]:
            return JsonResponse({'code': 2, 'msg': '您当前权限不够，请重新登录！'})
        cert_id = request.POST.get('cert_id')
        file_path = '%s\\cert\\template' % settings.UPLOAD_ROOT
        try:
            cert = Cert.objects.get(cert_id=cert_id)
            file_full_path = '%s\\%s' % (file_path, cert.cert_imgurl.split('/')[-1])
            if cert.cert_imgurl and os.path.exists(file_full_path):
                os.remove(file_full_path)
            cert.delete()
            msg = '删除成功'
            code = 6
        except Exception as ex:
            print(ex)
            msg = '删除失败，请检查该证书是否被其他竞赛使用，请先删除使用该证书的竞赛后再试！'
            code = 2
        return JsonResponse({
            "code": code
            , "msg": msg
        })
