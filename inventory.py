#!/usr/bin/env python

import argparse

try:
    import json
except ImportError:
    import simplejson as json


class DockerInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        self.hostname_base = 'ts'
        self.software_groups = ['app', 'web', 'db']
        self.environment_groups = ['dev', 'test', 'prod']
        # Count must be a multiple of 18. Need to fix this bug at some point
        self.host_count = 18
        self.host_range = range(1, self.host_count+1)
        self.ansible_groups = {}
        for _group in self.software_groups:
            self.ansible_groups[_group] = []
            for _group in self.environment_groups:
                self.ansible_groups[_group] = []

        # Called with "--list"
        if self.args.list:
            self.inventory = self.docker_inventory()
        elif self.args.host:
            # Implement a -- host option.. Probably not needed but
            # just leave it here
            self.inventory = self.empty_inventory()

        else:
            # if no --list or --host option are specified.  Return an empty inventory
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))

    def chunks(self, l, n):
        return [l[i:i + n] for i in xrange(0, len(l), n)]

    def docker_inventory(self):
        _software_groupings = self.chunks(self.host_range,
                                          (self.host_count /
                                           len(self.software_groups)))
        for _software_group_idx, _groupone in enumerate(_software_groupings):
            _env_groupings = self.chunks(
                _groupone,
                (len(_groupone)/len(self.environment_groups))
            )
            for _env_group_idx, _grouptwo in enumerate(_env_groupings):
                for _hostitem in _grouptwo:
                    self.ansible_groups[self.software_groups
                                        [_software_group_idx]].append(_hostitem)
                    self.ansible_groups[self.environment_groups
                                        [_env_group_idx]].append(_hostitem)
        self.inventory['all'] =  { 'hosts': [] }
        self.inventory['_meta'] = {'hostvars': {}}
        for _i in self.host_range:
            self.inventory['_meta']['hostvars']["ts%03d" % (_i)] = {
                'ansible_port': "9%03d" % (_i),
                'ansible_host': 'localhost',
                'ansible_user': 'root',
                'dbs': [
                    { 'name': "dbH%03d" % (_i), "portid": "20%03d" % (_i) },
                    { 'name': "dbS%03d" % (_i), "portid": "30%03d" % (_i) }
                ]
            }
            self.inventory['all']['hosts'].append("ts%03d" % (_i))

        for _ansible_group, _hostnumbers in self.ansible_groups.items():
            self.inventory[_ansible_group] = {}
            self.inventory[_ansible_group]['hosts'] = \
                ["%s%02d" % (self.hostname_base, x) for x in _hostnumbers]

        return self.inventory

    def empty_inventory(self):
        return {'_meta': {'host_vars': {}}}

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


if __name__ == '__main__':
    DockerInventory()
