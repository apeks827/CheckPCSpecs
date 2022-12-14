import asyncio
import datetime
import multiprocessing
import os
import platform
import string
import subprocess
import sys
import cpuinfo
import nest_asyncio
import psutil
import speedtest
import tkinter as tk
from tkinter import *
from PIL import ImageTk
from icmplib import ping
from internal import ram_gb
from internal import speedtest_rt
from internal import ping

nest_asyncio.apply()

# bug
# none ping test


# for pyinstaller
class SendeventProcess(multiprocessing.Process):
    def __init__(self, resultQueue):
        self.resultQueue = resultQueue
        multiprocessing.Process.__init__(self)
        self.start()

    def run(self):
        asyncio.run(main())
        self.resultQueue.put((1, 2))


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
    for_win11 = int(platform.version().translate(str.maketrans('', '', string.punctuation)))
    if os_platform == "10":
        if for_win11 >= 10022000:
            result = 2
            os_result = 2
        else:
            result = 2
            os_result = 1
    elif os_platform == "8" or os_platform == "8.1" or os_platform == "7":
        result = 1
        os_result = 0
    else:
        result = -999
        os_result = -1
    return pc_score(result), os_result, os_platform


# Arch
def arch_test():
    if platform.machine() == "AMD64":
        result = 1
        platform_result = 1
    else:
        platform_result = -1
        result = -999
    return pc_score(result), platform_result


# Memory
def memory():
    if ram_gb.ram_specs() >= 7.8:
        result = 5
        ram_result = 1
    elif ram_gb.ram_specs() >= 5.8:
        result = 2
        ram_result = 0
    else:
        result = -999
        ram_result = -1
    return pc_score(result), ram_result


# CPU
def cpu():
    bad_cpus = ['atom', 'duo', 'quad', 'dualcore', 'sempron']
    cpu = cpuinfo.get_cpu_info()['brand_raw']
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    fine_name_cpu = cpu.lower().translate(str.maketrans('', '', string.punctuation)).replace(' ', '')
    if [a for a in bad_cpus if a in fine_name_cpu]:
        result = -999
        cpu_result = -1
    else:
        if cores >= 4 and threads >= 4:
            result = 5
            cpu_result = 1
        elif cores >= 2 and threads >= 4:
            result = 2
            cpu_result = 0
        else:
            result = -999
            cpu_result = -1
    return pc_score(result), cpu_result, cpu


# Disk
def disk():
    ram = ram_gb.ram_specs()
    try:
        disk_type = subprocess.run(
            ["powershell", "-Command", "Get-PhysicalDisk | ft -AutoSize MediaType"],
            shell=True, capture_output=True)
        disk_type_old = subprocess.run(
            ["powershell", "-Command", 'Get-WmiObject Win32_DiskDrive'],
            shell=True, capture_output=True)

        disk_type = str(disk_type)
        disk_type_old = str(disk_type_old)
        if 'SSD' in disk_type or 'SSD' in disk_type_old:
            if 3.8 <= ram < 5.8:
                label_ram_result = tk.Label(text=f"{ram} Gb", fg="DarkOrange3")
                label_ram_result.grid(column=2, row=9, sticky="w")
                result = 1004
                disk_result = 1
            else:
                result = 5
                disk_result = 1
        # HDD or eMMC
        elif ram >= 7.8:
            result = 0
            disk_result = 0
        else:
            label_ram_result = tk.Label(text=f"{ram} Gb", fg="red")
            label_ram_result.grid(column=2, row=9, sticky="w")
            result = -999
            disk_result = -1
        return pc_score(result), disk_result

    except Exception as e:
        print("An error occurred:", e)
        if ram >= 7.8:
            disk_result = -2
            result = 0
        else:
            label_ram_result = tk.Label(text=f"{ram} Gb", fg="red")
            label_ram_result.grid(column=2, row=9, sticky="w")
            result = -999
            disk_result = -2
        return pc_score(result), disk_result


# speedtest
def check_eth(up, down, test_ping):
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
            result = 0
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
            result = 0
            eth_score = 0
    return success, pc_score(result), eth_score, down, up


def ethtest():
    sp = speedtest.Speedtest()
    down = round(sp.download() / (10 ** 6), 2)
    up = round(sp.upload() / (10 ** 6), 2)
    return down, up


def ethtest_backup():
    sp = speedtest.Speedtest(secure=True)
    down = round(sp.download() / (10 ** 6), 2)
    up = round(sp.upload() / (10 ** 6), 2)
    return down, up


def ethtest_backup_rt():
    sp = speedtest_rt.test_f()
    down = round(sp[0], 2)
    up = round(sp[1], 2)
    return down, up


def ping_test():
    try:
        ping_ya = ping.ping()
    except Exception as err:
        print(err)
        ping_ya = -999
    print(ping_ya)
    return ping_ya


def unlucky():
    success = 0
    result = 0
    eth_score = 0
    down = -999
    up = -999
    return success, pc_score(result), eth_score, down, up


async def main():
    def wait_for_name():

        def start():
            username_l["text"] = "??????:"
            username_entry["state"] = "readonly"
            send_btn.destroy()
            username_entry.grid(column=2, row=6, sticky="w")

            # ?????????? ????
            os_res = os_info()
            os_result, os_platform = os_res[1], os_res[2]
            lable_os_pre = tk.Label(text="???????????? ????:")
            lable_os_pre.grid(column=1, row=7, sticky="e")
            if os_result == 2:
                label_os_result = tk.Label(text=f"11", fg="green")
            elif os_result == 1:
                label_os_result = tk.Label(text=f"{os_platform}", fg="green")
            elif os_result == 0:
                label_os_result = tk.Label(text=f"{os_platform}", fg="DarkOrange3")
            elif os_result == -1:
                label_os_result = tk.Label(text=f"{os_platform}", fg="red")
            label_os_result.grid(column=2, row=7, sticky="w")

            # ??????????????????
            arch = arch_test()
            platform_result = arch[1]
            label_arch_pre = tk.Label(text="?????????????????????? ????:")
            label_arch_pre.grid(column=1, row=8, sticky="e")
            if platform_result == 1:
                label_platform_result = tk.Label(text=f"x64", fg="green")
            elif platform_result == -1:
                label_platform_result = tk.Label(text=f"x32", fg="red")
            label_platform_result.grid(column=2, row=8, sticky="w")

            # ????????????
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
        send_btn = Button(root, text='??????????????????', command=start)
        username_entry.grid(column=2, row=6, sticky="w")
        send_btn.grid(column=3, row=6, sticky="e")

    async def et_async():
        test_ping = ping_test()
        try:
            speedtest_result = ethtest()
        except Exception as err:
            print("err try1", err)
            try:
                speedtest_result = ethtest_backup()
            except Exception as err:
                print("err try2", err)
                try:
                    speedtest_result = ethtest_backup_rt()
                except Exception as err:
                    print("err3, exit:", err)
                    speedtest_result = unlucky()
        if os.path.exists('random7000x7000.jpg'):
            os.remove('random7000x7000.jpg')
        label_eth = tk.Label(text="???????????????? ????????:")
        label_eth.grid(column=1, row=12, sticky="e")
        finally_test = check_eth(speedtest_result[0], speedtest_result[1], test_ping)
        success = finally_test[0]
        eth_score, down, up = finally_test[2], finally_test[3], finally_test[4]
        if success == 1:
            if eth_score == 5:
                label_eth_result_d = tk.Label(text=f"????????????????: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"????????????: {up}", fg="green")
                if test_ping < 0:
                    label_eth_result_p = tk.Label(
                        text=f"????????: ????????????! ???????????????????? ?????????????????? ???? ?????????? ????????????????????????????", fg="red")
                else:
                    label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="green")
            elif eth_score == 4:
                label_eth_result_d = tk.Label(text=f"????????????????: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"????????????: {up}", fg="green")
                if test_ping < 0:
                    label_eth_result_p = tk.Label(
                        text=f"????????: ????????????! ???????????????????? ?????????????????? ???? ?????????? ????????????????????????????", fg="red")
                else:
                    label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="DarkOrange3")

            elif eth_score == 3:
                label_eth_result_d = tk.Label(text=f"????????????????: {down}", fg="green")
                label_eth_result_u = tk.Label(text=f"????????????: {up}", fg="green")
                if test_ping < 0:
                    label_eth_result_p = tk.Label(
                        text=f"????????: ????????????! ???????????????????? ?????????????????? ???? ?????????? ????????????????????????????", fg="red")
                else:
                    label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="red")
            elif eth_score == 2:
                label_eth_result_d = tk.Label(text=f"????????????????: {down}", fg="red")
                label_eth_result_u = tk.Label(text=f"????????????: {up}", fg="red")
                if test_ping < 0:
                    label_eth_result_p = tk.Label(
                        text=f"????????: ????????????! ???????????????????? ?????????????????? ???? ?????????? ????????????????????????????", fg="red")
                else:
                    label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="green")
            elif eth_score == 1:
                label_eth_result_d = tk.Label(text=f"????????????????: {down}", fg="red")
                label_eth_result_u = tk.Label(text=f"????????????: {up}", fg="red")
                if test_ping < 0:
                    label_eth_result_p = tk.Label(
                        text=f"????????: ????????????! ???????????????????? ?????????????????? ???? ?????????? ????????????????????????????", fg="red")
                else:
                    label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="DarkOrange3")
            elif eth_score == 0:
                label_eth_result_d = tk.Label(text=f"????????????????: {down}", fg="red")
                label_eth_result_u = tk.Label(text=f"????????????: {up}", fg="red")
                if test_ping < 0:
                    label_eth_result_p = tk.Label(
                        text=f"????????: ????????????! ???????????????????? ?????????????????? ???? ?????????? ????????????????????????????", fg="red")
                else:
                    label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="red")

            label_eth_result_d.grid(column=2, row=12, sticky="w")
            label_eth_result_u.grid(column=2, row=13, sticky="w")
            label_eth_result_p.grid(column=2, row=14, sticky="w")

        else:
            if test_ping <= 30:
                label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="green")
            elif test_ping <= 100:
                label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="DarkOrange3")
            elif test_ping > 100:
                label_eth_result_p = tk.Label(text=f"????????: {test_ping}", fg="red")
            elif test_ping < 0:
                pass
            label_eth_result_d = tk.Label(text=f"???????????????? ???????????????????? ???????????????????? ????????????????????", fg="red")
            label_eth_result_d.grid(column=2, row=12, sticky="w")
            label_eth_result_p.grid(column=2, row=13, sticky="w")
        # end score
        if end_score >= 18:
            label_pc_result = tk.Label(text="???? ?????????????????????????? ??????????????????????", fg="green", font=("Arial", 15))
        elif end_score < 0:
            label_pc_result = tk.Label(text="???? ???? ?????????????????????????? ??????????????????????", fg="red", font=("Arial", 15))
        else:
            label_pc_result = tk.Label(text="???? ???????????????????????? ?????????????????????? ??????????????????????", fg="DarkOrange3",
                                       font=("Arial", 12))

        label_pc_result.grid(column=2, row=15, sticky="w")

    async def before_et_async():
        label_eth = tk.Label(text="???????????????? ????????:")
        label_eth.grid(column=1, row=12, sticky="e")
        label_eth_result_d = tk.Label(text="??????????????????...")
        label_eth_result_d.grid(column=2, row=12, sticky="w")
        task = asyncio.create_task(et_async())
        pending = True
        while pending:
            root.update()
            await asyncio.sleep(.01)
            done, pending = await asyncio.wait({task})

    root = Tk()
    root.title("???????????????? ???? ???? ???????????????????????? ??????????????????????")
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

    # ??????????????

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

    # ????????

    dt = datetime.datetime.now()
    dt_string = dt.strftime("%d/%m/%Y %H:%M:%S")
    left_date = tk.Label(text="????????/??????????:")
    left_date.grid(column=1, row=5, sticky="e")
    right_date = tk.Label(text=f"{dt_string}")
    right_date.grid(column=2, row=5, sticky="w")

    # ??????
    username_l = tk.Label(text="?????????????? ??????:")
    username_l.grid(column=1, row=6, sticky="e")
    wait_for_name()

    # Disk

    async def disk_result():
        disk_result = disk()
        label_disk = tk.Label(text="?????? ??????????:")
        label_disk.grid(column=1, row=11, sticky="e")
        if disk_result[1] == 1:
            label_disk_result = tk.Label(text="SSD                      ", fg="green")
        elif disk_result[1] == 0:
            label_disk_result = tk.Label(text="HDD or eMMC                       ", fg="DarkOrange3")
        elif disk_result[1] == -1:
            label_disk_result = tk.Label(text="HDD or eMMC                      ", fg="red")
        else:
            label_disk_result = tk.Label(text=f"???????????????????? ????????????????????", fg="red")
        label_disk_result.grid(column=2, row=11, sticky="w")

    quitButton = Button(root, text="??????????????", command=root.quit)
    quitButton.place(x=200, y=370)
    root.mainloop()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    resultQueue = multiprocessing.Queue()
    SendeventProcess(resultQueue)

# Debug
# print(f"???????????? ????: score, os_result, os_platform {os_info()}")
# print(f"?????????????????????? ????: pc_score(result), platform_result) {arch_test()}")
# print(f"????????????: ram_gb.ram_specs(), pc_score(result), ram_result {ram_gb.ram_specs()}, {memory()}")
# print(f"CPU: pc_score(result), cpu_result, cpu {cpu()}")
# print(f"Disk: pc_score(result), disk_result {disk()}")
# print(f"speedtest: success, pc_score(result), eth_score, down, up, test_ping {speedtest}")
