# measure time spend on tasks
import os
from datetime import datetime, timedelta
import json
import write_create
import time

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


def read_json_tasks(file_name, time_now):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for tasks in file_data[time_now]:
            print(list(tasks.keys()))


def main():

    idle_time_start = time.time() # start idle time measure

    current_task = read_json("current_task", json_data_list_file)
    print(f"Current task: {current_task}")

    user_input = input("What to do: ").capitalize()
    idle_time_stop = time.time() # stop idle time measure
    idle_result = idle_time_stop - idle_time_start
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
        print(current_task)
        check_task_apearence = write_create.read_json_tasks_index(time_now, current_task, data_tasks_time)
        if check_task_apearence is not False:
            write_create.time_control(current_task)
        else:
            print("Seems line this task is not in the list, but i will write it for you")
            write_create.append_json(time_now, {current_task: []}, data_tasks_time)
            write_create.time_control(current_task)
        main()
    elif "Return" in user_input:
        read_json_tasks(data_tasks_time, time_now)
        back_to_task = input("Input task: ")
        if len(back_to_task) > 0:
            write_create.update_task_json("current_task", back_to_task, json_data_list_file)
            write_create.time_control(back_to_task)
        else:
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


#test_cases  --file-version=0.0.2.15 --product-name=Time_manager --enable-console --mingw64 --standalone --onefile --windows-icon-from-ico=coding.ico --output-dir="C:\Users\wda61\PycharmProjects\Builds\Organizer" --remove-output
# --file-version=0.0.2.15 --product-name=Time_manager --enable-console --mingw64 --standalone --onefile --windows-icon-from-ico=coding.ico --output-dir="C:\Distributed_apps" --remove-output
main()
