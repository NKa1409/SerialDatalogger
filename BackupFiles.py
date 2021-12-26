#folder_to_save_to = "C:/Users/nikal/OneDrive/Desktop/test1"
#folder_to_be_saved = "C:/Users/nikal/OneDrive/Desktop/Raspberry Pi"


def get_filechangetime(path):
    import os
    if os.path.exists(path):
        mtime = os.stat(path)
        mtime = mtime.st_mtime
        return mtime
    else:
        return None


def get_list_of_all_filepaths(path_to_read_backup_from):
    import os
    if not os.path.exists(path_to_read_backup_from):
        print("The Folder of which the backup should be created doesn´t exist!")
        return None
    all_filepaths = []
    for subdir, dirs, files in os.walk(path_to_read_backup_from):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            all_filepaths.append(filepath)
    return all_filepaths


def check_if_file_newer_than_prev(filepath, prev_epoch=0):
    if get_filechangetime(filepath) > prev_epoch:
        return filepath
    else:
        return None


def get_epoch_of_last_save(folder_with_logfile):
    import os
    value = 0
    log_filename = folder_with_logfile + "/lastSave.txt"
    try:
        if os.path.isfile(log_filename):
            f = open(log_filename, "r")
            lines = f.readlines()
            value = lines[0].strip()
            f.close()
            try:
                value = float(value)
            except:
                value = 0
                print("No valid epoch in logfile found.")
                print("All files will be saved!")
        else:
            value = 0
            print("No logfile found!")
            print("All files will be saved!")
    except:
        value = 0
        print("All files will be saved!")
    return value


def set_create_logfile_to_new_epoch(folder_with_logfile, sourcepath):
    import time
    current_epoch = time.time()
    current_epoch = str(current_epoch)
    log_filename = folder_with_logfile + "/lastSave.txt"
    try:
        f = open(log_filename, "w")
        f.write(current_epoch)
        f.write("\n")
        f.write(sourcepath)
        f.close()
    except:
        print("Logfile could not be created!")


def check_if_source_is_the_same_as_prev_source(folder_with_logfile, sourcepath):
    log_filename = folder_with_logfile + "/lastSave.txt"
    last_source = ""
    try:
        f = open(log_filename, "r")
        lines = f.readlines()
        last_source = lines[1].strip()
        f.close()
    except:
        pass
    is_the_right_folder = True
    if last_source == "":
        is_the_right_folder = True
    elif not (last_source == sourcepath) and not (last_source == ""):
        print("The folder you want to save is not the same folder you have currently backed up in your "
              "destination folder.\n")
        is_the_right_folder = False
    return is_the_right_folder


def unzip_zipfile_in_folder(zipfilepath):
    import zipfile
    try:
        if zipfilepath.split(".")[1] == "zip":
            pass
    except:
        import re
        filename = re.split('/ |\\\\', zipfilepath)[-1]
        zipfilepath = zipfilepath + "/" + filename + ".zip"
    zipfilepath = zipfilepath.replace("\\", "/")
    source = zipfilepath
    destination = zipfilepath.split("/")[:-2]
    destination = "/".join(destination)
    with zipfile.ZipFile(source, 'r') as zip_ref:
        zip_ref.extractall(destination)
    import os
    os.remove(zipfilepath)


def convert_folder_to_zip_in_that_folder(folder):
    import os
    import shutil
    os.chdir(folder)
    folder_in_which_saved = folder
    zip_filename = "zip"
    archive_from = os.path.dirname(folder)
    archive_to = os.path.basename(folder.strip(os.sep))
    shutil.make_archive(folder_in_which_saved, zip_filename, archive_from, archive_to)
    shutil.move('%s.%s'%(folder_in_which_saved, zip_filename), folder)
    for f in os.listdir(folder):
        if f.endswith(".zip"):
            continue
        try:
            os.remove(os.path.join(folder, f))
        except PermissionError:
            shutil.rmtree(os.path.join(folder, f), ignore_errors=True)


def check_if_only_one_zipfile_in_dest_folder(folder):
    import os
    files_in_folder = os.listdir(folder)
    if len(files_in_folder) > 1:
        return False
    elif len(files_in_folder) == 1:
        if files_in_folder[0].split(".")[1] == "zip":
            return True
        else:
            return False
    return False


def run_backup(folder_to_save_to="", folder_to_be_saved=""):
    import shutil
    import os
    if folder_to_save_to == "":
        print("No destination folder given. Choose destination folder.")
        import easygui
        easygui.msgbox(msg='Choose the folder where you want the backup to be saved.', title='Backup Destination',
                       ok_button='OK')
        folder_to_save_to = easygui.diropenbox(msg="Choose destination folder.", title="Destination Folder")
        if folder_to_save_to is None:
            import sys
            print("No folder chosen. Exiting program...")
            sys.exit()
    if not os.path.exists(folder_to_save_to):
        try:
            os.makedirs(folder_to_save_to)
        except:
            print("An error occured during folder creation (destination).")
            import easygui
            easygui.msgbox(msg='An error occured during creation of the destination folder.\n'
                               'Select a destination folder or create one.', title='Backup Destination',
                           ok_button='OK')
            folder_to_save_to = easygui.diropenbox(msg="Choose destination folder.", title="Destination Folder")
            if folder_to_save_to is None:
                import sys
                print("No folder chosen. Exiting program...")
                sys.exit()
    if folder_to_be_saved == "":
        print("No source folder given. Choose source folder.")
        import easygui
        easygui.msgbox(msg='Choose the folder you want the backup to be made from.', title='Backup Source',
                       ok_button='OK')
        folder_to_be_saved = easygui.diropenbox(msg="Choose source folder.", title="Source Folder")
        if folder_to_be_saved is None:
            import sys
            print("No folder chosen. Exiting program...")
            sys.exit()
    if not os.path.exists(folder_to_be_saved):
        print("No valid backup folder (source) given!")
        import easygui
        easygui.msgbox(msg='No valid source folder given! \n'
                           'Choose the folder you want the backup to be made from.', title='Backup Source',
                       ok_button='OK')
        folder_to_be_saved = easygui.diropenbox(msg="Choose source folder.", title="Source Folder")
        if folder_to_be_saved is None:
            import sys
            print("No folder chosen. Exiting program...")
            sys.exit()
    if check_if_only_one_zipfile_in_dest_folder(folder_to_save_to):
        unzip_zipfile_in_folder(folder_to_save_to)
    prev_save_at_epoch = get_epoch_of_last_save(folder_to_save_to)
    if check_if_source_is_the_same_as_prev_source(folder_to_save_to, folder_to_be_saved) == False:
        import easygui
        if easygui.ynbox(msg='The previously in this destination saved source folder differs from the source folder '
                             'you want to save to this destination folder now.\n'
                             '\n'
                             'Do you want to continue anyway?\n'
                             'The old backup gets deleted!!!', title='Warning'):
            prev_save_at_epoch = 0
            for f in os.listdir(folder_to_save_to):
                try:
                    os.remove(os.path.join(folder_to_save_to, f))
                except PermissionError:
                    shutil.rmtree(os.path.join(folder_to_save_to, f), ignore_errors=True)
        else:
            import sys
            convert_folder_to_zip_in_that_folder(folder_to_save_to)
            sys.exit(0)  # exit the program
    all_files = get_list_of_all_filepaths(folder_to_be_saved)
    changed_files = []
    for files in all_files:
        new_file = check_if_file_newer_than_prev(files, prev_save_at_epoch)
        if not new_file is None:
            changed_files.append(new_file)
    for files in changed_files:
        dest_fpath = files.replace(folder_to_be_saved, folder_to_save_to)
        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        shutil.copy(files, dest_fpath)
    set_create_logfile_to_new_epoch(folder_to_save_to, folder_to_be_saved)
    convert_folder_to_zip_in_that_folder(folder_to_save_to)



#run_backup()
#convert_folder_to_zip_in_that_folder("D:/test1")
#unzip_zipfile_in_folder("D:/test1/test1.zip")