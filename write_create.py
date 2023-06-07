# for quick and easy work organisation
import csv
import json
import time
import win32api
from datetime import timedelta
from datetime import datetime
import os
from shutil import copyfile
from columnar import columnar
import ast

json_data_file = os.path.join(os.getcwd(), r"notes_json.json")
json_data_list_file = os.path.join(os.getcwd(), r"data.json")
data_tasks_time = os.path.join(os.getcwd(), r"data_tasks_time.json")

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
        str_info_path = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
        # print str_info
        str_info[propName] = win32api.GetFileVersionInfo(f_name, str_info_path)

    props['StringFileInfo'] = str_info

    version = str_info["ProductVersion"]
    return version


"""
------------Create data base files----------------
"""


def create_directories():
    parent_dir = os.getcwd()
    dir_1 = "connected"
    path_1 = os.path.join(parent_dir, dir_1)
    try:
        os.mkdir(path_1)
    except FileExistsError:
        pass


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

    try:
        os.listdir("connected_test/")
    except FileNotFoundError:
        create_directories()


def create_null_data_tasks_json():
    with open(data_tasks_time, "w", encoding="utf-8") as json_file:
        data = {
            time_now: []
        }
        json_object = json.dumps(data, indent=4)
        json_file.write(json_object)


def create_null_list_json():
    with open(json_data_list_file, "w", encoding="utf-8") as json_file:
        data = {
            "tags": [],
            "current_task": ["Heer your current tasks will appear"],
            "artifacts": []
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
------------Create data base files----------------
"""


"""
delete function. 
in order to delete multiple notes from dictionary
it has to be separated from remove_notes()
"""


def delete(list_data, num):
    for i in num:
        list_data.pop(i)
    return list_data


# deletes notes from dictionary
def remove_notes(user_input):
    position = user_input[:10]
    index = user_input[11:].split()

    with open(json_data_file, "r") as json_file:
        file_data = json.load(json_file)
        index_list = []
        for order in file_data[position]:

            note_num = order[0].strip("#")

            for num in index:
                if int(num) == int(note_num):

                    index_list.append(file_data[position].index(order))

                    index_list.sort(reverse=True)
                    print("Note " + str(note_num) + " deleted")
        val = delete(file_data[position], index_list)
        file_data[position] = val

    with open(json_data_file, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


# read position of the file to display keys(-date)
def read_json_date(file_name, elem):
    with open(file_name, "r") as json_file:

        file_data = json.load(json_file)
        for day in file_data:
            if len(file_data[day]) > 0:
                full_day = datetime.strptime(day, '%m/%d/%Y')
                day_slash = full_day.strftime('%m/%d/%Y')
                day_name = full_day.strftime('%a %d')
                month_name = full_day.strftime('%b')
                year = full_day.strftime('\'%y')
                print(f"{day_name} {month_name} {year} {len(file_data[day])} {elem} {day_slash}")


def read_json_display_tags(position, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        table = columnar(file_data[position], headers=['Tag', 'Number of notes'],
                         no_borders=True,
                         max_column_width=None, wrap_max=1, terminal_width=None)
        print(table)


# read and display today keys
def read_json_keys_today(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        if len(file_data[time_now]) > 0:
            for today in file_data[time_now]:
                print(list(today.keys()))
            return True
        elif len(file_data[time_now]) <= 0:
            print("There is no notes yet")
            return False


# used by -date function
def read_json_date_func(position, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        try:
            data_pull = file_data[position]
            for data in data_pull:
                table = pretty_print(file_data[position], "notes")
            print(table)
            return data
        except KeyError:
            print("There is no notes that day or date is incorrect")
            return False


# open json_tasks_time and return spend time and task titles
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


# Append a new artefact to the position key in data_list.json.
# Contain test option remove, for future use.
def append_json(position, data, file_name, remove=False):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
    if not remove:
        file_data[position].append(data)
    else:
        file_data[position].remove(data)

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
        for item in data_pull:
            if item[0] == new_tag[0]:
                append_json("tags", item, json_data_list_file, remove=True)
                new_tag = [new_tag[0], new_tag[1]]
        if data_pull.count(new_tag) <= 0:
            append_json("tags", new_tag, json_data_list_file)
        else:
            pass


# find the note and replace it with edited one -edit
def update_json(replace_data, file_name, user_input):
    position = user_input[:10]
    index = int(user_input[11:13])

    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for order in file_data[position]:
            new_index = order[0].strip("#")

            if index == int(new_index):
                index_del = file_data[position].index(order)
                file_data[position].remove(order)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)

    new_note = ""
    for item in replace_data:
        if item == "'":
            item = '"'
        new_note += item

    new_note_processed = ast.literal_eval(new_note)  # transform string from input to list

    file_data[position].insert(index_del, new_note_processed)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def pretty_print(line, doc_type):
    if doc_type == "artifacts":
        table = columnar(line, headers=['Order', 'Extension', 'File name', 'Size', 'Type', 'Description'],
                         no_borders=True,
                         max_column_width=None, wrap_max=5, terminal_width=None)
        return table
    elif doc_type == "notes":
        table = columnar(line, headers=['Order', 'Date', 'Creation Time', 'Tag', 'Note'],
                         justify=["c", "c", "c", "c", "l"], no_borders=True,
                         max_column_width=None, wrap_max=5, terminal_width=None)
        return table


# read today
def read_json_by_time_for_disp_time(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_pull = file_data[time_now]
        for keys in file_data:
            if keys == time_now and len(data_pull) != 0:

                print(pretty_print(file_data[time_now], "notes"))

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


# display all "-all"
def read_json_by_time_for_disp_all(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for notes in file_data:
            if len(file_data[notes]) > 0:
                table = pretty_print(file_data[notes], "notes")
                print(table)


# read by certain position
def read_json_by_time_and_request(file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for item in file_data[time_now]:
            print(item)


# return index of dict with task in “time_now“ list ("time_control")
def read_json_tasks_index(position, task, file_name):  # <'index'>
    """

    :param position: takes "time_now"
    :param task: takes “name” of the task as a string
    :param file_name: current file name of the json
    :return: “numeric index” of a task or False if not.
    """
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        tasks = []
        try:
            data_pull = file_data[position]
            for data in data_pull:
                tasks.append(list(data))
            return tasks.index([task])
        except ValueError:
            return False


# search by key word in values
def read_json_to_search(file_name, search_entry):
    count = 0
    new_list = []
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for date in file_data:
            for tasks in file_data[date]:
                if search_entry.lower() in tasks[4].lower():
                    count += 1
                    index = file_data[date].index(tasks)
                    new_list.append(file_data[date][index])
        if new_list:
            print(pretty_print(new_list, "notes"))
            print(f"Found {count} match")
        else:
            print("There is no notes with key")


# search by tag field (-tag)
def read_json_to_search_by_tag(file_name, search_entry):
    count = 0
    new_list = []
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        for date in file_data:
            for task in file_data[date]:
                if search_entry.lower() in task[3].lower():
                    count += 1
                    index = file_data[date].index(task)
                    new_list.append(file_data[date][index])
    if new_list:
        print(pretty_print(new_list, "notes"))
        print(f"Found {count} match")
    else:
        print("There is no tag with this key")


"""
   start: block with working with files 
"""


#  function to view available artifacts
def read_file_list(position, file_name):
    names_list = []
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_pull = file_data[position]
        print(pretty_print(file_data[position], "artifacts"))
        for item in data_pull:
            names_list.append(item[2]+item[1])
        return names_list


# function form record with artifact data and write in data.json
def update_artifact_list(position, file_name, name, extension, size, key, description):

    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)
        data_pull = file_data[position]
        order = len(data_pull)

        # order+1==next to last number,
        # extension==file extension from an os.path.splitext(file_name),
        # size==size in bytes
        # data = {f"{order+1}%{extension}%{name}%{size}kb%{key}": f"{description}"}
        data = [order, extension, name, f"{size} kb", key, description]

    file_data[position].append(data)

    with open(file_name, "w") as json_file:
        json.dump(file_data, json_file, ensure_ascii=False, indent=4)


def importing_new_file(path):
    file_name = os.path.basename(path)  # extract only name.ext of file from path string
    name, extension = os.path.splitext(file_name)  # separate file name and extension
    size = os.path.getsize(path) / 1024  # get file size in bytes
    description = input("Input short description: ")
    content_category = input("Input category")
    size_in_bt = '{0:.2f}'.format(size)
    update_artifact_list("artifacts", json_data_list_file, name, extension, size_in_bt, content_category, description)
    parent_dir = os.getcwd()
    target_dir = os.path.join(parent_dir, "connected/"+str(file_name))

    copyfile(path, target_dir)


# function used to get list of files from a directory: "connected/"
# and open notepad to edit it.
def write_db(file_name):
    list_of_file = os.listdir("connected/")
    index = list_of_file.index(file_name)
    file_name = list_of_file[index]
    full_path = os.path.abspath("connected/"+str(file_name))
    os.startfile(full_path)


# function used to get list of files from a directory: "connected/"
# and print its content in the cmd.
def connected_db(file_name):
    list_of_file = os.listdir("connected/")
    index = list_of_file.index(file_name)
    connected_file = list_of_file[index]
    full_path = os.path.abspath("connected/" + str(connected_file))
    file = open("connected/" + str(connected_file), "r")
    try:
        content = file.read()
        print(content)
    except UnicodeDecodeError:
        os.startfile(full_path)

    file.close()


# test case of csv writer
def csv_writer():
    header = ["platform", "console", "command", "description"]

    data = ["linux", 1, "-ls", "Open a new single-pane window for the default selection. "
                               "This is usually the root of the drive Windows is installed on. "
                               "If the window is already open a duplicate opens"]

    with open('connected/code_snippets.csv', "w", encoding="UTF-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)


# test case of csv reader
def csv_reader():
    with open("connected/code_snippets.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        for line in reader:
            if line[1] == str(0):
                print(line)


# commented out due to lack of pandas import
# building package with pandas is costly and long,
# so it decided to stop work on it for now
# def pandas_reader():
#
#     # pd.set_option("max_columns", 2)  # Showing only two columns
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.width', None)
#     pd.set_option('display.max_colwidth', None)
#     df = pd.read_csv("connected/code_snippets.csv")
#     df["description"] = df["description"].str.wrap(100)
#     print(df)

"""
   end: block working with files 
"""


def formate_output(lines):
    values = []
    keys = []
    line = []
    for key, value in lines.items():
        keys.append(key)
        values.append(value)
        for item in keys:
            bar = item.index("#")-1
            colon = item.rindex(":")+2
            tag = item[colon:bar]
            creation_time = item.split()[0]
            date_time = item.split()[1]
            order = item.split()[-1]
            line.append(order)
            line.append(date_time)
            line.append(creation_time)
            line.append(tag)
            line.append(*values)

    return line


def tag_counting(item):
    with open(json_data_file, "r") as json_file:
        count = 0
        file_data = json.load(json_file)
        data_pull = file_data
        for data in data_pull:
            for i in data_pull[data]:
                for tag in i:
                    if item in tag:
                        count += 1
                        print(count)
                    else:
                        pass
        return count


# editing user input
def editing_user_input(user_input):
    # capitalize every character next to the dot
    order = read_json_by_time_for_return_order(json_data_file)
    # append_json("tags", data, file_data_list_json)

    dot = ". "

    slash_index = user_input.find("\\")

    if slash_index > 0:
        new_tag = user_input[:slash_index + 1]
        tag = new_tag[:-1]
        tag_amount = tag_counting(tag)
        tag_count = [tag, tag_amount]
        read_and_write_tag_json_list(tag_count, "tags", json_data_list_file)
        user_input = user_input[slash_index + 2:]  # +2 eliminates space before note
        # tag = tag[:-1]

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

    date_time = time_kz.strftime("%m/%d/%Y")
    time_now_clock = time.ctime()[11:19]
    formatted_dict_line = {time_now_clock + " " + date_time + f" tag: {tag}" + " #" + str(order): new_string}
    formatted_user_input = formate_output(formatted_dict_line)

    return formatted_user_input


def update_json_file(current_time, file_name):
    with open(file_name, "r") as json_file:
        file_data = json.load(json_file)

    file_data.update({current_time: []})

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
    print(f"Begin working on {new_task}\n")
    start = time.time()

    print("Input any key to stop the timer")
    input("Input: ")
    stop = time.time()
    elapsed_time = stop - start  # time in seconds

    task_index = read_json_tasks_index(time_now, new_task, data_tasks_time)
    append_json_tasks(time_now, task_index, new_task, elapsed_time, data_tasks_time)
    time_spend = timedelta(seconds=elapsed_time)
    print("\nWork stopped. Get some rest or start another one")
    print(f"Time spend on task {new_task} {time_spend}\n")


# show available dates open data_tasks_time.json and read all keys with seconds.
def read_time(file_name):
    read_json_date(file_name, "tasks")
    input_task = input("The date: ").capitalize()
    if not input_task:
        input_task = time_now
    data = read_json_tasks_time(data_tasks_time, input_task)  # <class 'list'>
    tasks_time = data[0]
    tasks_name = data[1]
    total_time_float = 0
    idle_time_float = 0
    for item in tasks_time[1:]:
        for seconds in item:
            total_time_float += seconds

    for idle_time in tasks_time[0:1]:
        for idle_seconds in idle_time:
            idle_time_float += idle_seconds

    total_idle_time = timedelta(seconds=idle_time_float)
    total_time_task = timedelta(seconds=total_time_float)

    total_time_seconds = idle_time_float + total_time_float
    total_time = timedelta(seconds=total_time_seconds)

    elapsed_time = []
    for t in tasks_time:
        elapsed_time.append(timedelta(seconds=sum(t)))

    for i in range(len(tasks_name)):
        tasks_names = tasks_name[i]
        elapsed_times = elapsed_time[i]
        print(f"Time spent on {tasks_names} is {elapsed_times}\n")
    print(f"Time total spent on tasks {total_time_task}")
    print(f"Time total spent idle {total_idle_time}")
    print(f"Time overall {total_time}")


"""
------Time manager control block-----------------
"""
