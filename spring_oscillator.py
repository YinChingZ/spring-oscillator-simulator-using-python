import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    # 设置参数
    m = 0.5  # 质量 (kg)
    k = 10   # 弹簧常数 (N/m)
    gamma = 0.1  # 阻尼系数 (kg/s)
    x0 = 0.1  # 初始位移 (m)
    v0 = 0    # 初始速度 (m/s)
    t = np.linspace(0, 10, 500)  # 时间从0到10秒，共500个点
    
    # 求解弹簧振子的运动
    solution = solve_oscillator(m, k, gamma, x0, v0, t)
    
    # 保存求解结果
    np.savetxt('oscillator_solution_with_damping.csv', np.column_stack((t, solution[:, 0], solution[:, 1])), delimiter=',', header="Time (s), Displacement (m), Velocity (m/s)", comments='')
