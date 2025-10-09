import pymysql

def db_config():
    db_conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='db_enrollment2',
        cursorclass=pymysql.cursors.DictCursor
    )

    return db_conn