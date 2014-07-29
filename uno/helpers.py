# -*- coding: utf-8 -*-

import itertools
from functools import wraps
from collections import Iterable

from uno import markup




def math_func(f):
    """
    Statics the methods.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            return_type = type(args[0])
        if kwargs.has_key('return_type'):
            return_type = kwargs['return_type']
            kwargs.pop('return_type')
            return return_type(f(*args, **kwargs))
        args = list((setify(x) for x in args))
        return return_type(f(*args, **kwargs))
    return wrapper

def listify(i):
    """
    Iterable to list.
    """
    return list(i)

def tuplify(i):
    """
    Iterable to tuple.
    """
    return tuple(i)

def setify(i):
    """
    Iterable to set.
    """
    return set(i)

@math_func
def intersection(a, b):
    """
    Returns the intersection of sets a and b.

    In plain english:
        Returns all the items that are in both a and b.
    """
    return a.intersection(b)

@math_func
def union(a, b):
    """
    Returns the union of sets a and b.

    In plain english:
        Returns all the items of a and b combined with duplications removed.
    """
    return a.union(b)

@math_func
def minus(a, b):
    """
    Returns the assymetrical difference of set 'a' to set 'b' (a minus b).

    In plain english:
        Remove all the items in 'a' from 'b'. Return 'a'. (Order matters.)

    Minus is set_a.difference(set_b). The nomenclature 'difference 
    is not linguistically descriptive (at least to a layman) so the 
    method 'minus' was used, as the meaning of 'minus' conveys the 
    result of the function more properly (once again... at least to 
    the layman).
    """
    return a.difference(b)

@math_func
def difference(a, b):
    """
    Returns the symmetric difference of sets 'a' and 'b'.

    In plain english:
        Removes all items that occur in both 'a' and 'b'

    Difference is actually set_a.symmetric_difference(set_b), not 
    set.difference(). See 'minus' for set.difference().
    """
    return a.symmetric_difference(b)


def flatten(l):
    return list(chain.from_iterable(l))

def combine_dicts(a, b):
    return dict(a.items() + b.items())

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

def remove_double_underscores(dictthing):
    for key in dictthing.keys():
        if key.startswith('__'):
            del dictthing[key]
    return dictthing

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

def render(obj):
    return getattr(markup, obj._tag).__call__(obj._payload, **obj._css_attrs())

def bi_gram_tuple_to_dict(tup):
    return dict((y, x) for x, y in tup)

from constants import (SELF_CLOSING_TAGS, PAYLOAD, CSS, STATIC_TAGS, 
                        NORMAL_TAGS, ABNORMAL_TAGS,)

PAYLOAD_TAGS = minus(NORMAL_TAGS, ABNORMAL_TAGS)


class ElementHelper(object):

    @staticmethod
    def setup_text_by_tag(tag):
        text = ElementHelper.generate_tag(tag)
        if tag != '':
            if tag in SELF_CLOSING_TAGS:
                text = '<'+ tag +' '+ CSS + ' />'
            for item in STATIC_TAGS:
                if item[0] == tag:
                    text = item[1]
        return text

    @staticmethod
    def bitup_to_css(kwarg_tuple):
        return '{}="{}" '.format(kwarg_tuple[0], kwarg_tuple[1])

    @staticmethod
    def kwargs_to_css(css_dict):
        attrs = ''
        for bi_tup in css_dict.items():
            new = ElementHelper.bitup_to_css(bi_tup)
            attrs += new
        return attrs

    @staticmethod
    def from_markup(tag):
        return getattr(markup, tag).__call__(PAYLOAD, **dict(replace_me=CSS))

    @staticmethod
    def generate_tag(tag):
        try:
            base_element = ElementHelper.from_markup(tag)
        except:
            base_element = ElementHelper.from_markup('div')
            base_element = base_element.replace('div', tag)
        return base_element.replace('replace_me=', '').replace('"', '').replace(' ','')

ele = ElementHelper()