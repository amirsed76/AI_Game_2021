import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile
from threading import Thread


def get_files(mypath):
    files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    files.sort()
    return files


def run_server():
    os.system(f"python ../server/server_main.py -config {config} > logs/{i}.txt")


def run_client():
    os.system(f"python ./sample_client/client_main.py")


if __name__ == '__main__':
    for i in range(1, 11):
        input(f"server on config {i} ??  ")
        config = f"config{i}.json"
        t1 = Thread(target=run_server)
        t1.start()
        print("server run.")
        t2 = Thread(target=run_client)
        t2.start()
        print("client run")
        t1.join()
        t2.join()

        # os.system(f"python ../server/server_main.py -config {config} > logs/{i}.txt")

    for i, file in enumerate(get_files("game_logs")):
        print(file, " moved")
        copyfile(file, f"gameLogs/{i}.json")
