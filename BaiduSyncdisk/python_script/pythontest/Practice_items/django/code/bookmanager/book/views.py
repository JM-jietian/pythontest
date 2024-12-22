import json
from http.client import responses
from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from book.models import BookInfo, PeopleInfo
from django.utils.datetime_safe import datetime
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
"""
试图：
    1.就是python函数
    2.函数的第一个参数就是请求, 请求相关的是 HttpRequest 的实例对象
    3.返回一个响应， 响应相关的是 HttpResponse 的实例对象/子类实例对象
"""

def book_list(request):
    books = BookInfo.objects.all()  # BookInfo.objects.all() = select * from bookinfo;
    # 参数1：当前的请求
    # 参数2：模板文件
    # 参数3：context-传递参数
    context = {
        "books": books
    }
    return render(request, 'book_list.html', context)

def index(request):
    # 通过试图名字找到路由(动态获取路由)
    # 在工程的url中设置了namespace，这里需要使用namespace:name
    index_path = reverse('book:index_name')
    print(index_path)

    # 跳转页面 redirect
    # return redirect('/book/list/')
    # return redirect(index_path)

###### HttpRequest对象
# HTTP协议向服务器传参:
#     提取URL的特定部分，如/weather/beijing/2018，可以在服务器端的路由中用正则表达式截取；
#     查询字符串（query string)，形如key1=value1&key2=value2；
#     请求体（body）中发送的数据，比如表单数据、json、xml；
#     在http报文的头（header）中

### URL路径参数
    # 1.URL中使用位置参数时，参数的位置不能错
    # 2.URL中使关键字参数时，参数的位置可以变，跟关键字保持一致即可
def detail_url(request, value1, value2):
    print(value1, value2)
    return HttpResponse('detail_url')

### Django中的QueryDict对象（HttpRequest对象的属性GET、POST都是QueryDict类型的对象）
def detail_get(request):
    """
    https://www.jd.com/?cu=true&utm_source=lianmeng__10__ntp.msn.cn&utm_medium=tuiguang&utm_campaign=t_2030767747_&utm_term=e64cecb9d13e45208eda0cf7375b5338
        以？作为分割
        ？前面是路由
        ？后面是get方式传递的参数（查询字符串）
        ？key1=value1&key2=value2
    """
    query_params = request.GET
    print(query_params)
    # 返回字典： <QueryDict: {'username': ['python', 'python1'], 'password': ['123456', '678910']}>

    ## 1.方法get()：根据键获取值，如果一个键同时拥有多个值将获取最后一个值
    # 如果键不存在则返回None值，可以设置默认值进行后续处
    # 语法：get('键',默认值)
    # 示例url：http://127.0.0.1:8000/book/detail_get/?username=python&username=python1&password=123456&password=678910
    username = query_params.get("username")  # python1
    password = query_params.get("password")  # 678910
    print("账号：%s， 密码：%s" % (username, password))  # 账号：python1， 密码：678910

    ## 2.方法getlist()：根据键获取值，值以列表返回，可以获取指定键的所有值
    # 如果键不存在则返回空列表[]，可以设置默认值进行后续处理
    # 语法：getlist('键',默认值)
    username = query_params.getlist("username")  # 'python', 'python1'
    password = query_params.getlist("password")  # '123456', '678910'
    print("账号：%s， 密码：%s" % (username, password))  # 账号：['python', 'python1']， 密码：['123456', '678910']

    return HttpResponse("detail_get")

### POST请求体
def detail_post(request):
    """
    请求体数据格式不固定，可以是表单类型字符串，可以是JSON字符串，可以是XML字符串，应区别对待。
    可以发送请求体数据的请求方式有POST、PUT、PATCH、DELETE
    Django默认开启了CSRF防护，会对上述请求方式进行CSRF防护验证，在测试时可以关闭CSRF防护机制，方法为在settings.py文件中注释掉CSRF中间件

    """
    ## 1.POST表单类型 from-data
    # 前端发送的表单类型的请求体数据，可以通过request.POST属性获取，返回QueryDict对象。
    data = request.POST
    print(data)
    # 返回字典 <QueryDict: {'username': ['python', 'python1'], 'password': ['123456', '78910']}>
    # 获取方式get()， getlist()

    ## 2.POST非表单类型 例如：json
    # 非表单类型的请求体数据，Django无法自动解析，可以通过request.body属性获取最原始的请求体数据，自己按照请求体格式（JSON、XML等）进行解析。request.body返回bytes类型。
    # 例如要获取请求体中的如下JSON数据
    # {"a": 1, "b": 2}
    body = request.body # 返回的是bytes类型数据，b'{\r\n    "username": "python",\r\n    "password": "123456"\r\n}'
    print(type(body))
    # bytes类型数据需要转换
    bod_str = body.decode()
    print(bod_str)
    # bytes类型数据转换后是json形式的字符串数据
    """
    {
        "username": "python",
        "password": "123456"
    }
    """
    # 将json数据转换为字典（json.dumps-将字典转换为json， json.loads-将json转换为字典）
    dat_str = json.loads(bod_str)
    print(dat_str)  # {'username': 'python', 'password': '123456'}
    # 获取方式get()， getlist()
    return HttpResponse("detail_post")


### http报请求头（header）中
# 可以通过request.META属性获取请求头headers中的数据，request.META为字典类型
def detail_header(request):
    print(request.META)
    # 自定义添加header NAME:JM
    # 在返回的请求头headers中，会自动在key前面加上HTTP_，例如：'HTTP_NAME': 'JM'
    print(request.META["HTTP_NAME"])  # JM

    ## 常用HttpRequest对象属性
    # method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
    print("method: ", request.method)  # method:  POST
    # user：请求的用户对象。
    print("user: ", request.user)  # user:  admin
    # path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
    print("path: ", request.path) # path:  /book/detail_header/
    # encoding：一个字符串，表示提交的数据的编码方式。
        # 如果为None则表示使用浏览器的默认设置，一般为utf-8。
        # 这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。
    print("encoding: ", request.encoding)  # encoding:  None
    # FILES：一个类似于字典的对象，包含所有的上传文件
    print("FILES: ", request.FILES)  # FILES:  <MultiValueDict: {}>
    return HttpResponse("detail_header")

####### HttpResponse对象
# 视图在接收请求并处理后，必须返回HttpResponse对象或子对象。
# HttpRequest对象由Django创建，HttpResponse对象由开发人员创建

### 1.HttpResponse
def detail_http_response(request):
    # HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)
    # content = 响应体,传递字符串，不要传递字典、对象等数据
    # content_type = 响应体数据类型（MIME类型，语法：大类/小类，例如：text/css、text/html）
    # status = 状态码，只能使用系统规定的状态码
        # HttpResponse子类
        # Django提供了一系列HttpResponse的子类，可以快速设置状态码:
        #     HttpResponseRedirect-301
        #     HttpResponsePermanentRedirect-302
        #     HttpResponseNotModified-304
        #     HttpResponseBadRequest-400
        #     HttpResponseNotFound-404
        #     HttpResponseForbidden-403
        #     HttpResponseNotAllowed-405
        #     HttpResponseGone-410
        #     HttpResponseServerError-500
    return HttpResponse(content="detail_http_response", content_type="text/html", status=200)

### 2.JsonResponse
# 若要返回json数据，可以使用JsonResponse来构造响应对象，作用：
# 帮助我们将数据转换为json字符串
# 设置响应头Content-Type为application/json
def detail_json_response(request):
    data = {'city': 'beijing', 'subject': 'python'}
    return JsonResponse(data)
# 返回转换后的json数据
"""
{
    "city": "beijing",
    "subject": "python"
}
"""

### 3.redirect重定向
def detail_redirect(request):
    # reverse 通过试图名字找到路由(动态获取路由)
    # 在工程的url中设置了namespace，这里需要使用namespace:name
    index_path = reverse('book:book_list_name')
    # redirect重定向
    return redirect(index_path)


######  状态保持
### - 在客户端存储信息使用`Cookie`
# 浏览器首次请求：不携带cookie信息，服务器设置cookie信息并响应给浏览器保存
# 浏览器第二次及以后的请求：都会携带cookie信息
def set_cookie(request):
    # 流程：
    #     1.浏览器第一次请求服务器的时候不会携带cookie信息
    #     2.服务器接收到请求后，发现请求中没有携带cookie信息，服务器会在响应中设置一个cookie信息
    #     3.浏览器接收到响应后，发现响应中有cookie信息，会将这个cookie信息保存起来
    #     4.浏览器第二次及以后的请求过程中，每次发送请求都会携带这个cookie信息
    #     5.服务器接收到浏览器的请求中携带的cookie信息，就会返回这个cookie对应的数据

    # http://127.0.0.1:8000/book/set_cookie/?username=itcast
    # 1.判断按是否有cookie信息（cookie信息在请求头中携带）
    # 2.获取用户名
    username = request.GET.get("username")
    # 3.设置cookie信息
    response = HttpResponse(username)  # 创建HttpResponse对象
    # 参数1：cookie的key
    # 参数2：cookie的value
    # 参数3：max_age设置cookie过时间，单位为秒
    #   默认为None；如果是临时cookie，可将max_age设置为None（None=浏览器关闭cookie过期）
    #   时间是从服务器接收到请求时开始计算
    response.set_cookie("username", username, max_age=None)  # 通过HttpResponse对象设置cookie
    # # 删除cookie有两种方式
    # response.delete_cookie(key)  # 调用delete_cookie方法删除
    # response.set_cookie(key, value, max_age=0)  # 设置过期时间为0
    # 4.返回响应
    return f"set_cookie: {response}"

# 服务器获取浏览器请求中的cookie信息，得到cookie信息后继续其业务逻辑
def get_cookie(request):
    # 1.服务器接收|查看cookie信息
    cookies = request.COOKIES  # cookies是字典类型
    username = cookies.get("username")
    # 2.得到cookie信息后继续其业务逻辑（例如：登录后，可以进行用户信息查询等）
    return HttpResponse(f"get_cookie: {username}")

### - 在服务器端存储信息使用`Session`
# session依赖于cookie，如果浏览器禁用了cookie，session就没法实现
def set_session(request):
    # 流程
    #     1.浏览器第一次请求时可以携带一些信息，例如：用户名|密码（cookie中没有任何信息）
    #     2.服务器接收到请求后，对携带的用户名|密码进行验证，验证通过，服务器会设置session信息，并将用户名|密码保存在session中
    #     3.服务器在设置session信息的同时会在响应中设置一个sessionid的cookie信息（服务器自动设置，不是手动设置的）
    #     4.浏览器在接收到响应后会将sessionid的cookie信息保存起来
    #     5.浏览器第二次及以后的请求过程中，每次发送请求都会携带这个sessionid的cookie信息
    #     6.服务器接收到浏览器的请求中携带sessionid的cookie信息时，会自动获取然后进行验证，验证通过则可以获取session信息

    # http://127.0.0.1:8000/book/set_cookie/?username=itcast&password=123456
    # 1.cookie中没有任何信息
    print(request.COOKIES)  # {'username': 'itcast', 'sessionid': '2pel1k47uaejt2gfehl4vhw1lai209ol'}
    # 2.对用户名|密码进行验证
    # 假设用户名|密码正确
    user_id = 123456
    # 3.设置session信息
    # 设置session信息的时候服务器有两个自动的操作：
    #     ① 将数据保存在数据库中
    #     ② 服务器自动设置cookie信息，以sessionid为key
    # request.session  返回的是字典数据
    response = request.session["user_id"] = user_id  # 123456
    # 清除所有session，在存储中删除值部分。
    # request.session.clear(
    # 清除session数据，在存储中删除session的整条数据。
    # request.session.flush()
    # 删除session中的指定键及值，在存储中只删除某个键及对应的值。
    # del request.session['键']
    # 设置session的有效期
    request.session.set_expiry(3600)
        # 如果value是一个整数，session将在value秒没有活动后过期。
        # 如果value为0，那么用户session的Cookie将在用户的浏览器关闭时过期。
        # 如果value为None，那么session有效期将采用系统默认值， 默认为两周，可以通过在settings.py中设置SESSION_COOKIE_AGE来设置全局默认值。
    # 4.返回响应
    return HttpResponse(f"set_session: {response}")

# 服务器获取浏览器请求中的sessionid的cookie信息，得到sessionid的cookie信息后继续其业务逻辑
def get_session(request):
    # 1.浏览器第二次及以后的请求过程中，每次发送请求都会携带这个sessionid的cookie信息
    print(request.COOKIES)  # {'sessionid': 'iu2ujmy5wwo4rqjtguwzj79fifq919eb'}
    # 2.服务器接收到浏览器的请求中携带sessionid的cookie信息时，会自动获取然后进行验证
    # request.session  返回的是字典数据
    user_id = request.session["user_id"]  # 123456
    # 3.返回响应
    return HttpResponse(f"get_session: {user_id}")


###### 类试图
"""
登录页面
    GET请求：获取登录页面
    POST请求：验证登录（用户名|密码是否正确）
"""
def login(request):
    # 根据请求方式区分业务逻辑
    # method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'
    if request.method == "GET":
        # GET请求：获取登录页面
        return render(request, 'book_list.html')
    else:
        # POST请求：验证登录（用户名|密码是否正确）
        index_path = reverse('book:book_list_name')
        return redirect(index_path)
"""
面向对象
    类试图采用面向对象的思路
    1.定义类试图：
        ①类试图继承View (from django.views import View)
        ②根据请求方式区分不同的业务逻辑，类试图的方法直接使用http请求方式命名，例如：get、post、put等
        ③类试图的方法第二个参数必须是请求实例对象
        ④类试图的方法必须有返回值，返是的值是HttpResopnse及其子类
"""
# View：
#   view方法：执行初始化
#   dispatch方法：判断请求的方法是否存在，存在则返回
class LoginView(View):

    def get(self, request):
        # 处理get请求逻辑
        return HttpResponse('get')

    def post(self, request):
        # 处理post请求逻辑
        return HttpResponse('post')

    def put(self, request):
        # 处理put请求逻辑
        return HttpResponse('put')

"""
个人中心页面 (需要先登录)
    GET请求：展示个人中心
    POST请求：实现个人中心数据修改
定义视图类(多继承)
"""
# LoginRequiredMixin验证登录（from django.contrib.auth.mixins import LoginRequiredMixin）
# 先执行LoginRequiredMixin的dispatch方法验证登录，验证成功则执行View的dispatch方法判断请求的方法是否存在，存在则返回
class CenterView(LoginRequiredMixin, View):

    def get(self, request):
        # 处理get请求逻辑
        return HttpResponse('个人中心展示')

    def post(self, request):
        # 处理post请求逻辑
        return HttpResponse('个人中心数据修改')


###### 模板
class HomeView(View):

    def get(self, request):
        # 1.获取数据
        username = request.GET.get("username")
        # 2.组织数据
        context = {
            "username": username,   # 姓名
            "age": 20,  # 年龄
            "birthday": datetime.now(),  # 日期
            "friends": ['tom', 'jack', 'rose'],  # 朋友
            "moneys": {
                '2019': 12000,
                '2020': 18000,
                '2021': 25000,
            },  # 月薪
            "desc": "<script>alert('这是我的个人信息')</script>",  # 简介
        }
        # return  render(request, "personal_information_django默认模板引擎.html", context)
        return  render(request, "personal_information_jinja2.html", context)


### 模板继承
class InheritView(View):

    def get(self, request):
        return render(request, "detail.html")  # detail.html继承自base.html