#!/usr/bin/env python3

from ..config import PanObject

sase_path = '/sse/config'
api_version = "v1"


class AuthenticationSettings(PanObject):
    """A SASE Mobile-Agent Authentication Settings"""
    _required = ['Mobile Users']
    _endpoint = f'{sase_path}/{api_version}/mobile-agent/authentication-settings'


class AgentProfiles(PanObject):
    """A SASE Mobile-Agent Profile"""
    _required = ['Mobile Users']
    _endpoint = f'{sase_path}/{api_version}/mobile-agent/agent-profiles'


class GlobalSettings(PanObject):
    """A SASE Mobile-Agent Global Settings"""
    _endpoint = f'{sase_path}/{api_version}/mobile-agent/global-settings'


class InfrastructureSettings(PanObject):
    """A SASE Mobile-Agent Infrastructure Settings"""
    _required = ['Mobile Users']
    _endpoint = f'{sase_path}/{api_version}/mobile-agent/infrastructure-settings'


class TunnelProfiles(PanObject):
    """A SASE Mobile-Agent Tunnel Profiles"""
    _required = ['Mobile Users']
    _endpoint = f'{sase_path}/{api_version}/mobile-agent/tunnel-profiles'


class Locations(PanObject):
    """A SASE Mobile-Agent Locations"""
    _required = ['Mobile Users']
    _endpoint = f'{sase_path}/{api_version}/mobile-agent/locations'