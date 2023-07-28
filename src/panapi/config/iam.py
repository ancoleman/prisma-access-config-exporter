#!/usr/bin/env python3

from ..config import PanObject

path = '/iam'
api_version = "v1"


class AccessPolicies(PanObject):
    """SASE Access Policies
        https://pan.dev/sase/api/iam/get-iam-v-1-access-policies/
    """
    _required = ["Shared"]
    _no_folder = True
    _endpoint = f'{path}/{api_version}/access_policies'


class Permissions(PanObject):
    """SASE Permissions
        https://pan.dev/sase/api/iam/get-iam-v-1-permissions/
    """
    _required = ["Shared"]
    _no_folder = True
    _endpoint = f'{path}/{api_version}/permissions'


class ServiceAccounts(PanObject):
    """SASE Service Accounts
        https://pan.dev/sase/api/iam/get-iam-v-1-service-accounts/
    """
    _required = ["Shared"]
    _no_folder = True
    _endpoint = f'{path}/{api_version}/service_accounts'


class Roles(PanObject):
    """SASE Roles
        https://pan.dev/sase/api/iam/get-iam-v-1-roles/
    """
    _required = ["Shared"]
    _no_folder = True
    _endpoint = f'{path}/{api_version}/roles'
