#coding:utf-8
import os, sys
from flask import Flask, session, redirect, url_for, request, render_template, jsonify, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash
from mylib.database.datamangers import UsersTable, RecordsTable
from mylib.models.nirvideomodels import INirVideoModel
from mylib.utils.imageutils import array_to_img
from datetime import datetime
from settings import PORT, HOST, DEBUG


# 配置
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = 'database/'
DATABASE_PATH = os.path.join(ROOT_PATH, DATABASE_DIR)
VIDEO_DIR = 'nirvideos/'
VIDEO_PATH = os.path.join(DATABASE_PATH, VIDEO_DIR)
IMAGE_DIR = 'resultimages/'
IMAGE_PATH = os.path.join(DATABASE_PATH, IMAGE_DIR)
NIR_VIDEO_MODEL = INirVideoModel()


# 创建Flask App
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
    if username is None:
        return redirect(url_for('login'))
    else:
        return render_template("measure.html", username=username)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html", infomation='Register')
    else:
        # 从表单提取数据
        username = request.form.get('username')
        password = request.form.get('password')
        age = int(request.form.get('age'))
        gender = int(request.form.get('gender'))
        diabetes = int(request.form.get('diabetes'))
        unicode = request.form.get('unicode')
        email = request.form.get('email')
        phone = request.form.get('phone')
        weights = request.form.get('weights')
        heights = request.form.get('heights')
        phone = 'null' if len(phone) == 0 else phone
        weights = 'null' if len(weights) == 0 else int(weights)
        heights = 'null' if len(heights) == 0 else int(heights)

        is_success, u_id = UsersTable.create_new_user(
            username=username,
            password=generate_password_hash(password), # 对密码哈希
            age=age,
            gender=gender,
            diabetes=diabetes,
            unicode=unicode,
            email=email,
            phone=phone,
            weights=weights,
            heights=heights
        )
        if is_success:
            return redirect(url_for('login'))
        else:
            return render_template("register.html", infomation=u'用户名已注册或设备编码错误')


# API
@app.route("/upload_measure", methods=['POST'])
def upload_measure():
    """
    上传测量的视频，保存视频、计算结果、保存结果、返回结果。
    <form action="/upload_measure" method="POST" enctype="multipart/form-data">
        <input type="file" name="video"><br>
        <input type="submit" value="Upload">
    </form>
    :return: response json like
            {
              "blood_glucose": 15.5,
              "blood_oxygen": 0.9,
              "blood_pressure": 70,
              "body_temperature": 35,
              "heart_rate": 10,
              "is_success": 1,
              "r_id": 33,
              "result_image": "database/resultimages/33.png"
            }
    """

    # 检查是否已经登录
    username = session['username']
    if username is None:
        return redirect(url_for('login'))

    # 获取相关信息
    info = UsersTable.get_user_info_by_username(username)
    u_id, unicode = info['u_id'], info['unicode']
    now = datetime.now()

    # 出错时返回
    wrong_json = {'is_success': 0}

    # 保存视频数据
    try:
        # 保存视频
        video_name = str(u_id) + '_' + now.strftime('%Y%m%d%H%M%S') + '.webm'
        video_save_path = os.path.join(VIDEO_PATH, video_name)
        video = request.files['video']
        video.save(video_save_path)

        # 写入数据库
        is_success, r_id = RecordsTable.create_new_record(u_id=u_id, record_time=now, unicode=unicode, video_name=video_name)

        if not is_success:
            wrong_json['reason'] = 'Inserting Video into mysql is wrong!'
            return jsonify(wrong_json)
    except:
        wrong_json['reason'] = 'Saving Video is wrong!'
        return jsonify(wrong_json)

    # 计算生理参数, 并返回json
    try:
        predict_result, result_img = NIR_VIDEO_MODEL.predict(video) # 计算生理结果


    except:
        wrong_json['reason'] = 'Predict process is wrong!'
        return jsonify(wrong_json)

    # 保存与返回
    try:
        # 存入数据库
        is_success = RecordsTable.update_predict_values(
            r_id=r_id,
            predict_blood_glucose=predict_result['blood_glucose'],
            predict_blood_oxygen=predict_result['blood_oxygen'],
            predict_heart_rate=predict_result['heart_rate'],
            predict_body_temperature=predict_result['body_temperature'],
            predict_blood_pressure=predict_result['blood_pressure']
        )

        # 保存结果图片
        result_img = array_to_img(result_img)
        img_name = str(r_id) + '.png'
        img_save_url = os.path.join(IMAGE_PATH, img_name)
        result_img.save(img_save_url)

        # 返回结果
        predict_result['r_id'] = r_id  # 添加r_id和is_success
        predict_result['is_success'] = 1 if is_success else 0
        predict_result['result_image'] = os.path.join(DATABASE_DIR, IMAGE_DIR, img_name)
        return jsonify(predict_result)
    except:
        wrong_json['reason'] = 'Saving Result is wrong!'
        return jsonify(wrong_json)

@app.route('/post_reference', methods=['POST'])
def post_reference():
    """
    接收用户输入的参考值，并存入数据库
    :return:
    """
    # 获取表单数据
    r_id = int(request.form.get('r_id'))
    reference_blood_glucose = request.form.get("blood_glucose")
    reference_blood_oxygen = request.form.get("blood_oxygen")
    reference_blood_pressure = request.form.get("blood_pressure")
    reference_heart_rate = request.form.get("heart_rate")
    reference_body_temperature = request.form.get("body_temperature")
    reference_blood_glucose = 'null' if len(reference_blood_glucose) == 0 else float(reference_blood_glucose)
    reference_blood_oxygen = 'null' if len(reference_blood_oxygen) == 0 else float(reference_blood_oxygen)
    reference_blood_pressure = 'null' if len(reference_blood_pressure) == 0 else float(reference_blood_pressure)
    reference_heart_rate = 'null' if len(reference_heart_rate) == 0 else float(reference_heart_rate)
    reference_body_temperature = 'null' if len(reference_body_temperature) == 0 else float(reference_body_temperature)

    # 存入数据库
    try:
        is_success = RecordsTable.update_reference_values(
            r_id=r_id,
            reference_blood_glucose=reference_blood_glucose,
            reference_blood_oxygen=reference_blood_oxygen,
            reference_blood_pressure=reference_blood_pressure,
            reference_heart_rate=reference_heart_rate,
            reference_body_temperature=reference_body_temperature
        )
        if is_success:
            return "Thank you for your data!"
        else:
            return "Error"
    except:
        return "Error"

@app.route('/database/resultimages/<img_name>', methods=['GET'])
def get_image(img_name):
    """
        用来发布/database/resultimages/中的图片，例如：GET http://IP/database/resultimages/33.png, 返回一张图片
    """
    img_url = os.path.join(IMAGE_PATH, img_name)
    try:
        response = send_file(img_url)
    except:
        response = abort(404)

    return response


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)