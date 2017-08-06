# DB To Host Mapping Demo - Ansible Playbook

This sample project shows how you can define an host inventory that houses
multiple unique databases and then provide a playbook that

a. Takes a database name as a parameter

b. The playbook will figure out the correct host to connect to and run a simulation
to confirm that it is connected to the correct host that houses that database.

c. The playbook has some checks. That is if the dbname is bogus then take no action and
alert the user of the fact. Also not all hosts listed in the inventory must contain ``dbs`` entries.
Script is intelligent enough to only search hosts with ``dbs`` entries.

d. Shows you how to use roles with this configuration

The Ansible inventory data feed into Ansible looks something like this:

```
{
    "_meta": {
        "hostvars": {
            "ts001": {
                "ansible_host": "localhost",
                "ansible_port": "9001",
                "ansible_user": "root",
                "dbs": [
                    {
                        "name": "dbH001",
                        "portid": "20001"
                    },
                    {
                        "name": "dbS001",
                        "portid": "30001"
                    }
                ]
            },
            "ts002": {
                "ansible_host": "localhost",
                "ansible_port": "9002",
                "ansible_user": "root",
                "dbs": [
                    {
                        "name": "dbH002",
                        "portid": "20002"
                    },
                    {
                        "name": "dbS002",
                        "portid": "30002"
                    }
                ]
            },

    "all": {
        "hosts": [
            "ts001",
            "ts002",
        ]
    },
    "dbcluster_oregon": {
        "hosts": [
            "ts001"
        ]
    },
    "dbcluster_michigan": {
        "hosts": [
            "ts002"
        ]
    }
}

```
## Requirements

* Ansible 2.3+
* Docker Engine
* docker.py Python module: Use ``pip install docker.py`` or yum/apt install ``python-docker``


## Install Procedure


### Start Docker containers
Install 18 docker containers with various database names attached to the inventory
```
ansible-playbook docker-containers.yml
```

To remove  all the docker containers run
```
ansible-playbook docker-containers -e "docker_ops=absent"
```

### Run the demo

Database names start with "dbH0XX" where XX is a number starting from 00 to 18.
Also database names start with "dbS0XX" where XX is a number starting from 00 to 18.

In this demo first test to see what happens when you put in a bogus database name

```
ansible-playbook --private-key=keys/ansible_test demo.yml -i inventory.py -e "dbname=bogus"
```

Then test to see what happens when you put in a valid name

```
ansible-playbook --private-key=keys/ansible_test demo.yml -i inventory.py -e "dbname=dbH002"
```

## Demo Output


### Wrong database name
```
:% ansible-playbook --private-key=keys/ansible_test  -i inventory.py -e "dbname=db" demo.yml                                 <roles ✗>

PLAY [localhost] ***************************************************************************************************************************************************************

TASK [assert] ******************************************************************************************************************************************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [Connect to the Local ansible server and parse out all the database to host mappings] *************************************************************************************
ok: [localhost]

TASK [Check that the database name entered exists in the mapping. After that connect the host found
where the database resides] ************************************************
fatal: [localhost]: FAILED! => {
    "assertion": "db_mapping != ''",
    "changed": false,
    "evaluated_to": false,
    "failed": true,
    "msg": "Unable to find the host of database db"
}
  to retry, use: --limit @/home/skamithi/git/demo-db-to-host-mapping/demo.retry

PLAY RECAP *********************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=1


```


### Correct Database name

```
% ansible-playbook --private-key=keys/ansible_test  -i inventory.py -e "dbname=dbS001" demo.yml                             <roles ✗>

PLAY [localhost] ***************************************************************************************************************************************************************

TASK [assert] ******************************************************************************************************************************************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [Connect to the Local ansible server and parse out all the database to host mappings] *************************************************************************************
ok: [localhost]

TASK [Check that the database name entered exists in the mapping. After that connect the host found
where the database resides] ************************************************
ok: [localhost] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY [all:&ts001] **************************************************************************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************************************************************
ok: [ts001]

TASK [get-db-details : assert] *************************************************************************************************************************************************
ok: [ts001] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [get-db-details : Get all the details regarding the database] *************************************************************************************************************
ok: [ts001]

TASK [db-maintenance : include] ************************************************************************************************************************************************
included: /home/skamithi/git/demo-db-to-host-mapping/roles/db-maintenance/tasks/startup.yml for ts001

TASK [db-maintenance : print out a message simulating a DB startup] ************************************************************************************************************
ok: [ts001] => {
    "changed": false,
    "msg": "Startup DB dbS001 on ts001 on port ID 30001"
}

TASK [db-maintenance : include] ************************************************************************************************************************************************
included: /home/skamithi/git/demo-db-to-host-mapping/roles/db-maintenance/tasks/shutdown.yml for ts001

TASK [db-maintenance : print out a message simulating a DB shutdown] ***********************************************************************************************************
ok: [ts001] => {
    "changed": false,
    "msg": "Shutting down DB dbS001 on ts001 on port ID 30001"
}

PLAY RECAP *********************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0
ts001                      : ok=7    changed=0    unreachable=0    failed=0


```
