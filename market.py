import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import sqlite3
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from database import DataBase
import time
from kivy.clock import Clock
import os
# conn = sqlite3.connect("market.db")

app_path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(app_path, 'market.db'))
c = conn.cursor()


class page(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.names_list = []
        self.inside4 = GridLayout(cols=2)

        self.inside = GridLayout(cols=1)
        self.inside1 = GridLayout(cols=1)
        self.inside3 = GridLayout(cols=1)
        self.inside2 = GridLayout(cols = 1)
        self.inside4.add_widget(self.inside3)

        self.plusbtn = Button(text='+', font_size='50sp')
        self.plusbtn.bind(on_press=self.plusbtn1)
        self.inside3.add_widget(self.plusbtn)

        self.logout_btn = Button(text="log out", font_size='50sp')
        self.logout_btn.bind(on_press=self.logout_btn1)
        self.inside3.add_widget(self.logout_btn)

        self.inpuut = TextInput(multiline=False, font_size=50)
        self.inside2.add_widget(self.inpuut)
        self.alredy = Button(text = "continue to the previous")
        self.alredy.bind(on_press = self.start)
        self.inside2.add_widget(self.alredy)
        self.inside4.add_widget(self.inside2)

        self.finish_btn = Button(text='Start', font_size='50sp')
        self.finish_btn.bind(on_press=self.finish_btn1)
        self.inside.add_widget(self.finish_btn)

        self.clear = Button(text="clear", font_size='50sp')
        self.clear.bind(on_press=self.clear1)
        self.inside.add_widget(self.clear)

        self.inside4.add_widget(self.inside)
        self.inside4.add_widget(self.inside1)
        self.add_widget(self.inside4)

        if __name__ == "__main__":
            Clock.schedule_once(self.first_pop, 2)

    def logout_btn1(self, instance):
        pass

    # sm.current = "login"

    def plusbtn1(self, instance):
        # self.cols = self.cols +1
        if self.inpuut.text in self.names_list:
            popupWindow = Popup(title="Error", content=Label(text="you write this name before"), size_hint=(None, None),
                                size=(400, 400))
            popupWindow.open()
            self.inpuut.text = ""
        elif self.inpuut.text == "":
            popupWindow = Popup(title="Error", content=Label(text="you didint write any name"), size_hint=(None, None),
                                size=(400, 400))
            popupWindow.open()


        else:

            name = self.inpuut.text

            self.inside1.add_widget(Label(text=name))
            self.names_list.append(name)
            self.inpuut.text = ""

    def show_popup(self):
        show = GridLayout(cols=1)

        show.add_widget(Label(text="are you sure to start by this names"))
        yess = Button(text="yes")
        self.noo = Button(text="no")
        showsh = GridLayout(cols=len(self.names_list))
        yess.bind(on_press=self.start)

        for name in self.names_list:
            showsh.add_widget(Label(text=name))
        show.add_widget(showsh)

        show.add_widget(self.noo)
        show.add_widget(yess)

        popupWindow = Popup(title="Confirmation", content=show, size_hint=(None, None), size=(400, 400))

        popupWindow.open()
        self.noo.bind(on_press=popupWindow.dismiss)
        yess.bind(on_press=popupWindow.dismiss)

    def start(self, instance):

        for name in self.names_list:
            c.execute(f"insert into names (name) values ('{name}')")
        conn.commit()

        self.demo()

    def finish_all1(self, instance):
        c.execute("""

        SELECT names.name,t2.pay
from
(
SELECT names_id , t1.summ - (SELECT ((SELECT sum(amount) from salary) / (SELECT count(id) from names)) avg) pay
FROM
(SELECT names_id,sum(amount) summ from salary group by 1) t1
) t2
JOIN names
on names.id = t2.names_id
        """)

        self.ret = c.fetchall()

        pop_finish = GridLayout(cols=1)
        for tupl in self.ret:
            # pop_finish.add_widget(Label(text = ))
            if tupl[1] < 0:
                tupl1 = str(tupl[1])
                pop_finish.add_widget(Label(text=f"{str(tupl[0])} should pay {tupl1[1:]}"))
            else:
                pop_finish.add_widget(Label(text=f"{str(tupl[0])} should recive {str(tupl[1])}"))

        c.execute("""
            SELECT names.name,t2.pay

FROM
(
SELECT id names_id,
CASE
    when id > 0 THEN (SELECT sum(avgg) / (SELECT count(id) from (SELECT id from names where id not in (SELECT DISTINCT names_id from salary))
) didnt_pay
from(
SELECT * , 
t1.summ - (SELECT ((SELECT sum(amount) from salary) / (SELECT count(id) from names)) avg) avgg
FROM
(SELECT names_id,sum(amount) summ from salary group by 1) t1)
)
    ELSE 100
END as pay
from names where id not in (SELECT DISTINCT names_id from salary)
) t2
JOIN names
on names.id = t2.names_id


            """)

        self.ret1 = c.fetchall()
        for tupl in self.ret1:
            # pop_finish.add_widget(Label(text = ))
            pop_finish.add_widget(Label(text=f"{str(tupl[0])} should pay {tupl[1]}"))

        pop_finish.add_widget(Label(text="do you want to continue", font_size=20))
        popinside = GridLayout(cols=2)
        no1 = Button(text="no")
        yes1 = Button(text="yes")
        no1.bind(on_press=self.delete1)
        popinside.add_widget(yes1)
        popinside.add_widget(no1)
        pop_finish.add_widget(popinside)

        popupWindow = Popup(title="thank you for using our app", content=pop_finish, size_hint=(None, None),
                            size=(400, 400))
        popupWindow.open()
        yes1.bind(on_press=popupWindow.dismiss)
        no1.bind(on_press=popupWindow.dismiss)

    def delete1(self, instance):
        for tupl in self.ret:
            c.execute(f"SELECT id from names where name = '{tupl[0]}'")
            id1 = c.fetchall()

            c.execute(f"DELETE from names WHERE name = '{tupl[0]}'")
            c.execute(f"DELETE from salary where names_id = {id1[0][0]}")
            conn.commit()
        self.clear_widgets()
        self.add_widget(self.inside4)

    def finish_btn1(self, instance):

        if len(self.names_list) < 2:
            popupWindow = Popup(title="Error", content=Label(text="you must put at least two names"),
                                size_hint=(None, None), size=(400, 400))
            popupWindow.open()
        else:

            self.show_popup()

    def plusbtn2(self, instance):
        self.name1.add_widget(TextInput())

    def goback_btn1(self, instance):
        self.table.remove_widget(self.write)
        self.inpuut1.text = ""
        self.table.remove_widget(self.view)
        try:
            self.table.remove_widget(self.infor)
            
        except:
            pass
        try:
            self.table.remove_widget(self.num_input)
            self.table.remove_widget(self.submit)
        except:
            pass

        self.table.remove_widget(self.goback_btn)
        self.table.remove_widget(self.finish_all)
        self.table.remove_widget(self.logout_btn2)
        self.table.add_widget(self.checbtn)
        self.table.add_widget(self.finish_all)
        self.table.add_widget(self.logout_btn2)

    def chec(self, instance):
        names_list2 = []
        c.execute("select name from names")
        names_db = c.fetchall()
        for name in names_db:
            names_list2.append(name[0])

        if self.inpuut1.text in names_list2:
            self.demo1()

        else:

            show = GridLayout(cols=1)

            only = Button(text="you cannot write onother name")
            show.add_widget(only)

            for name in names_list2:
                show.add_widget(Label(text=name))

            popupWindow = Popup(title="Error", content=show, size_hint=(None, None), size=(400, 400))

            popupWindow.open()
            only.bind(on_press=popupWindow.dismiss)

    def write1(self, instance):
        self.num_input = TextInput(multiline=False)
        self.table.add_widget(self.num_input)
        self.submit = Button(text="submit", font_size='50sp')
        self.submit.bind(on_press=self.submit1)
        self.table.add_widget(self.submit)

    def view1(self, instance):

        c.execute(f"select id from names where name = '{self.name2}'")
        id = c.fetchall()
        id = id[0][0]

        sal = []

        c.execute(f"select amount from salary where names_id = {id}")
        sal1 = c.fetchall()

        for num in sal1:
            sal.append(num[0])

        self.demo2(sal)

    def submit1(self, instance):
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]

        try:
            self.table.remove_widget(self.num_input)
            self.table.remove_widget(self.submit)

            c.execute(f"select id from names where name = '{self.name2}' and account_id = {id}")
            id = c.fetchall()
            id = id[0][0]

            c.execute(f"insert into salary (names_id,amount) values ({id},{self.num_input.text})")
            conn.commit()

            popupWindow = Popup(title="Information", content=Label(text="your money has been successfully added"),
                                size_hint=(None, None), size=(400, 400))
            popupWindow.open()
    

        except:
            popupWindow = Popup(title="Error", content=Label(text="must be a number"), size_hint=(None, None), size=(400, 400))
            popupWindow.open()


    def demo(self, instance=None):
        self.clear_widgets()
        self.table = GridLayout(cols=2)
        self.inpuut1 = TextInput(multiline=False)
        self.table.add_widget(self.inpuut1)
        self.checbtn = Button(text="go", font_size='50sp')
        self.checbtn.bind(on_press=self.chec)
        self.table.add_widget(self.checbtn)
        self.finish_all = Button(text="finish all and calculate", font_size='30sp')
        self.finish_all.bind(on_press=self.finish_all1)
        self.table.add_widget(self.finish_all)
        self.logout_btn2 = Button(text="log out", font_size='50sp')
        self.logout_btn2.bind(on_press=self.logout_btn1)
        self.table.add_widget(self.logout_btn2)

        self.add_widget(self.table)


    def clear1(self, instance):
        self.inside1.clear_widgets()
        self.names_list.clear()


    def demo1(self):
        self.table.remove_widget(self.checbtn)
        self.goback_btn = Button(text="go back", font_size='50sp')
        self.goback_btn.bind(on_press=self.goback_btn1)
        self.table.add_widget(self.goback_btn)

        self.name2 = self.inpuut1.text

        self.write = Button(text="write", font_size='50sp')
        self.write.bind(on_press=self.write1)
        self.table.add_widget(self.write)
        self.view = Button(text="view", font_size='50sp')
        self.view.bind(on_press=self.view1)
        self.table.add_widget(self.view)


    def demo2(self, sal):
        if len(sal) == 0:
            self.infor = Label(text="didin't pay any money")

        else:
            summ = []
            self.infor = GridLayout(cols=1)
            for num in sal:
                self.infor.add_widget(Label(text=str(num)))
                summ.append(num)
            self.infor.add_widget(Label(text=f"and the sum is : {str(sum(summ))}"))

        self.table.add_widget(self.infor)
        self.table.remove_widget(self.view)


    def first_pop(self, instance):
        names_list2 = []
        c.execute("select name from names")
        names_db = c.fetchall()
        for name in names_db:
            names_list2.append(name[0])

        firstGrid = GridLayout(cols=1)

        if len(names_list2) == 0:
            pass

        else:
            for name in names_list2:
                firstGrid.add_widget(Label(text=name))

            btn = Button(text="want to continue in this table")
            btn.bind(on_press=self.demo)
            firstGrid.add_widget(btn)
            popupWindow = Popup(title="Error", content=firstGrid, size_hint=(None, None), size=(400, 400))
            popupWindow.open()


    def haha(self, instance):
        self.demo()


    def haha2(self):
        pass


class market(App):
    def build(self):
        return page()


db = DataBase("market.db")

if __name__ == "__main__":
    market().run()

