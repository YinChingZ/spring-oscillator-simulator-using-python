import numpy as np
from scipy.integrate import odeint
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation

# 定义微分方程：带有阻尼的弹簧振子运动方程
def spring_oscillator(y, t, m, k, gamma):
    x, v = y
    dxdt = v
    dvdt = -(k / m) * x - (gamma / m) * v  # 只有弹簧力和阻尼力
    return [dxdt, dvdt]

# 求解弹簧振子运动方程
def solve_oscillator(m, k, gamma, x0, v0, t):
    y0 = [x0, v0]
    solution = odeint(spring_oscillator, y0, t, args=(m, k, gamma))
    return solution

# 创建动画展示
def create_animation(m, k, gamma, t, frame):
    # 初始位移和速度
    x0 = 0.1  # 初始位移 (m)
    v0 = 0    # 初始速度 (m/s)

    # 求解弹簧振子运动
    solution = solve_oscillator(m, k, gamma, x0, v0, t)

    # 设置绘图窗口
    fig, ax = plt.subplots(figsize=(8, 6))  # 只创建一个子图

    # 第一个子图：动画展示
    ax.set_xlim(-0.2, 0.2)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Displacement (m)")
    ax.set_title(f"Spring Oscillator with Damping: m={m}kg, k={k}N/m, gamma={gamma}kg/s")
    ax.grid(True)

    # 创建点和线条
    point, = ax.plot([], [], 'bo', markersize=10)  # 质点
    line, = ax.plot([], [], 'r-', lw=2)           # 弹簧

    # 第二个子图：位移随时间变化的图表
    fig2, ax2 = plt.subplots(figsize=(8, 6))  # 创建单独的图表用于显示位移 vs 时间
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-0.2, 0.2)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Displacement (m)")
    ax2.set_title("Displacement vs Time")
    ax2.grid(True)
    ax2.plot(t, solution[:, 0], 'b-', label="Displacement")
    ax2.legend()

    # 实时绘制位移数据
    line_data, = ax2.plot([], [], 'g-', label="Real-time Data")  # 用绿色线显示实时数据
    ax2.legend()

    # 更新函数，用于动画更新
    def update(frame):
        # 更新质点位置，y 坐标为弹簧的位移
        point.set_data([0], [solution[frame, 0]])
        # 更新弹簧的位置，垂直方向振动
        line.set_data([0, 0], [0, solution[frame, 0]])  # 更新弹簧的伸缩

        # 更新右侧图表的实时数据
        time_data = t[:frame+1]
        displacement_data = solution[:frame+1, 0]
        line_data.set_data(time_data, displacement_data)

        return point, line, line_data

    # 创建动画
    ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

    # 在Tkinter界面中嵌入图形
    def draw_canvas():
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT)  # 将动画画布放在左边

        canvas2 = FigureCanvasTkAgg(fig2, master=frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.RIGHT)  # 将位移-时间图放在右边

    draw_canvas()

# 创建仅显示实验结果的额外窗口
def create_result_window(m, k, gamma, t):
    # 初始位移和速度
    x0 = 0.1  # 初始位移 (m)
    v0 = 0    # 初始速度 (m/s)

    # 求解弹簧振子运动
    solution = solve_oscillator(m, k, gamma, x0, v0, t)

    # 创建结果窗口
    result_window = tk.Toplevel()  # 新建一个窗口
    result_window.title("Spring Oscillator Result")

    # 创建实验结果图表
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-0.2, 0.2)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Displacement (m)")
    ax2.set_title("Displacement vs Time")
    ax2.grid(True)
    ax2.plot(t, solution[:, 0], 'b-', label="Displacement")
    ax2.legend()

    # 在新窗口嵌入图表
    canvas2 = FigureCanvasTkAgg(fig2, master=result_window)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

    # 添加导航工具栏，仅在此窗口显示
    toolbar = NavigationToolbar2Tk(canvas2, result_window)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)

# 用于运行模拟的函数
def run_simulation():
    try:
        m = float(entry_mass.get())  # 获取质量输入
        k = float(entry_spring.get())  # 获取弹簧常数输入
        gamma = float(entry_damping.get())  # 获取阻尼系数输入
        t = np.linspace(0, 10, 500)  # 时间从0到10秒，共500个点

        # 清空之前的图表和动画
        clear_previous_content()

        # 创建并展示新的动画和图表
        create_animation(m, k, gamma, t, frame)

        # 创建新的结果窗口
        create_result_window(m, k, gamma, t)

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numerical values for mass, spring constant, and damping coefficient.")

# 清除旧的图表和动画
def clear_previous_content():
    for widget in frame.winfo_children():
        widget.destroy()

# 结束应用程序
def close_window():
    root.quit()

# 创建GUI界面
def create_gui():
    global frame, entry_mass, entry_spring, entry_damping, root

    root = tk.Tk()
    root.title("Spring Oscillator Simulation with Damping (Animation)")

    # 创建一个框架来放置matplotlib画布
    frame = tk.Frame(root)
    frame.pack()

    # 标签和输入框
    label_mass = tk.Label(root, text="Mass (kg):")
    label_mass.pack(padx=10, pady=10)

    entry_mass = tk.Entry(root)
    entry_mass.pack(padx=10, pady=10)

    label_spring = tk.Label(root, text="Spring Constant (N/m):")
    label_spring.pack(padx=10, pady=10)

    entry_spring = tk.Entry(root)
    entry_spring.pack(padx=10, pady=10)

    label_damping = tk.Label(root, text="Damping Coefficient (kg/s):")
    label_damping.pack(padx=10, pady=10)

    entry_damping = tk.Entry(root)
    entry_damping.pack(padx=10, pady=10)

    # 运行按钮
    button_run = tk.Button(root, text="Run Simulation", command=run_simulation)
    button_run.pack(pady=20)

    # 结束按钮
    button_end = tk.Button(root, text="End Simulation", command=close_window)
    button_end.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
