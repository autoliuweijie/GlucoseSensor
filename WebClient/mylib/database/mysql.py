#!/usr/bin/env python
# -*-coding:UTF-8-*-
import sys, MySQLdb, traceback
import time
import logging


class Mysql:
    def __init__(self,
                 host='',
                 user='',
                 passwd='',
                 db='',
                 port=3306,
                 charset='utf8'
                 ):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.conn = None
        is_success = self._conn()
        if is_success:
            logging.info('mysql connect successfully!')
        else:
            logging.warning('mysql connect failed!')

    def _conn(self):
        try:
            self.conn = MySQLdb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                charset=self.charset)
            return True
        except:
            return False

    def _reConn(self, num=3, stime=3):  # 重试连接总次数为9秒,这里根据实际情况自己设置,如果9秒都没连上就不连了
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()  # cping 校验连接是否异常
                _status = False
            except:
                if self._conn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

        if _number > num:
            logging.warning('mysql reconnect failed!')

    def select(self, sql=''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except MySQLdb.Error, e:
            logging.warning("Error %d: %s" % (e.args[0], e.args[1]))
            return None

    def select_limit(self, sql='', offset=0, length=20):
        sql = '%s limit %d , %d ;' % (sql, offset, length)
        return self.select(sql)

    def query(self, sql=''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute("set names utf8")  # utf8 字符集
            result = self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
            return (True, result)
        except MySQLdb.Error, e:
            return False

    def close(self):
        self.conn.close()
        logging.info('mysql close successfully!')


if __name__ == '__main__':
    my = Mysql('localhost', 'root', 'password', 'database', 3306)
    print my.select_limit('select * from sdb_admin_roles', 1, 1)
    my.close()