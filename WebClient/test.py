from mylib.database.datamangers import DevicesTable, UsersTable, RecordsTable
from datetime import datetime

# test()

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
