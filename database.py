import datetime
import sqlite3
import kivy
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import sqlite3
from kivy.uix.popup import Popup
import os
class DataBase:
    def __init__(self,db_file):
        self.users = None
        self.db_file = db_file

        app_path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(os.path.join(app_path, self.db_file))
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        
        
        self.load()

    def load(self):
        
        self.users = {}

        
        self.c.execute("SELECT * from accounts")
        ret = self.c.fetchall()
        for user in ret:
            email , password , account_name ,occured_at,id1 = user[2],user[3],user[1],user[-1],user[0]
            self.users[email] = (password,account_name,occured_at,id1)



    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.c.execute(f"insert into accounts (account_name,email,password,occured_at) values ('{name}','{email}','{password}','{DataBase.get_date()}')")
            self.conn.commit()
            self.load()
            return 1
        else:
            print("Email exists already")
            return -1


    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def start(self,names,id1):
        for name in names:

            self.c.execute(f"insert into names (name,account_id) values ('{name}',{id1})")
        self.conn.commit()
        
    def chec(self,id1):
        self.names_list2 = []

        self.c.execute(f"select name from names where account_id = {id1}")
        self.names_db = self.c.fetchall()
        for name in self.names_db:
            self.names_list2.append(name[0])

        return self.names_list2

    def view1(self,name,id1):


        self.c.execute(f"select id from names where name = '{name}' and account_id = {id1}")
        id = self.c.fetchall()
        id = id[0][0]

        sal = []

        self.c.execute(f"select amount from salary where names_id = {id}")
        sal1 = self.c.fetchall()

        for num in sal1:
            sal.append(num[0])
        return sal

    def finish_all1(self,account_id):
        self.c.execute(f"""
SELECT names.name , t1.pay
from
(
SELECT names_id ,
sum(amount) - (SELECT sum(amount) / (SELECT COUNT(*) FROM (SELECT id from names where account_id = {account_id})) avg from salary where names_id in (SELECT id from names where account_id = {account_id})) pay
from salary where names_id in (SELECT id from names where account_id = {account_id})
group by 1
) t1
JOIN names
on names.id = t1.names_id

            """)
        return self.c.fetchall()

    def finish_all(self,account_id):
        self.c.execute(f"""
SELECT names.name , t1.avg
FROM
(
SELECT id,
(SELECT sum(amount) / (SELECT COUNT(*) FROM (SELECT id from names where account_id = {account_id})) avg from salary where names_id in (SELECT id from names where account_id = {account_id})) avg

from names where account_id = {account_id} and id not in (SELECT names_id from salary)
) t1
join names
on names.id = t1.id

            """)
        return self.c.fetchall()

    def delete(self,id1):
        
        self.c.execute(f"DELETE from salary where names_id in (SELECT id from names where account_id = {id1})")
        self.conn.commit()
        self.c.execute(f"DELETE from names where account_id = {id1}")
        self.conn.commit()
    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

