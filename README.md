# THUeat--Backend
清华大学食堂App
## 虚拟环境初始化
先创建一个virtual environment，然后

    pip install -r requirements.txt

## 安装数据库
使用的是MySQL，须先从[官网](https://dev.mysql.com/downloads/windows/installer/8.0.html)下载MySQL server。
安装时注意，选择custom方式安装，选MySQL Server 8.0.26，MySQL Workbench可自行选择要不要装。
用户名：root
密码：root
安装后进入cmd，打开MySQL命令行

    mysql -u root -p
 输入密码后就可以进入MySQL命令行，如果有问题可以看[这里](https://www.php.cn/mysql-tutorials-442866.html)。
使用命令行创建数据库。

    mysql> CREATE DATABASE django_database
使用命令行查看所有数据库

    mysql> SHOW DATABASES

接下来可以安装[Dbeaver](https://dbeaver.io/?ref=eversql.com)来方便可视化数据库。

## 运行
打开文件后，在terminal运行

    python manage.py migrate
    python manage.py runserver
然后就能在浏览器中访问了，要停止server可以CTRL+BREAK或CTRL+C。
