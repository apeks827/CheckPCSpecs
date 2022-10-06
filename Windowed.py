import tkinter as tk
from tkinter import *
import string
import subprocess

import psutil
import win32com.client
import wmi
import platform
import cpuinfo
import speedtest
import out_color
import ram_gb
from ping3 import ping, verbose_ping
import tkinter as tk
from contextlib import redirect_stdout

pc_score = 0

bad_cpus = ['atom', 'duo', 'quad', 'dual-core', 'sempron']

# Operating system info
if platform.release() == "10" or platform.release() == "11":
    print(f"Версия ОС: {out_color.out_green(platform.release())}")
    out_color.clear_color()
    pc_score += 2
    os_result = 1
elif platform.release() == "8" or platform.release() == "8.1":
    print(f"Версия ОС: {out_color.out_yellow(platform.release())}")
    out_color.clear_color()
    pc_score += 1
    os_result = 0
else:
    print(f"Версия ОС: {out_color.out_red(platform.release())}")
    out_color.clear_color()
    pc_score -= 1
    os_result = -1

# Machine type
if platform.machine() == "AMD64":
    print(f"Разрядность ОС: {out_color.out_green('x64')}")
    out_color.clear_color()
    pc_score += 1
    platform_result = 1
else:
    print(f"Разрядность ОС: {out_color.out_red('x32')}")
    out_color.clear_color()
    platform_result = -1
    pc_score -= 999

# HARDWARE
# Memory
if ram_gb.ram_specs() >= 7.8:
    ram = print(f"Количество RAM: {out_color.out_green(ram_gb.ram_specs())} Gb")
    out_color.clear_color()
    pc_score += 5
    ram_result = 1
elif ram_gb.ram_specs() >= 5.8:
    print(f"Количество RAM: {out_color.out_yellow(ram_gb.ram_specs())} Gb")
    out_color.clear_color()
    pc_score += 2
    ram_result = 0
else:
    print(f"Количество RAM: {out_color.out_red(ram_gb.ram_specs())} Gb")
    out_color.clear_color()
    pc_score -= 999
    ram_result = -1

# CPU
cpu = cpuinfo.get_cpu_info()['brand_raw']
cores = psutil.cpu_count(logical=False)
threads = psutil.cpu_count(logical=True)
fine_name_cpu = cpu.lower().translate(str.maketrans('', '', string.punctuation)).replace(' ', '')
if [a for a in bad_cpus if a in fine_name_cpu]:
    print(f"CPU: {out_color.out_red(cpu)}")
    out_color.clear_color()
    pc_score -= 999
    cpu_result = -1
else:
    if cores >= 4 and threads >= 4:
        print(f"CPU: {out_color.out_green(cpu)}")
        out_color.clear_color()
        pc_score += 5
        cpu_result = 1
    elif cores >= 2 and threads >= 4:
        print(f"CPU: {out_color.out_yellow(cpu)}")
        out_color.clear_color()
        pc_score += 2
        cpu_result = 0
    else:
        print(f"CPU: {out_color.out_red(cpu)}")
        out_color.clear_color()
        pc_score -= 999
        cpu_result = -1
# Disk
wmiobj = win32com.client.GetObject("winmgmts:Win32_LogicalDisk.DeviceID='C:'")
c_drive = wmi._wmi_object(wmiobj)

DiskType = subprocess.run(["powershell", "-Command", "Get-PhysicalDisk | ft -AutoSize MediaType"],
                          capture_output=True)
DiskType = str(DiskType)
if 'SSD' in DiskType:
    print(f"Тип диска: {out_color.out_green('SSD')}")
    out_color.clear_color()
    pc_score += 5
    disk_result = 1
elif ram_gb.ram_specs() >= 7.8:
    print(out_color.out_yellow("HDD or eMMC"))
    disk_result = 0
else:
    print(out_color.out_red("HDD or eMMC"))
    pc_score -= 999
    disk_result = -1

# speedtest
print("Тестируем скорость интернета...")
test_ping = round(ping('ya.ru') * 1000, 2)
#sp = speedtest.Speedtest()
down = 100
up = 100
#down = round(sp.download() / (10 ** 6), 2)
#up = round(sp.upload() / (10 ** 6), 2)

if down >= 20 and up >= 10:
    if test_ping <= 30:
        print(f"Скорость загрузки: {out_color.out_green(down)} Mbps")
        out_color.clear_color()
        print(f"Скорость отдачи: {out_color.out_green(up)} Mbps")
        out_color.clear_color()
        print(f"Пинг: {out_color.out_green(test_ping)} ms")
        out_color.clear_color()
        pc_score += 5
        eth_score = 5
    elif test_ping <= 70:
        print(f"Скорость загрузки: {out_color.out_green(down)} Mbps")
        out_color.clear_color()
        print(f"Скорость отдачи: {out_color.out_green(up)} Mbps")
        out_color.clear_color()
        print(f"Пинг: {out_color.out_yellow(test_ping)} ms")
        out_color.clear_color()
        pc_score += 2
        eth_score = 4
    else:
        print(f"Скорость загрузки: {out_color.out_green(down)} Mbps")
        out_color.clear_color()
        print(f"Скорость отдачи: {out_color.out_green(up)} Mbps")
        out_color.clear_color()
        print(f"Пинг: {out_color.out_red(test_ping)} ms")
        out_color.clear_color()
        eth_score = 3
else:
    if test_ping <= 30:
        print(f"Скорость загрузки: {out_color.out_red(down)} Mbps")
        out_color.clear_color()
        print(f"Скорость отдачи: {out_color.out_red(up)} Mbps")
        out_color.clear_color()
        print(f"Пинг: {out_color.out_green(test_ping)} ms")
        out_color.clear_color()
        pc_score += 2
        eth_score = 2
    elif test_ping <= 70:
        print(f"Скорость загрузки: {out_color.out_red(down)} Mbps")
        out_color.clear_color()
        print(f"Скорость отдачи: {out_color.out_red(up)} Mbps")
        out_color.clear_color()
        print(f"Пинг: {out_color.out_yellow(test_ping)} ms")
        out_color.clear_color()
        pc_score += 1
        eth_score = 1
    else:
        print(f"Скорость загрузки: {out_color.out_red(down)} Mbps")
        out_color.clear_color()
        print(f"Скорость отдачи: {out_color.out_red(up)} Mbps")
        out_color.clear_color()
        print(f"Пинг: {out_color.out_red(test_ping)} ms")
        out_color.clear_color()
        eth_score = -1

if pc_score >= 18:
    print(out_color.out_green("ПК соответствует требованиям"))
    out_color.clear_color()
elif pc_score < 0:
    print(out_color.out_red("ПК не соответствует требованиям"))
    out_color.clear_color()
else:
    print(out_color.out_yellow("Приемлемо"))
    out_color.clear_color()
print(f"Debug: {pc_score}")
# screenshot = pyautogui.screenshot('C:/users/sergmakarov/Desktop/screenshot.png')

root = Tk()
root.title("Проверка ПК на соответствие требованиям")
root.columnconfigure(2)
w = 460
h = 250

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

x = (sw - w) / 2
y = (sh - h) / 2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
#Вывод ОС
lable_os_pre = tk.Label(text="Версия ОС:")
lable_os_pre.grid(column=0, row=0, sticky="e")
if os_result == 1:
    label_os_result = tk.Label(text=f"{platform.release()}", fg="green")
elif os_result == 0:
    label_os_result = tk.Label(text=f"{platform.release()}", fg="yellow")
else:
    label_os_result = tk.Label(text=f"{platform.release()}", fg="red")
label_os_result.grid(column=1,row=0, sticky="w")

#Платформа
label_arch_pre = tk.Label(text="Разрядность ОС:")
label_arch_pre.grid(column=0, row=1, sticky="e")
if platform_result == 1:
    label_platform_result = tk.Label(text=f"x64", fg="green")
else:
    label_platform_result = tk.Label(text=f"x32", fg="red")
label_platform_result.grid(column=1,row=1, sticky="w")

#Память
lable_ram_pre = tk.Label(text="RAM:")
lable_ram_pre.grid(column=0, row=2, sticky="e")
if ram_result == 1:
    label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="green")
elif ram_result == 0:
    label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="yellow")
else:
    label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="red")
label_ram_result.grid(column=1,row=2, sticky="w")

#CPU
label_cpu = tk.Label(text="CPU:")
label_cpu.grid(column=0, row=3, sticky="e")
if cpu_result == 1:
    label_cpu_result = tk.Label(text=f"{cpu}", fg="green")
elif cpu_result == 0:
    label_cpu_result = tk.Label(text=f"{cpu}", fg="yellow")
else:
    label_cpu_result = tk.Label(text=f"{cpu}", fg="red")
label_cpu_result.grid(column=1,row=3, sticky="w")

#Disk
#disk_result = -1
label_disk = tk.Label(text="Тип диска:")
label_disk.grid(column=0, row=4, sticky="e")
if disk_result == 1:
    label_disk_result = tk.Label(text=f"SSD", fg="green")
elif disk_result == 0:
    label_disk_result = tk.Label(text=f"HDD or eMMC", fg="yellow")
else:
    label_disk_result = tk.Label(text=f"HDD or eMMC", fg="red")
label_disk_result.grid(column=1,row=4, sticky="w")

#Speedtest
label_eth = tk.Label(text="Тип диска:")
label_eth.grid(column=0, row=5, sticky="e")
if eth_score >= 3:
    label_eth_result_d = tk.Label(text=f"SSD", fg="green")
    label_eth_result_u = tk.Label(text=f"SSD", fg="green")
    label_eth_result_d
elif disk_result == 2 or disk_result == 1:
    label_disk_result = tk.Label(text=f"HDD or eMMC", fg="yellow")
else:
    label_disk_result = tk.Label(text=f"HDD or eMMC", fg="red")
label_disk_result.grid(column=1,row=5, sticky="w")


quitButton = Button(root, text="Закрыть", command=root.quit)
quitButton.place(x=200, y=150)
root.mainloop()
