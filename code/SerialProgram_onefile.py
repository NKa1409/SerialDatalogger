#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
import datetime
import keyboard

class SerialClass:
    def __init__(self, filename="", comport="", baudrate=0, timestamp=""):
        # creates serial object in serial class.
        # Benutzer muss COM Port und Baudrate eingeben
        # ser = SerialClass()
        # ser ist jetzt das Objekt
        # es wird die variable self.comport erstellt, welche allerdings keine funktion besitzt.
        # ser.set_filename_and_timestamp(filenamefunc="asdf.txt") erstellt eine Datei mit namen asdf.txt und fragt den
        # Benutzer, ob er einen timestamp in der Datei angezeigt bekommt.
        # es werden die self.timestamp und self.filename variablen gesetzt.
        self.filename = ""
        self.timestamp = ""
        self.whole_buffer = ""
        self.volatile_storage_old_lines = []
        self.max_chars_in_volatile_storage = 3000000
        import serial.tools
        import serial.tools.list_ports
        self.ser = serial.Serial()
        if comport == "":
            print("Available COM Ports:")
            all_available_com_ports = serial.tools.list_ports.comports(include_links=False)
            for ports in all_available_com_ports:
                print(ports)
            com_port = input("Input name of COM Port of Serial Device (e.g. 'COM4') \n"
                             ">>> ")
            if com_port == "close program":
                sys.exit()
            is_eingabe_in_com_ports = False
            for ports in all_available_com_ports:
                if com_port in ports:
                    is_eingabe_in_com_ports = True
            while not is_eingabe_in_com_ports:
                print("COM Port is not available. Try an available COM Port!")
                print("Enter 'close program' to close program!")
                all_available_com_ports = serial.tools.list_ports.comports(include_links=False)
                for ports in all_available_com_ports:
                    print(ports)
                com_port = input("Input name of COM Port of Serial Device (e.g. 'COM4') \n"
                                 ">>> ")
                if com_port == "close program":
                    sys.exit()
                for ports in all_available_com_ports:
                    if com_port in ports:
                        is_eingabe_in_com_ports = True
                        break
            self.ser.port = com_port
            self.comport = com_port
        else:
            self.ser.port = comport
            self.comport = comport
        if baudrate == 0:
            print("")
            print("Default Baudrate of ESP32: 115200")
            print("Default Baudrate of Arduino: 9600")
            baudrate_val = input("Enter baudrate of Serial Connection \n"
                                 ">>> ")
            if baudrate_val == "close program":
                sys.exit()
            while True:
                try:
                    baudrate_val = int(baudrate_val)
                    if baudrate_val <= 0:
                        print("Baudrate must not be <= 0!")
                        baudrate_val = input("Enter baudrate of Serial Connection \n"
                                             ">>> ")
                        continue
                    break
                except ValueError:
                    print("Input was not a number!")
                    baudrate_val = input("Enter baudrate of Serial Connection \n"
                                         ">>> ")
                    if baudrate_val == "close program":
                        sys.exit()
            self.ser.baudrate = baudrate_val
            self.baudrate = baudrate_val
        else:
            self.ser.baudrate = baudrate
            self.baudrate = baudrate
        self.ser.timeout = 0.5
        try:
            self.ser.open()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print("Connected to: " + self.ser.portstr)
            print("")
        except serial.SerialException:
            print("Could not open COM Port. Exiting Program!")
            sys.exit()
        if filename == "":
            self.filename = ""
        elif filename == "dt":
            time = datetime.datetime.now()
            string = time.strftime("%Y_%m_%d %H-%M-%S")
            string = string + ".txt"
            string = "data/" + string
            self.filename = string
        else:
            filename = "data/" + filename
            self.filename = filename
        if timestamp.lower() == "y":
            self.timestamp = "y"
        elif timestamp.lower() == "n":
            self.timestamp = "n"
        else:
            self.timestamp = "y"
        try:
            self.whole_buffer = self.ser.read(self.ser.in_waiting).strip().decode("utf-8")
        except:
            self.whole_buffer = ""

    def set_filename_and_timestamp(self, filenamefunc="", timestampfunc=""):
        # self.set_filename_and_timestamp()
        # sorgt dafür dass der benutzer gefragt wird, wie die Datei heißen soll und ob sie einen Timestamp besitzen soll
        # self.set_filename_and_timestamp(filenamefunc="asdf.txt", timestampfunc="y")
        # sorgt dafür, dass eine datei erstellt wird (asdf.txt) und self.timestampfunc mit "y" beschrieben wird.
        # dabei werden vom benutzer keine eingaben verlangt!
        if filenamefunc == "":
            print("Specify textfile filename. If name should be current date and time write 'dt'!")
            print("File ending should be included. e.g.: 'test.txt'")
            self.filename = input("Filename \n"
                                  ">>> ")
        else:
            self.filename = filenamefunc
        if self.filename == "dt":
            time = datetime.datetime.now()
            string = time.strftime("%Y_%m_%d %H-%M-%S")
            string = "Serial_" + string + ".txt"
        else:
            string = self.filename
        wd = os.getcwd()
        if not os.path.isdir(wd + '/data'):
            wd = os.getcwd()
            path = wd + "/data"
            try:
                os.mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)
        string = "data/" + string
        self.filename = string
        while True:
            try:
                f = open(string, "a")
                break
            except OSError or FileNotFoundError:
                print("Error occured during initialising file! Try different name!")
                print("If name should be current date and time write 'dt'!")
                print("File ending should be included. e.g.: 'test.txt'")
                self.filename = input("Filename \n"
                                      ">>> ")
                if self.filename == "dt":
                    time = datetime.datetime.now()
                    string = time.strftime("%Y_%m_%d %H-%M-%S")
                    string = "Serial_" + string + ".txt"
                else:
                    string = self.filename
                string = "data/" + string
                self.filename = string
        f.close()
        print(f"File is created with name: {string}")
        self.filename = string
        while True:
            if timestampfunc == "":
                print("Should the file contain a timestamp? ('y' / 'n')")
                self.timestamp = input(">>> ")
            elif timestampfunc.lower() == "y":
                self.timestamp = timestampfunc
            elif timestampfunc.lower() == "n":
                self.timestamp = timestampfunc
            else:
                timestampfunc = "notValid"
            if self.timestamp.lower() == "y" or self.timestamp.lower() == "n":
                if self.timestamp.lower() == "y":
                    pass
                    #print(f"Timestamp for file {self.filename} will be created!")
                if self.timestamp.lower() == "n":
                    pass
                    #print(f"Timestamp for file {self.filename} will not be created!")
                break
            elif self.timestamp.lower() == "stop":
                sys.exit()
            else:
                print("Invalid input! Try again or type 'stop' to exit Program!")
        return string

    def serial_readline_if_line_is_available(self, print_line_to_console=False):
        # Wenn eine vollständige Zeile im Serial input verfügbar ist, wird diese Zeile eingelesen und als vollständig
        # decodierte Zeile zurückgegeben.
        # Wenn keine zeile verfügbar ist wird None zurückgegeben
        # serObject = SerialClass()
        # newserialLine = serObject.serial_readline_if_line_is_available()
        try:
            self.whole_buffer = self.whole_buffer + self.ser.read(self.ser.in_waiting).decode("utf-8")
        except UnicodeDecodeError:
            pass
        line = self.whole_buffer.split("\n", 1)
        try:
            self.whole_buffer = line[1]
            if print_line_to_console:
                print(line[0])
            temp_storage_line = line[0]
            num_chars_in_volatile_storage_old_lines = 0
            for element in self.volatile_storage_old_lines:
                num_chars_in_volatile_storage_old_lines = num_chars_in_volatile_storage_old_lines + len(element)
            while num_chars_in_volatile_storage_old_lines > self.max_chars_in_volatile_storage:
                del self.volatile_storage_old_lines[0]
                num_chars_in_volatile_storage_old_lines = 0
                for element in self.volatile_storage_old_lines:
                    num_chars_in_volatile_storage_old_lines = num_chars_in_volatile_storage_old_lines + len(element)
            self.volatile_storage_old_lines.append(temp_storage_line)
            return line[0]
        except:
            self.whole_buffer = line[0]
            return None

    def print_volatile_storage(self):
        for element in self.volatile_storage_old_lines:
            print(element)
        return self.volatile_storage_old_lines

    def serial_readline_to_file_if_line_is_available(self, print_line_to_console=False):
        # wenn eine vollständige serial Line im buffer ist, wird diese line ausgelesen und in eine file mit dem
        # filename self.filename geschrieben. dabei wird abhängig von self.timestamp ein timestamp hinzugefügt.
        # es wird die jeweils hinzugefügte Zeile zurückgegeben.
        # serialObject = SerialClass()
        # newLineToFile = serialObject.serial_readline_to_file_if_line_is_available()

        import serial.tools.list_ports
        if self.filename == "" or self.timestamp == "":
            self.set_filename_and_timestamp(filenamefunc="dt", timestampfunc="y")
        line = self.serial_readline_if_line_is_available(print_line_to_console=print_line_to_console)
        if not (line is None):
            try:
                f = open(self.filename, "a")
            except PermissionError:
                print("Critical Error while opening file!")
                sys.exit()
            if self.timestamp.lower() == "y":
                time = datetime.datetime.now()
                millisek = time.strftime("%f")
                millisek = int(millisek) / 1000
                millisek = int(millisek)
                time = time.strftime("%Y_%m_%d %H-%M-%S")
                time = time + "-" + str(millisek).zfill(3)
                all_available_com_ports = serial.tools.list_ports.comports(include_links=False)
                device = ""
                for entry in all_available_com_ports:
                    if self.comport in entry:
                        device = entry
                f.write(str(time) + " - " + str(device) + ";")
            f.write(str(line) + "\n")
            f.close()
            return str(line)
        else:
            return

    def serial_write_line(self, line):
        line = str(line) + "\n"
        self.ser.write(line.encode())
        return


def delete_valuenames_from_csv_file(filename="", delimiter="xxxxx", keep_value_after_this_upto_delimiter="xxxxx"):
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


def create_open_file_with_filename():
    # Fragt den Benutzer nach einem Dateinamen und erstellt die Datei
    # und gibt den Dateinamen dann als string zurück
    print("Specify filename. If name should be current date and time write 'dt'!")
    print("File ending should be included. e.g.: 'test.txt'")
    filename = input("Filename: ")
    print("")
    if filename == "dt":
        time = datetime.datetime.now()
        string = time.strftime("%Y_%m_%d %H-%M-%S")
        string = string + ".txt"
    else:
        string = filename
    wd = os.getcwd()
    if not os.path.isdir(wd + '/data'):
        wd = os.getcwd()
        path = wd + "/data"
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
    string = "data/" + string
    while True:
        try:
            f = open(string, "a")
            break
        except OSError or FileNotFoundError:
            print("Error occured during initialising file! Try different name!")
            print("If name should be current date and time write 'dt'!")
            print("File ending should be included. e.g.: 'test.txt'")
            filename = input("Filename: ")
            print("")
            if filename == "dt":
                time = datetime.datetime.now()
                string = time.strftime("%Y_%m_%d %H-%M-%S")
                string = "data/" + string
            else:
                string = filename
                string = "data/" + string
    f.close()
    print(f"File is created with name: {filename} with location: {string}")
    print("")
    print("")
    return filename


def write_list_as_csv_to_file(filename=None, liste=None, timestamp=False):
    if liste is None:
        print("List is not given. Give list and try again!")
        return 0
    if filename is None:
        print("Filename of textfile is not specified. Set filename! (Include Ending: '.txt') \n"
              "For date and time as filename: 'dt'")
        filename = input(">>> ")
    if filename == "dt":
        time = datetime.datetime.now()
        string = time.strftime("%Y_%m_%d %H-%M-%S")
        string = string + ".txt"
        filename = string
    wd = os.getcwd()
    if not os.path.isdir(wd + '/data'):
        wd = os.getcwd()
        path = wd + "/data"
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
    filename = "data/" + filename
    try:
        f = open(filename, "a")
    except PermissionError:
        return
    if timestamp:
        time = datetime.datetime.now()
        millisek = time.strftime("%f")
        millisek = int(millisek) / 1000
        millisek = int(millisek)
        time = time.strftime("%Y_%m_%d %H-%M-%S")
        time = time + "-" + str(millisek).zfill(3)
        f.write(str(time) + ", ")
    for item in liste:
        f.write(str(item) + ", ")
    f.write("\n")
    f.close()

##############################################################################

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


if __name__ == "__main__":
    print("Starting Program...")
    serial = SerialClass()
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
                        sys.stdout.write("\r" + "                                       "
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
                        sys.stdout.write("\r" + "                                       "
                                                "                                       ")
                        sys.stdout.flush()
                        sys.stdout.write("\r" + str(serial_data))
                        sys.stdout.flush()
                        delete_valuenames_from_csv_file(filename=serial.filename, delimiter=delimiter,
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
            elif cmd.lower() == "show old data" or cmd.lower() == "show old" or cmd.lower() == "print old" or cmd.lower() == "print old data":
                print("Recieved data:")
                print("")
                serial.print_volatile_storage()
                print("\n")
                serial_commands()
            elif cmd.lower() == "show update":
                print("Press 'q' to stop updating data.")
                print("")
                while True:
                    serial_data = serial.serial_readline_if_line_is_available()
                    if not (serial_data is None):
                        sys.stdout.write("\r" + "                                       "
                                                "                                       ")
                        sys.stdout.flush()
                        sys.stdout.write("\r" + str(serial_data))
                        sys.stdout.flush()
                    if keyboard.is_pressed("q"):
                        break
                print("")
                print("")
            elif cmd.lower() == "show serial":
                print("Press 'q' to stop updating data.")
                print("")
                while True:
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
    
