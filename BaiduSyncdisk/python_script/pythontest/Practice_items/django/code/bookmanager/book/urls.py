from django.urls import path, re_path
from book.views import (book_list, index, detail_url, detail_get, detail_post, detail_header,
                        detail_http_response, detail_json_response, detail_redirect,
                        set_cookie, get_cookie, set_session, get_session,
                        login, LoginView, CenterView, HomeView, InheritView,)  # 导入试图

app_name = "book"
urlpatterns = [
    # 第一个参数：正则
    # 第二个参数：试图函数名
    # 第三个参数：name 给url起名字，可以通过name找到这个路由
    path('list/', book_list, name='book_list_name'),
    path('index/', index, name='index_name'),

    ###### HTTP协议向服务器传参
    ### URL路径参数，使用re_path匹配正则
    ## 1.位置参数（根据位置传递参数，与试图中定义的变量位置对应）
    # \d匹配整数，+匹配多个最少有一个
    # 分组获取正则中的数据(分组的参数会传递给试图，定义试图的时候需要定义变量来接收)
    re_path(r'^(\d+)/(\d+)/$', detail_url, name='detail_url_name'),
    ## 2.关键字参数
    # ?P<value1>部分表示为这个参数定义的名称为value1（与试图中定义的变量名对应）
    re_path(r'^(?P<value1>\d+)/(?P<value2>\d+)/$', detail_url, name='detail_url_name'),
    ### Django中的QueryDict对象（HttpRequest对象的属性GET、POST都是QueryDict类型的对象）
    path('detail_get/', detail_get, name='detail_get_name'),
    ### POST请求体
    path('detail_post/', detail_post, name='detail_post_name'),
    ### http报请求头（header）中
    path('detail_header/', detail_header, name='detail_header_name'),


    ####### HttpResponse对象
    ### 1.HttpResponse
    path('detail_http_response/', detail_http_response, name='detail_http_response_name'),
    ### 2.JsonResponse
    path('detail_json_response/', detail_json_response, name='detail_json_response_name'),
    ### 3.redirect重定向
    path('detail_redirect/', detail_redirect, name='detail_redirect_name'),


    ######  状态保持
    ### - 在客户端存储信息使用`Cookie`
    # 浏览器第一次请求，服务器设置cookie，浏览器保存cookie
    path('set_cookie/', set_cookie, name='set_cookie_name'),
    # 浏览器第二次及以后的请求，服务获取到cookie
    path('get_cookie/', get_cookie, name='get_cookie_name'),
    ### - 在服务器端存储信息使用`Session`
    # 浏览器第一次请求，服务器设置session信息的同时在响应中设置一个sessionid的cookie信息，浏览器将sessionid的cookie信息保存起来
    path('set_session/', set_session, name='set_session_name'),
    # 浏览器第二次及以后的请求过程中，每次发送请求都会携带这个sessionid的cookie信息
    path('get_session/', get_session, name='get_session_name'),


    ###### 类试图
    ### 登录页面,根据请求方式区分业务逻辑
    path('login/', login, name='login_name'),
    ### 面向对象实现， url第一个参数是正则，第二个参数是视图函数名
    path('login_view/', LoginView.as_view(), name='login_view_name'),
    ### 个人中心
    path('center_view/', CenterView.as_view(), name='center_view_name'),


    ###### 模板
    path('home_view/', HomeView.as_view(), name='home_view_name'),
    ### 模板继承
    path('inherit_view/', InheritView.as_view(), name='inherit_view_name'),

]