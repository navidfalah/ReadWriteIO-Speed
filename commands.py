import os
from junker import junk_writer, junk_reader, junk_deleter, TimeoutException
import argparse
import json
from typing import Tuple


class Command():

    def execute(self):
        raise NotImplementedError("Commands must implement the execute method")


class WriteJunkFile(Command):

    """craete all junk files"""
    def execute(self, directory_path="junk_files", files_count=20, start_size=1000000, end_size=10000000, time_limit=20) -> Tuple[bool, str]:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        try:
            result = junk_writer(directory_path, files_count, start_size, end_size, time_limit)
        except IOError as e:
            print(e)
            return(False, str(e))
        except TimeoutException as e:
            print("Timeout exception occured")
            return(False, str(e))
        else:
            return(True, result)


class ReadJunkFile(Command):

    """read all junkfiles"""
    def execute(self, directory_path="junk_files", files_count=20, time_limit=20) -> Tuple[bool, str]:
        try:
            result = junk_reader(directory_path, files_count, time_limit)  
        except IOError as e:
            print(e)
            return(False, str(e))
        except TimeoutException as e:
            print("Timeout exception occured")
            return(False, str(e))
        else:
            return(True, result)
        

class DeleteJunkFile(Command):

    """delete all junkfiles"""
    def execute(self, directory_path="junk_files", files_count=20, time_limit=20) -> Tuple[bool, str]:
        try:
            result = junk_deleter(directory_path)
        except OSError as e:
            print(e)
            return(False, str(e))
        else:
            return(True, result)


class WriteAndReandJunkFile(Command):
    """craete all junk files"""
    def execute(self, directory_path="junk_files", files_count=20, start_size=1000000, end_size=10000000, time_limit=20,
    no_read=False,no_write=False,no_delete=False,no_caches=False) -> None:
        result = {}
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        if not no_write:
            write_result = WriteJunkFile().execute(directory_path, files_count, start_size, end_size, time_limit)
            result['write'] = write_result
        if not no_caches:
            with open('/proc/sys/vm/drop_caches', 'w') as cache_file:
                cache_file.write('3')
        if not no_read:
            read_result = ReadJunkFile().execute(directory_path, files_count, time_limit)
            result['read'] = read_result
        if not no_delete:
            delete_result = DeleteJunkFile().execute(directory_path)
            result['delete'] = delete_result
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory-path", help="directory path for junk files",
                        type=str)
    parser.add_argument("--files-count", help="number of files",
                        type=int)
    parser.add_argument("--start-size", help="minimum file size",
                        type=int)
    parser.add_argument("--end-size", help="maximum file size",
                        type=int)
    parser.add_argument("--time-limit", help="max time limit",
                        type=int)
    parser.add_argument("--no-caches", help="delete caches",
                        action='store_true')
    parser.add_argument("--no-read", help="allow reading files",
                        action='store_true')
    parser.add_argument("--no-write", help="allow writting files",
                        action='store_true')
    parser.add_argument("--no-delete", help="allow deleting files",
                        action='store_true')
    args = parser.parse_args()

    parameters = {k:v for k,v in vars(args).items() if v }
    print(parameters)
    result = WriteAndReandJunkFile().execute(**parameters)
    
    print(json.dumps(result))

