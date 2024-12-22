# Git单人本地仓库操作

- 课程目标：学习常用的Git终端命令
- 提示：本地仓库是个`.git`隐藏文件

> 以下为演示Git单人本地仓库操作

- **1.安装git**

  ```
    sudo apt-get install git
    密码：chuanzhi
  ```

  ![安装Git](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\安装Git.png)

- **2.查看git安装结果**

  ```
    git
  ```

- **3.创建项目**

  - 在桌面创建`test`文件夹，表示是工作项目

    ```
      Desktop/test/
    ```

**4.创建本地仓库**

1. 进入到`test`，并创建本地仓库`.git`

2. 新创建的本地仓库`.git`是个空仓库

   ```
     cd Desktop/test/
     git init
   ```

3. 创建本地仓库`.git`后

> 进入该待显示的文件路径，ctrl + h ，则显示隐藏文件

**5.配置个人信息**

```
  git config user.name '张三'
  git config user.email 'zhangsan@163.com'
```

- 配置个人信息后

  ![配置个人信息后](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\配置个人信息后.png)

> 默认不配置的话，会使用全局配置里面的用户名和邮箱
> 全局git配置文件路径：~/.gitconfig

- **6.新建py文件**

  - 在项目文件`test`里面创建`login.py`文件，用于版本控制演示

    ```
    将代码文件放入项目文件`test`里
    ```

- **7.查看文件状态**

  - 红色表示新建文件或者新修改的文件,都在工作区.

  - 绿色表示文件在暂存区

  - 新建的`login.py`文件在工作区，需要添加到暂存区并提交到仓库区

    ```
    git status
    ```

    ![配置个人信息后](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\配置个人信息后.png)

- **8.将工作区文件添加到暂存区**

  ```
    # 添加项目中所有文件
    git add .
    或者
    # 添加指定文件
    git add login.py
  ```

  ![添加到暂存区](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\添加到暂存区.png)

- **9.将暂存区文件提交到仓库区**

  - `commit`会生成一条版本记录

  - `-m`后面是版本描述信息

    ```
    git commit -m '版本描述'
    ```

    ![提交到仓库区](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\提交到仓库区.png)

- **10.接下来就可以在**`login.py`**文件中编辑代码**

  - 代码编辑完成后即可进行`add`和`commit`操作

  - 提示：添加和提交合并命令

    ```
      git commit -am "版本描述"
    ```

  - 提交两次代码，会有两个版本记录

- **11.查看历史版本**

  ```
    git log
    或者
    git reflog
  ```

  ![查看历史记录log](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\查看历史记录log.png)

> git reflog 可以查看所有分支的所有操作记录（包括commit和reset的操作），包括已经被删除的commit记录，git log 则不能察看已经删除了的commit记录

- **12.回退版本**

  - **方案一：**

    - `HEAD`表示当前最新版本

    - `HEAD^`表示当前最新版本的前一个版本

    - `HEAD^^`表示当前最新版本的前两个版本，**以此类推...**

    - `HEAD~1`表示当前最新版本的前一个版本

    - `HEAD~10`表示当前最新版本的前10个版本，**以此类推...**

      ```
      git reset --hard HEAD^
      ```

  - **方案二：当版本非常多时可选择的方案**

    - 通过每个版本的版本号回退到指定版本

      ```
        git reset --hard 版本号
      ```

      ![回退版本版本号](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\回退版本版本号.png)

- **13.撤销修改**

  - 只能撤销工作区、暂存区的代码,不能撤销仓库区的代码

  - 撤销仓库区的代码就相当于回退版本操作

    - 撤销工作区代码

      - 新加代码`num3 = 30`，不`add`到暂存区，保留在工作区

        ```
        git checkout 文件名
        ```

    - 撤销暂存区代码

      - 新加代码`num3 = 30`，并`add`到暂存区

        ```
        # 第一步：将暂存区代码撤销到工作区
        git reset HEAD  文件名
        # 第二步：撤销工作区代码
        git checkout 文件名
        ```

        ![撤销暂存区代码](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\撤销暂存区代码.png)

# Git远程仓库Github

## 创建远程仓库

> 以下操作为演示在Github网站上创建远程仓库

- 1.登陆注册Github

- 2.创建仓库入口

  ```
  登录github创建： https://github.com/
  ```

- 3.编辑仓库信息

  ![远程02](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\远程02.png)

- 4.仓库创建完成

- 5.查看仓库地址

  ![远程04](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\远程04.png)

- - 远程仓库地址 https://github.com/qruihua/info.git

## 配置SSH

选择SSH操作

![选择SSH](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\选择SSH.png)

- 如果某台电脑需要与`Github`上的仓库交互，那么就要把这台电脑的SSH公钥添加到这个`Github`账户上

- 1.配置SSH公钥入口

  ![SSH配置入口01](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\SSH配置入口01.png)

  ![SSH配置入口02](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\SSH配置入口02.png)

- 2.生成SSH公钥

  ```
    ssh-keygen -t rsa -C "qiruihua@itcast.cn"
  ```

  ![SSH生成公钥](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\SSH生成公钥.png)

- 3.配置SSH公钥

  ![ssh01](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\ssh01.png)

  ![ssh02](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\ssh02.png)

- 补充：删除旧的秘钥

  - 删除`~/.ssh`目录，这里存储了旧的密钥
    rm -r .ssh

> SSH操作报错

![ssh下载问题](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\ssh下载问题.png)

> **解决方案为**
>
> eval "$(ssh-agent -s)"
>
> ssh-add

![ssh下载解决](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\ssh下载解决.png)

## 克隆项目

- 准备经理的文件 `Desktop/manager/`
- 准备张三的文件 `Desktop/zhangsan/`

经理的工作

- 立项：克隆远程仓库+配置身份信息+创建项目+推送项目到远程仓库

- 1.克隆远程仓库的命令

  ```
    cd Desktop/manager/
    git clone https://github.com/qruihua/info.git
  ```

- 2.克隆远程仓库到本地

  ```
  git clone https://github.com/qruihua/info.git
  ```

- 3.克隆成功后查看经理的文件

- 4.配置经理身份信息

  ```
    cd Desktop/manager/info/
    git config user.name '经理'
    git config user.email 'manager@itcast.com'
  ```

- 5.创建项目

  ```
  创建test项目文件，内部存放.py文件
  ```

- 6.推送项目到远程仓库

  ```
    # 工作区添加到暂存区
    git add .
    # 暂存区提交到仓库区
    git commit -m '立项'
    # 推送到远程仓库
    git push
  ```

- 在 push 的时候需要设置账号与密码，该密码则是 github 的账号与密码

  - 如果在每次 push 都需要设置账号与密码，那么可以设置记住密码

    ```
    设置记住密码（默认15分钟）：
    git config --global credential.helper cache
    如果想自己设置时间，可以这样做(1小时后失效)：
    git config credential.helper 'cache --timeout=3600'
    长期存储密码：
    git config --global credential.helper store
    ```

    > 在以后的项目开发过程中，Pycharm 可以自动记住密码

张三的工作

- 获取项目：克隆项目到本地、配置身份信息

- 1.克隆项目到本地

  ```
    cd Desktop/zhangsan/
    git clone https://github.com/qruihua/info.git
  ```

- 2.克隆成功后查看张三的文件

- 3.配置张三身份信息

  ```
    cd Desktop/zhangsan/info/
    git config user.name '张三'
    git config user.email 'zhangsan@itcast.com'
  ```

> 张三身份信息配置成功后即可跟经理协同开发同一个项目

## 多人协同开发

- 1.代码编辑界面介绍：此处使用`gedit`做演示

  - 代码编辑界面左边为模拟经理的操作

  - 代码编辑界面右边为模拟张三的操作

    ![github代码编辑界面介绍](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github代码编辑界面介绍.png)

- 2.模拟张三先编辑`login.py`文件代码

  - 进入张三本地仓库：`cd Desktop/zhangsan/info`
  - 编辑代码：`num1 = 10`
  - 本地仓库记录版本：`git commit -am '第一个变量'`
  - 推送到远程仓库：`git push`

- 3.模拟经理后编辑`login.py`文件代码

  - 进入经理本地仓库：`cd Desktop/manager/info/`
  - 经理同步服务器代码：`git pull`
  - 编辑代码：`num2 = 20`
  - 本地仓库记录版本：`git commit -am '第二个变量'`
  - 推送到远程仓库：`git push`

- 4.模拟张三同步服务器代码

  - 本次可以把`num2`同步到张三的本地仓库

    ![github张三同步num2](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github张三同步num2.png)

- 5.按照以上`2-3-4`步骤循环操作，即可实现基本的协同开发

- 6.总结：

  - 要使用git命令操作仓库，需要进入到仓库内部
  - 要同步服务器代码就执行：`git pull`
  - 本地仓库记录版本就执行：`git commit -am '版本描述'`
  - 推送代码到服务器就执行：`git push`  (强制推送： git push origin --force --all)
  - 编辑代码前要先`pull`，编辑完再`commit`，最后推送是`push`

## 代码冲突

- **提示**：多人协同开发时，避免不了会出现代码冲突的情况
- **原因**：多人同时修改了同一个文件
- **危害**：会影响正常的开发进度
- **注意**：一旦出现代码冲突，必须先解决再做后续开发

代码冲突演练

- 1.张三先编辑`login.py`文件代码

  - 进入张三本地仓库：`cd Desktop/zhangsan/info`

  - 拉取服务器最新代码：`git pull`

  - 编辑代码：`num3 = 30`

  - 本地仓库记录版本：`git commit -am '第三个变量'`

  - 推送到服务器仓库：`git push`

  - 张三本地仓库和远程仓库代码如下：

    ![github查看张三本地仓库num3](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github查看张三本地仓库num3.png)

    ![github查看远程仓库num3](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github查看远程仓库num3.png)

- 2.经理后编辑`login.py`文件代码

  - 进入经理本地仓库：`cd Desktop/manager/info/`

  - 编辑代码：`num3 = 300`

  - 本地仓库记录版本：`git commit -am '第三个变量'`

  - 推送到服务器仓库：`git push`

  - **以上操作会出现代码冲突**

    - 提示需要先pull

      ![github冲突提示需要先pull](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github冲突提示需要先pull.png)

    - 提示冲突文件

      ![github冲突提示冲突文件](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github冲突提示冲突文件.png)

    - 冲突代码表现

      ![github冲突代码表现](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github冲突代码表现.png)

- 3.解决冲突

  - 原则：谁冲突谁解决，并且一定要协商解决
  - 方案：保留所有代码 或者 保留某一人代码
  - 解决完冲突代码后，依然需要`add`、`commit`、`push`
  - 提示：如果张三执行`pull`没有影响，就算真正解决了冲突代码

补充：

- **容易冲突的操作方式**
  - 多个人同时操作了同一个文件
  - 一个人一直写不提交
  - 修改之前不更新最新代码
  - 提交之前不更新最新代码
  - 擅自修改同事代码
- **减少冲突的操作方式**
  - 养成良好的操作习惯,先`pull`在修改,修改完立即`commit`和`push`
  - 一定要确保自己正在修改的文件是最新版本的
  - 各自开发各自的模块
  - 如果要修改公共文件,一定要先确认有没有人正在修改
  - 下班前一定要提交代码,上班第一件事拉取最新代码
  - 一定不要擅自修改同事的代码

## 标签

- 当某一个大版本完成之后,需要打一个标签
- 作用：
  - 记录大版本
  - 备份大版本代码

模拟经理打标签

- 1.进入到经理的本地仓库info

  ```
   cd Desktop/manager/info/
  ```

- 2.经理在本地打标签

  ```
   git tag -a 标签名 -m '标签描述'
   例：
   git tag -a v1.0 -m 'version 1.0'
  ```

- 3.经理推送标签到远程仓库

  ```
   git push origin 标签名
   例：
   git push origin v1.0
  ```

- 4.查看打标签结果

  ![github查看打标签结果](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github查看打标签结果.png)

- 补充：删除本地和远程标签

  ```
    # 删除本地标签
    git tag -d 标签名
    # 删除远程仓库标签
    git push origin --delete tag 标签名
  ```

## 分支

- 作用：
  - 区分生产环境代码以及开发环境代码
  - 研究新的功能或者攻关难题
  - 解决线上bug
- 特点：
  - 项目开发中公用分支包括master、dev
  - 分支master是默认分支，用于发布，当需要发布时将dev分支合并到master分支
  - 分支dev是用于开发的分支，开发完阶段性的代码后，需要合并到master分支

模拟经理分支操作

- 对比：操作分支前的代码

- 1.进入到经理的本地仓库info

  ```
   cd Desktop/manager/info/
  ```

- 2.查看当前分支

  ```
    git branch
  ```

  - 没有创建其他分支时，只有`master`分支

- 3.经理创建并切换到dev分支

  ```
   git checkout -b dev
  ```

- 4.设置本地分支跟踪远程指定分支（将分支推送到远程）

  ```
    git push -u origin dev
  ```

- 5.经理在dev分支编辑代码

- 6.管理dev分支源代码：`add`、`commit`、`push

  ![github经理dev编辑代码num4后推送](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github经理dev编辑代码num4后推送.png)

- 7.dev分支合并到master分支

  - 提示：只有当dev分支合并到master分支成功，张三才能获取到`num4`

  - 7.1 先切换到master分支

    ```
      git checkout master
    ```

  - 7.2 dev分支合并到master分支

    ```
      git merge dev
    ```

  - 7.3 经理推送合并分支操作到远程仓库

    - 合并分支默认在本地完成，合并后直接推送即可

      ```
      git push
      ```

- 8.张三同步经理合并后的`num4`

  - 只有当张三同步代码成功，分支合并才算成功

    ```
      cd Desktop/zhangsan/info/
      git pull
    ```

    ![github张三同步分支合并后git操作](D:\typora_synchronous\BaiduSyncdisk\同步文件\python笔记\Image\github张三同步分支合并后git操作.png)

## 问题处理：

### 1.超大文件push失败

```py
GitHub对常规Git仓库中的文件大小有限制，最大为100MB，并且推荐的最大文件大小为50MB。您推送的文件超过了这个限制，因此被远程仓库拒绝。
根据您提供的信息，以下是一些解决方案：

1.使用Git Large File Storage (LFS)：
    Git LFS是Git的一个扩展，允许您管理大文件，如您推送的这些大文件。
    可以通过以下步骤启用Git LFS：
    下载并安装Git LFS。
    运行git lfs install来设置您的用户账户。

    在您的Git仓库中，使用git lfs track命令来指定您希望Git LFS管理的文件类型。例如：
    git lfs track "*.psd"
    git add .gitattributes

    提交并推送您的更改：
    git add file.psd
    git commit -m "Add large file"
    git push origin main
    
2.增加 Git 推送超时时间：
    通过设置 Git 配置来增加推送超时时间：
    git config --global http.postBuffer 524288000  # 设置为500MB
    
3.使用SSH代替HTTPS：
    如果使用的是HTTPS方式克隆仓库，可以尝试切换到SSH方式，因为SSH通常更稳定：
    git remote set-url origin git@github.com:JM-jietian/pythontest.git
```

### 2.清除git暂缓区

```py
1.撤销所有文件的暂存状态：
    git reset
    或者使用：
    git reset HEAD .
    这两个命令都会将暂存区中的所有更改撤销，但不会删除工作目录中的更改。

2.撤销特定文件的暂存状态：
    git reset HEAD <file>
    将 <file> 替换成你想要撤销暂存的文件名。

3.如果你想要撤销暂存状态并删除工作目录中的更改（慎用，因为这会丢失未提交的更改）：
    git reset --hard
    这个命令会将暂存区和工作目录都重置到最后一次提交的状态。
```

### 3.中文乱码

```py
设置Git的编码：
    可以通过以下命令设置Git的编码，以解决乱码问题：
    git config --global core.quotepath false  # 显示status编码
    git config --global gui.encoding utf-8     # 图形界面编码
    git config --global i18n.commitencoding utf-8  # 提交信息编码
    git config --global i18n.logoutputencoding utf-8  # 输出log编码
```

