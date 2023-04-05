#!/usr/bin/env python3

from ..config import PanObject

path = '/mt/monitor'
api_version = "v1"
aggregate = 'agg/custom/license'


class LicenseQuotas(PanObject):
    """List License Quotas
        https://pan.dev/sase/api/mt-monitor/get-mt-monitor-v-1-agg-custom-license-quota/
    """
    _endpoint = f'{path}/{api_version}/{aggregate}/quota'


class LicenseUtilization(PanObject):
    """List License Utilization
        https://pan.dev/sase/api/mt-monitor/get-mt-monitor-v-1-agg-custom-license-utilization/
    """
    _endpoint = f'{path}/{api_version}/{aggregate}/utilization'


class LicenseServiceSetupStatus(PanObject):
    """Retrive an aggreated list of all license service setup statuses across tenants
        https://pan.dev/sase/api/mt-monitor/get-mt-monitor-v-1-agg-custom-license-setup-status/
    """
    _endpoint = f'{path}/{api_version}/{aggregate}/setup/status'
