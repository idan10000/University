# Author: adif

import os
import os.path
import operator

import multiprocessing
from contextlib import contextmanager
from threading import Thread
import functools
import signal

from importlib.machinery import SourceFileLoader
import xml.etree.ElementTree as ET
import csv


CSV_NAME = "grades.csv"
TIME_LIMIT = 4  # time limit for single function run in sec


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    # used to timeout on unix systems- see the optional in 'examine_for_errors'
    def signal_handler(_, __):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def timeout(time_out):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [TimeoutException("TimeOut!")]

            def new_func():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=new_func)
            t.daemon = True
            try:
                t.start()
                t.join(time_out)
            except Exception as je:
                print('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco


def examine_for_errors(module_path, test_schema, output_dict):
    total_grade = 0
    total_errors = ""
    student_id = get_id_from_path(module_path)

    root = ET.parse(test_schema).getroot()

    try:
        hw_module = SourceFileLoader("test_name", module_path).load_module()  # TODO: change module name
        set_tests(hw_module)
    except Exception as e:
        total_errors += "YYYE: " + str(e)

        if student_id not in output_dict:
            output_dict[student_id] = [0, ""]

        output_dict[student_id] = list(map(operator.add, output_dict[student_id], [total_grade, total_errors]))
        return

    for function_obj in root:
        try:
            curr_function = getattr(hw_module, function_obj.tag)
        except AttributeError:
            total_errors += function_obj.get("sign") + ", "
            continue

        for test in function_obj:
            grade = int(test.get("grade"))
            sign = function_obj.get("sign")
            inputs = test.iterfind("input")
            outputs = {output.get("id"): output for output in test.findall("output")}

            success = True

            for input_element in inputs:
                input_id = input_element.get("id")
                output_element = outputs[input_id]
                try:
                    input_values = eval("[" + input_element.text + "]")
                    output_values = eval("[" + output_element.text + "]")

                    @timeout(TIME_LIMIT)
                    def test_now(*input_values):
                        return curr_function(*input_values)


                    function_output = test_now(*input_values)
                    output_values = output_values[0]

                    if function_output != output_values:
                        total_errors += "T" + sign + "_" + input_id + ", "
                        success = False
                        break

                except Exception as e:
                    if "missing 1 required positional" in str(e):
                        continue
                    total_errors += "T" + sign + "_" + input_id + "E: '" + repr(e) + "', "
                    success = False
                    break

            if success:
                total_grade += grade

    if student_id not in output_dict:
        output_dict[student_id] = [0, ""]

    output_dict[student_id] = list(map(operator.add, output_dict[student_id], [total_grade, total_errors]))


def get_exercise_list(path):
    def filter_func(file_name):
        return file_name.endswith(".py")
    exercise_list = os.listdir(path)
    exercise_list = list(map(lambda file_name: path + file_name, filter(filter_func, exercise_list)))
    return exercise_list


def grade_submissions(exercise_list, test_schema):
    manager = multiprocessing.Manager()
    graded_submissions_dict = manager.dict()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # pool = multiprocessing.Pool(processes=1)  # for single process

    pool.starmap(
        examine_for_errors,
        ((exercise_path, test_schema, graded_submissions_dict) for exercise_path in exercise_list)
    )
    pool.starmap(find_conventions_errors, ((exercise_path, graded_submissions_dict) for exercise_path in exercise_list))

    return dict(graded_submissions_dict)


def find_conventions_errors(_, __):
    # for future implementation
    return


def write_results_to_csv(csv_path, graded_submissions):
    with open(csv_path+CSV_NAME, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "grade", "errors"], delimiter=",")
        for student_id in graded_submissions:
            grade = graded_submissions[student_id][0]
            errors = graded_submissions[student_id][1]
            writer.writerow({"id": student_id, "grade": grade, "errors": errors})


def get_id_from_path(path):
    return os.path.basename(path)[4:-3]


def set_tests(hw_module):
    """
    How to add function to the student module:

    %
    def add_me():
        print('yes!')

    d = {'add_me':add_me()}
    %

    call using: hw_module.add_me()
    """

    def check_output():
        file_name = "./output.txt"
        out = None
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                a = '7\n2\n5\n7\n7\n9\n9\n10\n7\n14\n9\n9\n0\n9\n11\n9\n0\n7\n8\n0\n10\n6\n0\n11\n6\n8\n9\n9\n11\n12\n11\n11\n5\n9\n7\n7\n10\n9\n9\n8\n6\n10\n0\n8\n0'
                if a!=f.read(100):
                    out = 'Wrong output :('

            os.remove(file_name)
            return out

        else:
            return 'no file found..'

    d = {
        'check_output': check_output,
    }

    for k in d:
        setattr(hw_module, k, d[k])


def main():


    file_location = input("Insert python file location (or folder for multiple files): ")
    scheme_path = input("Insert scheme file location: ")
    if os.path.isfile(file_location):
        d = {}
        examine_for_errors(file_location, scheme_path, d)
        out = d[list(d.keys())[0]]
        print("grade: ", out[0])
        print("errors: ", out[1])
        input()

    elif os.path.isdir(file_location):
        # expected python names are: "hw#_123456789.py"
        file_location += "\\"  # for sad Windows users
        submissions = get_exercise_list(file_location)
        graded_submissions_dict = grade_submissions(submissions, scheme_path)
        write_results_to_csv(file_location, graded_submissions_dict)

    else:
        print("Wrong input type")
        input()


if __name__ == '__main__':
    main()
