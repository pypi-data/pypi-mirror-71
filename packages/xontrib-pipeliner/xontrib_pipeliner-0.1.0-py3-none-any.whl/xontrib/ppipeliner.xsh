import os
from multiprocessing import Pool, cpu_count

class xontribPipelinerParallel(object):
   def __init__(self):
       pass

   def f(self, args):
       code, line, num = args
       return eval(code, globals(), locals())

   def go(self, func_args, stdout):
       with Pool(cpu_count()) as p:
           parallel_tasks = p.imap_unordered(self, func_args)
           for result in parallel_tasks:
               print(result, file=stdout, flush=True)

   def __call__(self, x):
     return self.f(x)