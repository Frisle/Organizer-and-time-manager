import write_create
import pyperclip
import time
import os
from datetime import datetime





time_kz = datetime.now()
time_now = time_kz.strftime("%m/%d/%Y")



json_data_file = " assets/notes_json.json"
json_data_list_file = "assets/data.json"
write_create.check_create_data_base()

def main():
    # current_version = write_create.get_file_properties(r"take_notes.exe")
    # print(f"Organizer. v{current_version} alfa")\


    write_create.check_current_date(json_data_file)

    def take_notes():
        order = write_create.read_json_by_time_for_return_order(json_data_file)  # return numeric order for notes
        user_prompt = input("Input= ")
        if user_prompt == "-copy":
            spam = pyperclip.waitForNewPaste()
            time_now_clock = time.ctime()[11:19]
            formated_user_input = {time_now_clock + " #" + str(order): "{}".format(spam)}
            write_create.append_json(time_now, formated_user_input, json_data_file)
            print("Note is created")
            take_notes()
        elif "-new" in user_prompt:
            # write new note by hand
            write_by_hand = user_prompt[5:]
            formated_user_input = write_create.editing_user_input(write_by_hand)
            write_create.append_json(time_now, formated_user_input, json_data_file)
            print("Note is created")
            take_notes()
        elif "-sh" in user_prompt:
            # search by key word in dict{values}
            search_entry = user_prompt[4:]
            if len(search_entry) <= 0:
                print("Enter valid symbols")
            else:
                write_create.read_json_to_search(json_data_file, search_entry)
            take_notes()
        elif "-tag" in user_prompt:
            search_entry = user_prompt[5:]
            if len(search_entry) <= 0:
                print("Enter valid symbols")
            else:
                write_create.read_json_to_search_by_tag(json_data_file, search_entry)
            take_notes()
        elif user_prompt == "-today":
            # read today
            write_create.read_json_by_time_for_disp_time(json_data_file)
            take_notes()
        elif user_prompt == "-all":
            # read all
            write_create.read_json_by_time_for_disp_all(json_data_file)
            take_notes()
        elif user_prompt == "-order":
            # read by order \\today
            write_create.read_json_keys_today(json_data_file)
            write_the_num = str(input("The order: "))
            write_create.read_json_by_time_and_request(json_data_file, write_the_num)
            take_notes()
        elif user_prompt == "-date":
            # open certain day
            write_create.read_json_date(json_data_file, "notes")
            write_the_date = str(input("The date: "))
            transform_string = f"{write_the_date[0:2]}/{write_the_date[2:4]}/20{write_the_date[4:6]}"
            write_create.read_json(transform_string, json_data_file)
            take_notes()
        elif "-cls" in user_prompt:
            os.system("cls")
            take_notes()
        elif "-test" in user_prompt:
            position = str(input("Date and index "))
            replace_data = str(input("Input replace note "))
            write_create.update_json(replace_data, json_data_file, position)
            take_notes()
        elif user_prompt == "-help" or user_prompt == "-h":
            print("Input \"-New\" and write a new note\n"
                  "Input \"-cls\" to clear the console\n"
                  "Input \"-sh\" to search the notes by key word\n"
                  "Input \"-tag\" to search the notes by tag word"
                  "Input \"-copy\" to use clipboard\n"
                  "Input \"-today\" to read today notes\n"
                  "Input \"-all\" to read all created notes\n"
                  "Input \"-order\" to open today note by number\n"
                  "Input \"-date\" to open notes by certain day")
            take_notes()
        else:
            take_notes()
    take_notes()


# --file-version=0.10.0.9 --product-name=Organizer --enable-console --mingw64 --standalone --onefile --windows-icon-from-ico=organizer_ico.ico --output-dir="C:\Users\wda61\PycharmProjects\Builds\Organizer" --remove-output


main()
