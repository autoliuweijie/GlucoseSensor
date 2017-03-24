#coding:utf-8
import os, sys
from flask import Flask
import logging


# logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#     datefmt='%a, %d %b %Y %H:%M:%S',
#     filename='./log.txt',
#     filemode='a'
# )

# 使用一个名字为fib的logger
logger = logging.getLogger('fib')
# 设置logger的level为DEBUG
logger.setLevel(logging.DEBUG)
# 创建一个输出日志到控制台的StreamHandler
hdr = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)
# 给logger添加上handler
logger.addHandler(hdr)


app = Flask(__name__)

@app.route('/')
def index():
    return 'hello'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7002)