# coding: utf-8

import importlib


def import_loading(path):
    parts = path.split('.')
    package = '.'.join(parts[-1])

    module = importlib.import_module(package)
    return getattr(module, parts[-1])
