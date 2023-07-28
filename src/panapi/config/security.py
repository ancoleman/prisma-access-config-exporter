#!/usr/bin/env python3

from ..config import PanObject

sase_path = '/sse/config'
api_version = "v1"

position = ['pre', 'post']


class AntiSpywareProfile(PanObject):
    'An anti-spyware profile'
    _endpoint = f'{sase_path}/{api_version}/anti-spyware-profiles'


class AntiSpywareSignature(PanObject):
    'An anti-spyware signature'
    _endpoint = f'{sase_path}/{api_version}/anti-spyware-signatures'


class DNSSecurityProfile(PanObject):
    'A DNS security profile'
    _endpoint = f'{sase_path}/{api_version}/dns-security-profiles'


class DecryptionExclusion(PanObject):
    'A decryption exclusion'
    _endpoint = f'{sase_path}/{api_version}/decryption-exclusions'


class DecryptionProfile(PanObject):
    'A decryption profile'
    _endpoint = f'{sase_path}/{api_version}/decryption-profiles'


class DecryptionRule(PanObject):
    'A decryption rule'
    _position = position
    _endpoint = f'{sase_path}/{api_version}/decryption-rules'


class FileBlockingProfile(PanObject):
    'A file blocking profile'
    _endpoint = f'{sase_path}/{api_version}/file-blocking-profiles'


class HTTPHeaderProfile(PanObject):
    'An HTTP header profile'
    _endpoint = f'{sase_path}/{api_version}/http-header-profiles'


class ProfileGroup(PanObject):
    'A profile group'
    _endpoint = f'{sase_path}/{api_version}/profile-groups'


class SecurityRule(PanObject):
    'A security rule'
    _position = position
    _endpoint = f'{sase_path}/{api_version}/security-rules'


class URLAccessProfile(PanObject):
    'A URL access profile'
    _endpoint = f'{sase_path}/{api_version}/url-access-profiles'


# class URLCategories(PanObject):
#     'A URL Custom Category'
#     _endpoint = f'{sase_path}/{api_version}/url-categories'


class URLFilteringCategories(PanObject):
    'A URL Filtering Category'
    _endpoint = f'{sase_path}/{api_version}/url-filtering-categories'


class VulnerabilityProtectionProfile(PanObject):
    'A vulnerability protection profile'
    _endpoint = f'{sase_path}/{api_version}/vulnerability-protection-profiles'


class VulnerabilityProtectionSignature(PanObject):
    'A vulnerability protection signature'
    _endpoint = f'{sase_path}/{api_version}/vulnerability-protection-signatures'


class WildFireAntivirusProfile(PanObject):
    'A WildFire antivirus profile'
    _endpoint = f'{sase_path}/{api_version}/wildfire-anti-virus-profiles'
