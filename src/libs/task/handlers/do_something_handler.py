from time import sleep


def do_something_handler(data):
    print("Start task", data)
    print("Just only for testing")
    sleep(10)
    print("End task")
