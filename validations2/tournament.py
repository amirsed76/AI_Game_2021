import os
import time
from os import listdir
from os.path import isfile, join
from shutil import copyfile
from threading import Thread
import os, shutil


def copytree(src, dst, symlinks=False, ignore=None):
    dst = "VS_logs\\" + dst
    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        copyfile(s, d)


CLIENT_ROOT = "F:\\dars\\AI_TA\\clients_phase2\\"
CLIENT_address = {
    "1": "cil\\cil\\client_main.py",
    "2": "AI_Phase2_AIPY\\AI\\client_main.py",
    "3": "finallll\\FINAAAAAAAAL\\part2\\client_main.py",
    "4": "AI001-phase2-player456\\Java-Client.jar",
    "5": "phase2\\ai\\client_main.py",
    "6": "ai-phase2\\python_client\\python_client\\client_main.py",
    "7": "AI001-phase2-Eshraghi\\src\\client_main.py",
    "8": "AI001-phase2-IMPERIUM\\AI001-phase2-IMPERIUM\\client_main.py"

}


def get_files(mypath):
    files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    files.sort(key=os.path.getmtime)
    return files


def run_server(log_name, config):
    os.system(f"python ../server/server_main.py -config {config} > server_logs/{log_name}.txt")


def run_client(path, log_name):
    is_python = True if ".py" in path else False

    try:
        if is_python:
            cmd = f"python {path} > client_logs/{log_name}.txt"

        else:
            cmd = f"java -jar {path} > client_logs/{log_name}.txt"

        os.system(cmd)

    except Exception as e:
        print(f"EXCEPT {path} : {e}")


def play(i, client1, client2, j):
    # input(f"server on config {i}  {'raft' if client1 < client2 else 'bargasht'} ")
    config = f"config{i}.json"

    server_log_name = f"{i}_{client1}_{client2}_{j}"

    client1_log_name = f"client{client1}_{server_log_name}"
    client2_log_name = f"client{client2}_{server_log_name}"
    client1_address = CLIENT_ROOT + client1 + "\\" + CLIENT_address[client1]
    client2_address = CLIENT_ROOT + client2 + "\\" + CLIENT_address[client2]

    t1 = Thread(target=run_server, args=(server_log_name, config))
    t1.start()
    print(f"server run => {server_log_name}")
    time.sleep(1)

    t2 = Thread(target=run_client, args=(client1_address, client1_log_name))
    t2.start()
    print(f"client1 run")
    time.sleep(1)

    t3 = Thread(target=run_client, args=(client2_address, client2_log_name))
    t3.start()
    print(f"client2 run")

    t1.join()
    t2.join()
    t3.join()
    print(">>>>>>>>> finish")


def main():
    # client1 = input("client1 => ")
    # client2 = input("client2 => ")

    for client1 in CLIENT_address:
        for client2 in CLIENT_address:
            if int(client1) < int(client2) and client1 != "1" and client2 != "1":
                shutil.rmtree("game_logs")
                os.makedirs("game_logs", exist_ok=True)
                for i in range(1, 11):
                    for j in range(1, 4):
                        play(i, client1, client2, j)
                        play(i, client2, client1, j)

                copytree(src="game_logs", dst=f"{client1}vs{client2}")


if __name__ == '__main__':
    main()
