from datetime import datetime

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import date
from django.urls import reverse
from jinja2 import Environment


# jinja2自定义过滤器，可以定义新的过滤器，也可以指向django的过滤器
def environment(**options):
    env = Environment(**options)  #  创建environment实例
    env.globals.update({                    # 修改jinja2的函数指向django的过滤器
        'static':staticfiles_storage.url,   # 模板出现static，调用url函数
        'url':reverse,                      # 模板出现url，调用reverse函数
        'date':date,
    })
    return env                              # 返回修改后的环境变量

