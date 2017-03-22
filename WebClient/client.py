#coding:utf-8
from flask import Flask, session, redirect, url_for, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from mylib.database.datamangers import UsersTable

app = Flask(__name__)
app.secret_key = '\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'


# 前端界面

@app.route("/", methods=['GET'])
def index():
    username = session.get('username')
    if username is None: #如果没有登录，跳转到登录界面
        return redirect(url_for('login'))
    else:
        return redirect(url_for('measure'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html", infomation="Please Login!")
    else:
        # 得到输入用户名、密码
        username = request.form.get('username')
        password = request.form.get('password')

        # 获取真实的密码的哈希
        info = UsersTable.get_user_info_by_username(username)
        if info is None:
            return render_template("login.html", infomation="Username does not exist!")
        password_hash = info['password']

        # 对比密码是否正确
        if check_password_hash(password_hash, password):
            session['username'] = username
            return redirect(url_for('measure'))
        else:
            return render_template("login.html", infomation="Password mistake!")

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/measure", methods=['GET'])
def measure():
    username = session.get('username')
    return render_template("measure.html", username=username)


# API


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7002)