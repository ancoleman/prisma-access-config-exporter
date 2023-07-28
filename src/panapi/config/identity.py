#!/usr/bin/env python3

from ..config import PanObject

sase_path = '/sse/config'
api_version = "v1"


class AuthenticationPortal(PanObject):
    """An authentication portal"""
    _endpoint = f'{sase_path}/{api_version}/authentication-portals'


class AuthenticationProfile(PanObject):
    """An authentication profile"""
    _endpoint = f'{sase_path}/{api_version}/authentication-profiles'


class AuthenticationRule(PanObject):
    """An authentication rule"""
    _endpoint = f'{sase_path}/{api_version}/authentication-rules'


class AuthenticationSequence(PanObject):
    """An authentication sequence"""
    _endpoint = f'{sase_path}/{api_version}/authentication-sequences'


class KerberosServiceProfile(PanObject):
    """A Kerberos server profile"""
    _endpoint = f'{sase_path}/{api_version}/kerberos-server-profiles'


class LDAPServerProfile(PanObject):
    """An LDAP server profile"""
    _endpoint = f'{sase_path}/{api_version}/ldap-server-profiles'


class LocalUser(PanObject):
    """A local user"""
    _endpoint = f'{sase_path}/{api_version}/local-users'


class MFAServer(PanObject):
    """A multi-factor authentication server"""
    _endpoint = f'{sase_path}/{api_version}/mfs-servers'


class RADIUSServerProfile(PanObject):
    """A RADIUS server profile"""
    _endpoint = f'{sase_path}/{api_version}/radius-server-profiles'


class SAMLServerProfile(PanObject):
    """A SAML server profile"""
    _endpoint = f'{sase_path}/{api_version}/saml-server-profiles'


class TACACSServerProfile(PanObject):
    """A TACACS server profile"""
    _endpoint = f'{sase_path}/{api_version}/tacacs-server-profiles'
