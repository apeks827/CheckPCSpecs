import subprocess
import speedtest
from ping3 import ping as p


def ping():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        timing = round(st.results.ping)
    except Exception as err:
        print(err)
        try:
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            timing = round(st.results.ping)
        except Exception as err:
            print(err)
            try:
                cmd = "ping ya.ru".split(' ')
                output = subprocess.check_output(cmd).decode('cp1125').strip()
                lines = output.split("\n")
                timing = int(lines[-1].split()[2].replace('мсек,', ''))
            except Exception as err:
                print('ping try 1 rus failed', err)
                try:
                    cmd = "ping ya.ru".split(' ')
                    output = subprocess.check_output(cmd).decode().st
                    lines = output.split("\n")
                    timing = int(lines[-1].split()[2].replace('ms,', ''))
                except Exception as err:
                    print('ping try 2 eng failed', err)
                    try:
                        timing = round(p('ya.ru') * 1000)
                    except Exception as err:
                        print("ping try3 failed", err)
    return timing
