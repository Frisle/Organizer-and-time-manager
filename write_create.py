# for quick and easy work organisation
import json
import time
import win32api
from datetime import timedelta
from datetime import datetime
import pprint



json_data_file = "assets/notes_json.json"
json_data_list_file = "assets/data.json"
data_tasks_time = "assets/data_tasks_time.json"

time_kz = datetime.now()
time_now = time_kz.strftime("%m/%d/%Y")


# Read all properties of the given file return them as a dictionary.
def get_file_properties(f_name):

    prop_names = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
    fixed_info = win32api.GetFileVersionInfo(f_name, '\\')
    props['FixedFileInfo'] = fixed_info
    props['FileVersion'] = "%d.%d.%d.%d" % (fixed_info['FileVersionMS'] / 65536,
    fixed_info['FileVersionMS'] % 65536, fixed_info['FileVersionLS'] / 65536,
    fixed_info['FileVersionLS'] % 65536)

    # \VarFileInfo\Translation returns list of available (language, codepage)
    # pairs that can be used to retreive string info. We are using only the first pair.
    lang, codepage = win32api.GetFileVersionInfo(f_name, '\\VarFileInfo\\Translation')[0]

    # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
    # two are language/codepage pair returned from above

    str_info = {}
    for propName in prop_names:
        strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
        ## print str_info
        str_info[propName] = win32api.GetFileVersionInfo(f_name, strInfoPath)

    props['StringFileInfo'] = str_info

    version = str_info["ProductVersion"]
    return version

"""
------------Create data json files----------------
"""


def check_create_data_base():

    try:
        with open(json_data_file, "r") as file_data:
            file_data.readlines()
    except FileNotFoundError:
        create_null_json()

    try:
        file = open(data_tasks_time, "r")
        file.close()
    except FileNotFoundError:
        create_null_data_tasks_json()

    try:
        with open(json_data_list_file, "r") as file_list:
            file_list.readlines()
    except FileNotFoundError:
        create_null_list_json()


def create_null_data_tasks_json():
    with open(data_tasks_time, "w") as json_file:
        data = {
            time_now: []
                }
        json_object = json.dumps(data, indent=4)
        json_file.write(json_object)


def create_null_list_json():
    with open(json_data_list_file, "w") as json_file:
        data = {
            "tags": [],
            "current_task": ["Heer your current tasks will appear"]
                }
        json_object = json.dumps(data, indent=4)
        json_file.write(json_object)


# create json data file
def create_null_json():
    with open(json_data_file, "w", encoding="utf-8") as json_file:
        data = {
            time_now: []
        }
        json_object = json.dumps(data, indent=4)
        json_file.write(json_object)



"""
------------Create data json files----------------
"""


# read position of the file to display keys(-date)
def read_json_date(file_name, elem):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for day in file_data:
            full_day = datetime.strptime(day, '%m/%d/%Y')
            day_name = full_day.strftime('%a %d')
            month_name = full_day.strftime('%b')
            year = full_day.strftime('\'%y')
            print(f"{day_name} {month_name} {year} {len(file_data[day])} {elem}")


# read and display today keys
def read_json_keys_today(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for today in file_data[time_now]:
            print(list(today.keys()))

# used by -date function
def read_json(position, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        try:
            data_pull = file_data[position]
            for data in data_pull:
                print(data)
                return data
        except KeyError:
            print("There is no notes that day")


def read_json_tasks_time(file_name, position):
    with open(file_name, "r") as json_file:
        tasks_time = []
        tasks_name = []
        file_data = json.load(json_file)
        data_pull = file_data[position]
        for items in data_pull:
            for key in items:
                tasks_time.append(items.get(key))
                tasks_name.append(key)
        return tasks_time, tasks_name



# write "data_json.json"
# def write_json(position, data, file_name):
#     with open(file_name, "r") as json_file:
#         file_data = json.load(json_file)
#
#     file_data[position] = data
#
#     with open(file_name, "w") as json_file:
#         json.dump(file_data, json_file)


# append new note to the time_now in data_list.json
def append_json(position, data, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data[position].append(data)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)

# clear list by position and append new data
def update_task_json(position, data, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data[position].clear()
    file_data[position].append(data)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


# use by read_time function
def append_json_tasks(position, index, task, data, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data[position][index][task].append(data)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


# read data_list.json find if new tag is in and operate upon it
def read_and_write_tag_json_list(new_tag, position, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_pull = file_data[position]  # <class 'list'>

        if data_pull.count(new_tag) <= 0:
            append_json("tags", new_tag, json_data_list_file)
        else:
            pass


# find the note and replace it with edited one (-test)
def update_json(replace_data, file_name, user_input):

    position = user_input[:10]
    index = int(user_input[11:13])

    print(position)
    print(index)
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data[position].pop(index)
    print(file_data[position][index])
    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)

    colon = replace_data.rfind(":")

    key = replace_data[:colon].strip("{")
    processed_key = ""
    for item in key:
        if item != "'":
            processed_key += item

    value = replace_data[colon+1:].strip("}")
    processed_value = ""
    for item in value:
        if item != "'":
            processed_value += item

    note = {processed_key: processed_value}

    file_data[position].insert(index, note)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def pretty_print(data_pull):
    for note in data_pull:
        for if_note_list in note.values():
            if type(if_note_list) == list:
                pretty_item = json.dumps(note, ensure_ascii=False, indent=1)  # test function
                print(pretty_item)
            else:
                print(note)

# read today
def read_json_by_time_for_disp_time(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_pull = file_data[time_now]
        for keys in file_data:
            if keys == time_now and len(data_pull) != 0:
                for note in data_pull:
                    for if_note_list in note.values():
                        if type(if_note_list) == list:
                            pretty_item = json.dumps(note, ensure_ascii=False, indent=1)  # test function
                            print(pretty_item)
                        else:
                            print(note)
            elif keys == time_now and len(data_pull) == 0:
                print("There is no notes yet")


# write order number to the notes
def read_json_by_time_for_return_order(file_name):
    with open(file_name, "r") as json_file:
        order_num = 0
        file_data = json.load(json_file)
        data_pull = file_data[time_now]
        for keys in file_data:
            if keys == time_now and len(data_pull) != 0:
                order_num = len(data_pull)
    return order_num


# display all
def read_json_by_time_for_disp_all(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        pprint.pprint(file_data, width=100)


# read by certain position
def read_json_by_time_and_request(file_name, number):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for item in file_data[time_now]:
            cage_index = str(item.keys()).find("#")
            if number in str(item.keys())[cage_index:]:
                print(list(item.keys())[-1])
                print(f"{list(item.keys())[0:7]} {item[list(item.keys())[-1]]}")


# return index of dict with task in time_now list (time_control)
def read_json_tasks_index(position, task, file_name): # <'index'>
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        tasks = []
        try:
            data_pull = file_data[position]
            for data in data_pull:
                tasks.append(list(data))
            return tasks.index([task])
        except KeyError:
            pass

# search by key word in values
def read_json_to_search(file_name, search_entry):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for date in file_data:
            for tasks in file_data[date]:
                for item in tasks.values():
                    if search_entry.lower() in item:
                        print(date, tasks)


# search by key word in keys (by -tag)
def read_json_to_search_by_tag(file_name, search_entry):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for date in file_data:
            for tasks in file_data[date]:
                for item in tasks.keys():
                    if search_entry.lower() in item.lower():
                        notes = pprint.pformat(tasks, indent=1, width=80, depth=2, compact=False, sort_dicts=True, underscore_numbers=False)
                        # print(date, str(tasks))
                        print(notes)


# editing user input
def editing_user_input(user_input):
    # capitalize every character next to the dot
    order = read_json_by_time_for_return_order(json_data_file)
    # append_json("tags", data, file_data_list_json)

    dot = ". "

    slash_index = user_input.find("\\")

    if slash_index > 0:
        tag = user_input[:slash_index + 1]
        tag = tag[:-1]
        read_and_write_tag_json_list(tag,"tags", json_data_list_file)
        user_input = user_input[slash_index+1:]
    else:
        tag = "other"

    dot_index = user_input.find(dot)
    occurrences = []

    while dot_index != -1:
        occurrences.append(dot_index)
        dot_index = user_input.find(dot, dot_index + 1)
    occurrences.append(-2)
    new_string = ""
    for i, char in enumerate(user_input):
        i += - 2
        if i in occurrences:
            new_string += char.upper()
        else:
            new_string += char

    time_now_clock = time.ctime()[11:19]
    formated_user_input = {time_now_clock + f" tag: {tag}" + " #" + str(order): new_string}

    return formated_user_input


def update_json_file(time_now, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data.update({time_now: []})

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)

# write next day date
def check_current_date(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_stamps = []
        try:
            data_stamps.append(file_data[time_now])
        except KeyError:
            update_json_file(time_now, file_name)

"""
------Time manager control block-----------------
"""


def time_control(new_task):

    print(f"Begin working on {new_task}")
    start = time.time()
    # test.main()
    user_input_stop = input("Input Stop to take a break: ").capitalize()
    if "Stop" in user_input_stop:
        stop = time.time()
        elapsed_time = stop - start  # time in seconds
        task_index = read_json_tasks_index(time_now, new_task, data_tasks_time)
        append_json_tasks(time_now, task_index, new_task, elapsed_time, data_tasks_time)
        time_spend = timedelta(seconds=elapsed_time)
        print(f"Time spend on task {new_task} {time_spend}")


# show available dates open data_tasks_time.json and read all keys with seconds
def read_time(file_name):
    read_json_date(file_name, "tasks")
    input_task = input("The date: ").capitalize()
    if not input_task:
        input_task = time_now
    data = read_json_tasks_time(data_tasks_time, input_task)  # <class 'list'>
    tasks_time = data[0]
    tasks_name = data[1]
    time_float = 0
    for item in tasks_time:
        for seconds in item:
            time_float += seconds
    total_time = timedelta(seconds=time_float)
    elapsed_time = []
    for t in tasks_time:
        elapsed_time.append(timedelta(seconds=sum(t)))

    for i in range(len(tasks_name)):
        tasks_names = tasks_name[i]
        elapsed_times = elapsed_time[i]
        print(f"Time spent on {tasks_names} is {elapsed_times}\n")
    print(f"Time total {total_time}")


"""
------Time manager control block-----------------
"""