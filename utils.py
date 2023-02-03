import datetime
from datetime import timedelta
import random
import string
byte_to_mg_dividor = 1000000

class Timer():

    def __init__(self):
        self.time = datetime.datetime.now()


def Printer_results(junker_tuple, type_operation):
    total_file_size = junker_tuple[2]/byte_to_mg_dividor
    total_seconds = (junker_tuple[1].time-junker_tuple[0].time).total_seconds()
    try:
        mg_per_sec = total_file_size/total_seconds
        print(f"{type_operation}, speed: {mg_per_sec} MB/s, Mg={total_file_size}, s={total_seconds}")
    except ZeroDivisionError:
        print("division zero, no file to read")

def random_string_generator(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)
