#!/usr/bin/env python3

from ..config import PanObject

path = '/tenancy'
api_version = "v1"


class Tenant(PanObject):
    'A Tenant Service Group ID'
    _endpoint = f'{path}/{api_version}/tenant_service_groups'
