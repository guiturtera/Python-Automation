from sys import flags
from threading import *
import threading
from time import sleep
import os

class Loading():
    def __init__(self, f):
        self.flag = False
        self.f = f

    def __call__(self, *args, **kwds):
        self.f(*args, **kwds)
        def wrapper():
            self.f(*args, **kwds)
        return wrapper


@Loading
def hello_world(text):
    print(text)

hello_world("Hello world")

lock = Lock()
lock.acquire()
flag = True
lock.release()

def load_func():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    loads = [ '|', '/', '-', '\\' ]
    i = 0
    while flag:
        clear()
        print(loads[i])     
        sleep(0.8)
        i = (i + 1) % len(loads)
    clear()

def loading(f):
    def wrapper(*args, **kwargs):
        flag = True
        Thread(target=load_func, name="LoadingThread").start()
        f(*args, **kwargs)    
        flag = False
    return wrapper

#print(a.isDaemon())

flag = True
def flag_changer(obj):
    obj = False

flag_changer(flag)
print(flag)

sleep(5)
flag = False