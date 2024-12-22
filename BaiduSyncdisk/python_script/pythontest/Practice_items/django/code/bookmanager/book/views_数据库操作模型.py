from django.db.models import F, Q, Avg, Count, Max, Min, Sum
from django.shortcuts import render
from book.models import BookInfo, PeopleInfo
from django.core.paginator import Paginator  # 导入分页类

"""
命令行：python manage.py shell
导入模型类：from book.models import BookInfo
"""

### 新增数据
# 方式一
# 返回新生成的对象 // <BookInfo: 书籍：python | 发布日期：2024-11-18 | 阅读量： 0 | 评论量：0 | 状态(是否删除)：False>
book = BookInfo(
    name="python",
    pub_date="2024-11-18"
)
# 手动调用save()方法入库
book.save()

# 方式二
# 使用objects模型管理器（增删改查），直接入库
# 返回新生成的对象 // <BookInfo: 书籍：java | 发布日期：2024-11-20 | 阅读量： 0 | 评论量：0 | 状态(是否删除)：False>
BookInfo.objects.create(
    name="java",
    pub_date="2024-11-20"
)

################## 更新（修改）数据 ##################
# 方式一
# 1.先查询数据
book = BookInfo.objects.get(id=1)
# 2.直接修改实例属性
book.readcount = 200
# 3.手动调用save()方法入库
book.save()

# 方式二
# 使用objects模型管理器（增删改查），直接入库
# filter 过滤
# update 修改
BookInfo.objects.filter(id=2).update(
    readcount=99999,
    commentcount=1000000
)

################## 删除数据 ##################
# 方式一
# 1.查询数据
book = BookInfo.objects.get(id=6)
# 2.调用删除方法,直接删除  // (1, {'book.BookInfo': 1})
book.delete()

# 方式二
# 使用objects模型管理器（增删改查） // (1, {'book.BookInfo': 1})
BookInfo.objects.filter(id=5).delete()

################## 查询数据 ##################
################## 基本查询
# get 得到某一个数据，查询的数据不存在抛出异常，要求使用try...except...捕获异常
book_get = BookInfo.objects.get(
    id=1)  # 返回单一对象 <BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>

# all 所有数据
book_all = BookInfo.objects.all()  # 返回列表，包含所有数据

# count 数据的个数
BookInfo.objects.all().count()  # 返回数据的个数

################## 过滤查询（相当于where查询 select * from bookinfo where 条件语句）
# 语法： 过滤条件(字段名__运算符=值)
# 过滤条件：
# filter 过滤出多个结果
# exclude 排除掉符合条件剩下的结果
# get 过滤单一结果
# 运算符：
# exact 等于
# contains 是否包含
# startswith 以指定值开头
# endswith 以指定值结尾
# isnull 是否为null
# in 是否包含在范围内
# gt 大于 (greater then)
# gte 大于等于 (greater then equal)
# lt 小于 (less then)
# lte 小于等于 (less then equal)
# year、month、day、week_day、hour、minute、second 对日期时间类型的属性进行运算

# 查询编号为1的图书
BookInfo.objects.get(id__exact=1)  # <BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>
BookInfo.objects.get(id=1)  # <BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>
BookInfo.objects.filter(
    id__exact=1)  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>]>
BookInfo.objects.filter(
    id=1)  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>]>
# 查询书名包含'湖'的图书
BookInfo.objects.filter(
    name__contains="湖")  # <QuerySet [<BookInfo: 书籍：笑傲江湖 | 发布日期：1995-12-24 | 阅读量： 20 | 评论量：80 | 状态(是否删除)：False>]>
# 查询书名以'部'结尾的图书
BookInfo.objects.filter(
    name__endswith="部")  # <QuerySet [<BookInfo: 书籍：天龙八部 | 发布日期：1986-07-24 | 阅读量： 99999 | 评论量：1000000 | 状态(是否删除)：False>]>
# 查询书名为空的图书
BookInfo.objects.filter(name__isnull=True)  # <QuerySet []>
# 查询编号为1或3或5的图书
BookInfo.objects.filter(id__in=(1, 3,
                                5))  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>, <BookInfo: 书籍：笑傲江湖 | 发布日期：1995-12-24 | 阅读量： 20 | 评论量：80 | 状态(是否删除)：False>]>
# 查询编号大于3的图书
BookInfo.objects.filter(
    id__gt=3)  # <QuerySet [<BookInfo: 书籍：雪山飞狐 | 发布日期：1987-11-11 | 阅读量： 58 | 评论量：24 | 状态(是否删除)：False>]>
# 查询1980年发表的图书
BookInfo.objects.filter(
    pub_date__year="1980")  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>]>
# 查询1990年1月1日后发表的图书
BookInfo.objects.filter(
    pub_date__gt="1990-01-10")  # <QuerySet [<BookInfo: 书籍：笑傲江湖 | 发布日期：1995-12-24 | 阅读量： 20 | 评论量：80 | 状态(是否删除)：False>]>

################## F、Q对象
# F对象：两个属性比较
# 语法：filter(字段名__运算符=F("字段名"))
# 查询阅读量大于等于评论量的图书
BookInfo.objects.filter(readcount__gte=F(
    "commentcount"))  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>, <BookInfo: 书籍：雪山飞狐 | 发布日期：1987-11-11 | 阅读量： 58 | 评论量：24 | 状态(是否删除)：False>]>
# 查询阅读量大于2倍评论量的图书
BookInfo.objects.filter(readcount__gte=F(
    "commentcount") * 2)  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>, <BookInfo: 书籍：雪山飞狐 | 发布日期：1987-11-11 | 阅读量： 58 | 评论量：24 | 状态(是否删除)：False>]>

# Q对象：结合运算符使用，&表示逻辑与，|表示逻辑或，~Q表示非not
# 语法：Q(属性名__运算符=值)
# 查询id大于2，且阅读量大于20的书籍
BookInfo.objects.filter(Q(id__gt=2) & Q(
    readcount__gt=20))  # <QuerySet [<BookInfo: 书籍：雪山飞狐 | 发布日期：1987-11-11 | 阅读量： 58 | 评论量：24 | 状态(是否删除)：False>]>
# 查询id大于2 或 阅读量大于20的书籍
BookInfo.objects.filter(Q(id__gt=2) | Q(
    readcount__gt=20))  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>, <BookInfo: 书籍：天龙八部 | 发布日期：1986-07-24 | 阅读量： 99999 | 评论量：1000000 | 状态(是否删除)：False>, <BookInfo: 书籍：笑傲江湖 | 发布日期：1995-12-24 | 阅读量： 20 | 评论量：80 | 状态(是否删除)：False>, <BookInfo: 书籍：雪山飞狐 | 发布日期：1987-11-11 | 阅读量： 58 | 评论量：24 | 状态(是否删除)：False>]>
# 查询id不等于3的图书
BookInfo.objects.filter(~Q(id=1))

################## 聚合函数
# Avg平均，Count数量，Max最大，Min最小，Sum求和
# 语法：aggragte(聚合函数("字段"))

# 查询当前书籍的阅读总量
BookInfo.objects.aggregate(Sum("readcount"))  # {'readcount__sum': 100277}

################## 排序函数
# order_by
BookInfo.objects.all().order_by("readcount")  # 从小到大 默认升序
BookInfo.objects.all().order_by("-readcount")  # 从大到小 降序

################## 关联查询
"""
表结构解析：
    1.主表-书籍表和从表-人物表的关系是1对多
    2.书籍表中没有任何与人物表相关的信息
    3.人物表中有关于书籍表的字段book(外键)

需求：
    1.查询书籍为1的所有人物信息
    2.查询人物为1的书籍信息

语法：
    1.1对多
        通过主表-书籍表查从表-人物表信息（已知主表数据，关联查询从表数据）
        主表模型.关联模型类小写_set
    2.多对1
        通过从表-人物表查主表书籍表信息（已知从表数据，关联查询主表数据）
        从表模型(从表实例对象).外键
"""

# 1.查询书籍为1的所有人物信息
# 查询书籍
book = BookInfo.objects.get(id=1)
# 通过书籍信息关联查询人物信息
book.peopleinfo_set.all()

# 2.查询人物为1的书籍信息
# 查询人物
person = PeopleInfo.objects.get(id=1)
# 根据人物信息关联查询书籍信息 person.book - 实例对象
person.book.name  # '射雕英雄传'

################## 关联过滤查询
"""
需求1：
    多对1
    1.查询图书，要求图书人物为"郭靖"
    2.查询图书，要求图书中人物的描述包含"八"
    需要主表数据，已知从表信息

    1对多
    1.查询书名为“天龙八部”的所有人物
    2.查询图书阅读量大于30的所有人物
    需要从表数据，已知主表信息

语法：
    filter(关联模型类名小写__字段__运算符=值)
"""

# 多对1
# 1.查询图书，要求图书人物为"郭靖"
BookInfo.objects.filter(
    peopleinfo__name__exact='郭靖')  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>]>
# 2.查询图书，要求图书中人物的描述包含"八"
BookInfo.objects.filter(
    peopleinfo__description__contains='八')  # <QuerySet [<BookInfo: 书籍：射雕英雄传 | 发布日期：1980-05-01 | 阅读量： 200 | 评论量：34 | 状态(是否删除)：False>, <BookInfo: 书籍：天龙八部 | 发布日期：1986-07-24 | 阅读量： 99999 | 评论量：1000000 | 状态(是否删除)：False>]>

# 1对多
# 1.查询书名为“天龙八部”的所有人物
PeopleInfo.objects.filter(
    book__name__exact="天龙八部")  # <QuerySet [<PeopleInfo: 人物名：乔峰>, <PeopleInfo: 人物名：段誉>, <PeopleInfo: 人物名：虚竹>, <PeopleInfo: 人物名：王语嫣>]>
# 2.查询图书阅读量大于30的所有人物
PeopleInfo.objects.filter(
    book__readcount__gt=1000)  # <QuerySet [<PeopleInfo: 人物名：乔峰>, <PeopleInfo: 人物名：段誉>, <PeopleInfo: 人物名：虚竹>, <PeopleInfo: 人物名：王语嫣>]>

################## 查询集QuerySet
# 使用以下过滤器方法时，Django会返回查询集  <QuerySet [<BookInfo: book_name：射雕英雄传>, <BookInfo: book_name：天龙八部>, <BookInfo: book_name：笑傲江湖>, <BookInfo: book_name：雪山飞狐>]>
# all()：返回所有数据。
# filter()：返回满足条件的数据。
# exclude()：返回满足条件之外的数据。
# order_by()：对结果进行排序。

# 两大特性
# 1.惰性执行
book = BookInfo.objects.all()  # 不会执行
book  # 只有调用的时候才会执行  <QuerySet [<BookInfo: book_name：射雕英雄传>, <BookInfo: book_name：天龙八部>, <BookInfo: book_name：笑傲江湖>, <BookInfo: book_name：雪山飞狐>]>

# 2.缓存
# 内存：存储容量小，读取速度快，断电即失
# 硬盘：存储容量大，读取速度慢，断电保存
# 当前缓存的概念：将硬盘的数据，存储到内存中，这样读取速度快

# 如下是两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载
[book.id for book in BookInfo.objects.all()]  # 与数据库交
[book.id for book in BookInfo.objects.all()]  # 与数据库交

# 优化
# 经过存储后，可以重用查询集，第二次使用缓存中的数据。
books = BookInfo.objects.all()

[book.id for book in books]  # 第一次与数据库交
[book.id for book in books]  # 第二次使用缓存数据，不会与数据库交互

################## 限制查询集
# 可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句。
# 注意：不支持负数索引。
# 对查询集进行切片后返回一个新的查询集，不会立即执行查询。
# 如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()如果没有数据引发DoesNotExist异常

# 获取第1、2项
books = BookInfo.objects.all()[0:2]
books  # <QuerySet [<BookInfo: 射雕英雄传>, <BookInfo: 天龙八部>]>

################## 分页
# 查询数据
books = BookInfo.objects.all()
# 创建分页实例
# 第一个参数:结果集（列表）
# 第二个参数：每页多少条记录
paginator = Paginator(books, 2)
# 获取指定页码的数据
page_skus = paginator.page(1)
page_skus[1]
# 获取分页数据
total_page = paginator.num_pages