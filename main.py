from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from database import DataBase
from market import page
import sqlite3

conn = sqlite3.connect("market.db")

c = conn.cursor()

class page1(page):

    def submit1(self, instance):
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]

        # try:
        self.table.remove_widget(self.num_input)
        self.table.remove_widget(self.submit)

        c.execute(f"select id from names where name = '{self.name2}' and account_id = {id1}")
        id = c.fetchall()
        id = id[0][0]

        c.execute(f"insert into salary (names_id,amount) values ({id},{self.num_input.text})")
        conn.commit()

        popupWindow = Popup(title="Information", content=Label(text="your money has been successfully added"),
                            size_hint=(None, None), size=(400, 400))
        popupWindow.open()
        # except:
        #     popupWindow = Popup(title="Error", content=Label(text="must be a number"), size_hint=(None, None), size=(400, 400))
        #     popupWindow.open()

    def window1(self):
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]

        names_list2 = []
        self.c.execute(f"select name from names where account_id = {id1}")
        names_db = self.c.fetchall()
        for name in names_db:
            names_list2.append(name[0])

        firstGrid = GridLayout(cols = 1)

        if len(names_list2) == 0:
            pass

        else:
            for name in names_list2:
                firstGrid.add_widget(Label(text = name))

            btn = Button(text = "want to continue in this table")
            btn.bind(on_press = self.start)
            firstGrid.add_widget(btn)
            popupWindow = Popup(title="Question", content= firstGrid, size_hint=(None,None),size=(400,400))
            popupWindow.open()

    def delete1(self,instance):
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]

        self.clear_widgets()
        self.inside1.clear_widgets()
        self.add_widget(self.inside4)
        db.delete(id1)




    def logout_btn1(self,instance):
        sm.current = "login"
        self.clear_widgets()
        self.inside1.clear_widgets()
        self.add_widget(self.inside4)

    def start(self,instance):

        
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]
        if instance.text == "continue to the previous":

            if len(db.chec(id1)) == 0:
                popupWindow = Popup(title="Error", content= Label(text = "you don't have a previus table"), size_hint=(None,None),size=(400,400))
                popupWindow.open()
            else:
                self.inside1.clear_widgets()
                self.names_list = []
                db.start(self.names_list,id1)
                self.demo()
        else:
            db.delete(id1)
            db.start(self.names_list,id1)
            
            self.demo()
    def chec(self,instance):
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]

        
        if self.inpuut1.text in db.chec(id1):
            self.demo1()

        else:
            show = GridLayout(cols = 1)
            only = Button(text = "you cannot write onother name")
            show.add_widget(only)
            for name in db.chec(id1):
       
                show.add_widget(Label(text = name))

            popupWindow = Popup(title="Error", content= show, size_hint=(None,None),size=(400,400))

            popupWindow.open()
            only.bind(on_press = popupWindow.dismiss)

    def view1(self,instance):
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]
       
        self.demo2(db.view1(self.name2,id1))

    def finish_all1(self,instance):
        current_user = db.get_user(MainWindow.current)
        id1 = current_user[-1]

        pop_finish = GridLayout(cols = 1)
        for tupl in db.finish_all1(id1):
            if tupl[1] < 0:
                tupl1 = str(tupl[1])
                pop_finish.add_widget(Label(text =f"{str(tupl[0])} should pay {tupl1[1:]}" ))
            else:
                pop_finish.add_widget(Label(text =f"{str(tupl[0])} should recive {str(tupl[1])}" ))

        for tupl in db.finish_all(id1):
            # pop_finish.add_widget(Label(text = ))
            pop_finish.add_widget(Label(text =f"{str(tupl[0])} should pay {tupl[1]}" ))



        pop_finish.add_widget(Label(text = "do you want to continue",font_size = 20))
        popinside = GridLayout(cols = 2)
        no1 = Button(text = "no")
        yes1 = Button(text = "yes")
        no1.bind(on_press = self.delete1)
        popinside.add_widget(yes1)
        popinside.add_widget(no1)
        pop_finish.add_widget(popinside)


        popupWindow = Popup(title = "thank you for using our app",content=pop_finish,size_hint=(None,None),size=(400,400))
        popupWindow.open()
        yes1.bind(on_press = popupWindow.dismiss)
        no1.bind(on_press = popupWindow.dismiss)

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                MainWindow.current = self.email.text
                sm.current = "market"
                self.reset()
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()

            sm.current = "market"

        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass



def sucsess():
    pop = Popup(title='Confirmation',
                  content=Label(text='your Email has benn successfully added'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
if __name__ == "__main__":
    db = DataBase("market.db")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"),page1(name="market")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
