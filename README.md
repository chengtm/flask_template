# 准备工作
   - 准备好项目需要的环境
     > - 如果没有安装`virtualenv`、 `pip`请先安装；
     > - 安装成功后在项目根目录下通过命令`virtualenv env -p python3`安装虚拟环境；
     > - 进入虚拟环境：`. env/bin/activate`或者`source env/bin/activate`；
     > - 安装需要的工具包：`pip install -r requirements.txt`；
   - 安装`mysql`，并创建`settings.py`文件中`SQLALCHEMY_DATABASE_URI`对应的数据库
   - 可以通过`flask`的`migrate`扩展包，可自动创建数据表，命令如下。你也可以通过手动create创建models里面对应的数据表
       ```
       python manage.py db init
       python manage.py db migrate
       python manage.py db upgrade
       ```
   
   - 启动`manage`
    `python manage.py runserver -h 0.0.0.0 -p 8080`

# 说明
  本项目是基于flask框架，Python3语言的迷你型项目，只包含一个登陆接口，所以在项目启动后，需要自己动手创建用户。