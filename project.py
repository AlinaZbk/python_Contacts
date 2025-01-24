import tkinter as tk 
from tkinter import ttk
import sqlite3

# создание главного окна
class Main(tk.Frame):
    
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()   
# хранение и создание виджетов
    def init_main(self):
        # создание области кнопок
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)
        toolbar.pack(side = tk.TOP, fill = tk.X) #растянуть по Х
        
#### СОЗДАНИЕ КНОПОК ###
          
        # ДОБАВЛЕНИЕ
        self.add_img = tk.PhotoImage(file = 'C:/Users/ali13/Desktop/Python/project/img/add.png')
        btn_add = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, image = self.add_img, command = self.open_child )
        btn_add.pack(side = tk.LEFT)
        # ОБНОВЛЕНИЕ (редактирование)
        self.upd_img = tk.PhotoImage(file = 'C:/Users/ali13/Desktop/Python/project/img/update.png')
        btn_upd = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, image = self.upd_img, command = self.open_update_child )
        btn_upd.pack(side = tk.LEFT)
        # УДАЛЕНИЕ
        self.del_img = tk.PhotoImage(file = 'C:/Users/ali13/Desktop/Python/project/img/delete.png')
        btn_del = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, image = self.del_img, command = self.delete_record )
        btn_del.pack(side = tk.LEFT)
        # ПОИСК ПО ФИО
        self.search_img = tk.PhotoImage(file = 'C:/Users/ali13/Desktop/Python/project/img/search.png')
        btn_search = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, image = self.search_img, command = self.open_search )
        btn_search.pack(side = tk.LEFT)
        #ОБНОВЛЕНИЕ
        self.refresh_img = tk.PhotoImage(file = 'C:/Users/ali13/Desktop/Python/project/img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, image = self.refresh_img, command = self.view_records)
        btn_refresh.pack(side = tk.LEFT)

### ТАБЛИЦА В ГЛАВНОМ ОКНЕ ###

        # создание таблицы
        self.tree = ttk.Treeview(self, columns=('id', 'Name', 'Phone', 'Email', 'Salary'), height = 45, show = 'headings') 
        # добавляем параметры колонки
        self.tree.column('id', width=65, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.CENTER)
        self.tree.column('Phone', width=150, anchor=tk.CENTER)
        self.tree.column('Email', width=150, anchor=tk.CENTER)
        self.tree.column('Salary', width=300, anchor=tk.CENTER)
        # подписи колонок
        self.tree.heading('id', text = 'id')
        self.tree.heading('Name', text = 'ФИО')
        self.tree.heading('Phone', text = 'Телефон')
        self.tree.heading('Email', text = 'Почта')
        self.tree.heading('Salary', text = 'Заработная плата')
        #упаковка
        self.tree.pack(side = tk.LEFT)
        # ползунок
        scroll = tk.Scrollbar(self, command = self.tree.yview)
        scroll.pack(side = tk.LEFT, fill = tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        
#### ОСНОВНЫЕ МЕТОДЫ
    
    # вызывает добавление данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()
    # просмотр записей
    def view_records(self):
        self.db.cur.execute('''SELECT * FROM Users''')
        #удалить все из виджета
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в таблицу все данные из базы данных
        [self.tree.insert('', 'end', values = row) for row in self.db.cur.fetchall()]
    # метод обновления данных
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1') # #1 - первый столбец
        self.db.cur.execute('''UPDATE Users SET name = ?, phone = ?, email = ?, salary = ? WHERE id = ?''', (name, phone, email, salary, id), )
        
        self.db.conn.commit()
        self.view_records()
    # метод удаления записи
    def delete_record(self):
        for row in self.tree.selection():
            self.db.cur.execute('''DELETE FROM Users WHERE id = ?''', (self.tree.set(row, '#1'), ))
            self.db.conn.commit()
            self.view_records()
    # метод поиска по ФИО
    def search_record(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('''SELECT * FROM Users WHERE name LIKE ?''', (name,  ))
        
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row) for row in self.db.cur.fetchall()]  
    # метод, отвечающий за вызов окна добавления
    def open_child(self):
        Child()
    # метод, отвечающий за вызов окна обновления(редактирования)
    def open_update_child(self):
        Update()
    # метод, вызывающий поиск по ФИО
    def open_search(self):
        Search()      

# окно добавления данных
class Child(tk.Toplevel):
    
     def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
     def init_child(self):
        self.title('Добавить')
        self.geometry('400x200')
        root.resizable(False, False)
        # перехватить все события, происходящие в приложении
        self.grab_set()
        # захватить фокус
        self.focus_set()        

        # ввод новых контактов
        label_name = tk.Label(self, text ='ФИО: ')
        label_name.place(x = 50, y = 50)
        label_phone = tk.Label(self, text ='Телефон: ')
        label_phone.place(x = 50, y = 80)
        label_email = tk.Label(self, text ='Почта: ')
        label_email.place(x = 50, y = 110)
        label_salary = tk.Label(self, text ='Заработная плата: ')
        label_salary.place(x = 50, y = 140)
        
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x = 200, y = 80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x = 200, y = 110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x = 200, y = 140)
        
        # кнопка закрытия
        self.btn_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        self.btn_cancel.place(x = 300, y = 170)
        
        #кнопка добавления
        self.btn_add = ttk.Button(self, text = 'Добавить')
        self.btn_add.place(x = 220, y = 170)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(), 
                                                                        self.entry_phone.get(), 
                                                                        self.entry_email.get(),
                                                                        self.entry_salary.get()))
        self.btn_add.bind('<Button-1>', lambda event: self.destroy(), add = '+')

# окно изменения данных
class Update(Child):
    
    def __init__(self):
        super().__init__()       
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()
    
    def init_edit(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()
        
        self.btn_upd = ttk.Button(self, text = 'Редактировать позицию')
        self.btn_upd.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(), 
                                                                              self.entry_phone.get(), 
                                                                              self.entry_email.get(),
                                                                              self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add = '+')
        self.btn_upd.place(x = 150, y = 170)
     
    # подгрузка данных в форму
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('''SELECT * FROM Users WHERE id = ?''', (id, ))
        
        # доступ к первой записис выборки
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1]) # спозиция - 0, берем из таблицы 1, 2, 3 элемент
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])       
        
### ПОИСК ПО ИМЕНИ
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        
        self.focus_set()
#### LABEL
        
        label_name = tk.Label(self, text = 'ФИО: ')
        label_name.place(x = 20, y = 20)
        
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x = 70, y = 20)
        
### КНОПКА

        self.btn_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        self.btn_cancel.place(x = 200, y = 70)
        
        self.btn_search = ttk.Button(self, text = 'Найти')
        self.btn_search.place(x = 70, y = 70)
        self.btn_search.bind('<Button-1>', lambda event: self.view.search_record(self.entry_name.get()))
        self.btn_search.bind('<Button-1>', lambda event: self.destroy(), add = '+')
        
###################################################################################################################### 
        
# класс базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('Contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Users(
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                phone TEXT NOT NULL,
                                email TEXT NOT NULL,
                                salary TEXT NOT NULL)''')
        self.conn.commit()
        
    def insert_data(self, name, phone, email, salary):
        self.cur.execute(''' INSERT INTO Users (name, phone, email, salary)
                         VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit()
        
        
# создание окна
if __name__ == '__main__':
    root = tk.Tk()
    
    # Экземпляр класса базы данных
    db = DB()
    
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('800x450')
    
    # нельзя изменять параметры окна
    root.resizable(False, False)
    
    root.configure(bg = 'White')
    root.mainloop()