import functools
from typing import Callable

# Decorators add functionalities into a function
# Hello world decorator
def hello_incremental(f):
    def how_doing(): # only good ones will know that one xD
        f()
        print("How you doing?")
    return how_doing
# Or even simpler
def hello_incremental2(f):
    return lambda:(f(), print("How you doing2"))
    
@hello_incremental2
@hello_incremental
def hello_world_func():
    print("Hello world\n")

hello_world_func()

# Simple decorator
# Adding a square to a function with decorator

# In order to accept arguments do as follows:
def green_text(f):
    @functools.wraps(f)
    def inside(*args, **kwargs):
        print('\033[92m', end="")
        f(*args, **kwargs)
        print('\033[m', end="")
    return inside

@green_text
def write_text(text):
    print(text)

write_text("hello world")

# You can pass arguments to decorators
def raise_exponent(exponent=2):
    def wrapper_1(f):
        @functools.wraps(f)
        def wrapper_2(*args, **kwargs):
            return f(*args, **kwargs) ** exponent
        return wrapper_2
    return wrapper_1 

@raise_exponent(exponent=3)
def sum(*nums):
    num = 0
    for i in nums:
        num += i
    return num

print(sum(2 + 2))

# You can build a class decorator    
class Lifecycle(object):
    def __init__(self, f) -> None:
        print("ClickSimulation -> __init__")
        self.memory = 0
        self.f = f

    # this method stores the state of the object.
    def __call__(self, *args, **kwargs):
        print("ClickSimulation -> __call__")
        self.memory += 1
        self.f(self.memory)
        return self.f

    def option(self, *args):
        print("ClickSimulation -> option")
        return self

# it is instantiated one only time
@Lifecycle.option
@Lifecycle # instantiates the class itself
def say_something(*args):
    print(*args)

say_something()
say_something()
say_something()
say_something()
say_something()

# even more advanced
print('\n\nMore advanced:')
class command(object): # very poor click example
    def __init__(self, value):
        print("ClickSimulation -> __init__")
        self.value = value

    # this method stores the state of the object.
    def __call__(self, *args):
        print("ClickSimulation -> __call__")
        def wrapper(*argss):
            f = args[0]
            f(f"value -> {self.value}\nother args -> {argss}")
        return wrapper

@command('command_name')
def say_something_else(command_name):
    print(command_name)

# here I'll simulate CLI command
say_something_else("command")