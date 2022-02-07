import Serial
import sys
import keyboard



def serial_commands():
        print("   'log' - Logs incoming data from serial port\n"
              "   'log strip' - Logs incoming data in a real csv-file (removes first and second delimiter)\n"
              "   'set filename' - Sets or changes the filename to which data is written\n"
              "   'write serial' - Lets you enter a message which is then sent to serial\n"
              "   'show update' - Prints serial data to screen by updating a single line\n"
              "   'show serial' - Prints all new serial data to screen\n"
              "   'show old data' - Prints all recieved serial data to screen\n"
              "\n"
              "   'close' - Closes Program\n")


def get_string_from_user(break_word="stop", first_accepted_word="", second_accepted_word="", second_close_program_word=""):
    import sys
    while True:
        user_input = input(">>> ")
        if user_input.lower() == "close program" or user_input.lower() == "close programm":
            sys.exit()
        elif user_input.lower() == break_word:
            return None
        elif not (second_close_program_word == "") and user_input.lower() == second_close_program_word:
            sys.exit()
        elif (not first_accepted_word == "") or (not second_accepted_word == ""):
            if user_input == first_accepted_word or user_input == second_accepted_word:
                return user_input
            else:
                print(f"Input was not an accepted word! The accepted words are: '{first_accepted_word}' and"
                      f" '{second_accepted_word}'!\n"
                      f"Or type '{break_word}' to return None.")
                continue
        else:
            return user_input


def delete_valuenames_from_csv(filename="", delimiter="xxxxx", keep_value_after_this_upto_delimiter="xxxxx"):
    import sys
    if filename == "":
        while True:
            file = input("From which file should the real csv be created? (include Fileending!) \n"
                         ">>> ")
            if file == "stop":
                sys.exit()
            try:
                with open(file, "r") as f:
                    testline = f.readline().strip()
                    filename = file
                    break
            except:
                print("File could not be opened! Try another filename or 'stop' to exit the program!")
                continue
    new_filename = filename.split(".")
    new_filename = new_filename[0]
    new_filename = new_filename + "-realcsv.txt"
    reading_file_line_counter = 0
    reading_new_file_line_counter = 0
    if delimiter == "xxxxx":
        delimiter = input("First Delimiter \n"
                          ">>> ")
        if delimiter == "stop":
            sys.exit()
    if keep_value_after_this_upto_delimiter == "xxxxx":
        keep_value_after_this_upto_delimiter = input("Specify the second delimiter! \n"
                                                     "For every element of the csv, everything behind the second "
                                                     "delimiter up to the first delimiter in a line will be saved! \n"
                                                     "Second Delimiter \n"
                                                     ">>> ")
        if keep_value_after_this_upto_delimiter == "stop":
            sys.exit()
    try:
        with open(filename, "r") as f:
            while True:
                try:
                    line = f.readline().strip()
                    if line is None or line == "":
                        break
                    reading_file_line_counter = reading_file_line_counter + 1
                except:
                    break
    except FileNotFoundError:
        print("No file found to convert to real csv!")
        return
    try:
        with open(new_filename, "r") as f:
            while True:
                try:
                    line = f.readline().strip()
                    if line is None or line == "":
                        break
                    reading_new_file_line_counter = reading_new_file_line_counter + 1
                except:
                    break
    except FileNotFoundError:
        pass
    if reading_file_line_counter > reading_new_file_line_counter:
        with open(filename, "r") as f:
            for iteration in range(reading_new_file_line_counter):
                line = f.readline().strip()
            while True:
                try:
                    line = f.readline().strip()
                    reading_file_line_counter = reading_file_line_counter + 1
                    if line is None or line == "":
                        break
                except:
                    break
                if keep_value_after_this_upto_delimiter in line:
                    liste = line.split(delimiter)
                    with open(new_filename, "a") as newfile:
                        for iteration in range(len(liste)):
                            value = liste[iteration].split(keep_value_after_this_upto_delimiter, 1)
                            if iteration >= 1:
                                try:
                                    newfile.write(", " + str(value[1]))
                                except IndexError:
                                    return new_filename
                            else:
                                try:
                                    newfile.write(str(value[1]))
                                except IndexError:
                                    return new_filename
                        newfile.write("\n")
                else:
                    with open(new_filename, "a") as newfile:
                        newfile.write(line)
                        newfile.write("\n")
    return new_filename



print("Starting Program...")
serial = Serial.SerialClass()
print("")
print("")
while True:
    serial_commands()
    while True:
        cmd = get_string_from_user()
        if cmd is None:
            serial_commands()
            continue
        if cmd.lower() == "close":
            sys.exit()
        elif cmd.lower() == "set filename":
            serial.set_filename_and_timestamp()
            serial_commands()
        elif cmd.lower() == "log" or cmd.lower() == "start logging":
            print("")
            print("Press 'q' to stop logging data.")
            while True:
                serial_data = serial.serial_readline_to_file_if_line_is_available()
                if not (serial_data is None):
                    sys.stdout.write("\r" + "                                                                          "
                                            "                                       ")
                    sys.stdout.flush()
                    sys.stdout.write("\r" + str(serial_data))
                    sys.stdout.flush()
                if keyboard.is_pressed("q"):
                    break
            print("")
            print("")
        elif cmd.lower() == "log strip":
            print("")
            print("What is the delimiter of the incoming data?"
                  "e.g.: incoming data: 'U1=0.243,U2=1.23,U3=1.002'; ',' is first delimiter, '=' is second delimiter")
            delimiter = get_string_from_user()
            print("What is the second delimiter? \n"
                  "The second delimiter stands in front of the actual value you want "
                  "to be saved.\n"
                  "e.g.: incoming data: 'U1=0.243,U2=1.23,U3=1.002'; ',' is first delimiter, '=' is second delimiter")
            second_delimiter = get_string_from_user()
            print("Press 'q' to stop logging data.")
            while True:
                serial_data = serial.serial_readline_to_file_if_line_is_available()
                if not (serial_data is None):
                    sys.stdout.write("\r" + "                                                                          "
                                            "                                       ")
                    sys.stdout.flush()
                    sys.stdout.write("\r" + str(serial_data))
                    sys.stdout.flush()
                    Serial.delete_valuenames_from_csv_file(filename=serial.filename, delimiter=delimiter,
                                                           keep_value_after_this_upto_delimiter=second_delimiter)
                if keyboard.is_pressed("q"):
                    break
            print("")
            print("")
        elif cmd.lower() == "write serial":
            print("What should be written to serial?")
            to_be_written_to_serial = get_string_from_user()
            if to_be_written_to_serial is None or to_be_written_to_serial == "":
                continue
            serial.serial_write_line(to_be_written_to_serial)
            print(f"'{to_be_written_to_serial}' was sent to serial device!")
            serial_commands()
        elif cmd.lower() == "show update":
            print("Press 'q' to stop updating data.")
            print("")
            while True:
                import sys
                serial_data = serial.serial_readline_if_line_is_available()
                if not (serial_data is None):
                    sys.stdout.write("\r" + "                                                                          "
                                            "                                       ")
                    sys.stdout.flush()
                    sys.stdout.write("\r" + str(serial_data))
                    sys.stdout.flush()
                if keyboard.is_pressed("q"):
                    break
            print("")
            print("")
        elif cmd.lower() == "show old data" or cmd.lower() == "show old" or cmd.lower() == "print old" or cmd.lower() == "print old data":
            print("Recieved data:")
            print("")
            serial.print_volatile_storage()
            print("\n")
            serial_commands()
        elif cmd.lower() == "show serial":
            print("Press 'q' to stop updating data.")
            print("")
            while True:
                import sys
                serial_data = serial.serial_readline_if_line_is_available()
                if not (serial_data is None):
                    print(serial_data)
                if keyboard.is_pressed("q"):
                    break
            print("")
            print("")
            serial_commands()
        else:
            print("Invalid input. Try again or type 'close' to close program.")
            serial_commands()
