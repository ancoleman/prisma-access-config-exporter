#!/usr/bin/env python3

from ..config import PanObject

path = '/sse/connector'
api_version = "v2.0"


class ZTNAConnectors(PanObject):
    """ZTNA Connectors"""
    _endpoint = f'{path}/{api_version}/api/connectors'


class ZTNAConnectorGroups(PanObject):
    """ZTNA Connector Groups"""
    _endpoint = f'{path}/{api_version}/api/connector-groups'


class ZTNAApplications(PanObject):
    """ZTNA Applications"""
    _endpoint = f'{path}/{api_version}/api/applications'


class ZTNADiscoveredApps(PanObject):
    """ZTNA Discovered Applications"""
    _endpoint = f'{path}/{api_version}/api/discovered-applications'


class ZTNALicense(PanObject):
    """ZTNA Licenses"""
    _endpoint = f'{path}/{api_version}/api/license'
