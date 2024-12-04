import numpy as np
import matplotlib.pyplot as plt

# 读取弹簧振子模拟结果
def plot_oscillator_results(filename):
    # 使用逗号分隔符读取数据
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    time = data[:, 0]
    displacement = data[:, 1]

    # 绘制位移随时间的变化图
    plt.figure(figsize=(8, 6))
    plt.plot(time, displacement, label="Displacement (m)", color="b")
    plt.title("Spring Oscillator with Damping: Displacement vs Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Displacement (meters)")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # 读取并绘制结果
    plot_oscillator_results("oscillator_solution_with_damping.csv")
