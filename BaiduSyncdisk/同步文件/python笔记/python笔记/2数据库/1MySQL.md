# MySQL数据库的基本使用

## 数据库

------

### 1. 数据库的介绍

数据库就是**存储和管理数据的仓库**，数据按照一定的格式进行存储，用户可以对数据库中的数据进行增加、修改、删除、查询等操作。

### 2. 数据库的分类

- 关系型数据库
- 非关系型数据库

**关系型数据库:**

是指采用了关系模型来组织数据的数据库，简单来说，**关系模型指的就是二维表格模型**，好比Excel文件中的表格，强调使用表格的方式存储数据。

**关系型数据库中核心元素**

- 数据行
- 数据列
- 数据表
- 数据库(数据表的集合)

**常用的关系型数据库:**

- Oracle
- Microsoft SQL Server
- MySQL
- SQLite

**非关系型数据库:**

非关系型数据库，又被称为NoSQL（Not Only SQL )，意为不仅仅是SQL，对NoSQL 最普遍的定义是“非关联型的”，强调 Key-Value 的方式存储数据。

**常用的非关系型数据库:**

- MongoDB
- Redis

提示: 目前我们先学习一下关系型数据库，而非关系型数据库会在后面课程中进行学习，大家先知道一下即可。

### 3. 数据库的作用

数据库的作用就是存储和管理数据的，比如: 我们在京东网站上的浏览的商品列表数据，这些数据都会存储在数据库。

### 4. 数据库的特点

1. 持久化存储
2. 读写速度极高
3. 保证数据的有效性

## 关系型数据库管理系统

------

### 1. 关系型数据库管理系统的介绍

数据库管理系统（英语全拼：Relational Database Management System，简称RDBMS）是**为管理关系型数据库而设计的软件系统，如果大家想要使用关系型数据库就需要安装数据库管理系统，其实就是一个应用软件**。

**关系型数据库管理系统可以分为:**

- 关系型数据库服务端软件
- 关系型数据库客户端软件

**关系型数据库服务端软件:**

主要负责管理不同的数据库，而每个数据库里面会有一系列数据文件，数据文件是用来存储数据的, 其实数据库就是一系列数据文件的集合。

**关系型数据库客户端软件:**

主要负责和关系型数据库服务端软件进行通信, 向服务端传输数据或者从服务端获取数据.

**说明:**

1. 用户操作关系型数据库客户端，实现数据库相关操作。
2. 关系数据库客户端借助网络使用SQL语言和关系型数据库服务端进行数据通信
3. 关系型数据库服务端管理着不同的数据库，每个数据库会有一系列的数据文件，数据都保存在数据文件里面，每个数据库可以理解成是一个文件夹。

通过上面的效果图我们可以得知，数据库客户端和数据库服务器想要通信需要使用SQL

### 2. SQL的介绍

SQL(Structured Query Language)是结构化查询语言，是一种用来操作RDBMS的数据库的语言。也就是说通过 SQL 可以操作 oracle,sql server,mysql,sqlite 等关系型的数据库。

SQL的作用是实现数据库客户端和数据库服务端之间的通信，SQL就是通信的桥梁。

**SQL语言主要分为：**

- **DQL：数据查询语言，用于对数据进行查询，如select**
- **DML：数据操作语言，对数据进行增加、修改、删除，如insert、update、delete**
- TPL：事务处理语言，对事务进行处理，包括begin transaction、commit、rollback
- DCL：数据控制语言，进行授权与权限回收，如grant、revoke
- DDL：数据定义语言，进行数据库、表的管理等，如create、drop

**说明:**

- 对于程序员来讲，重点是数据的增、删、改、查，必须熟练编写DQL、DML，能够编写DDL完成数据库、表的操作，其它操作如TPL、DCL了解即可.
- SQL语言不区分大小写

## MySQL数据库

------

### 1. MySQL数据库的介绍

MySQL是一个关系型数据库管理系统，在 WEB 应用方面，MySQL是最好的 RDBMS (Relational Database Management System，关系数据库管理系统) 应用软件，它是由瑞典MySQL AB 公司开发，目前属于 Oracle 旗下产品，MySQL 是最流行的关系型数据库管理系统中的一个。

**MySQL的特点:**

1. MySQL是开源的，所以你不需要支付额外的费用。
2. MySQL支持大型的数据库。可以处理拥有上千万条记录的大型数据库。
3. MySQL使用标准的SQL数据语言形式。
4. MySQL可以安装在不同的操作系统，并且提供多种编程语言的操作接口。这些编程语言包括C、C++、Python、Java、Ruby等等。

### 2. MySQL数据库的安装

- MySQL数据库服务端软件的安装
- MySQL数据库客户端软件的安装

**MySQL数据库服务端软件的安装:**

在Ubuntu中打开终端，输入下面的命令:

```
sudo apt-get install mysql-server
```

**说明:**

- 目前大家使用的Ubuntu中已经安装好了MySQL服务端软件，无需再安装。

**ps说明**

- ps 查看当前系统中的进程
- -a 表示所有用户
- -u 表示显示用户名
- -x 表示显示所有的执行程序

**查看MySQL服务状态:**

```
sudo service mysql status
```

**停止MySQL服务:**

```
sudo service mysql stop
```

**启动MySQL服务:**

```
sudo service mysql start
```

**重启MySQL服务:**

```
sudo service mysql restart
```

**MySQL配置文件的介绍:**

配置文件路径为: /etc/mysql/mysql.conf.d/mysqld.cnf

**主要配置信息说明:**

```
port表示端口号，默认为3306

bind-address表示服务器绑定的ip，默认为127.0.0.1

datadir表示数据库保存路径，默认为/var/lib/mysql

log_error表示错误日志，默认为/var/log/mysql/error.log
```

**MySQL数据库客户端软件的安装:**

客户端是程序员或者dba使用的软件，通过socket方式与服务端程序通信。

常用的MySQL数据库客户端软件有

1. 图形化界面客户端Navicat
2. 命令行客户端mysql

**图形化界面客户端Navicat的使用**

1. 可以到[Navicat官网下载](https://www.navicat.com.cn/download/navicat-for-mysql)
2. 将压缩文件拷贝到Ubuntu虚拟机中，放到桌面上，解压

**Navicat的使用说明:**

```
tar zxvf navicat112_mysql_cs_x64.tar.gz

./start_navicat
```

**说明:**

点击两次“取消”按钮, 不需要进行安装。

**试用过期的解决办法:**

当过期后，删除用户主目录下的.navicat64目录，继续再使用14天。

```
cd ~
rm -r .navicat64
```

**命令行客户端mysql的安装**

在Ubuntu中打开终端，输入下面的命令:

```
sudo apt-get install mysql-client
```

**说明:**

- 目前大家使用的Ubuntu中已经安装好了MySQL命令行客户端软件，无需再安装。

**显示MySQL客户端安装包信息效果图:**

![MySQL客户端安装包信息](imgs/mysql客户端软件安装包信息.png)

**mysql命令的使用帮助:**

```
mysql --help
```

**MySQL客户端的使用:**

MySQL客户端连接MySQL服务端命令

```
mysql -uroot -p
```

**说明:**

- -u: 表示MySQL服务端的用户名
- -p: 表示MySQL服务端的密码
- quit 或者 exit 或者 ctr + d 表示退出

## 数据类型和约束

------

大家都知道数据库中的数据保存在数据表中，在表中为了更加准确的存储数据，保证数据的正确有效，可以在创建表的时候，为表添加一些强制性的验证，比如:数据类型和约束。

### 1. 数据类型

数据类型是指在创建表的时候为表中字段指定数据类型，只有数据符合类型要求才能存储起来，使用数据类型的原则是:够用就行，尽量使用取值范围小的，而不用大的，这样可以更多的节省存储空间。

**常用数据类型如下:**

- 整数：int，bit
- 小数：decimal
- 字符串：varchar,char
- 日期时间: date, time, datetime
- 枚举类型(enum)

**数据类型说明:**

- decimal表示浮点数，如 decimal(5, 2) 表示共存5位数，小数占 2 位.
- char表示固定长度的字符串，如char(3)，如果填充'ab'时会补一个空格为'ab '，3表示字符数
- varchar表示可变长度的字符串，如varchar(3)，填充'ab'时就会存储'ab'，3表示字符数
- 对于图片、音频、视频等文件，不存储在数据库中，而是上传到某个服务器上，然后在表中存储这个文件的保存路径.
- 字符串 text 表示存储大文本，当字符大于 4000 时推荐使用, 比如技术博客.

### 2. 数据约束

约束是指数据在数据类型限定的基础上额外增加的要求.

**常见的约束如下:**

- 主键 primary key: 物理上存储的顺序. MySQL 建议所有表的主键字段都叫 id, 类型为 int unsigned.
- 非空 not null: 此字段不允许填写空值.
- 惟一 unique: 此字段的值不允许重复.
- 默认 default: 当不填写字段对应的值会使用默认值，如果填写时以填写为准.
- 外键 foreign key: 对关系字段进行约束, 当为关系字段填写值时, 会到关联的表中查询此值是否存在, 如果存在则填写成功, 如果不存在则填写失败并抛出异常.

### 3. 数据类型附录表

##### 1. 整数类型

| 类型        | 字节大小 | 有符号范围(Signed)                         | 无符号范围(Unsigned)     |
| :---------- | :------- | :----------------------------------------- | :----------------------- |
| TINYINT     | 1        | -128 ~ 127                                 | 0 ~ 255                  |
| SMALLINT    | 2        | -32768 ~ 32767                             | 0 ~ 65535                |
| MEDIUMINT   | 3        | -8388608 ~ 8388607                         | 0 ~ 16777215             |
| INT/INTEGER | 4        | -2147483648 ~2147483647                    | 0 ~ 4294967295           |
| BIGINT      | 8        | -9223372036854775808 ~ 9223372036854775807 | 0 ~ 18446744073709551615 |

##### 2. 字符串

| 类型     | 说明                        | 使用场景                     |
| :------- | :-------------------------- | :--------------------------- |
| CHAR     | 固定长度，小型数据          | 身份证号、手机号、电话、密码 |
| VARCHAR  | 可变长度，小型数据          | 姓名、地址、品牌、型号       |
| TEXT     | 可变长度，字符个数大于 4000 | 存储小型文章或者新闻         |
| LONGTEXT | 可变长度， 极大型文本数据   | 存储极大型文本数据           |

##### 3. 时间类型

| 类型      | 字节大小 | 示例                                                  |
| :-------- | :------- | :---------------------------------------------------- |
| DATE      | 4        | '2020-01-01'                                          |
| TIME      | 3        | '12:29:59'                                            |
| DATETIME  | 8        | '2020-01-01 12:29:59'                                 |
| YEAR      | 1        | '2017'                                                |
| TIMESTAMP | 4        | '1970-01-01 00:00:01' UTC ~ '2038-01-01 00:00:01' UTC |

## 图形化客户端Navicat

------

### 1. Navicat的介绍

Navicat 是一套快速、可靠并价格适宜的数据库管理工具, 适用于三种平台: Windows、mac OS 及 Linux。 可以用来对本机或远程的 MySQL、SQL Server、SQLite、Oracle 等数据库进行管理及开发。 专门为简化数据库的操作而设计。 它的设计符合数据库管理员、开发人员及中小企业的需求。 Navicat 是一个数据库图形化客户端软件, 让你可以以安全并且简单的方式对数据库进行操作。

### 2. Navicat的使用

Navicat 的使用从三方面来介绍:

1. 和MySQL数据库服务端建立连接
2. 数据库的操作
3. 数据表的操作
4. 数据表中数据的操作

**数据库的操作:**

1. 创建数据库
2. 编辑数据库
3. 删除数据库

**创建数据库:**

1. 在左侧栏空白处右击，选择“新建数据库”进行点击。

2. 点击后弹出新窗口，填写数据库名称并选择编码格式

   说明:

   - 字符集: 就是编码格式，**选择utf8的国际通用编码格式, 支持中文**。
   - 排序规则: **utf8_general_ci 表示大小写不敏感，不区分大小写字母,a 和 A 在字符判断中会被当做一样的处理，区分大小写可以选择utf8_bin**

3. 双击选择创建好的数据库进行使用

**编辑数据库:**

1. 选择对应的数据库，右击选择“编辑数据库”
2. 点击“编辑数据库”，可以修改字符集、排序规则

**删除数据库:**

1. 选择对应的数据库，右击选择“删除数据库” 

**数据表的操作:**

1. 创建数据表
2. 编辑数据表
3. 删除数据表

**创建数据表:**

1. 选择数据库中的表，右击选择“新建表”

   **说明:**

   - id 字段: int 类型 无符号 主键 非空 自动增长
   - name 字段: varchar 类型 非空
   - sex 字段: char 类型 允许为空 默认值:男

**编辑数据表:**

1. 选择需要编辑的表，右击选择“设计表”

**删除数据表:**

1. 选择对应的数据表，右击选择“删除表” 

**数据表中数据的操作:**

1. 查看表中数据
2. 添加数据
3. 修改数据
4. 删除数据

**查看表中数据:**

1. 双击对应的表，查看表中数据 

**添加数据:**

1. 点击加号添加数据，数据添加完成后需要点击对号让数据生效 

**修改数据:**

1. 选择需要修改的记录，进行编辑修改即可，修改后需要点击对号让数据生效 

**删除数据:**

1. 选中要删除的记录，右击选择“删除记录”或者点击减号进行删除 

   **说明:**

   - 对于重要数据，可以添加一个字段作为标识，而不是进行物理删除.

## 命令行客户端MySQL的使用

------

### 1. 登录和登出数据库

**登录数据库:**

输入下面命令:

```sql
mysql -uroot -p
```

**说明:**

- -u 后面是登录的用户名
- -p 后面是登录密码, 如果不填写, 回车之后会提示输入密码

**登录成功后, 输入如下命令查看效果：**

```sql
# 显示当前时间
select now();
```

**登出(退出)数据库:**

```sql
quit 或 exit 或 ctrl + d
```

### 2. 数据库操作的SQL语句

1. 查看所有数据库

   ```sql
   show databases;
   ```

2. 创建数据库

   ```sql
   create database 数据库名 charset=utf8;
   例：
   create database python charset=utf8;
   ```

3. 使用数据库

   ```sql
   use 数据库名;
   ```

4. 查看当前使用的数据库

   ```sql
   select database();
   ```

5. 删除数据库-慎重

   ```sql
   drop database 数据库名;
   例：
   drop database python;
   ```

### 3. 表结构操作的SQL语句

1. 查看当前数据库中所有表

   ```sql
   show tables;
   ```

2. 创建表

   ```sql
   create table students(
    id int unsigned primary key auto_increment not null,
    name varchar(20) not null,
    age tinyint unsigned default 0,
    height decimal(5,2),
    gender enum('男','女','人妖','保密')
   );
   ```

   **说明:**

   ```sql
   create table 表名(
   字段名称 数据类型  可选的约束条件,
   column1 datatype contrai,
   ...
   );
   ```

3. 修改表-添加字段

   ```sql
   alter table 表名 add 列名 类型 约束;
   例：
   alter table students add birthday datetime;
   ```

4. 修改表-修改字段类型

   ```sql
   alter table 表名 modify 列名 类型 约束;
   例：
   alter table students modify birthday date not null;
   ```

   **说明:**

   - modify: 只能修改字段类型或者约束，不能修改字段名

5. 修改表-修改字段名和字段类型

   ```sql
   alter table 表名 change 原名 新名 类型及约束;
   例：
   alter table students change birthday birth datetime not null;
   ```

   **说明:**

   - change: 既能对字段重命名又能修改字段类型还能修改约束

6. 修改表-删除字段

   ```sql
   alter table 表名 drop 列名;
   例：
   alter table students drop birthday;
   ```

7. 查看创表SQL语句

   ```sql
   show create table 表名;
   例：
   show create table students;
   ```

8. 查看创库SQL语句

   ```sql
   show create database 数据库名;
   例：
   show create database mytest;
   ```

9. 删除表

   ```sql
   drop table 表名;
   例：
   drop table students;
   ```

### 4. 表数据操作的SQL语句

1. 查询数据

   ```sql
   -- 1. 查询所有列
   select * from 表名;
   例：
   select * from students;
   -- 2. 查询指定列
   select 列1,列2,... from 表名;
   例：
   select id,name from students;
   ```

2. 添加数据

   ```sql
   -- 1. 全列插入：值的顺序与表结构字段的顺序完全一一对应
   insert into 表名 values (...)
   例:
   insert into students values(0, 'xx', default, default, '男');
   -- 2. 部分列插入：值的顺序与给出的列顺序对应
   insert into 表名 (列1,...) values(值1,...)
   例:
   insert into students(name, age) values('王二小', 15);
   -- 3. 全列多行插入
   insert into 表名 values(...),(...)...;
   例:
   insert into students values(0, '张飞', 55, 1.75, '男'),(0, '关羽', 58, 1.85, '男');
   -- 4. 部分列多行插入
   insert into 表名(列1,...) values(值1,...),(值1,...)...;
   例：
   insert into students(name, height) values('刘备', 1.75),('曹操', 1.6);
   ```

   **说明:**

   - 主键列是自动增长，但是在全列插入时需要占位，通常使用空值(0或者null或者default)
   - 在全列插入时，如果字段列有默认值可以使用 default 来占位，插入后的数据就是之前设置的默认值

3. 修改数据

   ```sql
   update 表名 set 列1=值1,列2=值2... where 条件
   例：
   update students set age = 18, gender = '女' where id = 6;
   ```

4. 删除数据

   ```sql
   delete from 表名 where 条件
   例：
   delete from students where id=5;
   ```

   问题:

   上面的操作称之为物理删除，一旦删除就不容易恢复，我们可以使用逻辑删除的方式来解决这个问题。

   ```sql
   -- 添加删除表示字段，0表示未删除 1表示删除
   alter table students add isdelete bit default 0;
   -- 逻辑删除数据
   update students set isdelete = 1 where id = 8;
   ```

   **说明:**

   - 逻辑删除，本质就是修改操作

## as和distinct关键字

------

### 1. as关键字

在使用SQL语句显示结果的时候，往往在屏幕显示的字段名并不具备良好的可读性，此时可以使用 as 给字段起一个别名。

1. 使用 as 给字段起别名

   ```sql
   select id as 序号, name as 名字, gender as 性别 from students;
   ```

2. 可以通过 as 给表起别名

   ```sql
   -- 如果是单表查询 可以省略表名
   select id, name, gender from students;
   
   -- 表名.字段名
   select students.id,students.name,students.gender from students;
   
   -- 可以通过 as 给表起别名 
   select s.id,s.name,s.gender from students as s;
   ```

   **说明:**

   - 在这里给表起别名看起来并没有什么意义,然而并不是这样的，我们在后期学习 自连接 的时候，必须要对表起别名。

### 2. distinct关键字

distinct可以去除重复数据行。

```sql
select distinct 列1,... from 表名;

例： 查询班级中学生的性别
select name, gender from students;

-- 看到了很多重复数据 想要对其中重复数据行进行去重操作可以使用 distinct
select distinct name, gender from students;
```

## where条件查询

------

### 1. where条件查询的介绍

使用where条件查询可以对表中的数据进行筛选，条件成立的记录会出现在结果集中。

**where语句支持的运算符:**

1. 比较运算符
2. 逻辑运算符
3. 模糊查询
4. 范围查询
5. 空判断

**where条件查询语法格式如下:**

```sql
select * from 表名 where 条件;
例：
select * from students where id = 1;
```

### 2. 比较运算符查询

1. 等于: =
2. 大于: >
3. 大于等于: >=
4. 小于: <
5. 小于等于: <=
6. 不等于: != 或 <>

**例1：查询编号大于3的学生:**

```sql
select * from students where id > 3;
```

**例2：查询编号不大于4的学生:**

```sql
select * from students where id <= 4;
```

**例3：查询姓名不是“黄蓉”的学生:**

```sql
select * from students where name != '黄蓉';
```

**例4：查询没被删除的学生:**

```sql
select * from students where is_delete=0;
```

### 3. 逻辑运算符查询

1. and
2. or
3. not

**例1：查询编号大于3的女同学:**

```sql
select * from students where id > 3 and gender=0;
```

**例2：查询编号小于4或没被删除的学生:**

```sql
select * from students where id < 4 or is_delete=0;
```

**例3：查询年龄不在10岁到15岁之间的学生:**

```sql
select * from students where not (age >= 10 and age <= 15);
```

**说明:**

- 多个条件判断想要作为一个整体，可以结合‘()’。

### 4. 模糊查询

1. like是模糊查询关键字
2. %表示任意多个任意字符
3. _表示一个任意字符

**例1：查询姓黄的学生:**

```sql
select * from students where name like '黄%';
```

**例2：查询姓黄并且“名”是一个字的学生:**

```sql
select * from students where name like '黄_';
```

**例3：查询姓黄或叫靖的学生:**

```sql
select * from students where name like '黄%' or name like '%靖';
```

### 5. 范围查询

1. between .. and .. 表示在一个连续的范围内查询
2. in 表示在一个非连续的范围内查询

**例1：查询编号为3至8的学生:**

```sql
select * from students where id between 3 and 8;
```

**例2：查询编号不是3至8的男生:**

```
select * from students where (not id between 3 and 8) and gender='男';
```

### 6. 空判断查询

1. 判断为空使用: is null
2. 判断非空使用: is not null

**例1：查询没有填写身高的学生:**

```sql
select * from students where height is null;
```

**注意:**

1. 不能使用 where height = null 判断为空
2. 不能使用 where height != null 判断非空
3. null 不等于 '' 空字符串

## 排序

------

### 1. 排序查询语法

排序查询语法：

```sql
select * from 表名 order by 列1 asc|desc [,列2 asc|desc,...]
```

**语法说明:**

1. 先按照列1进行排序，如果列1的值相同时，则按照 列2 排序，以此类推
2. asc从小到大排列，即升序
3. desc从大到小排序，即降序
4. 默认按照列值从小到大排列（即asc关键字）

**例1：查询未删除男生信息，按学号降序:**

```sql
select * from students where gender=1 and is_delete=0 order by id desc;
```

**例2：显示所有的学生信息，先按照年龄从大-->小排序，当年龄相同时 按照身高从高-->矮排序:**

```sql
select * from students  order by age desc,height desc;
```

## 分页查询

------

### 1. 分页查询的介绍

当我们在京东购物，浏览商品列表的时候，由于数据特别多，一页显示不完，一页一页的进行显示，这就是分页查询

### 2. 分页查询的语法

```sql
select * from 表名 limit start,count
```

**说明:**

1. limit是分页查询关键字
2. start表示开始行索引，默认是0
3. count表示查询条数

**例1：查询前3行男生信息:**

```sql
select * from students where gender=1 limit 0,3;
简写
select * from students where gender=1 limit 3;
```

### 3. 分页查询案例

已知每页显示m条数据，求第n页显示的数据

提示: 关键是求每页的开始行索引

**查询学生表，获取第n页数据的SQL语句:**

```sql
select * from students limit (n-1)*m,m
```

# MySQL数据库的条件查询

## 聚合函数

------

### 1. 聚合函数的介绍

聚合函数又叫组函数，通常是对表中的数据进行统计和计算，一般结合分组(group by)来使用，用于统计和计算分组数据。

**常用的聚合函数:**

1. count(col): 表示求指定列的总行数
2. max(col): 表示求指定列的最大值
3. min(col): 表示求指定列的最小值
4. sum(col): 表示求指定列的和
5. avg(col): 表示求指定列的平均值

### 2. 求总行数

```sql
-- 返回非NULL数据的总行数.
select count(height) from students; 
-- 返回总行数，包含null值记录;
select count(*) from students;
```

### 3. 求最大值

```sql
-- 查询女生的编号最大值
select max(id) from students where gender = 2;
```

### 4. 求最小值

```sql
-- 查询未删除的学生最小编号
select min(id) from students where is_delete = 0;
```

### 5. 求和

```sql
-- 查询男生的总身高
select sum(height) from students where gender = 1;
-- 平均身高
select sum(height) / count(*) from students where gender = 1;
```

### 6. 求平均值

```sql
-- 求男生的平均身高, 聚合函数不统计null值，平均身高有误
select avg(height) from students where gender = 1;
-- 求男生的平均身高, 包含身高是null的
select avg(ifnull(height,0)) from students where gender = 1;
```

**说明**

- ifnull函数: 表示判断指定字段的值是否为null，如果为空使用自己提供的值。

### 7. 聚合函数的特点

- 聚合函数默认忽略字段为null的记录 要想列值为null的记录也参与计算，必须使用ifnull函数对null值做替换。

## 分组查询

------

### 1. 分组查询介绍

分组查询就是将查询结果按照指定字段进行分组，字段中数据相等的分为一组。

**分组查询基本的语法格式如下：**

GROUP BY 列名 [HAVING 条件表达式] [WITH ROLLUP]

**说明:**

- 列名: 是指按照指定字段的值进行分组。
- HAVING 条件表达式: 用来过滤分组后的数据。
- WITH ROLLUP：在所有记录的最后加上一条记录，显示select查询时聚合函数的统计和计算结果

### 2. group by的使用

group by可用于单个字段分组，也可用于多个字段分组

```sql
-- 根据gender字段来分组
select gender from students group by gender;
-- 根据name和gender字段进行分组
select name, gender from students group by name, gender;
```

### 3. group by + group_concat()的使用

group_concat(字段名): 统计每个分组指定字段的信息集合，每个信息之间使用逗号进行分割

```sql
-- 根据gender字段进行分组， 查询gender字段和分组的name字段信息
select gender,group_concat(name) from students group by gender;
```

### 4. group by + 聚合函数的使用

```sql
-- 统计不同性别的人的平均年龄
select gender,avg(age) from students group by gender;
-- 统计不同性别的人的个数
select gender,count(*) from students group by gender;
```

### 5. group by + having的使用

having作用和where类似都是过滤数据的，但having是过滤分组数据的，只能用于group by

```sql
-- 根据gender字段进行分组，统计分组条数大于2的
select gender,count(*) from students group by gender having count(*)>2;
```

### 6. group by + with rollup的使用

with rollup的作用是：在最后记录后面新增一行，显示select查询时聚合函数的统计和计算结果

```sql
-- 根据gender字段进行分组，汇总总人数
select gender,count(*) from students group by gender with rollup;
-- 根据gender字段进行分组，汇总所有人的年龄
select gender,group_concat(age) from students group by gender with rollup;
```

## 连接查询-内连接

------

### 1. 连接查询的介绍

连接查询可以实现多个表的查询，当查询的字段数据来自不同的表就可以使用连接查询来完成。

连接查询可以分为:

1. 内连接查询
2. 左连接查询
3. 右连接查询
4. 自连接查询

### 2. 内连接查询

查询两个表中符合条件的共有记录

**内连接查询效果图:**

![内连接查询](imgs/内连接查询.png)

**内连接查询语法格式:**

```sql
select 字段 from 表1 inner join 表2 on 表1.字段1 = 表2.字段2
```

**说明:**

- inner join 就是内连接查询关键字
- on 就是连接查询条件

**例1：使用内连接查询学生表与班级表:**

```sql
select * from students as s inner join classes as c on s.cls_id = c.id;
```

## 连接查询-左连接

------

### 1. 左连接查询

以左表为主根据条件查询右表数据，如果根据条件查询右表数据不存在使用null值填充

**左连接查询效果图:**

![内连接查询](imgs/左连接查询.png)

**左连接查询语法格式:**

```sql
select 字段 from 表1 left join 表2 on 表1.字段1 = 表2.字段2
```

**说明:**

- left join 就是左连接查询关键字
- on 就是连接查询条件
- 表1 是左表
- 表2 是右表

**例1：使用左连接查询学生表与班级表:**

```sql
select * from students as s left join classes as c on s.cls_id = c.id;
```

## 连接查询-右连接

------

### 1. 右连接查询

以右表为主根据条件查询左表数据，如果根据条件查询左表数据不存在使用null值填充

**右连接查询效果图:**

![内连接查询](imgs/右连接查询.png)

**右连接查询语法格式:**

```sql
select 字段 from 表1 right join 表2 on 表1.字段1 = 表2.字段2
```

**说明:**

- right join 就是右连接查询关键字
- on 就是连接查询条件
- 表1 是左表
- 表2 是右表

**例1：使用右连接查询学生表与班级表:**

```sql
select * from students as s right join classes as c on s.cls_id = c.id;
```

## 连接查询-自连接

------

### 1. 自连接查询

左表和右表是同一个表，根据连接查询条件查询两个表中的数据。

**区域表效果图**

![区域表](imgs/区域表.png)

**例1：查询省的名称为“山西省”的所有城市**

![区域表](imgs/区域表连表查询分析.png)

**创建areas表:**

```sql
create table areas(
    id varchar(30) not null primary key, 
    title varchar(30), 
    pid varchar(30)
);
```

**执行sql文件给areas表导入数据:**

```sql
source areas.sql;
```

**说明:**

- source 表示执行的sql文件

**自连接查询的用法:**

```sql
select c.id, c.title, c.pid, p.title from areas as c inner join areas as p on c.pid = p.id where p.title = '山西省';
```

**说明:**

- 自连接查询必须对表起别名

## 子查询

------

### 1. 子查询的介绍

在一个 select 语句中,嵌入了另外一个 select 语句, 那么被嵌入的 select 语句称之为子查询语句，外部那个select语句则称为主查询.

**主查询和子查询的关系:**

1. 子查询是嵌入到主查询中
2. 子查询是辅助主查询的,要么充当条件,要么充当数据源
3. 子查询是可以独立存在的语句,是一条完整的 select 语句

### 2. 子查询的使用

**例1. 查询大于平均年龄的学生:**

```sql
select * from students where age > (select avg(age) from students);
```

**例2. 查询学生在班的所有班级名字:**

```sql
select name from classes where id in (select cls_id from students where cls_id is not null);
```

**例3. 查找年龄最大,身高最高的学生:**

```sql
select * from students where (age, height) =  (select max(age), max(height) from students);
```

## 数据库设计之三范式

------

### 1. 数据库设计之三范式的介绍

范式: 对设计数据库提出的一些规范，目前有迹可寻的共有8种范式，一般遵守3范式即可。

- 第一范式（1NF）: 强调的是列的原子性，即列不能够再分成其他几列。
- 第二范式（2NF）: 满足 1NF，另外包含两部分内容，一是表必须有一个主键；二是非主键字段 必须完全依赖于主键，而不能只依赖于主键的一部分。
- 第三范式（3NF）: 满足 2NF，另外非主键列必须直接依赖于主键，不能存在传递依赖。即不能存在：非主键列 A 依赖于非主键列 B，非主键列 B 依赖于主键的情况。

### 2. 第一范式的介绍

**说明:**

- 这种表结构设计就没有达到 1NF，要符合 1NF 我们只需把列拆分，即：把 contact 字段拆分成 name 、tel、addr 等字段。

### 3. 第二范式的介绍

**说明:**

- 这种表结构设计就没有达到 2NF，因为 Discount（折扣），Quantity（数量）完全依赖于主键（OrderID），而 UnitPrice单价，ProductName产品名称 只依赖于 ProductID, 所以 OrderDetail 表不符合 2NF。
- 我们可以把【OrderDetail】表拆分为【OrderDetail】（OrderID，ProductID，Discount，Quantity）和【Product】（ProductID，UnitPrice，ProductName）这样就符合第二范式了。

### 4. 第三范式的介绍

**说明:**

- 这种表结构设计就没有达到 3NF，因为 OrderDate，CustomerID，CustomerName，CustomerAddr，CustomerCity 等非主键列都完全依赖于主键（OrderID），所以符合 2NF。不过问题是 CustomerName，CustomerAddr，CustomerCity 直接依赖的是 CustomerID（非主键列），而不是直接依赖于主键，它是通过传递才依赖于主键，所以不符合 3NF。
- 我们可以把【Order】表拆分为【Order】（OrderID，OrderDate，CustomerID）和【Customer】（CustomerID，CustomerName，CustomerAddr，CustomerCity）从而达到 3NF。

### 5. E-R模型的介绍

E-R模型即实体-关系模型，E-R模型就是描述数据库存储数据的结构模型。

**E-R模型的使用场景:**

1. 对于大型公司开发项目，我们需要根据产品经理的设计，我们先使用建模工具, 如:power designer，db desinger等这些软件来画出实体-关系模型(E-R模型)
2. 然后根据三范式设计数据库表结构

**E-R模型的效果图:**

**说明:**

- 实体: 用矩形表示，并标注实体名称
- 属性: 用椭圆表示，并标注属性名称，
- 关系: 用菱形表示，并标注关系名称
  - 一对一
  - 一对多
  - 多对多

**一对一的关系:**

**说明:**

- 关系也是一种数据，需要通过一个字段存储在表中
- 1对1关系，在表A或表B中创建一个字段，存储另一个表的主键值

**一对多的关系:**

**说明:**

- 1对多关系，在多的一方表(学生表)中创建一个字段，存储班级表的主键值

**多对多的关系:**

**说明:**

- 多对多关系，新建一张表C，这个表只有两个字段，一个用于存储A的主键值，一个用于存储B的主键值

## 外键SQL语句的编写

------

### 1. 外键约束作用

外键约束:对外键字段的值进行更新和插入时会和引用表中字段的数据进行验证，数据如果不合法则更新和插入会失败，保证数据的有效性

### 2. 对于已经存在的字段添加外键约束

```sql
-- 为cls_id字段添加外键约束
alter table students add foreign key(cls_id) references classes(id);
```

### 3. 在创建数据表时设置外键约束

```sql
-- 创建学校表
create table school(
    id int not null primary key auto_increment, 
    name varchar(10)
);

-- 创建老师表
create table teacher(
    id int not null primary key auto_increment, 
    name varchar(10), 
    s_id int not null, 
    foreign key(s_id) references school(id)
);
```

### 4. 删除外键约束

```sql
-- 需要先获取外键约束名称,该名称系统会自动生成,可以通过查看表创建语句来获取名称
show create table teacher;

-- 获取名称之后就可以根据名称来删除外键约束
alter table teacher drop foreign key 外键名;
```

## 演练-分组和聚合函数的组合使用

------

### 1. 数据准备

```sql
-- 创建 "京东" 数据库
create database jing_dong charset=utf8;

-- 使用 "京东" 数据库
use jing_dong;

-- 创建一个商品goods数据表
create table goods(
    id int unsigned primary key auto_increment not null,
    name varchar(150) not null,
    cate_name varchar(40) not null,
    brand_name varchar(40) not null,
    price decimal(10,3) not null default 0,
    is_show bit not null default 1,
    is_saleoff bit not null default 0
);

-- 向goods表中插入数据

insert into goods values(0,'r510vc 15.6英寸笔记本','笔记本','华硕','3399',default,default); 
insert into goods values(0,'y400n 14.0英寸笔记本电脑','笔记本','联想','4999',default,default);
insert into goods values(0,'g150th 15.6英寸游戏本','游戏本','雷神','8499',default,default); 
insert into goods values(0,'x550cc 15.6英寸笔记本','笔记本','华硕','2799',default,default); 
insert into goods values(0,'x240 超极本','超级本','联想','4880',default,default); 
insert into goods values(0,'u330p 13.3英寸超极本','超级本','联想','4299',default,default); 
insert into goods values(0,'svp13226scb 触控超极本','超级本','索尼','7999',default,default); 
insert into goods values(0,'ipad mini 7.9英寸平板电脑','平板电脑','苹果','1998',default,default);
insert into goods values(0,'ipad air 9.7英寸平板电脑','平板电脑','苹果','3388',default,default); 
insert into goods values(0,'ipad mini 配备 retina 显示屏','平板电脑','苹果','2788',default,default); 
insert into goods values(0,'ideacentre c340 20英寸一体电脑 ','台式机','联想','3499',default,default); 
insert into goods values(0,'vostro 3800-r1206 台式电脑','台式机','戴尔','2899',default,default); 
insert into goods values(0,'imac me086ch/a 21.5英寸一体电脑','台式机','苹果','9188',default,default); 
insert into goods values(0,'at7-7414lp 台式电脑 linux ）','台式机','宏碁','3699',default,default); 
insert into goods values(0,'z220sff f4f06pa工作站','服务器/工作站','惠普','4288',default,default); 
insert into goods values(0,'poweredge ii服务器','服务器/工作站','戴尔','5388',default,default); 
insert into goods values(0,'mac pro专业级台式电脑','服务器/工作站','苹果','28888',default,default); 
insert into goods values(0,'hmz-t3w 头戴显示设备','笔记本配件','索尼','6999',default,default); 
insert into goods values(0,'商务双肩背包','笔记本配件','索尼','99',default,default); 
insert into goods values(0,'x3250 m4机架式服务器','服务器/工作站','ibm','6888',default,default); 
insert into goods values(0,'商务双肩背包','笔记本配件','索尼','99',default,default);
```

**表结构说明:**

- id 表示主键 自增
- name 表示商品名称
- cate_name 表示分类名称
- brand_name 表示品牌名称
- price 表示价格
- is_show 表示是否显示
- is_saleoff 表示是否售完

### 2. SQL语句演练

1. 查询类型cate_name为 '超极本' 的商品名称、价格

   ```sql
    select name,price from goods where cate_name = '超级本';
   ```

2. 显示商品的分类

   ```sql
    select cate_name from goods group by cate_name;
   ```

3. 求所有电脑产品的平均价格,并且保留两位小数

   ```sql
    select round(avg(price),2) as avg_price from goods;
   ```

4. 显示每种商品的平均价格

   ```sql
    select cate_name,avg(price) from goods group by cate_name;
   ```

5. 查询每种类型的商品中 最贵、最便宜、平均价、数量

   ```sql
    select cate_name,max(price),min(price),avg(price),count(*) 
    from goods group by cate_name;
   ```

6. 查询所有价格大于平均价格的商品，并且按价格降序排序

   ```sql
    select id,name,price from goods 
    where price > (select round(avg(price),2) as avg_price from goods) 
    order by price desc;
   ```

# MySQL数据库的高级使用

## 将查询结果插入到其它表中

------

### 1. 思考

目前只有一个goods表，我们想要增加一个商品分类信息，比如：移动设备这个分类信息，只通过goods表无法完成商品分类的添加，那么如何实现添加商品分类信息的操作?

**答案:**

1. 创建一个商品分类表，把goods表中的商品分类信息添加到该表中。
2. 将goods表中的分类名称更改成商品分类表中对应的分类id

### 2. 创建商品分类表

```sql
-- 创建商品分类表
create table good_cates(
    id int not null primary key auto_increment, 
    name varchar(50) not null
);
```

### 3. 把goods表中的商品分类添加到商品分类表

```sql
-- 查询goods表中商品的分类信息
select cate_name from goods group by cate_name;

-- 将查询结果插入到good_cates表中
insert into good_cates(name) select cate_name from goods group by cate_name;

-- 添加移动设备分类信息
insert into good_cates(name) values('移动设备');
```

**说明:**

- insert into .. select .. 表示: 把查询结果插入到指定表中，也就是表复制。

## 使用连接更新表中某个字段数据

------

### 1. 更新goods表中的商品分类信息

上一节课我们已经创建了一个商品分类表(good_cates)，并完成了商品分类信息的插入，现在需要更新goods表中的商品分类信息，把商品分类名称改成商量分类id。

接下来我们实现第二步操作:

- **将goods表中的分类名称更改成商品分类表中对应的分类id**

```sql
-- 查看goods表中的商品分类名称对应的商品分类id
select * from goods inner join good_cates on goods.cate_name = good_cates.name;

-- 把该语句中from 后的语句理解为一张虚表  
update goods g inner join good_cates gc on g.cate_name=gc.name set g.cate_name=gc.id;
```

## 创建表并给某个字段添加数据

------

### 1. 思考

上一节课我们完成了商品分类表(good_cates)的创建和商品分类信息的添加以及把商品表(goods)中的商品分类名称改成了对应的商品分类id，假如我们想要添加一个品牌，比如：双飞燕这个品牌信息，只通过goods表无法完成品牌信息的添加，那么如何实现添加品牌信息的操作?

**答案:**

1. 创建一个品牌表，把goods表中的品牌信息添加到该表中。
2. 将goods表中的品牌名称更改成品牌表中对应的品牌id

### 2. 创建品牌表

```sql
-- 查询品牌信息 
select brand_name from goods group by brand_name;

-- 通过create table ...select来创建数据表并且同时插入数据
-- 创建商品分类表，注意: 需要对brand_name 用as起别名，否则name字段就没有值
create table good_brands (     
id int unsigned primary key auto_increment,     
name varchar(40) not null) select brand_name as name from goods group by brand_name;
```

**说明:**

- create table .. select 列名 .. 表示创建表并插入数据

### 3. 更新goods表中的品牌信息

```sql
-- 将goods表中的品牌名称更改成品牌表中对应的品牌id
update goods as g inner join good_brands gb on g.brand_name = gb.name set g.brand_name = gb.id;
```

## 修改goods表结构

------

### 修改goods表结构

目前我们已经把good表中的商品分类和品牌信息已经更改成了商品分类id和品牌id，接下来需要把 cate_name 和 brand_name 字段分别改成 cate_id和 brand_id 字段，类型都改成int类型

```sql
-- 查看表结构
desc goods;
-- 通过alter table语句修改表结构
alter table goods change cate_name cate_id int not null, change brand_name brand_id int not null;
```

**说明:**

- alert table 可以同时修改多个字段信息

## PyMySQL的使用

------

### 1. 思考

如何实现将100000条数据插入到MySQL数据库?

**答案:**

如果使用之前学习的MySQL客户端来完成这个操作，那么这个工作量无疑是巨大的，我们可以通过使用程序代码的方式去连接MySQL数据库，然后对MySQL数据库进行增删改查的方式，实现10000条数据的插入，像这样使用代码的方式操作数据库就称为数据库编程。

### 2. Python程序操作MySQL数据库

**安装pymysql第三方包:**

```
sudo pip3 install pymysql
```

**说明:**

- 安装命令使用 sudo pip3 install 第三方包名
- 卸载命令使用 sudo pip3 uninstall 第三方包
- 大家现在使用的虚拟机已经安装了这个第三方包，可以使用： **pip3 show pymysql** 命令查看第三方包的信息
- **pip3 list** 查看使用pip命令安装的第三方包列表

**pymysql的使用:**

1. 导入 pymysql 包

   ```py
    import pymysql
   ```

2. 创建连接对象

   调用pymysql模块中的connect()函数来创建连接对象,代码如下:

   ```py
    conn=connect(参数列表)
   
    * 参数host：连接的mysql主机，如果本机是'localhost'
    * 参数port：连接的mysql主机的端口，默认是3306
    * 参数user：连接的用户名
    * 参数password：连接的密码
    * 参数database：数据库的名称
    * 参数charset：通信采用的编码方式，推荐使用utf8
   ```

   **连接对象操作说明:**

   - 关闭连接 conn.close()
   - 提交数据 conn.commit()
   - 撤销数据 conn.rollback()

3. 获取游标对象

   获取游标对象的目标就是要执行sql语句，完成对数据库的增、删、改、查操作。代码如下:

   ```py
    # 调用连接对象的cursor()方法获取游标对象   
    cur =conn.cursor()
   ```

   **游标操作说明:**

   - 使用游标执行SQL语句: execute(operation [parameters ]) 执行SQL语句，返回受影响的行数，主要用于执行insert、update、delete、select等语句
   - 获取查询结果集中的一条数据:cur.fetchone()返回一个元组, 如 (1,'张三')
   - 获取查询结果集中的所有数据: cur.fetchall()返回一个元组,如((1,'张三'),(2,'李四'))
   - 关闭游标: cur.close(),表示和数据库操作完成

4. pymysql完成数据的查询操作

   ```py
   import pymysql
   
   # 创建连接对象
   conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql',database='python', charset='utf8')
   
   # 获取游标对象
   cursor = conn.cursor()
   
   # 查询 SQL 语句
   sql = "select * from students;"
   # 执行 SQL 语句 返回值就是 SQL 语句在执行过程中影响的行数
   row_count = cursor.execute(sql)
   print("SQL 语句执行影响的行数%d" % row_count)
   
   # 取出结果集中一行数据,　例如:(1, '张三')
   # print(cursor.fetchone())
   
   # 取出结果集中的所有数据, 例如:((1, '张三'), (2, '李四'), (3, '王五'))
   for line in cursor.fetchall():
       print(line)
   
   # 关闭游标
   cursor.close()
   
   # 关闭连接
   conn.close()
   ```

5. pymysql完成对数据的增删改

   ```py
   import pymysql
   
   # 创建连接对象
   conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql',database='python', charset='utf8')
   
   # 获取游标对象
   cursor = conn.cursor()
   
   try:
       # 添加 SQL 语句
       # sql = "insert into students(name) values('刘璐'), ('王美丽');"
       # 删除 SQ L语句
       # sql = "delete from students where id = 5;"
       # 修改 SQL 语句
       sql = "update students set name = '王铁蛋' where id = 6;"
       # 执行 SQL 语句
       row_count = cursor.execute(sql)
       print("SQL 语句执行影响的行数%d" % row_count)
       # 提交数据到数据库
       conn.commit()
   except Exception as e:
       # 回滚数据， 即撤销刚刚的SQL语句操作
       conn.rollback()
   
   # 关闭游标
   cursor.close()
   
   # 关闭连接
   conn.close()
   ```

   **说明:**

   - conn.commit() 表示将修改操作提交到数据库
   - conn.rollback() 表示回滚数据

6. 防止SQL注入

   什么是SQL注入?

   用户提交带有恶意的数据与SQL语句进行字符串方式的拼接，从而影响了SQL语句的语义，最终产生数据泄露的现象。

   如何防止SQL注入?

   SQL语句参数化

   - SQL语言中的参数使用%s来占位，此处不是python中的字符串格式化操作
   - 将SQL语句中%s占位所需要的参数存在一个列表中，把参数列表传递给execute方法中第二个参数

   **防止SQL注入的示例代码:**

   ```py
   from pymysql import connect
   
   def main():
   
       find_name = input("请输入物品名称：")
   
       # 创建Connection连接
       conn = connect(host='localhost',port=3306,user='root',password='mysql',database='jing_dong',charset='utf8')
       # 获得Cursor对象
       cs1 = conn.cursor()
   
       # 非安全的方式
       # 输入 ' or 1 = 1 or '   (单引号也要输入)
       # sql = "select * from goods where name='%s'" % find_name
       # print("""sql===>%s<====""" % sql)
       # # 执行select语句，并返回受影响的行数：查询所有数据
       # count = cs1.execute(sql)
   
       # 安全的方式
       # 构造参数列表
       params = [find_name]
       # 执行select语句，并返回受影响的行数：查询所有数据
       count = cs1.execute("select * from goods where name=%s", params)
       # 注意：
       # 如果要是有多个参数，需要进行参数化
       # 那么params = [数值1, 数值2....]，此时sql语句中有多个%s即可
       # %s 不需要带引号
   
       # 打印受影响的行数
       print(count)
       # 获取查询的结果
       # result = cs1.fetchone()
       result = cs1.fetchall()
       # 打印查询的结果
       print(result)
       # 关闭Cursor对象
       cs1.close()
       # 关闭Connection对象
       conn.close()
   
   if __name__ == '__main__':
       main()
   ```

   **说明:**

   - execute方法中的 %s 占位不需要带引号

## 事务

------

### 1. 事务的介绍

事务就是用户定义的一系列执行SQL语句的操作, 这些操作要么完全地执行，要么完全地都不执行， 它是一个不可分割的工作执行单元。

**事务的使用场景:**

在日常生活中，有时我们需要进行银行转账，这个银行转账操作背后就是需要执行多个SQL语句，假如这些SQL执行到一半突然停电了，那么就会导致这个功能只完成了一半，这种情况是不允许出现，要想解决这个问题就需要通过事务来完成。

### 2. 事务的四大特性

- 原子性(Atomicity)
- 一致性(Consistency)
- 隔离性(Isolation)
- 持久性(Durability)

**原子性:**

一个事务必须被视为一个不可分割的最小工作单元，整个事务中的所有操作要么全部提交成功，要么全部失败回滚，对于一个事务来说，不可能只执行其中的一部分操作，这就是事务的原子性

**一致性:**

数据库总是从一个一致性的状态转换到另一个一致性的状态。（在前面的例子中，一致性确保了，即使在转账过程中系统崩溃，支票账户中也不会损失200美元，因为事务最终没有提交，所以事务中所做的修改也不会保存到数据库中。）

**隔离性:**

通常来说，一个事务所做的修改操作在提交事务之前，对于其他事务来说是不可见的。（在前面的例子中，当执行完第三条语句、第四条语句还未开始时，此时有另外的一个账户汇总程序开始运行，则其看到支票帐户的余额并没有被减去200美元。）

**持久性:**

一旦事务提交，则其所做的修改会永久保存到数据库。

**说明:**

事务能够保证数据的完整性和一致性，让用户的操作更加安全。

### 3. 事务的使用

在使用事务之前，先要确保表的存储引擎是 InnoDB 类型, 只有这个类型才可以使用事务，MySQL数据库中表的存储引擎默认是 InnoDB 类型。

**表的存储引擎说明:**

表的存储引擎就是提供存储数据一种机制，不同表的存储引擎提供不同的存储机制。

**说明:**

- 不同的汽车引擎，提供的汽车动力也是不同的。

**查看MySQL数据库支持的表的存储引擎:**

```sql
-- 查看MySQL数据库支持的表的存储引擎
show engines;
```

**说明:**

- 常用的表的存储引擎是 InnoDB 和 MyISAM
- InnoDB 是支持事务的
- MyISAM 不支持事务，优势是访问速度快，对事务没有要求或者以select、insert为主的都可以使用该存储引擎来创建表

**查看goods表的创表语句:**

```sql
-- 选择数据库
use jing_dong;
-- 查看goods表
show create table goods;

mysql root@(none):jing_dong> show create table goods;
+-------+--------------------------------------------------------+
| Table | Create Table                                           |
+-------+--------------------------------------------------------+
| goods | CREATE TABLE `goods` (                                 |
|       |   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,       |
|       |   `name` varchar(150) NOT NULL,                        |
|       |   `cate_id` int(10) unsigned NOT NULL,                 |
|       |   `brand_id` int(10) unsigned NOT NULL,                |
|       |   `price` decimal(10,3) NOT NULL DEFAULT '0.000',      |
|       |   `is_show` bit(1) NOT NULL DEFAULT b'1',              |
|       |   `is_saleoff` bit(1) NOT NULL DEFAULT b'0',           |
|       |   PRIMARY KEY (`id`)                                   |
|       | ) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 |
+-------+--------------------------------------------------------+
```

**说明:**

- 通过创表语句可以得知，goods表的存储引擎是InnoDB。
- 修改表的存储引擎使用: alter table 表名 engine = 引擎类型;
  - 比如: alter table students engine = 'MyISAM';

**开启事务:**

```sql
begin;
或者
start transaction;
```

**说明:**

- **开启事务后执行修改命令，变更数据会保存到MySQL服务端的缓存文件中，而不维护到物理表中**

- **MySQL数据库默认采用自动提交(autocommit)模式，如果没有显示的开启一个事务,那么每条sql语句都会被当作一个事务执行提交的操作**

- 当设置autocommit=0就是取消了自动提交事务模式，直到显示的执行commit和rollback表示该事务结束。

  - set autocommit = 0 表示取消自动提交事务模式，需要手动执行commit完成事务的提交

  ```sql
  set autocommit = 0;
  insert into students(name) values('刘三峰');
  -- 需要执行手动提交，数据才会真正添加到表中, 验证的话需要重新打开一个连接窗口查看表的数据信息，因为是临时关闭自动提交模式
  commit
  
  -- 重新打开一个终端窗口，连接MySQL数据库服务端
  mysql -uroot -p
  
  -- 然后查询数据,如果上个窗口执行了commit，这个窗口才能看到数据
  select * from students;
  ```

  **提交事务:**

  将本地缓存文件中的数据提交到物理表中，完成数据的更新。

  ```sql
  commit;
  ```

  **回滚事务:**

  放弃本地缓存文件中的缓存数据, 表示回到开始事务前的状态

  ```
  rollback;
  ```

  **事务演练的SQL语句:**

  ```sql
  begin;
  insert into students(name) values('李白');
  -- 查询数据，此时有新增的数据, 注意: 如果这里后续没有执行提交事务操作，那么数据是没有真正的更新到物理表中
  select * from students;
  -- 只有这里提交事务，才把数据真正插入到物理表中
  commit;
  
  -- 新打开一个终端，重新连接MySQL数据库，查询students表,这时没有显示新增的数据，说明之前的事务没有提交，这就是事务的隔离性
  -- 一个事务所做的修改操作在提交事务之前，对于其他事务来说是不可见的
  select * from students;
  ```

## 索引

------

### 1. 索引的介绍

索引在MySQL中也叫做“键”，它是一个特殊的文件，它保存着数据表里所有记录的位置信息，更通俗的来说，数据库索引好比是一本书前面的目录，能加快数据库的查询速度。

**应用场景:**

当数据库中数据量很大时，查找数据会变得很慢，我们就可以通过索引来提高数据库的查询效率。

### 2. 索引的使用

**查看表中已有索引:**

```sql
show index from 表名;
```

**说明:**

- 主键列会自动创建索引

**索引的创建:**

```sql
-- 创建索引的语法格式
-- alter table 表名 add index 索引名[可选](列名, ..)
-- 给name字段添加索引
alter table classes add index my_name (name);
```

**说明:**

- 索引名不指定，默认使用字段名

**索引的删除:**

```sql
-- 删除索引的语法格式
-- alter table 表名 drop index 索引名
-- 如果不知道索引名，可以查看创表sql语句
show create table classes;
alter table classes drop index my_name;
```

### 3. 案例-验证索引查询性能

**创建测试表testindex:**

```sql
create table test_index(title varchar(10));
```

**向表中插入十万条数据:**

```py
from pymysql import connect

def main():
    # 创建Connection连接
    conn = connect(host='localhost',port=3306,database='python',user='root',password='mysql',charset='utf8')
    # 获得Cursor对象
    cursor = conn.cursor()
    # 插入10万次数据
    for i in range(100000):
        cursor.execute("insert into test_index values('ha-%d')" % i)
    # 提交数据
    conn.commit()

if __name__ == "__main__":
    main()
```

**验证索引性能操作：**

```sql
-- 开启运行时间监测：
set profiling=1;
-- 查找第1万条数据ha-99999
select * from test_index where title='ha-99999';
-- 查看执行的时间：
show profiles;
-- 给title字段创建索引：
alter table test_index add index (title);
-- 再次执行查询语句
select * from test_index where title='ha-99999';
-- 再次查看执行的时间
show profiles;
```

### 4. 联合索引

联合索引又叫复合索引，即一个索引覆盖表中两个或者多个字段，一般用在多个字段一起查询的时候。

```sql
-- 创建teacher表
create table teacher
(
    id int not null primary key auto_increment,
    name varchar(10),
    age int
);

-- 创建联合索引
alter table teacher add index (name,age);
```

**联合索引的好处:**

- 减少磁盘空间开销，因为每创建一个索引，其实就是创建了一个索引文件，那么会增加磁盘空间的开销。

### 5. 联合索引的最左原则

在使用联合索引的时候，我们要遵守一个最左原则,即index(name,age)支持 name 、name 和 age 组合查询,而不支持单独 age 查询，因为没有用到创建的联合索引。

**最左原则示例:**

```sql
-- 下面的查询使用到了联合索引
select * from stu where name='张三' -- 这里使用了联合索引的name部分
select * from stu where name='李四' and age=10 -- 这里完整的使用联合索引，包括 name 和 age 部分 
-- 下面的查询没有使用到联合索引
select * from stu where age=10 -- 因为联合索引里面没有这个组合，只有 name | name age 这两种组合
```

**说明:**

- 在使用联合索引的查询数据时候一定要保证联合索引的最左侧字段出现在查询条件里面，否则联合索引失效

### 6. MySQL中索引的优点和缺点和使用原则

- 优点：
  1. 加快数据的查询速度
- 缺点：
  1. 创建索引会耗费时间和占用磁盘空间，并且随着数据量的增加所耗费的时间也会增加
- 使用原则：
  1. 通过优缺点对比，不是索引越多越好，而是需要自己合理的使用。
  2. 对经常更新的表就避免对其进行过多索引的创建，对经常用于查询的字段应该创建索引，
  3. 数据量小的表最好不要使用索引，因为由于数据较少，可能查询全部数据花费的时间比遍历索引的时间还要短，索引就可能不会产生优化效果。
  4. 在一字段上相同值比较多不要建立索引，比如在学生表的"性别"字段上只有男，女两个不同值。相反的，在一个字段上不同值较多可是建立索引。