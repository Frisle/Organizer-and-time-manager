# measure time spend on tasks
import os
from datetime import datetime, timedelta
import json
import write_create
import time

import threading



data_tasks_time = "data_tasks_time.json"
json_data_list_file = "data.json"

time_kz = datetime.now()
time_now = time_kz.strftime("%m/%d/%Y")
write_create.check_create_data_base()
write_create.check_current_date(data_tasks_time)


def read_json(position, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_pull = file_data[position]
        return data_pull[0]


def read_json_tasks(file_name, task_time):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        count = 0
        list_tasks = []
        for tasks in file_data[task_time][1:]:
            count += 1
            list_tasks.append(list(tasks.keys()))
            print(f"{count-1} {list(tasks.keys())}")
        return list_tasks

def interface():
    os.popen("interface.py")


def main():

    idle_time_start = time.time()  # start idle time measure
    write_create.update_task_json("idle_parameter", "idle", json_data_list_file)

    current_task = read_json("current_task", json_data_list_file)
    print(f"Current task: {current_task}")
    # temp_test_1.TaskbarWindow("text") # add support for external tasks displaying.
    user_input = input("What to do: ").capitalize()
    idle_time_stop = time.time()  # stop idle time measure
    idle_result = idle_time_stop - idle_time_start
    write_create.update_task_json("idle_parameter", "work", json_data_list_file)
    time_spend = timedelta(seconds=idle_result)
    """
    Idle time write block
    """
    # current_task = read_json("current_task", json_data_list_file)
    task_index = write_create.read_json_tasks_index(time_now, "Idle time", data_tasks_time)
    if task_index is not False:
        write_create.append_json_tasks(time_now, task_index, "Idle time", idle_result, data_tasks_time)
    else:
        write_create.append_json(time_now, {"Idle time": []}, data_tasks_time)
        write_create.append_json_tasks(time_now, task_index, "Idle time", idle_result, data_tasks_time)

    """
    ------------------
    """
    print(f"Time between tasks {time_spend}\n")
    if "Begin" in user_input:
        new_task = input("New task: ")
        if len(new_task) > 0:
            write_create.update_task_json("current_task", new_task, json_data_list_file)
            write_create.append_json(time_now, {new_task: []}, data_tasks_time)
            write_create.time_control(new_task)
        else:
            print("Enter valid string")
        main()
    elif "Current" in user_input:
        current_task = read_json("current_task", json_data_list_file)
        check_task_appearance = write_create.read_json_tasks_index(time_now, current_task, data_tasks_time)
        if check_task_appearance is not False:
            write_create.time_control(current_task)
        else:
            print("Seems line this task is not in the list, but i will write it for you")
            write_create.append_json(time_now, {current_task: []}, data_tasks_time)
            write_create.time_control(current_task)
        main()
    elif "Return" in user_input:
        list_of_tasks = read_json_tasks(data_tasks_time, time_now)
        try:
            back_to_task = int(input("Input task: "))
            tasks = " ".join(list_of_tasks[back_to_task])
            write_create.update_task_json("current_task", tasks, json_data_list_file)
            write_create.time_control(tasks)
            main()
        except ValueError:
            print("Input valid symbols")
            main()
    elif "Read time" in user_input:
        write_create.read_time(data_tasks_time)
        main()
    elif "Cls" in user_input:
        os.system("cls")
        main()
    elif user_input == "Help" or user_input == "H":
        print("Input \"Begin.\" This will create and start new task\n"
              "Input \"Current\" and you will continue last task\n"
              "Input \"Return\" will take you back to previous task\n"
              "Input \"Read time\" show how much time is spend on each task\n"
              "Input \"cls\" to clean the console"
              )
        main()
    else:
        main()
    main()


# test_cases  --file-version=0.0.4.16 --product-name=Time_manager --enable-console --mingw64 --standalone --onefile --windows-icon-from-ico=coding.ico --output-dir="C:\Users\wda61\PycharmProjects\Builds\Organizer" --remove-output
# --file-version=0.0.4.16 --product-name=Time_manager --enable-console --mingw64 --standalone --onefile --windows-icon-from-ico=coding.ico --output-dir="C:\Distributed_apps" --remove-output



def interfaceThreadFunction():
    thread1 = threading.Thread(target=interface)
    thread1.start()
interfaceThreadFunction()

def mainThreadFunction():
    thread2 = threading.Thread(target=main)
    thread2.start()
mainThreadFunction()