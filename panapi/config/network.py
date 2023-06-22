#!/usr/bin/env python3

from ..config import PanObject

sase_path = '/sse/config'
api_version = "v1"

position = ['pre', 'post']


class BandwidthAllocation(PanObject):
    """A bandwidth allocation"""
    _endpoint = f'{sase_path}/{api_version}/bandwidth-allocations'


class IKECryptoProfile(PanObject):
    """An IKE crypto profile"""
    _required = ['Remote Networks', 'Service Connections']
    _endpoint = f'{sase_path}/{api_version}/ike-crypto-profiles'


class IKEGateway(PanObject):
    """An IKE gateway"""
    _required = ['Remote Networks', 'Service Connections']
    _endpoint = f'{sase_path}/{api_version}/ike-gateways'


class IPSecCryptoProfile(PanObject):
    """An IPSec crypto profile"""
    _required = ['Remote Networks', 'Service Connections']
    _endpoint = f'{sase_path}/{api_version}/ipsec-crypto-profiles'


class IPSecTunnel(PanObject):
    """An IPSec tunnel"""
    _required = ['Remote Networks', 'Service Connections']
    _endpoint = f'{sase_path}/{api_version}/ipsec-tunnels'


class Location(PanObject):
    """A SASE location"""
    _endpoint = f'{sase_path}/{api_version}/locations'
    folder = 'Shared'
    name = 'dummy'

    def list(self, session):
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint
        params = {'folder': self.folder}
        try:
            session.response = session.get(
                url=url,
                params=params
            )
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 200:
                result = session.response.json()
                return result


class QoSPolicyRule(PanObject):
    """A QoS policy rule"""
    _required = ['Remote Networks', 'Service Connections']
    _position = position
    _endpoint = f'{sase_path}/{api_version}/qos-policy-rules'


class QoSProfile(PanObject):
    """A QoS profile"""
    _required = ['Remote Networks', 'Service Connections']
    _endpoint = f'{sase_path}/{api_version}/qos-profiles'


class RemoteNetwork(PanObject):
    """A SASE remote network"""
    _required = ['Remote Networks']
    _endpoint = f'{sase_path}/{api_version}/remote-networks'


class SharedInfrastructureSetting(PanObject):
    """Shared Infrastructure Settings"""
    _required = ['Shared']
    _endpoint = f'{sase_path}/{api_version}/shared-infrastructure-settings'


class ServiceConnection(PanObject):
    """Service Connections"""
    _required = ['Service Connections']
    _endpoint = f'{sase_path}/{api_version}/service-connections'


class InternalDNSServer(PanObject):
    """Internal DNS Servers"""
    _endpoint = f'{sase_path}/{api_version}/internal-dns-servers'


class TrafficSteeringRule(PanObject):
    """Traffic steering rules"""
    _endpoint = f'{sase_path}/{api_version}/traffic-steering-rules'


class BgpRouting(PanObject):
    """SC BGP Routing Configuration"""
    _endpoint = f'{sase_path}/{api_version}/bgp-routing'
