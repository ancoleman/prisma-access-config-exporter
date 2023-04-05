#!/usr/bin/env python3

from ..config import PanObject

path = '/subscription'
api_version = "v1"


class Licenses(PanObject):
    """Subscription Licenses"""
    _required = ["Shared"]
    _no_folder = True
    _endpoint = f'{path}/{api_version}/licenses'


class Instances(PanObject):
    """Subscription Instances"""
    _required = ["Shared"]
    _no_folder = True
    _endpoint = f'{path}/{api_version}/instances'
