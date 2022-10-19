import subprocess


def ping():
    """

    :rtype: dict or None
    """
    cmd = "ping ya.ru".split(' ')
    try:
        output = subprocess.check_output(cmd).decode().strip()
        lines = output.split("\n")
        timing = int(lines[-1].split()[2].replace('ms,', ''))
        return timing
    except Exception as e:
        print(e)
        return None


print(ping())

disk_type = subprocess.check_output("powershell -Command Get-PhysicalDisk | ft -AutoSize MediaType")
print(disk_type)
disk_type_old = subprocess.run(
    ["powershell", "-Command", 'Get-WmiObject Win32_DiskDrive'],
    shell=True, capture_output=True)