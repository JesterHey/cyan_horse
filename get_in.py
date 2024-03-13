import tkinter as tk
from tkinter import ttk
import json


def create_login_window():
    # 创建主窗口
    root = tk.Tk()
    root.title("Integrated Window")

    # 设置窗口的初始大小并居中显示
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # 用户名和密码变量
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    # 下拉选择框的选项
    options = ['网络文明志愿者', '团学干部', '大学生心理健康教育', '入党积极分子']

    # 创建下拉选择框
    combo_label = tk.Label(root, text="选择学习类型", font=('Helvetica', 12))
    combo_label.pack(pady=(10, 5))

    combo = ttk.Combobox(root, values=options, width=15, state="readonly")
    combo.pack(pady=(0, 20))  # pady增加垂直外边距，有助于在窗口中垂直居中

    # 创建用户名和密码的标签和输入框
    username_label = tk.Label(root, text="账号", font=('Helvetica', 12))
    username_label.pack(pady=(5, 5))

    username_entry = tk.Entry(
        root, textvariable=username_var, font=('Helvetica', 12))
    username_entry.pack(pady=(0, 10))

    password_label = tk.Label(root, text="密码", font=('Helvetica', 12))
    password_label.pack(pady=(5, 5))

    password_entry = tk.Entry(
        root, textvariable=password_var, font=('Helvetica', 12), show="*")
    password_entry.pack(pady=(0, 20))

    # 确定按钮的事件处理函数
    def submit_action():
        username = username_var.get().upper()
        password = password_var.get()
        study_type = combo.get()
        if study_type not in options:
            return
        with open('info.json', 'w') as f:
            json.dump({'username': username, 'password': password,
                      'study_type': study_type}, f)
        root.destroy()

    submit_button = tk.Button(root, text="提交", command=submit_action)
    submit_button.pack(pady=(10, 0))

    # 运行主循环
    root.mainloop()


# 调用函数以创建和显示登录窗口
if __name__ == "__main__":
    create_login_window()
