import subprocess

# 定义要执行的脚本路径
scripts = [
    # "python c:/Users/shark/Desktop/jinze/jinze_rob.py",
    "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 席常钦 --phone 17317788327 --court 3 --time 2",
    "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 陈翔   --phone 15601851930 --court 3 --time 1",
    "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 孙鸿宇 --phone 13871378861 --court 4 --time 2",
    # "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 曹彦卓 --phone 18069436311 --court 3 --time 1",
    # "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 许倩   --phone 18217505032 --court 5 --time 2",
    "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 陈武祥 --phone 17521181596 --court 4 --time 1",
    "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 高俊杰 --phone 18721554963 --court 5 --time 2",
    "python c:/Users/shark/Desktop/jinze/jinze_rob.py --usr 汤军   --phone 13576869169 --court 5 --time 1"

]

# 启动多个 CMD 窗口并执行不同的脚本
for script in scripts:
    subprocess.Popen(['cmd', '/K', script])
