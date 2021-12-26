
def get_int_from_user(lower_limit=0, higher_limit=0):
    import sys
    if lower_limit > higher_limit:
        temp = lower_limit
        lower_limit = higher_limit
        higher_limit = temp
    while True:
        user_input = input(">>> ")
        if user_input.lower() == "close program":
            sys.exit()
        if user_input.lower() == "stop":
            return None
        try:
            user_input = int(user_input)
        except ValueError:
            print("Input was not an integer! \n"
                  "Type 'close program' to close program or 'break' to return None.")
            continue
        if not lower_limit == higher_limit:
            if user_input < lower_limit:
                print(f"Input Integer was too low. Input a value above or equal to {lower_limit}.")
                continue
            elif user_input > higher_limit:
                print(f"Input Integer was too high. Input a value below or equal to {higher_limit}.")
                continue
            else:
                break
    return user_input


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


def get_existing_filename_from_user(break_word="stop"):
    print("Specify filename (include fileending)! \n"
          "e.g. 'filename.csv'")
    while True:
        filename = get_string_from_user(break_word=break_word)
        if filename is None:
            return None
        import os.path
        if os.path.isfile(csv_filename):
            return filename
        else:
            print("The file does not exist. Type 'close program' to close program or 'stop' to return None!")


def check_create_folder_in_wd(name="data"):
    import os
    if name == "/" or name == "":
        print("No name of Folder given. No folder will be created!")
        return True
    name = "/" + name
    wd = os.getcwd()
    if not os.path.isdir(wd + name):
        wd = os.getcwd()
        path = wd + name
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
            return False
        else:
            print("Successfully created the directory %s " % path)
            return True
    return True


def get_unique_filename_in_folder(folder="data", filename="file", fileending=".txt"):
    if filename == "":
        print("No filename specified! Give filename.\n"
              "No fileending needed! (e.g. 'filename')")
        filename = get_string_from_user()
    filename_current = filename
    if check_create_folder_in_wd(folder):
        import os
        wd = os.getcwd()
        counter = 0
        if folder == "":
            if os.path.isfile(wd + "/" + filename + fileending):
                while True:
                    if os.path.isfile(wd + "/" + filename_current + fileending):
                        counter = counter + 1
                        filename_current = filename + "_" + str(counter)
                    else:
                        filename_current = filename + "_" + str(counter)
                        filename = filename_current
                        break
        else:
            if os.path.isfile(wd + "/" + folder + "/" + filename + fileending):
                while True:
                    if os.path.isfile(wd + "/" + folder + "/" + filename_current + fileending):
                        counter = counter + 1
                        filename_current = filename + "_" + str(counter)
                    else:
                        filename_current = filename + "_" + str(counter)
                        filename = filename_current
                        break
        return folder + "/" + filename + fileending


def update_progress(progress):
    #  in the real code you just have to call update_progress(float from 0 to 1 how far the progress is)
    import sys
    bar_length = 10  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#"*block + "-"*(bar_length-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def open_a_csv_dataframe(csv_filename_or_df=None, header_is_existing="", separator="", decimal_separator=""):
    import pandas as pd
    df = None
    while True:
        if (isinstance(csv_filename_or_df, str)) or (csv_filename_or_df is None) or not (isinstance(csv_filename_or_df,
                                                                                                    pd.DataFrame)):
            if not (isinstance(csv_filename_or_df, str)) and not (csv_filename_or_df is None):
                print("The given file / dataframe was bullshit! Set a new one!")
            while True:
                if csv_filename_or_df == "" or csv_filename_or_df is None:
                    print("No filename given. Specify filename (include fileending)! \n"
                          "e.g. 'filename.csv'")
                    import NormalFunctions
                    while True:
                        csv_filename_or_df = NormalFunctions.get_string_from_user(break_word="stop")
                        if csv_filename_or_df is None:
                            return None
                        import os.path
                        if os.path.isfile(csv_filename_or_df):
                            break
                        else:
                            print(
                                "The file does not exist. Type 'close program' to close program or 'stop' to return None!")
                else:
                    import os.path
                    if os.path.isfile(csv_filename_or_df):
                        pass
                    else:
                        print(
                            "The file does not exist. Type 'close program' to close program or enter new file!")
                        continue
                if header_is_existing == "":
                    import NormalFunctions
                    print("Has the File a header-line? ('y'/'n')")
                    header_is_existing = NormalFunctions.get_string_from_user(first_accepted_word="y",
                                                                              second_accepted_word="n")
                    if header_is_existing == "y":
                        header_is_existing = 0
                    else:
                        header_is_existing = None
                elif header_is_existing == "y":
                    header_is_existing = 0
                elif header_is_existing == "n":
                    header_is_existing = None
                if separator == "":
                    import NormalFunctions
                    while True:
                        print("What is the delimiter of the csv file? \n"
                              "E.g. ',' or ', ' or ';' or '; '")
                        separator = NormalFunctions.get_string_from_user()
                        if not (separator[0] == ",") and not (separator[0] == ";") and not (
                                separator[0] == "\t") and not (
                                separator[0] == " "):
                            print("That is a very unusual separator! Are you sure? ('y'/'n')")
                            sure = NormalFunctions.get_string_from_user(first_accepted_word="y",
                                                                        second_accepted_word="n")
                            if sure.lower() == "y":
                                break
                            if sure.lower() == "n":
                                continue
                        else:
                            break
                if decimal_separator == "":
                    import NormalFunctions
                    while True:
                        print("What is the decimal spearator? \n"
                              "',' or '.'")
                        decimal_separator = NormalFunctions.get_string_from_user()
                        if not (decimal_separator[0] == ",") and not (decimal_separator[0] == "."):
                            print("That is a very unusual decimal separator! Are you sure? ('y'/'n')")
                            sure = NormalFunctions.get_string_from_user(first_accepted_word="y",
                                                                        second_accepted_word="n")
                            if sure.lower() == "y":
                                break
                            if sure.lower() == "n":
                                continue
                        else:
                            break

                df = pd.read_table(csv_filename_or_df, sep=separator, header=header_is_existing, decimal=decimal_separator)
                pd.options.display.max_rows = 8
                print(df)
                print("Is the file correct? ('y'/'n')")
                import NormalFunctions
                file_correct = NormalFunctions.get_string_from_user(first_accepted_word="y", second_accepted_word="n")
                if file_correct == "n":
                    print("Starting again!")
                    csv_filename_or_df = ""
                    separator = ""
                    decimal_separator = ""
                    continue
                elif file_correct == "y":
                    break
            break
        elif isinstance(csv_filename_or_df, pd.DataFrame):
            pd.options.display.max_rows = 8
            df = csv_filename_or_df
            print(df)
            print("Is the dataframe correct? ('y'/'n')")
            import NormalFunctions
            file_correct = NormalFunctions.get_string_from_user(first_accepted_word="y", second_accepted_word="n")
            if file_correct == "n":
                print("Starting again!")
                csv_filename_or_df = ""
                separator = ""
                decimal_separator = ""
                continue
            elif file_correct == "y":
                break
    df.columns = df.columns.astype(str)
    return df
