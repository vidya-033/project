from flask import Flask,render_template,request
import psycopg2
from dotenv import load_dotenv
import os
import gunicorn

app=Flask(__name__)

load_dotenv()

try:
    connection=psycopg2.connect(os.getenv('DB_URL')
    cursor = connection.cursor()

    sql="""create table if not exists todo_list(
    id serial primary key,
    task varchar(30),
    status varchar(10));"""

    cursor.execute(sql)
    cursor.commit()
    print("Connection")

except:
    print("DB connection error")

@app.route('/',methods=['POST'])
def home():
    data=request.json
    input_value=data['input']
    status = data['status']
    query="""insert into todo_list (task,status) values(%s,%s)"""
    cursor.execute(query,(input_value,status,))
    cursor.commit()
    query = """select count(*) from todo_list"""
    cursor.execute(query)
    cursor.commit()
    res = cursor.fetchone()
    return str(res[0])

@app.route('/done',methods=['POST'])
def complete():
    data=request.json
    value=data['task']
    status = data['status']
    query = """update todo_list set status=%s where task=%s"""
    cursor.execute(query,(status,value,))
    cursor.commit()
    return ''

@app.route('/delete',methods=['POST'])
def delete():
    data=request.json
    value = data['task']
    query = """delete from todo_list where task=%s"""
    cursor.execute(query,(value,))
    cursor.commit()
    query = """select count(*) from todo_list"""
    cursor.execute(query)
    cursor.commit()
    res = cursor.fetchone()
    return str(res[0])

@app.route('/')
def homepage():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
