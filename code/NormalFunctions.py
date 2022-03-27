class Benchmark:
    def __init__(self):
        import psutil
        import platform
        self.sys_cores = psutil.cpu_count()
        if platform.system() == "Windows":
            self.os = "windows"
        elif platform.system() == "Linux":
            self.os = "linux"
        elif platform.system() == "Darwin":
            self.os = "mac"
        else:
            self.os = "unknown"
        self.flops_per_core = 0
        self.calc_per_sec_per_core = 0
        self.calc_per_sec_whole_system = 0
        self.write_speed = 0
        self.read_speed = 0

    def multiprocess_double_float_cmds_per_sec(self, iterations=50000000, processnumber=0, return_dict={}):
        import time
        import random
        random.seed(time.time())
        start = random.random() * 50
        float_increment = 10 / iterations * random.random()
        floating_point = start
        iterations_in_loop = int(iterations / 10)
        start_time = time.time()
        for i in range(0, iterations_in_loop, 1):
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment
            floating_point += float_increment  # 44 Assembler Anweisungen für einen Schleifendurchlauf
        end_time = time.time()
        calc_per_second = iterations / (end_time - start_time)
        assembler_comands_per_sec = calc_per_second * 4.4
        return_dict[processnumber] = calc_per_second
        return calc_per_second

    def cpu_benchmark(self, cores="max-1", iterations=50000000):
        import psutil
        from multiprocessing import Process, Manager
        max_cores = psutil.cpu_count()
        if cores == "max-1":
            cores = max_cores-1
        elif cores == "max":
            cores = max_cores
        elif cores == "1":
            cores = 1
        else:
            try:
                cores = int(cores)
            except:
                print("The argument for 'cores='num_cores'' could not be converted to an integer! \n"
                      "The argument is required to be of type string and accepted values are: 'max', 'max-1', '1', ..., '16'")
                print("The benchmark will be executed with one core only!")
                cores = 1
        if cores > max_cores:
            print(f"The given number of cores is too large. The number of cores on this system is: {max_cores} \n"
                  f"The benchmark will be executed with {max_cores} cores.")
            cores = max_cores
        elif cores <= 0:
            print(f"The benchmark needs at least one core to run. \n"
                  f"The benchmark will be executed with 1 core.")
            cores = 1
        print("Starting the CPU benchmark...")
        manager = Manager()
        return_dict = manager.dict()
        processes = []
        for core in range(0, cores, 1):
            p = Process(target=self.multiprocess_double_float_cmds_per_sec, args=(iterations, core, return_dict))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        return_values = []
        for i in return_dict:
            return_values.append(return_dict[i])
        self.flops_per_core = return_values
        self.calc_per_sec_per_core = sum(return_values)/cores
        self.calc_per_sec_whole_system = self.calc_per_sec_per_core * self.sys_cores
        return return_values

    def storage_benchmark(self, test_file_size_in_mb=1000, path=""):
        import os
        import time
        filename = "testfileforbenchmarking.txt"
        folder_file_separator = ""
        if os.name == "nt":
            folder_file_separator = "//"
        elif os.name == "posix":
            folder_file_separator = "/"
        string = ""
        for i in range(0, 998, 1):
            string = string + "0"
        string = string + "\n"
        if path == "":
            pass
        else:
            if os.path.isdir(path):
                os.chdir(path)
            else:
                print("Your given path does not exist!")
                print("The current directory will be benchmarked.")
                print("Current directory: " + str(os.getcwd()))
        path = os.getcwd() + folder_file_separator + filename
        try:
            f = open(path, "a")
        except IOError:
            print("The given directory is read-only!")
            print("Current directory: " + str(os.getcwd()))
            return 99999
        print("Starting the storage benchmark...")
        print("File will be written to: " + str(path))
        start_time = time.time()
        for total_mb in range(0, test_file_size_in_mb, 1):
            for iteration in range(0, 1000, 1):
                f.write(string)
        f.close()
        end_time = time.time()
        create_duration = end_time - start_time
        try:
            import shutil
            new_path = os.getcwd() + folder_file_separator
            new_path = new_path + "copytestfileforBenchmark.txt"
            start_time = time.time()
            shutil.copy2(path, new_path)
            end_time = time.time()
            copy_duration = end_time - start_time
            os.remove(new_path)
        except:
            copy_duration = 999999
        start_time = time.time()
        f1 = open(path)
        f1.readlines()
        f1.close()
        end_time = time.time()
        read_duration = end_time - start_time
        remove_time_start = time.time()
        os.remove(path)
        remove_time_end = time.time()
        remove_duration = remove_time_end - remove_time_start
        return_values = [(test_file_size_in_mb / copy_duration), (test_file_size_in_mb / read_duration)]
        self.write_speed = (test_file_size_in_mb / copy_duration)
        self.read_speed = (test_file_size_in_mb / read_duration)
        return return_values

    def check_internet(self):
        import requests
        url_list = ["https://www.google.com/",
                    "https://www.github.com",
                    "https://www.facebook.com",
                    "https://www.bundestag.de",
                    "https://www.example.com"]
        timeout = 5
        for url in url_list:
            try:
                request = requests.get(url, timeout=timeout)
                return True
            except (requests.ConnectionError, requests.Timeout) as exception:
                continue
        return False

    def benchmark(self, cpu=True, storage=True, print_to_terminal=True, cpu_iter=500000000, storage_filesize=5000):
        if __name__ == '__main__':
            if cpu:
                self.cpu_benchmark(iterations=cpu_iter)
            if storage:
                self.storage_benchmark(test_file_size_in_mb=storage_filesize)
            if print_to_terminal:
                if storage:
                    print("Read speed:       " + str(self.read_speed))
                    print("Write speed:      " + str(self.write_speed))
                if cpu:
                    print("FLOPS per core:   " + str(self.calc_per_sec_per_core))
                    print("Systemwide FLOPS: " + str(self.calc_per_sec_whole_system))
            if cpu and storage:
                return [self.read_speed, self.write_speed, self.flops_per_core, self.calc_per_sec_whole_system]
            elif cpu:
                return [self.flops_per_core, self.calc_per_sec_whole_system]
            elif storage:
                return [self.read_speed, self.write_speed]
            else:
                return None


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


def get_string_from_user(break_word="stop", first_accepted_word="", second_accepted_word="",
                         second_close_program_word="", accepted_words=None):
    import sys
    if accepted_words is None:
        accepted_words = []
        accepted_words.append(first_accepted_word)
        accepted_words.append(second_accepted_word)
    else:
        if isinstance(accepted_words, list):
            for iteration in range(0, len(accepted_words), 1):
                if not isinstance(accepted_words[iteration], str):
                    accepted_words[iteration] = str(accepted_words[iteration])
        if isinstance(accepted_words, str):
            accepted_words = [accepted_words]
        if isinstance(accepted_words, int) or isinstance(accepted_words, float):
            accepted_words = [accepted_words]
            for iteration in range(0, len(accepted_words), 1):
                if not isinstance(accepted_words[iteration], str):
                    accepted_words[iteration] = str(accepted_words[iteration])
        if not first_accepted_word == "":
            accepted_words.append(first_accepted_word)
        if not second_accepted_word == "":
            accepted_words.append(second_accepted_word)
    while True:
        user_input = input(">>> ")
        if user_input.lower() == "close program" or user_input.lower() == "close programm":
            sys.exit()
        elif user_input.lower() == break_word:
            return None
        elif not (second_close_program_word == "") and user_input.lower() == second_close_program_word:
            sys.exit()
        elif len(accepted_words) == 0:
            return user_input
        elif (user_input.lower() in accepted_words):
            return user_input
        elif not (user_input.lower() in accepted_words):
            print(f"Input was not an accepted word! The accepted words are:")
            print(accepted_words)
            continue
        else:
            return user_input


def get_string_from_user_v2(break_word="stop", accepted_words=None):
    if accepted_words is None:
        accepted_words = []
    if not accepted_words is None:
        if isinstance(accepted_words, list):
            for iteration in range(0, len(accepted_words), 1):
                if not isinstance(accepted_words[iteration], str):
                    accepted_words[iteration] = str(accepted_words[iteration])
        if isinstance(accepted_words, str):
            accepted_words = [accepted_words]
        if isinstance(accepted_words, int) or isinstance(accepted_words, float):
            accepted_words = [accepted_words]
            for iteration in range(0, len(accepted_words), 1):
                if not isinstance(accepted_words[iteration], str):
                    accepted_words[iteration] = str(accepted_words[iteration])
    import sys
    while True:
        user_input = input(">>> ")
        if user_input.lower() == "close program" or user_input.lower() == "close programm":
            sys.exit()
        elif user_input.lower() == break_word:
            return None
        elif len(accepted_words) == 0:
            return user_input
        elif (user_input.lower() in accepted_words):
            return user_input
        elif not (user_input.lower() in accepted_words):
            print(f"Input was not an accepted word! The accepted words are:")
            print(accepted_words)
            continue
        else:
            return user_input


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
    block = int(round(bar_length * progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block + "-" * (bar_length - block), str(round(progress * 100, 2)),
                                              status)
    sys.stdout.write(text)
    sys.stdout.flush()


def get_existing_filename_from_user(break_word="stop"):
    print("Specify filename (include fileending)! \n"
          "e.g. 'filename.csv'")
    while True:
        import sys
        while True:
            user_input = input(">>> ")
            if user_input.lower() == "close program" or user_input.lower() == "close programm":
                sys.exit()
            elif user_input.lower() == break_word:
                return None
            else:
                filename = user_input
                break
        if filename is None:
            return None
        import os.path
        if os.path.isfile(filename):
            return filename
        else:
            print("The file does not exist. Type 'close program' to close program or 'stop' to return None!")


def get_cpu_percent(core=None):
    import psutil
    cpu_val = psutil.cpu_percent(interval=1, percpu=True)
    if core is None:
        return cpu_val
    elif isinstance(core, int):
        return cpu_val[core]
    else:
        return cpu_val


def get_cpu_cores():
    import psutil
    cpu_cores = psutil.cpu_count()
    return cpu_cores


def get_cpu_freq():
    import psutil
    cpu_freq = psutil.cpu_freq(percpu=False).current
    return cpu_freq


def get_temperatures():
    import psutil
    temperatures = psutil.sensors_temperatures()
    return temperatures


def get_fan_speed():
    import psutil
    fans = psutil.sensors_fans()
    return fans


def get_battery():
    import psutil
    battery = psutil.sensors_battery()
    return battery


def get_disk_usage(return_percent_used=True):
    import psutil
    disk_usage = psutil.disk_usage("/")
    percent_used = disk_usage[3]
    if return_percent_used == True:
        return percent_used
    else:
        return disk_usage


def get_uptime():
    import time
    import psutil
    uptime = time.time() - psutil.boot_time()
    return uptime


def get_boottime(epoch=True):
    import psutil
    import datetime
    if epoch == True:
        boot_time = psutil.boot_time()
        return boot_time
    else:
        boot_time = psutil.boot_time()
        time = datetime.datetime.fromtimestamp(boot_time)
        return time


def get_cur_time(epoch=True):
    import datetime
    import time
    if epoch == True:
        time = time.time()
        return time
    else:
        time = time.time()
        time = datetime.datetime.fromtimestamp(time)
        return time


def check_internet():
    import requests
    url_list = ["https://www.google.com/",
                "https://www.github.com",
                "https://www.facebook.com",
                "https://www.bundestag.de",
                "https://www.example.com"]
    timeout = 5
    for url in url_list:
        try:
            request = requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            continue
    return False


def check_internetspeed():
    import requests
    url = "https://www.google.com/"
    timeout = 5
    try:
        internet_test = requests.get(url, timeout=timeout)
        import speedtest
        wifi = speedtest.Speedtest()
        download = (wifi.download()) / 1000 / 1000
        upload = wifi.upload() / 1000 / 1000
        return download, upload
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Problem with speedtest (try to import module 'speedtest-cli')")
        return 0, 0


