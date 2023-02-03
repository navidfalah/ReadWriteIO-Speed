import os
import random
from utils import Timer, random_string_generator
import datetime
import shutil


class TimeoutException(Exception):
    pass


def junk_writer(directory_path, num_files, start_size, end_size, time_limit):
    random_string = random_string_generator(1000)
    total_file_size = 0
    start_time = Timer()
    files_step = num_files//10
    for file_count in range(1, num_files+1):
        if file_count%files_step==0:
            with open('/var/run/rw_bench/progress.txt', "w") as f:
                f.write("write "+str(file_count))
        file_name = directory_path + "/" + "junk" + str(file_count) + ".txt"
        if (datetime.datetime.now()-start_time.time).total_seconds() < time_limit:
            with open(file_name, 'w') as bigfile:
                file_size = random.randint(start_size, end_size)
                for _ in range(file_size//1000):
                    total_file_size += bigfile.write(random_string)
                total_file_size += bigfile.write(random_string[:file_size%1000])
                bigfile.flush()
                os.fsync(bigfile.fileno())
        else:
            raise TimeoutException("Timeout exception occured") 
    end_time = Timer()
    return {'duration': (end_time.time-start_time.time).total_seconds(), 'size': total_file_size}


def junk_reader(directory_path, num_files, time_limit):
    start_time = Timer()
    total_file_size = 0
    files_step = num_files//10
    for file_count in range(1, num_files+1):
        if file_count%files_step==0:
            with open('/var/run/rw_bench/progress.txt', "w") as f:
                f.write("read "+str(file_count))
        file_name = directory_path + "/" + "junk" + str(file_count) + ".txt"
        if (datetime.datetime.now()-start_time.time).total_seconds() < time_limit:
            with open(file_name, 'r') as bigfile:
                total_file_size += len(bigfile.read())
        else:
            raise TimeoutException("Timeout exception occured")
    end_time = Timer()
    return {'duration': (end_time.time-start_time.time).total_seconds(), 'size': total_file_size}


def junk_deleter(directory_path):
    start_time = Timer()
    shutil.rmtree(directory_path)
    end_time = Timer()
    return {'duration': (end_time.time-start_time.time).total_seconds()} 
