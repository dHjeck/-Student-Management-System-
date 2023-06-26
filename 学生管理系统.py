import tkinter
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import pymysql


def sql_link():
    db = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='xsglxt')
    cursor = db.cursor()
    return db, cursor


# 测试与数据库连接 23/6/20：暂时舍弃！
def chu_shi_hua():
    link = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='xsglxt')
    if link.ping(reconnect=True):
        messagebox.showinfo("成功", "已经与数据库建立联系！")
    else:
        messagebox.showerror("错误", "连接失败，请检查网络连接")


# 测试窗口
def ce_shi_chuang_ko():
    window = tk.Tk()
    window.resizable(False, False)
    window.minsize(600, 500)
    window.maxsize(600, 500)
    window.title("测试窗口")
    csh_bt = tk.Button(window, text="初始化", command=chu_shi_hua)
    csh_bt.grid(column=1, row=0)
    login_bt = tk.Button(window, text="login", command=login)
    login_bt.grid(column=1, row=1)
    login_bt = tk.Button(window, text="管理员面板", command=manager_table)
    login_bt.grid(column=1, row=2)


# 添加学生
def add_sutdent():
    add_student_root = tk.Tk()
    add_student_root.title("添加学生")
    add_student_root.config(width=600, height=600)

    student_id = tkinter.StringVar(add_student_root, value='')
    student_name = tkinter.StringVar(add_student_root, value='')
    student_age = tkinter.StringVar(add_student_root, value='')
    student_sex = tkinter.StringVar(add_student_root, value='')
    student_class = tkinter.StringVar(add_student_root, value='')

    labelstudent_name = tk.Label(add_student_root, text='学生姓名', font=("微软雅黑 -20"))
    labelstudent_id = tk.Label(add_student_root, text='学号', font=("微软雅黑 -20"))
    labelstudent_age = tk.Label(add_student_root, text='年龄', font=("微软雅黑 -20"))
    labelstudent_sex = tk.Label(add_student_root, text='性别', font=("微软雅黑 -20"))
    labelstudent_class = tk.Label(add_student_root, text='班级', font=("微软雅黑 -20"))

    labelstudent_id.place(x=25, y=100, height=40, width=200)
    labelstudent_name.place(x=25, y=200, height=40, width=200)
    labelstudent_age.place(x=225, y=100, height=40, width=200)
    labelstudent_sex.place(x=225, y=200, height=40, width=200)
    labelstudent_class.place(x=400, y=100, height=40, width=200)

    entrystudent_name = tk.Entry(add_student_root, textvariable=student_name)
    entrystudent_id = tk.Entry(add_student_root, textvariable=student_id)
    entrystudent_age = tk.Entry(add_student_root, textvariable=student_age)
    entrystudent_sex = tk.Entry(add_student_root, textvariable=student_sex)
    entrystudent_class = tk.Entry(add_student_root, textvariable=student_class)

    entrystudent_id.place(x=25, y=150, height=40, width=200)
    entrystudent_name.place(x=25, y=250, height=40, width=200)
    entrystudent_age.place(x=225, y=150, height=40, width=200)
    entrystudent_sex.place(x=225, y=250, height=40, width=200)
    entrystudent_class.place(x=400, y=150, height=40, width=200)

    def Button_ok():
        flag = 0
        db, cur = sql_link()
        data_student_id = str(entrystudent_id.get())
        data_student_name = str(entrystudent_name.get())
        data_student_age = str(entrystudent_age.get())
        data_student_sex = str(entrystudent_sex.get())
        data_student_class = str(entrystudent_class.get())
        search = cur.execute("SELECT * FROM student WHERE id = %s AND name = '%s' AND age = %s "
                             "AND sex = '%s' AND class = '%s'",
                             (data_student_id, data_student_name, data_student_age, data_student_sex,
                              data_student_class))
        if (search > 0):
            flag = 1
        else:
            flag = 0
        if (flag == 0):
            try:
                sql1 = "INSERT INTO student(id,name,age,sex,class)"
                sql1 += "VALUES('%s', '%s', '%s', '%s', '%s')" % (data_student_id, data_student_name, data_student_age,
                                                                  data_student_sex, data_student_class)
                cur.execute(sql1)
                db.commit()
                messagebox.showinfo(title="恭喜", message="注册成功!!!")
                add_student_root.destroy()
            except:
                messagebox.showerror(message='注册失败')
        else:
            messagebox.showerror(title="error", message="该学生已存在！")

    ok_button = tk.Button(add_student_root, text="确认", font=("微软雅黑 -20"), command=Button_ok)
    Exit_Button = tk.Button(add_student_root, text="退出", font=("微软雅黑 -20"),
                            command=add_student_root.destroy)
    ok_button.place(x=75, y=350, height=40, width=200)
    Exit_Button.place(x=325, y=350, height=40, width=200)


# 显示所有学生信息
def show_all_student():
    db, cur = sql_link()
    sql = "SELECT * FROM student"
    cur.execute(sql)
    db.commit()
    results = cur.fetchall()

    show_all_student_root = tk.Tk()
    show_all_student_root.title("查询结果")

    columns = ['ID', 'Name', 'Age', 'Sex', 'Class']
    tree = ttk.Treeview(show_all_student_root, show='headings', columns=columns)

    for col in columns:
        tree.heading(col, text=col)

    for row in results:
        tree.insert('', 'end', values=row)

    tree.pack()
    show_all_student_root.mainloop()


# 按id查找
def seach_student_id():
    search_studen_root = tk.Tk()
    search_studen_root.title("查找学生-ID")
    search_studen_root.config(width=600, height=600)

    search_student_id = tk.StringVar(search_studen_root, value='')
    laber_sch_student_id = tk.Label(search_studen_root, text='学生学号', font=("微软雅黑 -20"))
    laber_sch_student_id.place(x=200, y=100, height=40, width=200)
    enty_sch_student_id = tk.Entry(search_studen_root, textvariable=search_student_id)
    enty_sch_student_id.place(x=200, y=150, height=40, width=200)

    def button_ok():
        db, cur = sql_link()
        data_student_id = str(enty_sch_student_id.get())
        sql = "SELECT * FROM student WHERE id = %s" % data_student_id
        cur.execute(sql)
        db.commit()
        results = cur.fetchall()

        show_all_student_root = tk.Tk()
        show_all_student_root.title("查询结果")

        columns = ['ID', 'Name', 'Age', 'Sex', 'Class']
        tree = ttk.Treeview(show_all_student_root, show='headings', columns=columns)

        for col in columns:
            tree.heading(col, text=col)

        for row in results:
            tree.insert('', 'end', values=row)

        tree.pack()

    ok_button = tk.Button(search_studen_root, text="确认", font=("微软雅黑 -20"), command=button_ok)
    Exit_Button = tk.Button(search_studen_root, text="退出", font=("微软雅黑 -20"),
                            command=search_studen_root.destroy)
    ok_button.place(x=75, y=350, height=40, width=200)
    Exit_Button.place(x=325, y=350, height=40, width=200)


# 按姓名查找
def seacher_studnet_name():
    search_studen_root = tk.Tk()
    search_studen_root.title("查找学生-姓名")
    search_studen_root.config(width=600, height=600)

    search_student_name = tk.StringVar(search_studen_root, value='')
    laber_sch_student_name = tk.Label(search_studen_root, text='学生姓名', font=("微软雅黑 -20"))
    laber_sch_student_name.place(x=200, y=100, height=40, width=200)
    enty_sch_student_name = tk.Entry(search_studen_root, textvariable=search_student_name)
    enty_sch_student_name.place(x=200, y=150, height=40, width=200)

    def button_ok():
        db, cur = sql_link()
        data_student_name = str(enty_sch_student_name.get())
        sql = "SELECT * FROM student WHERE name = '%s'" % data_student_name
        cur.execute(sql)
        db.commit()
        results = cur.fetchall()

        show_all_student_root = tk.Tk()
        show_all_student_root.title("查询结果")

        columns = ['ID', 'Name', 'Age', 'Sex', 'Class']
        tree = ttk.Treeview(show_all_student_root, show='headings', columns=columns)

        for col in columns:
            tree.heading(col, text=col)

        for row in results:
            tree.insert('', 'end', values=row)

        tree.pack()

    ok_button = tk.Button(search_studen_root, text="确认", font=("微软雅黑 -20"), command=button_ok)
    Exit_Button = tk.Button(search_studen_root, text="退出", font=("微软雅黑 -20"),
                            command=search_studen_root.destroy)
    ok_button.place(x=75, y=350, height=40, width=200)
    Exit_Button.place(x=325, y=350, height=40, width=200)


# 按班级查找
def search_student_class():
    search_studen_root = tk.Tk()
    search_studen_root.title("查找学生-班级")
    search_studen_root.config(width=600, height=600)

    search_student_name = tk.StringVar(search_studen_root, value='')
    laber_sch_student_name = tk.Label(search_studen_root, text='学生班级', font=("微软雅黑 -20"))
    laber_sch_student_name.place(x=200, y=100, height=40, width=200)
    enty_sch_student_name = tk.Entry(search_studen_root, textvariable=search_student_name)
    enty_sch_student_name.place(x=200, y=150, height=40, width=200)

    def button_ok():
        db, cur = sql_link()
        data_student_name = str(enty_sch_student_name.get())
        sql = "SELECT * FROM student WHERE class = '%s'" % data_student_name
        cur.execute(sql)
        db.commit()
        results = cur.fetchall()

        show_all_student_root = tk.Tk()
        show_all_student_root.title("查询结果")

        columns = ['ID', 'Name', 'Age', 'Sex', 'Class']
        tree = ttk.Treeview(show_all_student_root, show='headings', columns=columns)

        for col in columns:
            tree.heading(col, text=col)

        for row in results:
            tree.insert('', 'end', values=row)

        tree.pack()

    ok_button = tk.Button(search_studen_root, text="确认", font=("微软雅黑 -20"), command=button_ok)
    Exit_Button = tk.Button(search_studen_root, text="退出", font=("微软雅黑 -20"),
                            command=search_studen_root.destroy)
    ok_button.place(x=75, y=350, height=40, width=200)
    Exit_Button.place(x=325, y=350, height=40, width=200)


# 查找学生菜单
def search_studen_mue():
    search_studen_root = tk.Tk()
    search_studen_root.title("查找学生")
    search_studen_root.config(width=600, height=600)

    id_button = tk.Button(search_studen_root, text="id查找", font=("微软雅黑 -20"), command=seach_student_id)
    id_button.grid(column=1, row=0)
    id_button = tk.Button(search_studen_root, text="姓名查找", font=("微软雅黑 -20"), command=seacher_studnet_name)
    id_button.grid(column=1, row=1)
    id_button = tk.Button(search_studen_root, text="班级查找", font=("微软雅黑 -20"), command=search_student_class)
    id_button.grid(column=1, row=2)


# 修改学生信息
def change_student_info():
    add_student_root = tk.Tk()
    add_student_root.title("修改学生信息")
    add_student_root.config(width=600, height=600)

    messagebox.showwarning("警告", "请先查询学生学号！")

    student_id = tkinter.StringVar(add_student_root, value='')
    student_name = tkinter.StringVar(add_student_root, value='')
    student_age = tkinter.StringVar(add_student_root, value='')
    student_sex = tkinter.StringVar(add_student_root, value='')
    student_class = tkinter.StringVar(add_student_root, value='')

    labelstudent_name = tk.Label(add_student_root, text='学生姓名', font=("微软雅黑 -20"))
    labelstudent_id = tk.Label(add_student_root, text='学号', font=("微软雅黑 -20"))
    labelstudent_age = tk.Label(add_student_root, text='年龄', font=("微软雅黑 -20"))
    labelstudent_sex = tk.Label(add_student_root, text='性别', font=("微软雅黑 -20"))
    labelstudent_class = tk.Label(add_student_root, text='班级', font=("微软雅黑 -20"))

    labelstudent_id.place(x=25, y=100, height=40, width=200)
    labelstudent_name.place(x=25, y=200, height=40, width=200)
    labelstudent_age.place(x=225, y=100, height=40, width=200)
    labelstudent_sex.place(x=225, y=200, height=40, width=200)
    labelstudent_class.place(x=400, y=100, height=40, width=200)

    entrystudent_name = tk.Entry(add_student_root, textvariable=student_name)
    entrystudent_id = tk.Entry(add_student_root, textvariable=student_id)
    entrystudent_age = tk.Entry(add_student_root, textvariable=student_age)
    entrystudent_sex = tk.Entry(add_student_root, textvariable=student_sex)
    entrystudent_class = tk.Entry(add_student_root, textvariable=student_class)

    entrystudent_id.place(x=25, y=150, height=40, width=200)
    entrystudent_name.place(x=25, y=250, height=40, width=200)
    entrystudent_age.place(x=225, y=150, height=40, width=200)
    entrystudent_sex.place(x=225, y=250, height=40, width=200)
    entrystudent_class.place(x=400, y=150, height=40, width=200)

    def Button_ok():
        flag = 0

        db, cur = sql_link()
        data_student_id = str(entrystudent_id.get())
        data_student_name = str(entrystudent_name.get())
        data_student_age = str(entrystudent_age.get())
        data_student_sex = str(entrystudent_sex.get())
        data_student_class = str(entrystudent_class.get())
        search = cur.execute("SELECT * FROM student WHERE id = %s;",
                             data_student_id)
        if (search > 0):
            flag = 1
        else:
            flag = 0
        if (flag != 0):
            try:
                sql1 = "UPDATE student SET name = '%s', age = %s, sex = '%s', " \
                       "class = '%s' WHERE id = %s" % (
                       data_student_name, data_student_age, data_student_sex, data_student_class, data_student_id)

                cur.execute(sql1)
                db.commit()
                messagebox.showinfo(title="恭喜", message="修改成功!!!")
                add_student_root.destroy()
            except:
                messagebox.showerror(message='修改失败')
        else:
            messagebox.showerror(title="error", message="该学生不存在！")

    ok_button = tk.Button(add_student_root, text="确认", font=("微软雅黑 -20"), command=Button_ok)
    Exit_Button = tk.Button(add_student_root, text="退出", font=("微软雅黑 -20"),
                            command=add_student_root.destroy)
    ok_button.place(x=75, y=350, height=40, width=200)
    Exit_Button.place(x=325, y=350, height=40, width=200)


# 删除学生
def delet_student():
    delet_manager_root = tk.Tk()
    delet_manager_root.title("删除学生")
    delet_manager_root.config(width=600, height=600)

    manager_name = tk.StringVar(delet_manager_root, value='')

    labelmanager_name = tk.Label(delet_manager_root, text="学生学号：", font=("微软雅黑 -20"))

    labelmanager_name.place(x=200, y=100, height=40, width=200)

    entrymanager_name = tk.Entry(delet_manager_root, textvariable=manager_name)

    entrymanager_name.place(x=200, y=150, height=40, width=200)

    def Button_ok():
        flag = 0
        db, cur = sql_link()
        data_manger_name = str(entrymanager_name.get())

        search = cur.execute("SELECT * FROM student WHERE id = " + data_manger_name + ";")
        if search > 0:
            flag = 1
        else:
            flag = 0

        if flag == 1:
            try:
                cur.execute("DELETE FROM student WHERE id = " + data_manger_name + ";")
                db.commit()
                messagebox.showinfo("信息", "删除成功！")
            except:
                messagebox.showerror(message="删除失败！")
        else:
            messagebox.showerror("错误", "没有找到该学生！")

    ok_button = tk.Button(delet_manager_root, text="确定", font=("微软雅黑 -20"), command=Button_ok)
    ok_button.place(x=75, y=350, height=40, width=200)
    quit_bt = tk.Button(delet_manager_root, text="退出", font=("微软雅黑 -20"), command=delet_manager_root.quit)
    quit_bt.place(x=325, y=350, height=40, width=200)


# 新建管理员
def create_manager():
    create_manager_root = tk.Tk()
    create_manager_root.title("管理员创建")
    create_manager_root.config(width=600, height=600)

    manager_name = tkinter.StringVar(create_manager_root, value='')
    manager_code = tkinter.StringVar(create_manager_root, value='')

    labelmanager_name = tk.Label(create_manager_root, text='管理员ID注册', font=("微软雅黑 -20"))
    labelmanager_code = tk.Label(create_manager_root, text='管理员密码设置', font=("微软雅黑 -20"))

    labelmanager_name.place(x=200, y=100, height=40, width=200)
    labelmanager_code.place(x=200, y=200, height=40, width=200)

    entrymanager_name = tk.Entry(create_manager_root, textvariable=manager_name)
    entrymanager_code = tk.Entry(create_manager_root, textvariable=manager_code)
    entrymanager_name.place(x=200, y=150, height=40, width=200)
    entrymanager_code.place(x=200, y=250, height=40, width=200)

    def Button_ok():
        flag = 0
        db, cur = sql_link()
        data_manager_name = str(entrymanager_name.get())
        data_manager_code = str(entrymanager_code.get())
        search = cur.execute("SELECT * FROM user WHERE name = %s AND password = %s",
                             (data_manager_name, data_manager_code))
        if (search > 0):
            flag = 1
        else:
            flag = 0
        if (flag == 0):
            try:
                sql1 = "INSERT INTO manager(name,password)"
                sql1 += "VALUES('%s', '%s')" % (data_manager_name, data_manager_code)
                cur.execute(sql1)
                db.commit()
                messagebox.showinfo(title="恭喜", message="注册成功!!!")
                create_manager_root.destroy()
            except:
                messagebox.showerror(message='注册失败')
        else:
            messagebox.showerror(title="error", message="该用户名已存在！")

    ok_button = tk.Button(create_manager_root, text="确认", font=("微软雅黑 -20"), command=Button_ok)
    Exit_Button = tk.Button(create_manager_root, text="退出", font=("微软雅黑 -20"),
                            command=create_manager_root.destroy)
    ok_button.place(x=75, y=350, height=40, width=200)
    Exit_Button.place(x=325, y=350, height=40, width=200)


# 删除管理员
def delet_manager():
    delet_manager_root = tk.Tk()
    delet_manager_root.title("删除管理员")
    delet_manager_root.config(width=600, height=600)

    manager_name = tk.StringVar(delet_manager_root, value='')

    labelmanager_name = tk.Label(delet_manager_root, text="管理员名：", font=("微软雅黑 -20"))

    labelmanager_name.place(x=200, y=100, height=40, width=200)

    entrymanager_name = tk.Entry(delet_manager_root, textvariable=manager_name)

    entrymanager_name.place(x=200, y=150, height=40, width=200)

    def Button_ok():
        flag = 0
        db, cur = sql_link()
        data_manger_name = str(entrymanager_name.get())

        search = cur.execute("SELECT * FROM manager WHERE name = '" + data_manger_name + "';")
        if search > 0:
            flag = 1
        else:
            flag = 0

        if flag == 1:
            try:
                cur.execute("DELETE FROM manager WHERE name = '" + data_manger_name + "';")
                db.commit()
                messagebox.showinfo("信息", "删除成功！")
            except:
                messagebox.showerror(message="删除失败！")
        else:
            messagebox.showerror("错误", "没有找到该管理员！")

    ok_button = tk.Button(delet_manager_root, text="确定", font=("微软雅黑 -20"), command=Button_ok)
    ok_button.place(x=75, y=350, height=40, width=200)
    quit_bt = tk.Button(delet_manager_root, text="退出", font=("微软雅黑 -20"), command=delet_manager_root.quit)
    quit_bt.place(x=325, y=350, height=40, width=200)


# 创建用户
def create_user():
    create_user_root = tk.Tk()
    create_user_root.title("用户创建")
    create_user_root.config(width=600, height=600)

    user_name = tkinter.StringVar(create_user_root, value='')
    user_code = tkinter.StringVar(create_user_root, value='')

    labeluser_name = tk.Label(create_user_root, text='用户名：', font=("微软雅黑 -20"))
    labeluser_code = tk.Label(create_user_root, text='密码：', font=("微软雅黑 -20"))

    labeluser_name.place(x=200, y=100, height=40, width=200)
    labeluser_code.place(x=200, y=200, height=40, width=200)

    entryuser_name = tk.Entry(create_user_root, textvariable=user_name)
    entryuser_code = tk.Entry(create_user_root, textvariable=user_code)
    entryuser_name.place(x=200, y=150, height=40, width=200)
    entryuser_code.place(x=200, y=250, height=40, width=200)

    def Button_ok():
        flag = 0
        db, cur = sql_link()
        data_user_name = str(entryuser_name.get())
        data_user_code = str(entryuser_code.get())
        search = cur.execute("SELECT * FROM user WHERE name = %s AND password = %s",
                             (data_user_name, data_user_code))
        if (search > 0):
            flag = 1
        else:
            flag = 0
        if (flag == 0):
            try:
                sql1 = "INSERT INTO user(name,password)"
                sql1 += "VALUES('%s', '%s')" % (data_user_name, data_user_code)
                cur.execute(sql1)
                db.commit()
                messagebox.showinfo(title="恭喜", message="注册成功!!!")
                create_user_root.destroy()
            except:
                messagebox.showerror(message='注册失败')
        else:
            messagebox.showerror(title="error", message="该用户名已存在！")

    ok_button = tk.Button(create_user_root, text="确认", font=("微软雅黑 -20"), command=Button_ok)
    Exit_Button = tk.Button(create_user_root, text="退出", font=("微软雅黑 -20"),
                            command=create_user_root.destroy)
    ok_button.place(x=75, y=350, height=40, width=200)
    Exit_Button.place(x=325, y=350, height=40, width=200)


# 删除用户
def delet_user():
    delet_user_root = tk.Tk()
    delet_user_root.title("删除管理员")
    delet_user_root.config(width=600, height=600)

    user_name = tk.StringVar(delet_user_root, value='')

    labeluser_name = tk.Label(delet_user_root, text="用户名：", font=("微软雅黑 -20"))

    labeluser_name.place(x=200, y=100, height=40, width=200)

    entryuser_name = tk.Entry(delet_user_root, textvariable=user_name)

    entryuser_name.place(x=200, y=150, height=40, width=200)

    def Button_ok():
        flag = 0
        db, cur = sql_link()
        data_manger_name = str(entryuser_name.get())

        search = cur.execute("SELECT * FROM user WHERE name = '" + data_manger_name + "';")
        if search > 0:
            flag = 1
        else:
            flag = 0

        if flag == 1:
            try:
                cur.execute("DELETE FROM user WHERE name = '" + data_manger_name + "';")
                db.commit()
                messagebox.showinfo("信息", "删除成功！")
            except:
                messagebox.showerror(message="删除失败！")
        else:
            messagebox.showerror("错误", "没有找到该用户！")

    ok_button = tk.Button(delet_user_root, text="确定", font=("微软雅黑 -20"), command=Button_ok)
    ok_button.place(x=75, y=350, height=40, width=200)
    quit_bt = tk.Button(delet_user_root, text="退出", font=("微软雅黑 -20"), command=delet_user_root.quit)
    quit_bt.place(x=325, y=350, height=40, width=200)


# 管理员面板
def manager_table():
    window = tk.Tk()
    window.resizable(False, False)
    window.minsize(600, 500)
    window.maxsize(600, 500)
    window.title("管理员面板")
    chuang_jian = tk.Button(window, text="创建管理员", command=create_manager)
    chuang_jian.grid(column=1, row=0)
    chuang_jian = tk.Button(window, text="删除管理员", command=delet_manager)
    chuang_jian.grid(column=1, row=1)
    chuang_jian = tk.Button(window, text="创建用户", command=create_user)
    chuang_jian.grid(column=1, row=2)
    chuang_jian = tk.Button(window, text="删除用户", command=delet_user)
    chuang_jian.grid(column=1, row=3)
    chuang_jian = tk.Button(window, text="添加学生", command=add_sutdent)
    chuang_jian.grid(column=1, row=4)
    chuang_jian = tk.Button(window, text="显示所有学生", command=show_all_student)
    chuang_jian.grid(column=1, row=5)
    chuang_jian = tk.Button(window, text="查找指定学生", command=search_studen_mue)
    chuang_jian.grid(column=1, row=6)
    chuang_jian = tk.Button(window, text="修改学生信息", command=change_student_info)
    chuang_jian.grid(column=1, row=7)


# 管理员登录
def manager_login():
    login_win = tk.Tk()
    login_win.title("管理员登录")
    login_win.config(width=200, height=100)

    login_name = tk.StringVar(login_win, value='')
    login_password = tk.StringVar(login_win, value='')

    labellogin_name = tk.Label(login_win, text="用户名:", font=("微软雅黑 -20"))
    labellogin_password = tk.Label(login_win, text="密码:", font=("微软雅黑 -20"))

    labellogin_name.place(x=10, y=20, height=20, width=65)
    labellogin_password.place(x=30, y=40, height=20, width=45)

    entrylogin_name = tk.Entry(login_win, textvariable=login_name)
    entrylogin_password = tk.Entry(login_win, textvariable=login_password)
    entrylogin_name.place(x=75, y=20, height=20, width=100)
    entrylogin_password.place(x=75, y=40, height=20, width=100)

    def Button_login():
        flag = 0
        db, cur = sql_link()
        data_user_name = str(entrylogin_name.get())
        data_user_password = str(entrylogin_password.get())
        search = cur.execute("SELECT * FROM manager WHERE name = %s AND password = %s",
                             (data_user_name, data_user_password))
        if (search > 0):
            flag = 1
        else:
            flag = 0

        if (flag == 0):
            messagebox.showerror("登录失败", "请检查用户名或密码是否错误！")
        else:
            manager_table()
            login_win.destroy()

    def quite():
        login_win.destroy()

    login_bt = tk.Button(login_win, text="登录", font=("微软雅黑 -20"), command=Button_login)
    exit_bt = tk.Button(login_win, text="退出", font=("微软雅黑 -20"), command=quite)

    login_bt.place(x=75, y=60, height=25, width=45)
    exit_bt.place(x=125, y=60, height=25, width=45)


def user_table():
    window = tk.Tk()
    window.resizable(False, False)
    window.minsize(600, 500)
    window.maxsize(600, 500)
    window.title("用户面板")
    chuang_jian1 = tk.Button(window, text="搜索学生", command=search_studen_mue)
    chuang_jian1.grid(column=1, row=0)
    chuang_jian2 = tk.Button(window, text="展示所有学生", command=show_all_student)
    chuang_jian2.grid(column=1, row=1)
    chuang_jian3 = tk.Button(window, text="修改学生信息", command=change_student_info)
    chuang_jian3.grid(column=1, row=2)
    chuang_jian3 = tk.Button(window, text="删除学生信息", command=delet_student)
    chuang_jian3.grid(column=1, row=3)
    chuang_jian3 = tk.Button(window, text="添加学生信息", command=add_sutdent)
    chuang_jian3.grid(column=1, row=4)



# 用户登录
def login():
    login_win = tk.Tk()
    login_win.title("登录")
    login_win.config(width=200, height=100)

    login_name = tk.StringVar(login_win, value='')
    login_password = tk.StringVar(login_win, value='')

    labellogin_name = tk.Label(login_win, text="用户名:", font=("微软雅黑 -20"))
    labellogin_password = tk.Label(login_win, text="密码:", font=("微软雅黑 -20"))

    labellogin_name.place(x=10, y=20, height=20, width=65)
    labellogin_password.place(x=30, y=40, height=20, width=45)

    entrylogin_name = tk.Entry(login_win, textvariable=login_name)
    entrylogin_password = tk.Entry(login_win, textvariable=login_password)
    entrylogin_name.place(x=75, y=20, height=20, width=100)
    entrylogin_password.place(x=75, y=40, height=20, width=100)

    def Button_login():
        flag = 0
        db, cur = sql_link()
        data_user_name = str(entrylogin_name.get())
        data_user_password = str(entrylogin_password.get())
        search = cur.execute("SELECT * FROM user WHERE name = %s AND password = %s",
                             (data_user_name, data_user_password))
        if (search > 0):
            flag = 1
        else:
            flag = 0

        if (flag == 0):
            messagebox.showerror("登录失败", "请检查用户名或密码是否错误！")
        else:
            user_table()
            login_win.destroy()

    def quite():
        login_win.destroy()

    def mg_l():
        manager_login()
        login_win.destroy()

    login_bt = tk.Button(login_win, text="登录", font=("微软雅黑 -20"), command=Button_login)
    exit_bt = tk.Button(login_win, text="退出", font=("微软雅黑 -20"), command=quite)
    manager_bt = tk.Button(login_win, text="管理员", font=("微软雅黑 -20"), command=mg_l)
    login_bt.place(x=75, y=60, height=25, width=45)
    exit_bt.place(x=125, y=60, height=25, width=45)
    manager_bt.place(x=10, y=60, height=25, width=65)


# 主窗口
root = tk.Tk()
root.resizable(False, False)
root.minsize(600, 500)
root.maxsize(600, 500)
root.title("学生管理系统")


def main_login():
    login()
    root.destroy()


test_bt = tk.Button(root, text="登录", command=main_login)
test_bt.place(x=400, y=300)

root.mainloop()
