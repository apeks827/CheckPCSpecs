import asyncio
import datetime
import multiprocessing
import os
import platform
import string
import subprocess
import sys
import speedtest
import tkinter as tk
from tkinter import *

import cpuinfo
import nest_asyncio
import psutil
from PIL import ImageTk
from ping3 import ping

from internal import ram_gb
from internal import speedtest_rt

nest_asyncio.apply()


# for pyinstaller
class SendeventProcess(multiprocessing.Process):
    def __init__(self, resultQueue):
        self.resultQueue = resultQueue
        multiprocessing.Process.__init__(self)
        self.start()

    def run(self):
        asyncio.run(main())
        self.resultQueue.put((1, 2))
        # print('exit process guard')


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


end_score = 0


def pc_score(score):
    global end_score
    end_score += score


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
    try:
        disk_type = subprocess.run(
            ["powershell", "-Command", "Get-PhysicalDisk | ft -AutoSize MediaType"], shell=True, capture_output=True
        )

        disk_type = str(disk_type)
        if 'SSD' in disk_type:
            if 3.8 <= ram_gb.ram_specs() < 5.8:
                label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="DarkOrange3")
                label_ram_result.grid(column=2, row=9, sticky="w")
                result = 1004
                disk_result = 1
            # print(f"Тип диска: SSD")
            else:
                result = 5
                disk_result = 1
        elif ram_gb.ram_specs() >= 7.8:
            # print("HDD or eMMC")
            disk_result = 0
        else:
            # print("HDD or eMMC")
            result = -999
            disk_result = -1

        return pc_score(result), disk_result

    except:
        result = 0
        disk_result = -2
        return pc_score(result), disk_result


# speedtest
def ethtest():
    print("Тестируем скорость интернета...")
    test_ping = round(ping('ya.ru') * 1000, 2)
    try:
        sp = speedtest.Speedtest(secure=True)
        down = round(sp.download() / (10 ** 6), 2)
        up = round(sp.upload() / (10 ** 6), 2)
        success = 1

        if down >= 20 and up >= 10:
            # Excellent
            if test_ping <= 30:
                result = 5
                eth_score = 5

            # Good
            elif test_ping <= 100:
                result = 2
                eth_score = 4

            # Average
            else:
                eth_score = 3
        else:
            # Poor
            if test_ping <= 30:
                result = 2
                eth_score = 2

            # Very poor
            elif test_ping <= 100:
                result = 1
                eth_score = 1

            # Very poor x2
            else:
                eth_score = -1
    except Exception as e:
        print("An error occurred:", e.__class__)
        try:
            sp = speedtest_rt.test_f()
            down = round(sp[0], 2)
            up = round(sp[1], 2)
            success = 1

            if down >= 20 and up >= 10:
                # Excellent
                if test_ping <= 30:
                    result = 5
                    eth_score = 5

                # Good
                elif test_ping <= 100:
                    result = 2
                    eth_score = 4

                # Average
                else:
                    eth_score = 3
            else:
                # Poor
                if test_ping <= 30:
                    result = 2
                    eth_score = 2
                # Very poor
                elif test_ping <= 100:
                    result = 1
                    eth_score = 1
                # Very poor x2
                else:
                    eth_score = -1

        # except Exception as e:
        #     print('Ошибка:\n', traceback.format_exc())
        # print("Невозможно определить скорость соединения")
        except:
            success = 0
            result = 0
            eth_score, down, up = -999, -999, -999

    return success, pc_score(result), eth_score, down, up, test_ping
    # return 1, pc_score(5), 5, 100, 100, test_ping


async def main():
    def wait_for_name():

        def start():
            username_l["text"] = "ФИО:"
            username_entry["state"] = "readonly"
            send_btn.destroy()
            username_entry.grid(column=2, row=6, sticky="w")

            # Вывод ОС
            os_res = os_info()
            os_result, os_platform = os_res[1], os_res[2]
            lable_os_pre = tk.Label(text="Версия ОС:")
            lable_os_pre.grid(column=1, row=7, sticky="e")
            if os_result == 1:
                label_os_result = tk.Label(text=f"{os_platform}", fg="green")
            elif os_result == 0:
                label_os_result = tk.Label(text=f"{os_platform}", fg="DarkOrange3")
            elif os_result == -1:
                label_os_result = tk.Label(text=f"{os_platform}", fg="red")
            label_os_result.grid(column=2, row=7, sticky="w")

            # Платформа
            arch = arch_test()
            platform_result = arch[1]
            label_arch_pre = tk.Label(text="Разрядность ОС:")
            label_arch_pre.grid(column=1, row=8, sticky="e")
            if platform_result == 1:
                label_platform_result = tk.Label(text=f"x64", fg="green")
            elif platform_result == -1:
                label_platform_result = tk.Label(text=f"x32", fg="red")
            label_platform_result.grid(column=2, row=8, sticky="w")

            # Память
            mem = memory()
            ram_result = mem[1]
            lable_ram_pre = tk.Label(text="RAM:")
            lable_ram_pre.grid(column=1, row=9, sticky="e")
            if ram_result == 1:
                label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="green")
            elif ram_result == 0:
                label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="DarkOrange3")
            else:
                label_ram_result = tk.Label(text=f"{ram_gb.ram_specs()} Gb", fg="red")
            label_ram_result.grid(column=2, row=9, sticky="w")

            # CPU
            cpu_complete_query = cpu()
            cpu_result, cpu_res = cpu_complete_query[1], cpu_complete_query[2]
            label_cpu = tk.Label(text="CPU:")
            label_cpu.grid(column=1, row=10, sticky="e")
            if cpu_result == 1:
                label_cpu_result = tk.Label(text=f"{cpu_res}", fg="green")
            elif cpu_result == 0:
                label_cpu_result = tk.Label(text=f"{cpu_res}", fg="DarkOrange3")
            else:
                label_cpu_result = tk.Label(text=f"{cpu_res}", fg="red")
            label_cpu_result.grid(column=2, row=10, sticky="w")
            # run disk check
            asyncio.run(disk_result())
            # run eth test
            asyncio.run(before_et_async())

        username_entry = tk.Entry(root, width=37)
        send_btn = Button(root, text='Сохранить', command=start)
        username_entry.grid(column=2, row=6, sticky="w")
        send_btn.grid(column=3, row=6, sticky="e")

        # Debug print('%s executed!' % do_something.__name__)

    async def et_async():
        speedtest_result = ethtest()
        if os.path.exists('random7000x7000.jpg'):
            os.remove('random7000x7000.jpg')
        label_eth = tk.Label(text="Скорость сети:")
        label_eth.grid(column=1, row=12, sticky="e")
        success = speedtest_result[0]
        eth_score, down, up, test_ping = speedtest_result[2], speedtest_result[3], speedtest_result[4], \
                                         speedtest_result[5]
        if success == 1:
            if eth_score == 5:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="green")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="green")
            elif eth_score == 4:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="green")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="DarkOrange3")
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
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="DarkOrange3")
            elif eth_score == 0:
                label_eth_result_d = tk.Label(text=f"Загрузка: {down}", fg="red")
                label_eth_result_u = tk.Label(text=f"Отдача: {up}", fg="red")
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="red")

            label_eth_result_d.grid(column=2, row=12, sticky="w")
            label_eth_result_u.grid(column=2, row=13, sticky="w")
            label_eth_result_p.grid(column=2, row=14, sticky="w")
        else:
            if test_ping <= 30:
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="green")
            elif test_ping <= 100:
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="DarkOrange3")
            elif test_ping > 100:
                label_eth_result_p = tk.Label(text=f"Пинг: {test_ping}", fg="red")
            label_eth_result_d = tk.Label(text=f"Скорость соединения определить невозможно", fg="red")
            label_eth_result_d.grid(column=2, row=12, sticky="w")
            label_eth_result_p.grid(column=2, row=13, sticky="w")
        # end score
        if end_score >= 18:
            label_pc_result = tk.Label(text="ПК соответствует требованиям", fg="green", font=("Arial", 15))
        elif end_score < 0:
            label_pc_result = tk.Label(text="ПК не соответствует требованиям", fg="red", font=("Arial", 15))
        else:
            label_pc_result = tk.Label(text="Приемлемо", fg="DarkOrange3", font=("Arial", 15))

        label_pc_result.place(x=470 / 2, y=350, anchor="center")

    async def before_et_async():
        label_eth = tk.Label(text="Скорость сети:")
        label_eth.grid(column=1, row=12, sticky="e")
        label_eth_result_d = tk.Label(text="Подождите...")
        label_eth_result_d.grid(column=2, row=12, sticky="w")
        task = asyncio.create_task(et_async())
        pending = True
        while pending:
            root.update()
            await asyncio.sleep(.01)

            done, pending = await asyncio.wait({task})

    root = Tk()
    root.title("Проверка ПК на соответствие требованиям")
    w = 480
    h = 400

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(0, 0)

    path = resource_path("icon.ico")
    path2 = resource_path("logo.png")
    root.iconbitmap(default=path)
    logo = ImageTk.PhotoImage(file=path2)

    top_logo = tk.Label(image=logo)
    top_logo.image = logo
    top_logo.place(x=10, y=0)

    # Костыль

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

    # Дата

    dt = datetime.datetime.now()
    dt_string = dt.strftime("%d/%m/%Y %H:%M:%S")
    left_date = tk.Label(text="Дата/Время:")
    left_date.grid(column=1, row=5, sticky="e")
    right_date = tk.Label(text=f"{dt_string}")
    right_date.grid(column=2, row=5, sticky="w")

    # Имя
    username_l = tk.Label(text="Введите ФИО:")
    username_l.grid(column=1, row=6, sticky="e")
    wait_for_name()

    # Disk

    async def disk_result():
        disk_result = disk()
        label_disk = tk.Label(text="Тип диска:")
        label_disk.grid(column=1, row=11, sticky="e")
        if disk_result[1] == 1:
            label_disk_result = tk.Label(text="SSD                      ", fg="green")
        elif disk_result[1] == 0:
            label_disk_result = tk.Label(text="HDD or eMMC                       ", fg="DarkOrange3")
        elif disk_result[1] == -1:
            label_disk_result = tk.Label(text="HDD or eMMC                      ", fg="red")
        else:
            label_disk_result = tk.Label(text=f"Процесс завершился некорректно, определить невозможно", fg="red")
        label_disk_result.grid(column=2, row=11, sticky="w")

    quitButton = Button(root, text="Закрыть", command=root.quit)
    quitButton.place(x=200, y=370)
    root.mainloop()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    resultQueue = multiprocessing.Queue()
    SendeventProcess(resultQueue)

# Debug
# print(f"Версия ОС: score, os_result, os_platform {os_info()}")
# print(f"Разрядность ОС: pc_score(result), platform_result) {arch_test()}")
# print(f"Память: ram_gb.ram_specs(), pc_score(result), ram_result {ram_gb.ram_specs()}, {memory()}")
# print(f"CPU: pc_score(result), cpu_result, cpu {cpu()}")
# print(f"Disk: pc_score(result), disk_result {disk()}")
# print(f"speedtest: success, pc_score(result), eth_score, down, up, test_ping {speedtest}")
