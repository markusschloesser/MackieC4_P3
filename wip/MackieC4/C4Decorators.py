
import time
import functools
from functools import partial, wraps

class TooSoon(Exception):
  """Can't be called so soon"""
  pass

class CoolDownDecorator(object):
  def __init__(self,func,interval):
    self.func = func
    self.interval = interval
    self.last_run = 0
  def __get__(self,obj,objtype=None):
    if obj is None:
      return self.func
    return partial(self,obj)
  def __call__(self,*args,**kwargs):
    now_nanos = time.process_time_ns()
    now_ms = now_nanos / 1e6
    if now_ms - self.last_run < self.interval:
        to_go = self.last_run + self.interval - now_ms
        raise TooSoon(f"Call after {to_go} milliseconds")
    else:
      self.last_run = now_ms
      return self.func(*args,**kwargs)

def CoolDown(interval):
  def applyDecorator(func):
    decorator = CoolDownDecorator(func=func,interval=interval)
    return wraps(func)(decorator)
  return applyDecorator

# class EmptyMag(Exception):
#   """Can only be called until magazine is empty"""
#   pass

# original code found as answer at https://stackoverflow.com/questions/28767826/python-decorator-call-function-multiple-times
# changes based on the Max Uzi object that rapid-fire-outputs a set number of 'bangs' for every input 'bang'
# changes untested and only useful for rapid-fire bursts, no delay between decorated function calls
# def uzi_func(cache=None, bang_count=1, **func_args):
#     if cache is None:
#         cache = {}
#     if not func_args.keys().__contains__("bang_count"):
#         func_args["bang_count"] = bang_count
#
#     def decorator(func):
#         funcname = func.__name__
#         if funcname not in cache:
#             # save the original function
#             cache[funcname] = func
#         @functools.wraps(func)
#         def wrapped_function(**kwargs):
#             bang_count = func_args.pop("bang_count")
#             while bang_count > 0:
#                 if cache[funcname] != func:
#                     # if cached decorated func-value object with funcname key is != to the wrapped func object,
#                     # also call the cached func with same kwargs
#                     cache[funcname](**func_args)
#                 func(**func_args)
#                 bang_count -= 1
#                 # would need to wait here for any delays, time.sleep() or something?
#         return wrapped_function
#     return decorator