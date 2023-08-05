#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 22:36:13 2020

@author: yves
"""


def filename_prepare(name, extensions, defaut_extension):
    """ 
    return basename, extension tuple
    keeping extension given if it's in extensions list
    add default_extension if not
    """
    name = '_'.join(name.split()).split('.')
    ext = name[-1]
    
    if ext.upper() in [ extension.upper() for extension in extensions]:
        basename = '.'.join(name[:-1])
        ext = ext.lower()
    else:
        basename = '.'.join(name)
        ext = defaut_extension.lower()
        
    return basename, ext

def ensure_attr(obj, key, default):
    """
    put a default attribute if it does not exists or is None
    """
    if hasattr(obj, key):
        if getattr(obj,key) is None:
            setattr(obj,key, default)
    else:
        setattr(obj,key, default)
