"""bookmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

"""
1.urlpattern是固定写法，值是列表
2.在浏览器中输入的路径会和urlpatterns中的每一项顺序进行匹配
    -匹配成功：直接引导到对应的模块(子应用)，匹配结束
        -引导到对应的模块(子应用)中继续匹配
            -匹配成功：返回对应的试图
            -匹配失败：继续和总工程中的urlpatterns中的剩下的继续匹配
    -匹配失败（指的是把urlpatterns中的每一项都匹配完了）：返回404
3.urlpatterns中的元素是url
    -url的第一个参数：正则表达式（r 转义|^严格的开始|严格的结束$）
4.浏览器输入的路由中，ip:port和get|post参数不参与正则匹配
    -http://127.0.0.1:8000/admin/？key=value中仅/admin部分参与正则匹配
"""

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 防止url重名，在include的第二个参数添加一个namespace，这样url的name就变成了namespace:name（习惯使用应用名，需要在应用中添加参数app_name = "book"）
    path('book/', include("book.urls", "book")),
]
