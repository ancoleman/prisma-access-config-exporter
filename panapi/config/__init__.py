#!/usr/bin/env python3


class PanObject:
    """Base class for all resource objects

    This class defines a configuration object that can defined in Palo Alto Networks Unified Cloud Manager. 
    """
    _base_url = 'https://api.sase.paloaltonetworks.com'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._headers = {'Content-Type': 'application/json'}

    def __str__(self):
        return str(self.__dict__)

    def create(self, session):
        params = {}
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint
        headers = {'Content-Type': 'application/json'}
        if hasattr(self, 'folder'):
            params.update({'folder': self.folder})
        if hasattr(self, 'position'):
            params.update({'position': self.position})
        if hasattr(self, 'name'):
            params.update({'name': self.name})
        else:
            params = {}
        try:
            print(self.payload)
            session.response = session.post(
                url=url,
                headers=self.headers,
                params=params,
                json=self.payload
            )
            status_code = session.response.status_code
        except Exception as err:
            print(err)
            return err
        else:
            if status_code == 201 or status_code == 200:
                config = session.response.json()
                self.id = config.get('id')
                return type(self)(**config)
            if status_code == 404 or status_code == 400:
                config = session.response.json()
                errors = config.get('_errors')
                details = errors[0].get('details')
                nerrors = details.get('errors')[0]
                return type(self)(**nerrors)

    def monitor(self, session):
        params = {}
        if session.is_expired:
            session.reauthenticate()
        # ptype = hasattr(self, 'product_type')
        # tperiod = hasattr(self, 'time_period')
        if hasattr(self, 'product_type'):
            params.update({'product_type': self.product_type})
        if hasattr(self, 'time_period'):
            params.update({'time_period': self.time_period})
        try:
            url = self._base_url + self._endpoint
            session.response = session.get(
                url=url,
                params=params,
                headers=self.headers
            )
            status_code = session.response.status_code
        except Exception as err:
            print(err)
            return err
        else:
            if status_code == 200:
                result = session.response.json()
                if 'data' in result:
                    if len(result['data']) > 0:
                        config = result['data'][0]
                        return type(self)(**config)
                    else:
                        result['data'].append({'message': 'no license info found'})
                        config = result['data'][0]
                        return type(self)(**config)
            if status_code == 404 or status_code == 400:
                result = session.response.json()
                return type(self)(**result)

    def read(self, session):
        params = {}
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint
        if hasattr(self, 'folder'):
            params.update({'folder': self.folder})
        if hasattr(self, 'position'):
            params.update({'position': self.position})
        if hasattr(self, 'name'):
            params.update({'name': self.name})
        has_id = hasattr(self, 'id')
        has_name = hasattr(self, 'name')
        has_tsg_id = hasattr(self, 'tsg_id')
        has_p_type = hasattr(self, 'product_type')
        if has_id:
            url = self._base_url + self._endpoint + '/{}'.format(self.id)
        elif has_name:
            params.update({'name': self.name})
        elif has_tsg_id:
            url = self._base_url + self._endpoint + f'/{self.tsg_id}/operations/list_children'
        elif has_p_type:
            url = self._base_url + self._endpoint
        else:
            raise ValueError('name or id value is required')
        try:
            if has_tsg_id:
                session.response = session.post(
                    url=url,
                    params=params,
                    headers=self.headers
                )
            else:
                session.response = session.get(
                    url=url,
                    params=params,
                    headers=self.headers
                )
                print(session.response.json())
        except Exception as err:
            print(err)
            return err
        else:
            if session.response.status_code == 200:
                result = session.response.json()
                if has_id:
                    return type(self)(**result)
                elif has_name:
                    if 'data' in result:
                        config = result['data'][0]
                        return type(self)(**config)
                    elif 'id' in result:
                        return type(self)(**result)
                elif has_tsg_id:
                    return type(self)(**result)
            if session.response.status_code == 404:
                result = session.response.json()
                print(result)
                return type(self)(**result)

    def list(self, session):
        params = {}
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint
        if hasattr(self, 'folder'):
            params.update({'folder': self.folder})
        if hasattr(self, 'position'):
            params.update({'position': self.position})
        if hasattr(self, 'name'):
            params.update({'name': self.name})
        if hasattr(self, 'limit'):
            params.update({'limit': self.limit})
        if hasattr(self, 'offset'):
            params.update({'offset': self.offset})
        try:
            session.response = session.get(
                url=url,
                params=params
            )
        except Exception as err:
            print(err)
            return err
        else:
            if session.response.status_code == 200:
                result = session.response.json()
                # if self._endpoint == '/subscription/v1/instances':
                #     print(result)
                obj_list = []
                if 'data' in result:
                    for config in result['data']:
                        obj_list.append(type(self)(**config))
                elif type(result) == list:
                    for config in result:
                        obj_list.append(type(self)(**config))
                else:
                    obj_list.append(type(self)(**result))
                return obj_list

    def update(self, session):
        if session.is_expired:
            session.reauthenticate()
        if hasattr(self, 'id'):
            url = self._base_url + self._endpoint + '/{}'.format(self.id)
        else:
            url = self._base_url + self._endpoint
        # headers = {'Content-Type': 'application/json'}
        if hasattr(self, 'folder'):
            params = {'folder': self.folder}
        else:
            params = {}
        try:
            session.response = session.put(
                url=url,
                headers=self.headers,
                params=params,
                json=self.payload
            )
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 200:
                config = session.response.json()
            # return config

    def delete(self, session):
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint + '/{}'.format(self.id)
        headers = {'Content-Type': 'application/json'}
        if hasattr(self, 'folder'):
            params = {'folder': self.folder}
        else:
            params = {}
        try:
            session.response = session.delete(
                url=url,
                headers=self.headers,
                params=params
            )
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 200:
                del (self)
                return session.response.json()

    @property
    def payload(self):
        # items = {k:v for k,v in self.__dict__.items() if k not in {'folder', 'id'}}
        items = {k: v for k, v in self.__dict__.items()}
        return items

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, val):
        self._headers = val
