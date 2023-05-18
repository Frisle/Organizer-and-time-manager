import write_create
import pyperclip
import os
from datetime import datetime
import json
import test_case

print("Organizer v0.14.0.12\nPrint \"-h or -help\" to see what you can do")

time_kz = datetime.now()
time_now = time_kz.strftime("%m/%d/%Y")


json_data_file = r"notes_json.json"
json_data_list_file = r"data.json"
write_create.check_create_data_base()
write_create.create_directories()


def main():
    # current_version = write_create.get_file_properties(r"take_notes.exe")
    # print(f"Organizer. v{current_version} alfa")\

    write_create.check_current_date(json_data_file)

    # output content from an artifact processed by connected_db()
    def conn_func():
        file_metadata = write_create.read_file_list("artifacts", json_data_list_file)
        if not file_metadata:
            print("List is empty")
            take_notes()
        try:
            file_number = input("Index of file: ")
            chosen_line = file_metadata[int(file_number)-1]
            file_name = f"{chosen_line[2]}{chosen_line[1]}"
            write_create.connected_db(file_name)
        except Exception as error:
            print(error)
            conn_func()

        take_notes()

    # open appropriate app for redacting an artifact (now its notepad for .txt only)
    def conn_edit_func():
        file_metadata = write_create.read_file_list("artifacts", json_data_list_file)
        if not file_metadata:
            print("List is empty")
            take_notes()
        try:
            file_number = input("Index of file: ")
            chosen_line = file_metadata[int(file_number)-1]
            file_name = f"{chosen_line[2]}{chosen_line[1]}"
            write_create.write_db(file_name)
        except Exception as error:
            print(error)
            conn_edit_func()

        take_notes()

    # function takes complete input in form {-new whatever tag you want\ body of the note}
    # and send it to write_create.editing_user_input
    # then receive back and write with write_create.append_json
    def new_func(user_prompt):
        write_by_hand = user_prompt[5:]
        formated_user_input = write_create.editing_user_input(write_by_hand)
        write_create.append_json(time_now, formated_user_input, json_data_file)
        print("Note is created")
        take_notes()

    # take file path as an input and copy it with importing_new_file
    def import_func():
        path = input("Enter path: ")
        if path:
            write_create.importing_new_file(path)
        else:
            print("Path is probably empty")
            import_func()
        print("File successfully imported")
        take_notes()

    # take whatever is in clipboard and format it as a note with write_create.editing_user_input
    def copy_func(user_prompt):
        tag = user_prompt[6:]
        spam = pyperclip.waitForNewPaste()
        copied_note = f"{tag} {spam}"
        # formated_user_input = {time_now_clock + " #" + str(order): "{}".format(spam)}
        formated_user_input = write_create.editing_user_input(copied_note)
        write_create.append_json(time_now, formated_user_input, json_data_file)
        print("Note is created")
        take_notes()

    # function take input in exact form {-sh yourSearchWord}
    # and make search through every single note
    # search is not precise result can be half of the search request
    # also search request have to be exact word
    def sh_func(user_prompt):
        search_entry = user_prompt[4:]
        if len(search_entry) <= 0:
            print("Enter valid symbols")
        else:
            write_create.read_json_to_search(json_data_file, search_entry)
        take_notes()

    # function take input in exact form {-tag yourTagWord}
    # search through notes with this tags
    # and display any not with this occasion
    def tag_func(user_prompt):
        search_entry = user_prompt[5:]
        if len(search_entry) <= 0:
            print("Enter valid symbols")
        else:
            write_create.read_json_to_search_by_tag(json_data_file, search_entry)
        take_notes()

    # function simply displays every single tag available
    def display_tags_func():
        tags = write_create.read_json_display_tags("tags", json_data_list_file)
        for i in range(len(tags)):
            print(f"{tags[i]}")
        take_notes()

    # function displays only today notes
    def display_today_func():
        write_create.read_json_by_time_for_disp_time(json_data_file)
        take_notes()

    # display all notes from the top to the bottom
    def read_all_func():
        write_create.read_json_by_time_for_disp_all(json_data_file)
        take_notes()

    # function return list of keys and grant user with prompt
    # input the numberd order to display required note
    def read_by_order_func():
        order = write_create.read_json_keys_today(json_data_file)
        if order:
            write_the_num = str(input("The order: "))
            write_create.read_json_by_time_and_request(json_data_file, write_the_num)
        take_notes()

    # comment required
    def display_by_date_func():
        write_create.read_json_date(json_data_file, "notes")
        write_the_date = str(input("The date: "))
        transform_string = f"{write_the_date[0:2]}/{write_the_date[2:4]}/20{write_the_date[4:6]}"
        date = write_create.read_json_date_func(transform_string, json_data_file)
        if not date:
            display_by_date_func()
        take_notes()

    output_reader = test_case.OutputReader()

    # Start reading the output

    # function display available options and commands
    def help_func():
        print("Input \"-new\" and write a new note.\n"
              "Write your \"tag\\\" after it if needed\n\n"
              "Input \"-cls\" to clear the console\n\n"
              "Input \"-sh\" to search the notes by key word\n"
              "Search notes by key-words in body of a note\n\n"
              "Input \"-tag\" to search the notes by tag word\n\n"
              "Input \"-copy\" to use clipboard.\n"
              "Write your tag after flag if needed\n\n"
              "Input \"-today\" to read today notes\n"
              "Input \"-all\" to read all created notes\n"
              "Input \"-order\" to open today note by number\n"
              "Input \"-date\" to open notes by certain day\n"
              "Input \"-display tags\" to view available tags\n\n"
              "Input \"-conn\" to view list of connected files\n"
              "Then you will be prompted to input index of file you need\n"
              "Text files will be printed directly in console\n"
              "Others will be opened by default application\n\n"
              "Input \"-conn edit\" to open text file for editing\n"
              "Similar to \"-conn\" except it can open Notepad.exe for text file to edit them\n\n"
              "Input \"-import\" to copy files to app directory\n"
              "Then input full path to new file.")
        take_notes()

    def take_notes():
        user_prompt = input("Input= ")
        if "-copy" in user_prompt:
            copy_func(user_prompt)
        elif user_prompt == "-conn":
            conn_func()
        elif user_prompt == "-conn edit":
            conn_edit_func()
        elif user_prompt == "-import":
            import_func()
        elif "-new" in user_prompt:
            new_func(user_prompt)
        elif "-sh" in user_prompt:
            # search by key word in dict{values}
            sh_func(user_prompt)
        elif "-tag" in user_prompt:
            tag_func(user_prompt)
        elif user_prompt == "-display tags":
            # display all tags
            display_tags_func()
        elif user_prompt == "-today":
            # read today
            display_today_func()
        elif user_prompt == "-all":
            # read all
            read_all_func()
        elif user_prompt == "-order":
            # read by order \\today
            read_by_order_func()
        elif user_prompt == "-date":
            # open certain day
            display_by_date_func()
        elif "-cls" in user_prompt:
            os.system("cls")
            take_notes()
        elif "timer" in user_prompt:
            os.system("python /addons/test.py")
            take_notes()
        elif "-test" in user_prompt:
            position = str(input("Date and index "))
            note_time = position[:10]
            index = int(position[11:13])
            with open(json_data_file, "r") as json_file:
                file_data = json.load(json_file)
            output_reader.start_reading()

            print(file_data[note_time][index])

            output_reader.stop_reading()

            captured_output = ''.join(output_reader.captured_output)
            pyperclip.copy(captured_output.rstrip())

            replace_data = str(input("Input replace note: "))

            write_create.update_json(replace_data, json_data_file, position)
            take_notes()
        elif user_prompt == "-help" or user_prompt == "-h":
            help_func()
        else:
            take_notes()
    take_notes()




# test_case --file-version=0.15.1.14 --product-name=Organizer --enable-console --mingw64 --standalone --onefile --windows-icon-from-ico=organizer_ico.ico --output-dir="C:\Users\wda61\PycharmProjects\Builds\Organizer" --remove-output
# --file-version=0.15.1.14 --product-name=Organizer --enable-console --mingw64 --standalone --onefile --windows-icon-from-ico=organizer_ico.ico --output-dir="C:\Distributed_apps" --remove-output



main()
