import psycopg2

conn = psycopg2.connect(database="practicedb",host="localhost",user="postgres",password="1234",port="5432")
cursor=conn.cursor()

def insert(date_value,time_value,shift_value,id_value,result_value):
    executedstring="insert into turbo_table(date, time, shift, id, result) values('{0}','{1}',{2},'{3}','{4}');".format(date_value,time_value,shift_value,id_value,result_value)
    cursor.execute(executedstring)
    conn.commit()
    print("Records inserted........")

