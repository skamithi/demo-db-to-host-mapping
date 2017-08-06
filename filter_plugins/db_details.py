#!/usr/bin/python

import unittest


def db_details(_dbs, dbname):
    """
    Return db details
    """
    for _db_entry in _dbs:
        if _db_entry.get('name') == dbname:
            return _db_entry
    return {}

class FilterModule(object):
    """ Ansible custom filter plugin """

    def filters(self):
        return {
            'db_details': db_details
        }


class TestDbToHost(unittest.TestCase):
    """
    test case for this filter plugin. to execute
    run ``python db_details.py``
    """
    def test_db_to_host(self):
        dbs =  [{
            "name": "soa0001",
            "portid": "20001"
        }, {
            "name": "boa001",
            "portid": "30001"
        }]
        # Test empty dbs entry
        self.assertEqual(db_details({},'sd'), {})

        # Test formatting returning db entry
        self.assertEqual(db_details(dbs, 'soa0001'), {'name': 'soa0001', 'portid': '20001'})
        # Test that empty entry is returned if dbname is bogus
        self.assertEqual(db_details(dbs, 'soa'), {})

if __name__ == '__main__':
    unittest.main()
