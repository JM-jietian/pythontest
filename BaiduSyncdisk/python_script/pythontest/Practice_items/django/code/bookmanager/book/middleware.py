"""
中间件的作用： 每次请求和响应的时候都会调用
中间件的使用：例 - 可以判断每次请求是否携带了某些信息
中间件的执行顺序： 请求的时候是按照从上往下的顺序，响应的时候是按照从下往上的顺序
"""
# 定义中间件
def my_middleware1(get_response):
    print('init 被调用 - 1')
    # 试图函数
    def middleware1(request):
        # 请求前
        print('before request 被调用 - 1')
        response = get_response(request)
        # 响应后
        print('after response 被调用 - 1')
        return response

    return middleware1

def my_middleware2(get_response):
    print('init 被调用 - 2')
    # 试图函数
    def middleware2(request):
        # 请求前
        print('before request 被调用 - 2')
        response = get_response(request)
        # 响应后
        print('after response 被调用 - 2')
        return response

    return middleware2