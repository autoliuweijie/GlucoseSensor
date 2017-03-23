from mylib.database.datamangers import DevicesTable, UsersTable, RecordsTable
from datetime import datetime

# test()


dt = datetime(2012,11,11, 11, 11, 11)
ret = RecordsTable.create_new_record(1, dt, 'ICSLNGM0001', '1213312.webm')