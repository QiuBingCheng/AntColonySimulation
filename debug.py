# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:46:44 2021

@author: Jerry
"""
import functools,inspect

def print_log():
    """
    We create a parent function to take arguments
    :param path:
    :return:
    """
    
    def get_default_args(func):
        signature = inspect.signature(func)
        return {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }

    def log(func):
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_names = list(inspect.signature(func).parameters.keys())
            dic = {arg:value for arg,value in zip(args_names,args)}
            
            default_args = get_default_args(func)
            for key,val in default_args.items():
                if key not in dic:
                    dic[key] = val
            dic.pop('self', None)
            dic.pop('cls', None)
            print(f"====={func.__name__} is called=====")
            print(dic)
            #print(f"return:{func(*args, **kwargs)}")
            return func(*args, **kwargs)
        return wrapper
    
    return log

