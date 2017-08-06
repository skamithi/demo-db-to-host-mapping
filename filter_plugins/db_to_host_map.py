#!/usr/bin/python

import unittest


def db_to_host(_hostvars):
    """
    Return db_to_host mapping.
    """
    _db_to_host_var = {}
    if _hostvars:
        for _hostname, _entry in _hostvars.items():
            _dbs = _entry.get('dbs')
            if _dbs:
                for _db_entry in _entry.get('dbs'):
                    _db_to_host_var[_db_entry.get('name')] = {
                        'host': _hostname,
                        'portid': _db_entry.get('portid')}
    return _db_to_host_var


def get_single_db_entry(_hostvars, dbname):
    result = db_to_host(_hostvars)
    return result.get(dbname)


class FilterModule(object):
    """ Ansible custom filter plugin """

    def filters(self):
        return {
            'db_to_host_map': get_single_db_entry
        }


class TestDbToHost(unittest.TestCase):
    """
    test case for this filter plugin. to execute
    run ``python db_to_host.py``
    """
    def test_db_to_host(self):
        _hostvars = {
            "ts001": {
                "dbs": [{
                    "name": "soa0001",
                    "portid": "20001"
                }, {
                    "name": "boa001",
                    "portid": "30001"
                }]
            },
            "ts003": {
            },
            "ts002": {
                "dbs": [{
                    "name": "soa0002",
                    "portid": "20002"
                }, {
                    "name": "boa002",
                    "portid": "30002"
                }]
            }
        }
        # Test empty hostvars
        self.assertEqual(db_to_host({}), {})

        result = db_to_host(_hostvars)
        # Test formatting hostvars to give you Host to DB mapping.
        self.assertEqual(result.keys().sort(),
                         ['soa0001', 'boa001', 'soa0002', 'boa002'].sort())
        # Test getting a single DB to host mapping.
        self.assertEqual(get_single_db_entry(_hostvars, 'soa0002'),
                         {'host': 'ts002', 'portid': '20002'})
        # Test if db name is invalid. return nothing
        self.assertEqual(get_single_db_entry(_hostvars, 'soa002'), None)

if __name__ == '__main__':
    unittest.main()
