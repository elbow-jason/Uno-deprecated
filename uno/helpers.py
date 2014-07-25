# -*- coding: utf-8 -*-

def namestr(obj, namespace):
    """
    called via:
        >>> a = 'some var'
        >>> b = namestr(a, globals())
        assert b == ['a'] #for test
    """
    return [name for name in namespace if namespace[name] is obj]

def get_all_parent_methods(cls):
    num_of_dicts = len(cls.mro())
    method_dict = {}
    index_list = list(xrange(num_of_dicts))
    index_list.reverse()
    for i in index_list:
        method_dict = dict(method_dict.items() + cls.mro()[i].__dict__.items())
    return method_dict

def startswith_underscore(dictthing):
    return [x for x in dictthing.keys() if x.startswith('_')]

def startswith_double_underscore(dictthing):
    return [x for x in dictthing.keys() if x.startswith('__')]

def subtract_lists(a, b):
    return list(set(a)-set(b))

def subtract_dicts(a, b):
    a_b = subtract_lists(a.keys(), b.keys())
    new_dict = {}
    for i in a_b:
        new_dict[i] = a[i]
    return new_dict

def remove_list_items_from_dict(list_items, dictthing):
        for x in list_items:
            try:
                del dictthing[x]
            except:
                pass
        return dictthing

def set_kwargs(obj, kwargs):
    if kwargs is not None:
        for key, val in kwargs:
            setattr(obj, key, val)

def set_args_blank(obj, args):
    if args is not None:
        for arg in args:
            setattr(obj, arg, '')


class PlaceHolder(object):
    """
    DO NOT ALTER THIS OBJECT. is for referencing the dict of an __init__ed
    object. Seriously. You'll break everything.
    """
    pass