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
import sys

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")
        b1 = tk.Button(self, text="print to stdout", command=self.print_stdout)
        b2 = tk.Button(self, text="print to stderr", command=self.print_stderr)
        b1.pack(in_=toolbar, side="left")
        b2.pack(in_=toolbar, side="left")
        self.text = tk.Text(self, wrap="word")
        self.text.pack(side="top", fill="both", expand=True)
        self.text.tag_configure("stderr", foreground="#b22222")

        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")

    def print_stdout(self):
        main()
    def print_stderr(self):
        '''Illustrate that we can write directly to stderr'''
        sys.stderr.write("this is stderr\n")

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")


def main():
    pc_score = 0

    bad_cpus = ['atom', 'duo', 'quad', 'dual-core', 'sempron']

    # Operating system info
    if platform.release() == "10" or platform.release() == "11":
        print(f"Версия ОС: {out_color.out_green(platform.release())}")
        out_color.clear_color()
        pc_score += 2
    elif platform.release() == "8" or platform.release() == "8.1":
        print(f"Версия ОС: {out_color.out_yellow(platform.release())}")
        out_color.clear_color()
        pc_score += 1
    else:
        print(f"Версия ОС: {out_color.out_red(platform.release())}")
        out_color.clear_color()
        pc_score -= 1

    # Machine type
    if platform.machine() == "AMD64":
        print(f"Разрядность ОС: {out_color.out_green('x64')}")
        out_color.clear_color()
        pc_score += 1
    else:
        print(f"Разрядность ОС: {out_color.out_red('x32')}")
        out_color.clear_color()
        pc_score -= 999

    # HARDWARE
    # Memory
    if ram_gb.ram_specs() >= 7.8:
        print(f"Количество RAM: {out_color.out_green(ram_gb.ram_specs())} Gb")
        out_color.clear_color()
        pc_score += 5
    elif ram_gb.ram_specs() >= 5.8:
        print(f"Количество RAM: {out_color.out_yellow(ram_gb.ram_specs())} Gb")
        out_color.clear_color()
        pc_score += 2
    else:
        print(f"Количество RAM: {out_color.out_red(ram_gb.ram_specs())} Gb")
        out_color.clear_color()
        pc_score -= 999

    # System

    # CPU
    cpu = cpuinfo.get_cpu_info()['brand_raw']
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    fine_name_cpu = cpu.lower().translate(str.maketrans('', '', string.punctuation)).replace(' ', '')
    if [a for a in bad_cpus if a in fine_name_cpu]:
        print(f"CPU: {out_color.out_red(cpu)}")
        out_color.clear_color()
        pc_score -= 999
    else:
        if cores >= 4 and threads >= 4:
            print(f"CPU: {out_color.out_green(cpu)}")
            out_color.clear_color()
            pc_score += 5
        elif cores >= 2 and threads >= 4:
            print(f"CPU: {out_color.out_yellow(cpu)}")
            out_color.clear_color()
            pc_score += 2
        else:
            print(f"CPU: {out_color.out_red(cpu)}")
            out_color.clear_color()
            pc_score -= 999
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
    elif ram_gb.ram_specs() >= 7.8:
        print(out_color.out_yellow("HDD or eMMC"))
    else:
        print(out_color.out_red("HDD or eMMC"))
        pc_score -= 999

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
        elif test_ping >= 70:
            print(f"Скорость загрузки: {out_color.out_green(down)} Mbps")
            out_color.clear_color()
            print(f"Скорость отдачи: {out_color.out_green(up)} Mbps")
            out_color.clear_color()
            print(f"Пинг: {out_color.out_yellow(test_ping)} ms")
            out_color.clear_color()
            pc_score += 2
        else:
            print(f"Скорость загрузки: {out_color.out_green(down)} Mbps")
            out_color.clear_color()
            print(f"Скорость отдачи: {out_color.out_green(up)} Mbps")
            out_color.clear_color()
            print(f"Пинг: {out_color.out_red(test_ping)} ms")
            out_color.clear_color()
    else:
        if test_ping <= 30:
            print(f"Скорость загрузки: {out_color.out_red(down)} Mbps")
            out_color.clear_color()
            print(f"Скорость отдачи: {out_color.out_red(up)} Mbps")
            out_color.clear_color()
            print(f"Пинг: {out_color.out_green(test_ping)} ms")
            out_color.clear_color()
            pc_score += 2
        elif test_ping >= 70:
            print(f"Скорость загрузки: {out_color.out_red(down)} Mbps")
            out_color.clear_color()
            print(f"Скорость отдачи: {out_color.out_red(up)} Mbps")
            out_color.clear_color()
            print(f"Пинг: {out_color.out_yellow(test_ping)} ms")
            out_color.clear_color()
            pc_score += 1
        else:
            print(f"Скорость загрузки: {out_color.out_red(down)} Mbps")
            out_color.clear_color()
            print(f"Скорость отдачи: {out_color.out_red(up)} Mbps")
            out_color.clear_color()
            print(f"Пинг: {out_color.out_red(test_ping)} ms")
            out_color.clear_color()

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

app = ExampleApp()
app.title("Проверка ПК на соответствие требованиям")
app.geometry('480x250')
app.mainloop()

