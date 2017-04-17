"""
This files adds Python decorators to the program.
Decorators can be used as a wrapper around methods. This way,
code can be executed as a wrapper around any defined method.

The syntax looks like this:
    @wrapper_function
    def main_function():

What basically happens is this:
    wrapper_function()
        # This the outer wrapper
        execute some code
        main_function()
        return
By using decorators, a wrapper can be added to EVERY method.
This is used to print the method name whenerver it is entered, without having
to use print statements in the methods themselves. This cleans up the code
by quite a lot.
"""
import settings


def check_debug(func):
    """ Use a wrapper around the given function. The wrapper will cause
        every method to print its own name when called if debugging
        has been enabled in the settings. """
    def print_debug_statement(*args, **kwargs):
        if settings.ENABLE_DEBUG:
            print("DEBUG -- Entered method %s" % func.func_name)
        return func(*args, **kwargs)
    return print_debug_statement
