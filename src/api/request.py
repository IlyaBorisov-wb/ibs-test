import requests


class Request:
    BASE_URL = 'https://reqres.in/api'
    TIMEOUT = 1 

    @classmethod
    def post(cls,  path, data={}):
        response = requests.post(f'{cls.BASE_URL}{path}', data=data, timeout=cls.TIMEOUT)
        return response

    @classmethod
    def delete(cls, path):
        response = requests.delete(f'{cls.BASE_URL}{path}', timeout=cls.TIMEOUT)
        return response

    @classmethod
    def get(cls, path, params=''):
        response = requests.get(f'{cls.BASE_URL}{path}', params=params)
        return response


    @classmethod
    def put(cls, path, data):
        response = requests.put(f'{cls.BASE_URL}{path}', data=data)
        return response

    @classmethod
    def patch(cls, path, data={}):
        response = requests.patch(f'{cls.BASE_URL}{path}', data=data)
        return response
