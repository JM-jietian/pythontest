from django.db import models

# Create your models here.
"""
1.定义模型类
    1.模型类需要继承models.Model
    2.模型类会自动生成主键
    3.属性名=属性类型（选项）
        -属性名：不要使用python，mysql关键字
        -属性类型：和mysql的类型类似
        -选项：
            -charfiled(max_length=10)
            -varchar(10)
            -null 是否为空
            -unique=（True|False） 是否唯一
            -default=（0|True|False） 设置默认值
            -verbose_name="描述"  
2.模型迁移
    1.先生成迁移文件（不会再数据库生成表，只会创建一个数据表和模型的对应关系）
        -python manage.py makemigrations
    2.再执行迁移
        -python manage.py migrate
3.操作数据库
"""

# 书籍
class BookInfo(models.Model):  # 继承models.Model
    # 1.主键（自动创建）
    # 2.属性
    # 书籍名
    name = models.CharField(max_length=10, unique=True, verbose_name="书籍名")  # unique唯一
    # 发布日期
    pub_date = models.DateField(verbose_name="发布日期", default='2024-01-01')
    # 阅读量
    readcount = models.IntegerField(default=0, verbose_name="阅读量")  # default设置默认值
    # 评论量
    commentcount = models.IntegerField(default=0, verbose_name="评论量")
    # 是否逻辑删除
    is_delete = models.BooleanField(default=False, verbose_name="是否逻辑删除")

    # django自动生成了一个属性，通过这个属性可以根据主表查询从表信息
    # 属性：从表模型类名小写_set

    def __str__(self):
        """将模型类以字符串的方式输出"""
        # return f"book_name：{self.name} | pub_date：{self.pub_date} | readcount： {self.readcount} | commentcount：{self.commentcount} | is_delete：{self.is_delete}"
        return f"book_name：{self.name}"

    class Meta:
        # 修改表名
        db_table = "bookinfo"
        # 修改后台（admin）显示信息
        verbose_name = "书籍信息"


# 人物
class PeopleInfo(models.Model):
    # 有序字典
    GENDER_CHOICES = (
        (0, "male"),
        (1, "female")
    )
    # 人物姓名
    name = models.CharField(max_length=20, verbose_name="人物姓名")
    # 人物性别
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name="人物性别")
    # 人物描述信息
    description = models.CharField(max_length=200, null=True, verbose_name="人物描述信息")
    # 外键，与书籍表关联  设置 on_delete=models.CASCADE，当被引用的对象（即外键指向的对象）被删除时，所有依赖于它的对象（即包含外键指向该对象的记录）也会被自动删除
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)
    # 是否逻辑删除
    is_delete = models.BooleanField(default=False, verbose_name="是否逻辑删除")

    def __str__(self):
        # return f"book_name：{self.book.name} | name：{self.name} | gender：{self.gender} | description：{self.description} | is_delete：{self.is_delete}"
        return f"name：{self.name}"

    class Meta:
        # 修改表名
        db_table = "peopleinf"
        # 修改后台（admin）显示信息
        verbose_name = "人物信息"