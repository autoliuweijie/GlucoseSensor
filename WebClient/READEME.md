# READEME

## 0.创建数据库

先到数据库服务器下，确保后台Mysql服务是开着的，把项目中的create_database.sql文件复制到服务器任意目录中，并修改以下两行：

    create user 'glucose_user'@'localhost' identified by 'glucosepassword';
    grant select, update, insert on glucose_sensor.* to 'glucose_user'@'localhost' identified by 'glucosepassword';

把'glucose'改成定义的mysql用户名，'localhost'改成允许访问的IP（%表示允许任何IP访问, localhost表示只能从本地访问），'glucosepassword'改成密码. 
然后执行这个SQL脚本，自动创建数据库。

```
$ mysql -uroot -prootpassword -e "source ./create_database.sql"
```

"root" 和 "rootpassword" 分别是这台服务器中mysql的root账号和密码。

这样数据库就创建好了。你可以用navicat软件来查看这个数据库。如果是远程访问，请确保数据库开通了远程访问。

## 1.部署项目

假设部署项目的服务器和数据库服务器是分开的，那么登录到项目服务器的项目目录，假设项目目录是/home/glucose/ （建议建立一个独立的linux用户来部署项目）

### 1.1 下载项目

把项目下载到项目目录中：

```
$ git clone ********
```

进入到GlucoseSensor/WebClient目录下，以后如果不特殊指名，所有命令都是在这个目录下执行。


### 1.2 配置数据库账号密码

打开settings.py文件.

```
$ vim settings.py
```

修改数据库相关的内容

    # MYSQL Configuration
    MYSQL_HOST = '***.***.***.***'
    MYSQL_USER = 'username'
    MYSQL_PASSWORD = 'password'
    MYSQL_DATABASE = 'glucose_sensor'
    MYSQL_PORT = 3306

主要修改数据库服务器的IP(MYSQL_HOST)、MYSQL用户名(MYSQL_USER)、MYSQL密码(MYSQL_PASSWORD).

修改后保存

### 1.3 配置运行环境

创建和配置虚拟环境, 假设本机已经安装好virtualenv

```
$ virtualenv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
$ deactivate
```

### 1.4 启动服务

```
$ source .env/bin/activate
$ python client.py
```


