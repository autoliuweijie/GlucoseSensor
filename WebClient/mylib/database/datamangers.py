"""
    This script contains some data i/o of database
    @author: Liu Weijie
    @Date: 2017-03-22
"""
from mylib.database.mysql import Mysql
from datetime import datetime
from settings import *


# Configuratin



# Create Mysql
mysql = Mysql(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DATABASE,
    port=MYSQL_PORT,
)


class DevicesTable(object):

    @classmethod
    def get_device_info_by_unicode(cls, unicode):
        '''
        get device information by unicode
        :param unicode: unicode(str)
        :return: dict like {'d_id': 1L, 'date': datetime.date(2017, 3, 22), 'type': u'1', 'unicode': u'ICSLNGM0001', 'others': u'test'}
        '''
        try:
            sql = "select * from devices where unicode='%s';"%(unicode)
            info = mysql.select(sql=sql)[0]
            return info
        except:
            return None


class UsersTable(object):

    @classmethod
    def create_new_user(
            cls, username, password, age, gender, diabetes, unicode, email,
            phone='null', weights='null', heights='null'
    ):
        '''
        create new user
        :return: True or False means whether success.
        '''

        try:
            # insert record
            sql = """
                insert into users(username, password, email, age, gender, diabetes, unicode, phone, weights, heights)
                values('%s', '%s', '%s', %s, %s, %s, '%s', %s, %s, %s);
            """
            sql = sql%(username, password, email, age, gender, diabetes, unicode, phone, weights, heights)
            is_success = mysql.query(sql=sql)[0]

            # get u_id
            sql = "select u_id from users where username='%s';"%(username)
            u_id = mysql.select(sql=sql)[-1]['u_id']
            return is_success, u_id

        except:
            return False, 0

    @classmethod
    def get_user_info_by_username(cls, username):
        """
        get user info by username
        :param username: username
        :return: info dict like {'username': u'liuweijie3', 'u_id': 20L, 'gender': 0, 'age': 12L, 'heights': 12L,
                            'phone': u'18600117376', 'weights': None, 'unicode': u'ICLSNGM0001', 'password': u'p**',
                            'email': u'autoliuweijie@163.com', 'diabetes': 1}
        """
        try:
            sql = "select * from users where username='%s';"%(username)
            info = mysql.select(sql=sql)[0]
            info['gender'] = 1 if info['gender'] == '\x01' else 0
            info['diabetes'] = 1 if info['diabetes'] == '\x01' else 0
            return info
        except:
            return None

    @classmethod
    def get_user_info_by_uid(cls, u_id):
        """
        get user info by uid
        :param u_id:  u_id
        :return: info
        """
        try:
            sql = "select * from users where u_id='%s';"%(u_id)
            info = mysql.select(sql=sql)[0]
            info['gender'] = 1 if info['gender'] == '\x01' else 0
            info['diabetes'] = 1 if info['diabetes'] == '\x01' else 0
            return info
        except:
            return None


class RecordsTable(object):

    @classmethod
    def create_new_record(
            cls, u_id, record_time, unicode, video_name,
            predict_blood_glucose='null', predict_blood_oxygen='null', predict_heart_rate='null', predict_body_temperature='null', predict_blood_pressure='null',
            reference_blood_glucose='null', reference_blood_oxygen='null', reference_heart_rate='null', reference_body_temperature='null', reference_blood_pressure='null',
    ):
        """
            create a new record
        :return: is_success, r_id
        """
        record_time = record_time.strftime('%Y-%m-%d %H:%M:%S')
        try:

            # insert record
            sql = """
                insert into records(u_id, record_time, unicode, video_name,
                predict_blood_glucose, predict_blood_oxygen, predict_heart_rate, predict_body_temperature, predict_blood_pressure,
                reference_blood_glucose, reference_blood_oxygen, reference_heart_rate, reference_body_temperature, reference_blood_pressure)
                values(%s, '%s', '%s', '%s',
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
                )
            """
            sql = sql%(u_id, record_time, unicode, video_name,
                       predict_blood_glucose, predict_blood_oxygen, predict_heart_rate, predict_body_temperature, predict_blood_pressure,
                       reference_blood_glucose, reference_blood_oxygen, reference_heart_rate, reference_body_temperature, reference_blood_pressure
                       )
            is_success = mysql.query(sql=sql)[0]

            # get r_id
            sql = "select r_id from records where u_id=%s and record_time='%s';"%(u_id, record_time)
            r_id = mysql.select(sql=sql)[-1]['r_id']

            return is_success, r_id

        except:
            return False, 0

    @classmethod
    def update_predict_values(cls, r_id, predict_blood_glucose='null', predict_blood_oxygen='null', predict_heart_rate='null', predict_body_temperature='null', predict_blood_pressure='null'):
        """
        update predict values
        :param r_id: r_id
        :return: is_success
        """
        try:
            sql = """
                update records set predict_blood_glucose=%s, predict_blood_oxygen=%s, predict_heart_rate=%s, predict_body_temperature=%s, predict_blood_pressure=%s where r_id=%s;
            """
            sql = sql%(predict_blood_glucose, predict_blood_oxygen, predict_heart_rate, predict_body_temperature, predict_blood_pressure, r_id)
            is_success = mysql.query(sql=sql)[0]
            return is_success

        except:
            return False

    @classmethod
    def update_reference_values(cls, r_id, reference_blood_glucose='null', reference_blood_oxygen='null',
                              reference_heart_rate='null', reference_body_temperature='null', reference_blood_pressure='null'):
        """
        update reference values
        :param r_id: r_id
        :return: is_success
        """
        try:
            sql = """
                update records set reference_blood_glucose=%s, reference_blood_oxygen=%s, reference_heart_rate=%s, reference_body_temperature=%s, reference_blood_pressure=%s where r_id=%s;
            """
            sql = sql % (reference_blood_glucose, reference_blood_oxygen, reference_heart_rate, reference_body_temperature,
                         reference_blood_pressure, r_id)
            print sql
            is_success = mysql.query(sql=sql)[0]
            return is_success

        except:
            return False


if __name__ == "__main__":
    pass
    # print DevicesTable.get_device_info_by_unicode('ICSLNGM0001')
    # print UsersTable.create_new_user(
    #     username='liuweijie',
    #     password='liuweijie',
    #     age=23,
    #     gender=1,
    #     diabetes=0,
    #     unicode='ICSLNGM0001',
    #     email='liuweijie@163.com'
    # )

    # gender = UsersTable.get_user_info_by_username('liuweijie')['gender']
    # print gender

    # dt = datetime(2012,11,11, 11, 11, 11)
    # ret = RecordsTable.create_new_record(1, dt, 'ICSLNGM0001', '1213312.webm')

    # print RecordsTable.update_predict_values(
    #     r_id=13,
    #     predict_blood_glucose=11,
    #     predict_blood_oxygen=11,
    #     predict_heart_rate=11,
    #     predict_body_temperature=11,
    #     predict_blood_pressure=11
    # )
    #
    # print RecordsTable.update_reference_values(
    #     r_id=13,
    #     reference_blood_glucose=11,
    #     reference_blood_oxygen=11,
    #     reference_heart_rate=11,
    #     reference_body_temperature=11,
    #     reference_blood_pressure=11
    # )