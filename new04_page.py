import new03_itemcf_run as item
import tkinter as tk

def choose_user():
    user_id = int(user.get())  # 获取tk.Entry中的用户数据并转换为整数
    return user_id
def choose_num():
    num_id = int(number.get())
    return num_id
def start_comm():
    item.main()

def restart_comm():
    output_text.delete(1.0, tk.END)
    user.delete(0, tk.END)
    number.delete(0, tk.END)

def result(user_id,recommendations):
    recommendation = item.get_recommendations(user_id,recommendations)

    output_text.insert(tk.END, recommendation + '\n')

# 创建窗口
window = tk.Tk()
window.title("基于K-Means的超市客户分组研究与实现")

user_label = tk.Label(window, text="请输入用户id：")
user = tk.Entry(window, width=15)

number_label = tk.Label(window, text="请输入推荐商品个数：")
number = tk.Entry(window, width=15)

startbut = tk.Button(window, text="开始推荐", width=15, height=2, command=start_comm)
restartbut = tk.Button(window, text="重新选择", width=15, height=2, command=restart_comm)

# 创建输出框
output_text = tk.Text(window, width=50, height=10)

# 将元素放置到窗口上
user_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
user.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

number_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
number.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

startbut.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
restartbut.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

output_text.grid(row=3, columnspan=2, padx=5, pady=5, sticky=tk.W)

# 运行主循环
window.mainloop()

