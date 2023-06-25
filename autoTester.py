import sys
import threading
import subprocess
import numpy as np
import pyautogui
import signal
import time
import os

iteration = 0
lastSort = 3

def startGame():
    
    global iteration
    global lastSort
    file = open('helios-base/src/coach/sample_coach.cpp', 'r')
    file_lines = file.readlines()

    print('Compiling now. Ensure monitor is on screen.')
    speed = np.array([1.000, 0.947, 0.922, 0.898, 0.820, 0.763, 0.803, 1.047, 0.844, 0.880, 0.909, 0.814, 0.866, 1.009, 0.919, 0.809, 1.041, 1.035])
    stamina_comsumption = np.array([55.0, 54.8, 58.3, 57.9, 52.2, 52.4, 56.5, 55.9, 52.7, 56.2, 49.4, 50.5, 57.6, 57.8, 55.4, 48.6, 54.7, 59.3])
    karea = np.array([1.085, 1.116, 1.090, 1.162, 1.170, 1.013, 1.027, 1.010, 1.080, 1.066, 1.032, 1.111, 1.016, 1.153, 1.136, 1.146, 1.171, 1.122])

    sorted_by_speed = np.argsort(-speed[1:])
    sorted_by_stamina = np.argsort(stamina_comsumption[1:])
    sorted_by_karea = np.argsort(karea[1:])

    iteration = iteration + 1
    string_array = ""
    if lastSort == 3:
        print("Iterating by speed.")
        string_array = "{" + ", ".join(str(i + 1) for i in sorted_by_speed) + "}"
        lastSort = 1
    elif lastSort == 2:
        print("Iterating by kickable area.")
        string_array = "{" + ", ".join(str(i + 1) for i in sorted_by_karea) + "}"
        lastSort = 3
    else:
        print("Iterating by stamina cost per step.")
        string_array = "{" + ", ".join(str(i + 1) for i in sorted_by_stamina) + "}"
        lastSort = 2

    file_lines[410] = '\tconst std::vector<int> ids = '+ string_array +';\n'
    #file_lines[430] = '\t\t\tsubstituteTo( *unum, '+str(random.randint(1, 16))+' );\n'

    file.close()
    file = open('helios-base/src/coach/sample_coach.cpp', 'w')
    file = file.writelines(file_lines)

    dir = '/home/eric/Downloads/players/tcc/helios-base'

    bash = 'sudo ./bootstrap'
    process = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dir)

    process.communicate()

    bash = 'sudo ./configure'
    process = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dir)

    process.communicate()

    bash = 'sudo make'
    process = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dir)

    saida, erro = process.communicate()

    if erro.decode() == "":
        print("Compilation ok. Starting game. Ensure monitor is on screen.")

    def killGame(process):
        time.sleep(900)
        print('I believe the game is over. Killing process.')
        pgrp = os.getpgid(process.pid)
        try:
            os.killpg(pgrp, signal.SIGINT)
        except Exception as e:
            return
        return
    
    def startGame():
        bash = ['bash', 'quickStartGame.sh']
        dir = '/home/eric'
        #os.chdir(dir)
        process = subprocess.Popen(bash, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dir)
        killGame(process)
        return

    thread = threading.Thread(target=startGame)
    thread.start()

    time.sleep(3)
    print('Connecting now')
    pyautogui.hotkey('ctrl', 'c', interval=0.1)
    time.sleep(5)
    print('Starting now')
    pyautogui.hotkey('ctrl', 'k', interval=0.1)
    time.sleep(450)
    print('I believe the first half ended now. Starting again.')
    pyautogui.hotkey('ctrl', 'k', interval=0.1)
    thread.join()

while True:
    if iteration == 15:
        print('End of execution')
        exit()
    print("Iteration:", iteration)
    startGame()
    

