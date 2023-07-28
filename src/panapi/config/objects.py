#!/usr/bin/env python3

from ..config import PanObject

sase_path = '/sse/config'
api_version = "v1"

filtered = ["Shared", "Mobile Users", "Mobile Users Explicit Proxy", 'Remote Networks']
position = ['pre', 'post']


class Address(PanObject):
    """An address object"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/addresses'


class AddressGroup(PanObject):
    """An address group"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/address-groups'


class Application(PanObject):
    """An application object"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/applications'


class ApplicationFilter(PanObject):
    """An application filter"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/application-filters'


class ApplicationGroup(PanObject):
    """An application group"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/application-groups'


class ApplicationOverrideRule(PanObject):
    """An application override rule"""
    _required = filtered
    _position = position
    _endpoint = f'{sase_path}/{api_version}/app-override-rules'


class AutoTagAction(PanObject):
    """An auto-tag action"""
    _required = ['Shared']
    _endpoint = f'{sase_path}/{api_version}/auto-tag-actions'


class Certificate(PanObject):
    """An X.509 certificate"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/certificates'


class CertificateProfile(PanObject):
    """A certificate profile"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/certificate-profiles'


class DynamicUserGroup(PanObject):
    """A dynamic user group"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/dynamic-user-groups'


class ExternalDynamicList(PanObject):
    """An external dynamic list"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/external-dynamic-lists'


class HipObject(PanObject):
    """A HIP object"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/hip-objects'


class HipProfile(PanObject):
    """A HIP profile"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/hip-profiles'


class Region(PanObject):
    """A region"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/regions'


class Schedule(PanObject):
    """A schedule"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/schedules'


class Service(PanObject):
    """An application group"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/services'


class ServiceGroup(PanObject):
    """A service group"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/service-groups'


class Tags(PanObject):
    """A Tag"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/tags'


class URLCategory(PanObject):
    """A custom URL category"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/url-categories'


class URLFilteringCategory(PanObject):
    """A prefined URL category"""
    _required = filtered
    _endpoint = f'{sase_path}/{api_version}/url-filtering-categories'
