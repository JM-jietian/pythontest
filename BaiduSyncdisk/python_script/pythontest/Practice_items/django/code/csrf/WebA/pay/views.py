from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token
from django.urls import reverse
from django.views import View

# Create your views here.


class LoginView(View):

    def post(self,request):

        # 取到表单中提交上来的参数
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not all([username, password]):
            print('参数错误')
        else:
            print(username, password)
            if username == 'laowang' and password == '1234':
                # 状态保持，设置用户名到cookie中表示登录成功
                response = redirect(reverse('transfer'))
                response.set_cookie('username', username)
                return response
            else:
                print('密码错误')
        return render(request,'login.html')

    def get(self,request):
        return render(request,'login.html')

class TransferView(View):

    def post(self,request):
        # 从cookie中取到用户名
        username = request.COOKIES.get('username', None)
        # 如果没有取到，代表没有登录
        if not username:
            return redirect(reverse('index'))

        # 转账的逻辑有问题，需要添加再次验证

        # 1.短信验证码
        # user_sms_code = request.POST.get('ses_code')  # 用户输入的验证码
        # # server_sms_code = redis.ger('sms_code')
        # server_sms_code = '123456'  # 服务端的验证码
        # print(user_sms_code)
        # if user_sms_code != server_sms_code:
        #     return HttpResponse('验证失败，无法转账！！！')

        # 2.随机码验证
        user_sms_code = request.POST.get('csrftoken')  # 用户请求时生成得到随机码
        server_sms_code = request.COOKIES.get('csrf_token')  # 获取cookie中的随机码
        if user_sms_code != server_sms_code:
            return HttpResponse('验证失败，无法转账！！！')

        to_account = request.POST.get("to_account")
        money = request.POST.get("money")

        print('假装执行转操作，将当前登录用户的钱转账到指定账户')
        return HttpResponse('转账 %s 元到 %s 成功' % (money, to_account))

    def get(self, request):
        from django.middleware.csrf import get_token
        # 生成随机码
        csrf_token = get_token(request)

        response = render(request, 'transfer.html', context={'csrf_token':csrf_token})

        # 将随机码csrf_token放在cookie中保存
        # 因为同源策略的原因，钓鱼网站不可能获取到随机码csrf_token
        response.set_cookie("csrf_token", csrf_token)
        return response
