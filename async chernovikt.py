import tkinter as tk
import sys
import os
import string
import subprocess
from turtle import update

import psutil
import win32com.client
import wmi
import threading
import platform
import cpuinfo
import speedtest
import asyncio
from tkinter import *
from ping3 import ping
from internal import ram_gb
from PIL import ImageTk

end_score = 0


def pc_score(score):
    global end_score
    end_score += score


print("Работаем...")


# Operating system info
def os_info():
    os_platform = platform.release()

    if os_platform == "10" or os_platform == "11":

        result = 2
        os_result = 1
    elif os_platform == "8" or os_platform == "8.1":
        # print(f"Версия ОС: {os_platform}")
        result = 1
        os_result = 0
    else:
        # print(f"Версия ОС: {os_platform}")
        result = -1
        os_result = -1
    return pc_score(result), os_result, os_platform


# Arch
def arch_test():
    if platform.machine() == "AMD64":
        # print(f"Разрядность ОС: x64")
        result = 1
        platform_result = 1
    else:
        # print(f"Разрядность ОС: x32")
        platform_result = -1
        result = -999
    return pc_score(result), platform_result


# Memory
def memory():
    if ram_gb.ram_specs() >= 7.8:
        # print(f"Количество RAM: {ram_gb.ram_specs()} Gb")
        result = 5
        ram_result = 1
    elif ram_gb.ram_specs() >= 5.8:
        # print(f"Количество RAM: {ram_gb.ram_specs()} Gb")
        result = 2
        ram_result = 0
    else:
        # print(f"Количество RAM: {ram_gb.ram_specs()} Gb")
        result = -999
        ram_result = -1
    return pc_score(result), ram_result


# CPU
def cpu():
    bad_cpus = ['atom', 'duo', 'quad', 'dual-core', 'sempron']
    cpu = cpuinfo.get_cpu_info()['brand_raw']
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    fine_name_cpu = cpu.lower().translate(str.maketrans('', '', string.punctuation)).replace(' ', '')
    if [a for a in bad_cpus if a in fine_name_cpu]:
        # print(f"CPU: {cpu}")
        result = -999
        cpu_result = -1
    else:
        if cores >= 4 and threads >= 4:
            # print(f"CPU: {cpu}")

            result = 5
            cpu_result = 1
        elif cores >= 2 and threads >= 4:
            # print(f"CPU: {cpu}")

            result = 2
            cpu_result = 0
        else:
            # print(f"CPU: {cpu}")

            result = -999
            cpu_result = -1
    return pc_score(result), cpu_result, cpu


# Disk
def disk():
    disk_type = subprocess.run(
        ["powershell", "-Command", "Get-PhysicalDisk | ft -AutoSize MediaType"], capture_output=True
    )

    disk_type = str(disk_type)
    if 'SSD' in disk_type:
        # print(f"Тип диска: SSD")
        result = 5
        disk_result = 1
    elif ram_gb.ram_specs() >= 7.8:
        # print("HDD or eMMC")
        disk_result = 0
    else:
        # print("HDD or eMMC")
        result = 999
        disk_result = -1

    return pc_score(result), disk_result


# speedtest
def ethtest():
    # print("Тестируем скорость интернета...")
    test_ping = round(ping('ya.ru') * 1000, 2)
    # try:
    #     sp = speedtest.Speedtest()
    #     # down = 100
    #     # up = 100
    #     down = round(sp.download() / (10 ** 6), 2)
    #     up = round(sp.upload() / (10 ** 6), 2)
    #     success = 1
    #
    #     if down >= 20 and up >= 10:
    #         if test_ping <= 30:
    #             # print(f"Скорость загрузки: {down} Mbps")
    #             #
    #             # print(f"Скорость отдачи: {up} Mbps")
    #             #
    #             # print(f"Пинг: {test_ping} ms")
    #
    #             result = 5
    #             eth_score = 5
    #         elif test_ping <= 70:
    #             # print(f"Скорость загрузки: {down} Mbps")
    #             #
    #             # print(f"Скорость отдачи: {up} Mbps")
    #             #
    #             # print(f"Пинг: {test_ping} ms")
    #
    #             result = 2
    #             eth_score = 4
    #         else:
    #             # print(f"Скорость загрузки: {down} Mbps")
    #             #
    #             # print(f"Скорость отдачи: {up} Mbps")
    #             #
    #             # print(f"Пинг: {test_ping} ms")
    #
    #             eth_score = 3
    #     else:
    #         if test_ping <= 30:
    #             # print(f"Скорость загрузки: {down} Mbps")
    #             # print(f"Скорость отдачи: {up} Mbps")
    #             # print(f"Пинг: {test_ping} ms")
    #             result = 2
    #             eth_score = 2
    #         elif test_ping <= 70:
    #             # print(f"Скорость загрузки: {down} Mbps")
    #             # print(f"Скорость отдачи: {up} Mbps")
    #             # print(f"Пинг: {test_ping} ms")
    #             result = 1
    #             eth_score = 1
    #
    #         else:
    #             # print(f"Скорость загрузки: {down} Mbps")
    #             # print(f"Скорость отдачи: {up} Mbps")
    #             # print(f"Пинг: {test_ping} ms")
    #             eth_score = -1
    #
    # except:
    #     # print("Невозможно определить скорость соединения")
    #     success = 0
    #     result = 0
    #     eth_score, down, up = -999, -999, -999

    # return success, pc_score(result), eth_score, down, up, test_ping
    return 1, pc_score(5), 5, 100, 100, test_ping


class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.spam();


class Window(tk.Tk):
    # Speedtest
    def __init__(self, loop):
        self.loop = loop
        self.self.root = tk.Tk()
        self.self.root.title("Проверка ПК на соответствие требованиям")
        self.root.columnconfigure(2)
        w = 485
        h = 350

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(0, 0)

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        path = resource_path("res/icon.ico")
        path2 = resource_path("res/logo.png")
        self.root.iconbitmap(default=path)
        logo = ImageTk.PhotoImage(file=path2)

        top_logo = tk.Label(image=logo)
        top_logo.image = logo
        top_logo.place(x=10, y=0)
        label2 = tk.Label(text="")
        label3 = tk.Label(text="")
        label4 = tk.Label(text="")
        label5 = tk.Label(text="")
        label6 = tk.Label(text="")
        label2.grid(column=0, row=0)
        label3.grid(column=0, row=1)
        label4.grid(column=0, row=2)
        label5.grid(column=0, row=3)
        label6.grid(column=0, row=4)
        # Вывод ОС
        os_res = os_info()
        os_result, os_platform = os_res[1], os_res[2]
        lable_os_pre = tk.Label(text="Версия ОС:")
        lable_os_pre.grid(column=1, row=5, sticky="e")
        if os_result == 1:
            label_os_result = tk.Label(text=f"{os_platform}", fg="green")
        elif os_result == 0:
            label_os_result = tk.Label(text=f"{os_platform}", fg="yellow")
        elif os_result == -1:
            label_os_result = tk.Label(text=f"{os_platform}", fg="red")
        label_os_result.grid(column=2, row=5, sticky="w")

        # Платформа
        arch = arch_test()
        platform_result = arch[1]
        label_arch_pre = tk.Label(text="Разрядность ОС:")
        label_arch_pre.grid(column=1, row=6, sticky="e")
        if platform_result == 1:
            label_platform_result = tk.Label(text=f"x64", fg="green")
        elif platform_result == -1:
            label_platform_result = tk.Label(text=f"x32", fg="red")
        label_platform_result.grid(column=2, row=6, sticky="w")

        # Память
        mem = memory()
        ram_result = mem[1]
        lable_ram_pre = tk.Label(text="RAM:")
        lable_ram_pre.grid(column=1, row=7, sticky="e")
        if ram_result == 1:
            label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="green")
        elif ram_result == 0:
            label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="yellow")
        else:
            label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="red")
        label_ram_result.grid(column=2, row=7, sticky="w")

        # CPU
        cpu_complete_query = cpu()
        cpu_result, cpu_res = cpu_complete_query[1], cpu_complete_query[2]
        label_cpu = tk.Label(text="CPU:")
        label_cpu.grid(column=1, row=8, sticky="e")
        if cpu_result == 1:
            label_cpu_result = tk.Label(text=f"{cpu_res}", fg="green")
        elif cpu_result == 0:
            label_cpu_result = tk.Label(text=f"{cpu_res}", fg="yellow")
        else:
            label_cpu_result = tk.Label(text=f"{cpu_res}", fg="red")
        label_cpu_result.grid(column=2, row=8, sticky="w")

        # Disk
        # disk_result = -1
        disk_result = disk()
        label_disk = tk.Label(text="Тип диска:")
        label_disk.grid(column=1, row=9, sticky="e")
        if disk_result[1] == 1:
            label_disk_result = tk.Label(text=f"SSD", fg="green")
        elif disk_result[1] == 0:
            label_disk_result = tk.Label(text=f"HDD or eMMC", fg="yellow")
        else:
            label_disk_result = tk.Label(text=f"HDD or eMMC", fg="red")
        label_disk_result.grid(column=2, row=9, sticky="w")

        # end score
        if end_score >= 18:
            label_pc_result = tk.Label(text="ПК соответствует требованиям", fg="green", font=("Arial", 15))
        elif end_score < 0:
            label_pc_result = tk.Label(text="ПК не соответствует требованиям", fg="red", font=("Arial", 15))
        else:
            label_pc_result = tk.Label(text="Приемлемо", fg="yellow", font=("Arial", 15))

        label_pc_result.place(x=470 / 2, y=290, anchor="center")

        quitButton = Button(self.root, text="Закрыть", command=self.root.quit)
        quitButton.place(x=200, y=310)

    # def _configure_bindings(self):
    #     self.bind('<F5>', lambda event: )

    async def spam(self):
        await self.do_something()
        while True:
            self.root.update()
            await asyncio.sleep(.01)
        speedtest_result = ethtest()
        label_eth = tk.Label(text="Скорость сети:")
        label_eth.grid(column=1, row=10, sticky="e")
        success = speedtest_result[0]

        if success == 1:
            eth_score, down, up, test_ping = speedtest_result[2], speedtest_result[3], speedtest_result[4], \
                                             speedtest_result[5]
            if eth_score == 5:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="green")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="green")
            elif eth_score == 4:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="green")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="yellow")
            elif eth_score == 3:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="green")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="red")
            elif eth_score == 2:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="red")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="red")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="green")
            elif eth_score == 1:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="red")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="red")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="yellow")
            elif eth_score == 0:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="red")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="red")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="red")

            label_eth_result_d.grid(column=2, row=10, sticky="w")
            label_eth_result_u.grid(column=2, row=11, sticky="w")
            label_eth_result_p.grid(column=2, row=12, sticky="w")
        else:
            label_eth_result_d = tk.Label(text=f"Скорость соединения определить невозможно", fg="red")
            label_eth_result_d.grid(column=2, row=10, sticky="w")
        await asyncio.sleep(12)
        print('%s executed!' % self.spam.__name__)

    async def do_something(self):
        label_eth = tk.Label(text="Скорость сети:")
        label_eth.grid(column=1, row=10, sticky="e")
        label_eth_result_d = tk.Label(text="Подождите...")
        label_eth_result_d.grid(column=2, row=10, sticky="w")
        print('%s executed!' % self.do_something.__name__)


asyncio.run(App().exec())

# async def run_tk(root):
#     try:
#         while True:
#             root.update()
#             await asyncio.sleep(.01)
#     except tk.TclError as e:
#         if "application has been destroyed" not in e.args[0]:
#             raise
#
# if __name__ == '__main__':
#     app = App()
#     asyncio.get_event_loop().run_until_complete(run_tk(app.exec()))
