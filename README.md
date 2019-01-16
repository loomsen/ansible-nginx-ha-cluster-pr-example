# `whoami`
The main purpose of this repo is to provide a meaningful example for [a pull request against molecule.](https://github.com/ansible/molecule/pull/1646)
This is an example ansible role to set up an active-active keepalived cluster, which monitors nginx on two hosts.
There's a molecule scenario in the generic_laodbalancer repo, which will setup the cluster and run a side-effect playbook afterwards, to kill nginx on one host.
The verifier, [which is goss](https://github.com/aelsabbahy/goss), will check if the IP moved to the second host.

## Installation/Usage
Checkout the repo, install requirements, cd into the roles/generic_loadbalancer directory, install optional requirements if you want to use mitogen, and run 
`molecule test`

##### Converge
This is the setup after converge. Active-active nginx cluster with keepalived managing the IPs.
```
|  nginx - glb-001 | <-- keepalived active/active --> |  nginx - glb-002 |
| vip: 10.10.10.10 | <-- keepalived active/active --> | vip: 10.10.10.11 |
```
##### Side-Effect
Our side-effect playbook now kills nginx on the first host. We are expecting the keepalived to move over the IP to the second host.

```
|  nginx - glb-001 -> dead  | <-- keepalived active/active --> |      nginx - glb-002         |
| vip: move ip to glb-002   | <-- keepalived active/active --> | ip: 10.10.10.10, 10.10.10.11 |
```

## Tests

#### common tests
These tests should run on both nodes:

```yaml
---
package:
  nginx:
    installed: true
  keepalived:
    installed: true
user:
  nginx:
    exists: true
    groups:
    - nginx
    home: /var/lib/nginx
    shell: /sbin/nologin
group:
  nginx:
    exists: true
```

#### node specific tests
This test should run only on node2, where we expect both our VIPs to be now.
```yaml
---
service:
  nginx:
    enabled: true
    running: true
port:
  tcp:80:
    listening: true
    ip:
      - 0.0.0.0
eth0:
  exists: true
  addrs:
    - 10.10.10.11/32
    - 10.10.10.10/32
```

This test should run only on node1, where we killed nginx.
```yaml
---
service:
  nginx:
    enabled: true
    running: false
port:
  tcp:80:
    listening: false

eth0:
  exists: true
  addrs: []

```



##### example output
Here's what a test run looks like.
```
--> Validating schema /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/molecule.yml.
Validation completed successfully.
--> Test matrix
    
└── default
    ├── lint
    ├── destroy
    ├── dependency
    ├── syntax
    ├── create
    ├── prepare
    ├── converge
    ├── idempotence
    ├── side_effect
    ├── verify
    └── destroy
    
--> Scenario: 'default'
--> Action: 'lint'
--> Executing Yamllint on files found in /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/...
Lint completed successfully.
--> Executing Yamllint on files found in /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/tests/...
Lint completed successfully.
--> Executing Ansible Lint on /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/playbook.yml...
Lint completed successfully.
--> Scenario: 'default'
--> Action: 'destroy'
    
    PLAY [Destroy] *****************************************************************
    
    TASK [Destroy molecule instance(s)] ********************************************
    Wednesday 16 January 2019  10:42:23 +0100 (0:00:00.107)       0:00:00.107 *****
    changed: [localhost] => (item=None)
    changed: [localhost] => (item=None)
    changed: [localhost]
    
    TASK [Wait for instance(s) deletion to complete] *******************************
    Wednesday 16 January 2019  10:42:26 +0100 (0:00:02.527)       0:00:02.634 *****
    ok: [localhost] => (item=None)
    ok: [localhost] => (item=None)
    ok: [localhost]
    
    TASK [Delete docker network(s)] ************************************************
    Wednesday 16 January 2019  10:42:26 +0100 (0:00:00.596)       0:00:03.231 *****
    skipping: [localhost]
    
    PLAY RECAP *********************************************************************
    localhost                  : ok=2    changed=1    unreachable=0    failed=0
    
    Wednesday 16 January 2019  10:42:27 +0100 (0:00:00.104)       0:00:03.336 *****
    ===============================================================================
    Destroy molecule instance(s) -------------------------------------------- 2.53s
    Wait for instance(s) deletion to complete ------------------------------- 0.60s
    Delete docker network(s) ------------------------------------------------ 0.10s
    
--> Scenario: 'default'
--> Action: 'dependency'
Skipping, missing the requirements file.
--> Scenario: 'default'
--> Action: 'syntax'
    
    playbook: /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/playbook.yml
    
--> Scenario: 'default'
--> Action: 'create'
    
    PLAY [Create] ******************************************************************
    
    TASK [Log into a Docker registry] **********************************************
    Wednesday 16 January 2019  10:42:29 +0100 (0:00:00.104)       0:00:00.104 *****
    skipping: [localhost] => (item=None) 
    skipping: [localhost] => (item=None) 
    skipping: [localhost]
    
    TASK [Create Dockerfiles from image names] *************************************
    Wednesday 16 January 2019  10:42:29 +0100 (0:00:00.190)       0:00:00.295 *****
    changed: [localhost] => (item=None)
    ok: [localhost] => (item=None)
    changed: [localhost]
    
    TASK [Discover local Docker images] ********************************************
    Wednesday 16 January 2019  10:42:31 +0100 (0:00:01.330)       0:00:01.626 *****
    ok: [localhost] => (item=None)
    ok: [localhost] => (item=None)
    ok: [localhost]
    
    TASK [Build an Ansible compatible image] ***************************************
    Wednesday 16 January 2019  10:42:32 +0100 (0:00:01.069)       0:00:02.695 *****
    changed: [localhost] => (item=None)
    changed: [localhost] => (item=None)
    changed: [localhost]
    
    TASK [Create docker network(s)] ************************************************
    Wednesday 16 January 2019  10:42:42 +0100 (0:00:10.204)       0:00:12.900 *****
    skipping: [localhost]
    
    TASK [Create molecule instance(s)] *********************************************
    Wednesday 16 January 2019  10:42:42 +0100 (0:00:00.109)       0:00:13.010 *****
    changed: [localhost] => (item=None)
    changed: [localhost] => (item=None)
    changed: [localhost]
    
    TASK [Wait for instance(s) creation to complete] *******************************
    Wednesday 16 January 2019  10:42:45 +0100 (0:00:02.728)       0:00:15.738 *****
    changed: [localhost] => (item=None)
    changed: [localhost] => (item=None)
    changed: [localhost]
    
    PLAY RECAP *********************************************************************
    localhost                  : ok=5    changed=4    unreachable=0    failed=0
    
    Wednesday 16 January 2019  10:42:47 +0100 (0:00:02.043)       0:00:17.782 *****
    ===============================================================================
    Build an Ansible compatible image -------------------------------------- 10.20s
    Create molecule instance(s) --------------------------------------------- 2.74s
    Wait for instance(s) creation to complete ------------------------------- 2.04s
    Create Dockerfiles from image names ------------------------------------- 1.33s
    Discover local Docker images -------------------------------------------- 1.07s
    Log into a Docker registry ---------------------------------------------- 0.19s
    Create docker network(s) ------------------------------------------------ 0.11s
    
--> Scenario: 'default'
--> Action: 'prepare'
    
    PLAY [Prepare] *****************************************************************
    
    TASK [install dependencies] ****************************************************
    Wednesday 16 January 2019  10:42:52 +0100 (0:00:00.320)       0:00:00.320 *****
    changed: [glb-002.example.com] => (item=[u'iproute', u'sysvinit-tools', u'epel-release'])
    changed: [glb-001.example.com] => (item=[u'iproute', u'sysvinit-tools', u'epel-release'])
    
    TASK [create facts dir] ********************************************************
    Wednesday 16 January 2019  10:43:00 +0100 (0:00:08.084)       0:00:08.404 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    TASK [set fact] ****************************************************************
    Wednesday 16 January 2019  10:43:01 +0100 (0:00:00.929)       0:00:09.334 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    PLAY RECAP *********************************************************************
    glb-001.example.com        : ok=3    changed=3    unreachable=0    failed=0
    glb-002.example.com        : ok=3    changed=3    unreachable=0    failed=0
    
    Wednesday 16 January 2019  10:43:03 +0100 (0:00:01.412)       0:00:10.746 *****
    ===============================================================================
    install dependencies ---------------------------------------------------- 8.08s
    set fact ---------------------------------------------------------------- 1.41s
    create facts dir -------------------------------------------------------- 0.93s
    
--> Scenario: 'default'
--> Action: 'converge'
    
    PLAY [Converge] ****************************************************************
    
    TASK [Gathering Facts] *********************************************************
    Wednesday 16 January 2019  10:43:04 +0100 (0:00:00.108)       0:00:00.109 *****
    ok: [glb-001.example.com]
    ok: [glb-002.example.com]
    
    TASK [nginx : enable ipv4 non local bind] **************************************
    Wednesday 16 January 2019  10:43:08 +0100 (0:00:03.726)       0:00:03.835 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    TASK [nginx : install nginx and rngd] ******************************************
    Wednesday 16 January 2019  10:43:09 +0100 (0:00:01.341)       0:00:05.176 *****
    changed: [glb-001.example.com] => (item=[u'nginx', u'rng-tools'])
    changed: [glb-002.example.com] => (item=[u'nginx', u'rng-tools'])
    
    TASK [nginx : check if nginx is compiled with dynamic or static stream module] ***
    Wednesday 16 January 2019  10:43:46 +0100 (0:00:36.633)       0:00:41.810 *****
    ok: [glb-002.example.com]
    ok: [glb-001.example.com]
    
    TASK [nginx : install mod-stream] **********************************************
    Wednesday 16 January 2019  10:43:47 +0100 (0:00:01.221)       0:00:43.032 *****
    ok: [glb-001.example.com] => (item=[u'nginx-mod-stream'])
    ok: [glb-002.example.com] => (item=[u'nginx-mod-stream'])
    
    TASK [nginx : create default nginx.conf] ***************************************
    Wednesday 16 January 2019  10:43:48 +0100 (0:00:01.120)       0:00:44.153 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    TASK [nginx : Create systemd service override directory] ***********************
    Wednesday 16 January 2019  10:43:49 +0100 (0:00:01.530)       0:00:45.683 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    TASK [nginx : Copy systemd overrides] ******************************************
    Wednesday 16 January 2019  10:43:50 +0100 (0:00:00.898)       0:00:46.581 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    TASK [nginx : create empty dummy default.conf] *********************************
    Wednesday 16 January 2019  10:43:52 +0100 (0:00:01.371)       0:00:47.953 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    RUNNING HANDLER [nginx : enable nginx] *****************************************
    Wednesday 16 January 2019  10:43:53 +0100 (0:00:01.366)       0:00:49.319 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    RUNNING HANDLER [nginx : reload nginx] *****************************************
    Wednesday 16 January 2019  10:43:55 +0100 (0:00:01.658)       0:00:50.977 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    RUNNING HANDLER [nginx : restart nginx] ****************************************
    Wednesday 16 January 2019  10:43:56 +0100 (0:00:01.348)       0:00:52.326 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    RUNNING HANDLER [nginx : enable rngd] ******************************************
    Wednesday 16 January 2019  10:43:57 +0100 (0:00:01.427)       0:00:53.753 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    RUNNING HANDLER [nginx : reload systemd] ***************************************
    Wednesday 16 January 2019  10:43:59 +0100 (0:00:01.957)       0:00:55.711 *****
    ok: [glb-001.example.com]
    ok: [glb-002.example.com]
    
    TASK [generic_loadbalancer : gather facts from all servers in cluster] *********
    Wednesday 16 January 2019  10:44:03 +0100 (0:00:03.558)       0:00:59.270 *****
    ok: [glb-001.example.com -> glb-001.example.com] => (item=glb-001.example.com)
    ok: [glb-002.example.com -> glb-001.example.com] => (item=glb-001.example.com)
    ok: [glb-001.example.com -> glb-002.example.com] => (item=glb-002.example.com)
    ok: [glb-002.example.com -> glb-002.example.com] => (item=glb-002.example.com)
    
    TASK [generic_loadbalancer : include_tasks] ************************************
    Wednesday 16 January 2019  10:44:18 +0100 (0:00:14.570)       0:01:13.840 *****
    included: /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/tasks/keepalived.yml for glb-001.example.com, glb-002.example.com
    
    TASK [generic_loadbalancer : install keepalived] *******************************
    Wednesday 16 January 2019  10:44:18 +0100 (0:00:00.182)       0:01:14.022 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    TASK [generic_loadbalancer : create keepalived config] *************************
    Wednesday 16 January 2019  10:44:27 +0100 (0:00:09.464)       0:01:23.487 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    TASK [generic_loadbalancer : enable and start keepalived] **********************
    Wednesday 16 January 2019  10:44:29 +0100 (0:00:02.020)       0:01:25.508 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    TASK [generic_loadbalancer : include_tasks] ************************************
    Wednesday 16 January 2019  10:44:31 +0100 (0:00:02.003)       0:01:27.512 *****
    included: /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/tasks/nginx/main.yml for glb-001.example.com, glb-002.example.com
    
    TASK [generic_loadbalancer : nginx | create fallback vhost] ********************
    Wednesday 16 January 2019  10:44:32 +0100 (0:00:00.244)       0:01:27.756 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    RUNNING HANDLER [nginx : reload nginx] *****************************************
    Wednesday 16 January 2019  10:44:33 +0100 (0:00:01.317)       0:01:29.073 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    RUNNING HANDLER [generic_loadbalancer : restart keepalived] ********************
    Wednesday 16 January 2019  10:44:35 +0100 (0:00:01.938)       0:01:31.011 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    PLAY RECAP *********************************************************************
    glb-001.example.com        : ok=23   changed=16   unreachable=0    failed=0
    glb-002.example.com        : ok=23   changed=16   unreachable=0    failed=0
    
    Wednesday 16 January 2019  10:44:38 +0100 (0:00:02.829)       0:01:33.841 *****
    ===============================================================================
    nginx : install nginx and rngd ----------------------------------------- 36.63s
    generic_loadbalancer : gather facts from all servers in cluster -------- 14.57s
    generic_loadbalancer : install keepalived ------------------------------- 9.46s
    Gathering Facts --------------------------------------------------------- 3.73s
    nginx : reload systemd -------------------------------------------------- 3.56s
    generic_loadbalancer : restart keepalived ------------------------------- 2.83s
    generic_loadbalancer : create keepalived config ------------------------- 2.02s
    generic_loadbalancer : enable and start keepalived ---------------------- 2.00s
    nginx : enable rngd ----------------------------------------------------- 1.96s
    nginx : reload nginx ---------------------------------------------------- 1.94s
    nginx : enable nginx ---------------------------------------------------- 1.66s
    nginx : create default nginx.conf --------------------------------------- 1.53s
    nginx : restart nginx --------------------------------------------------- 1.43s
    nginx : Copy systemd overrides ------------------------------------------ 1.37s
    nginx : create empty dummy default.conf --------------------------------- 1.37s
    nginx : enable ipv4 non local bind -------------------------------------- 1.34s
    generic_loadbalancer : nginx | create fallback vhost -------------------- 1.32s
    nginx : check if nginx is compiled with dynamic or static stream module --- 1.22s
    nginx : install mod-stream ---------------------------------------------- 1.12s
    nginx : Create systemd service override directory ----------------------- 0.90s
    
--> Scenario: 'default'
--> Action: 'idempotence'
Idempotence completed successfully.
--> Scenario: 'default'
--> Action: 'side_effect'
    
    PLAY [kill nginx on glb-001] ***************************************************
    
    TASK [stop nginx] **************************************************************
    Wednesday 16 January 2019  10:45:19 +0100 (0:00:00.107)       0:00:00.107 *****
    changed: [glb-001.example.com]
    
    TASK [wait for keepalived to move IP] ******************************************
    Wednesday 16 January 2019  10:45:21 +0100 (0:00:01.950)       0:00:02.058 *****
    changed: [glb-001.example.com]
    
    PLAY RECAP *********************************************************************
    glb-001.example.com        : ok=2    changed=2    unreachable=0    failed=0
    
    Wednesday 16 January 2019  10:45:27 +0100 (0:00:05.889)       0:00:07.947 *****
    ===============================================================================
    wait for keepalived to move IP ------------------------------------------ 5.89s
    stop nginx -------------------------------------------------------------- 1.95s
    
--> Scenario: 'default'
--> Action: 'verify'
--> Executing Goss tests found in /home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/tests/...
    
    PLAY [Verify] ******************************************************************
    
    TASK [Gathering Facts] *********************************************************
    Wednesday 16 January 2019  10:45:28 +0100 (0:00:00.106)       0:00:00.106 *****
    ok: [glb-001.example.com]
    ok: [glb-002.example.com]
    
    TASK [Download and install Goss] ***********************************************
    Wednesday 16 January 2019  10:45:31 +0100 (0:00:03.504)       0:00:03.611 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    TASK [Create Molecule directory for test files] ********************************
    Wednesday 16 January 2019  10:45:41 +0100 (0:00:09.593)       0:00:13.204 *****
    changed: [glb-002.example.com]
    changed: [glb-001.example.com]
    
    TASK [Find Goss tests on localhost] ********************************************
    Wednesday 16 January 2019  10:45:42 +0100 (0:00:01.193)       0:00:14.398 *****
    changed: [glb-001.example.com -> localhost]
    changed: [glb-002.example.com -> localhost]
    
    TASK [debug] *******************************************************************
    Wednesday 16 January 2019  10:45:43 +0100 (0:00:00.480)       0:00:14.879 *****
    skipping: [glb-001.example.com]
    skipping: [glb-002.example.com]
    
    TASK [Copy Goss tests to remote] ***********************************************
    Wednesday 16 January 2019  10:45:43 +0100 (0:00:00.286)       0:00:15.165 *****
    changed: [glb-002.example.com] => (item=/home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/tests/test_default.yml)
    changed: [glb-001.example.com] => (item=/home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/tests/test_default.yml)
    changed: [glb-002.example.com] => (item=/home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/tests/test_host_glb-002.example.com.yml)
    changed: [glb-001.example.com] => (item=/home/nvarz/git/molecule-pr-example/roles/generic_loadbalancer/molecule/default/tests/test_host_glb-001.example.com.yml)
    
    TASK [Register test files] *****************************************************
    Wednesday 16 January 2019  10:45:46 +0100 (0:00:03.392)       0:00:18.558 *****
    changed: [glb-001.example.com]
    changed: [glb-002.example.com]
    
    TASK [Execute Goss tests] ******************************************************
    Wednesday 16 January 2019  10:45:48 +0100 (0:00:01.198)       0:00:19.757 *****
    changed: [glb-001.example.com] => (item=/tmp/molecule/goss/test_default.yml)
    changed: [glb-002.example.com] => (item=/tmp/molecule/goss/test_default.yml)
    changed: [glb-002.example.com] => (item=/tmp/molecule/goss/test_host_glb-002.example.com.yml)
    changed: [glb-001.example.com] => (item=/tmp/molecule/goss/test_host_glb-001.example.com.yml)
    
    TASK [Display details about the Goss results] **********************************
    Wednesday 16 January 2019  10:45:50 +0100 (0:00:02.095)       0:00:21.853 *****
    ok: [glb-001.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:48.962033', '_ansible_no_log': False, u'stdout': u'Group: nginx: exists: matches expectation: [true]\nUser: nginx: exists: matches expectation: [true]\nUser: nginx: home: matches expectation: ["/var/lib/nginx"]\nUser: nginx: groups: matches expectation: [["nginx"]]\nUser: nginx: shell: matches expectation: ["/sbin/nologin"]\nPackage: keepalived: installed: matches expectation: [true]\nPackage: nginx: installed: matches expectation: [true]\n\n\nTotal Duration: 0.032s\nCount: 7, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_default.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_default.yml', u'delta': u'0:00:00.307828', '_ansible_item_label': u'/tmp/molecule/goss/test_default.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_default.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Group: nginx: exists: matches expectation: [true]', u'User: nginx: exists: matches expectation: [true]', u'User: nginx: home: matches expectation: ["/var/lib/nginx"]', u'User: nginx: groups: matches expectation: [["nginx"]]', u'User: nginx: shell: matches expectation: ["/sbin/nologin"]', u'Package: keepalived: installed: matches expectation: [true]', u'Package: nginx: installed: matches expectation: [true]', u'', u'', u'Total Duration: 0.032s', u'Count: 7, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:48.654205', '_ansible_ignore_errors': True, 'failed': False}) => {
        "msg": [
            "Group: nginx: exists: matches expectation: [true]", 
            "User: nginx: exists: matches expectation: [true]", 
            "User: nginx: home: matches expectation: [\"/var/lib/nginx\"]", 
            "User: nginx: groups: matches expectation: [[\"nginx\"]]", 
            "User: nginx: shell: matches expectation: [\"/sbin/nologin\"]", 
            "Package: keepalived: installed: matches expectation: [true]", 
            "Package: nginx: installed: matches expectation: [true]", 
            "", 
            "", 
            "Total Duration: 0.032s", 
            "Count: 7, Failed: 0, Skipped: 0"
        ]
    }
    ok: [glb-002.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:48.987570', '_ansible_no_log': False, u'stdout': u'Group: nginx: exists: matches expectation: [true]\nUser: nginx: exists: matches expectation: [true]\nUser: nginx: home: matches expectation: ["/var/lib/nginx"]\nUser: nginx: groups: matches expectation: [["nginx"]]\nUser: nginx: shell: matches expectation: ["/sbin/nologin"]\nPackage: nginx: installed: matches expectation: [true]\nPackage: keepalived: installed: matches expectation: [true]\n\n\nTotal Duration: 0.041s\nCount: 7, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_default.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_default.yml', u'delta': u'0:00:00.314446', '_ansible_item_label': u'/tmp/molecule/goss/test_default.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_default.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Group: nginx: exists: matches expectation: [true]', u'User: nginx: exists: matches expectation: [true]', u'User: nginx: home: matches expectation: ["/var/lib/nginx"]', u'User: nginx: groups: matches expectation: [["nginx"]]', u'User: nginx: shell: matches expectation: ["/sbin/nologin"]', u'Package: nginx: installed: matches expectation: [true]', u'Package: keepalived: installed: matches expectation: [true]', u'', u'', u'Total Duration: 0.041s', u'Count: 7, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:48.673124', '_ansible_ignore_errors': True, 'failed': False}) => {
        "msg": [
            "Group: nginx: exists: matches expectation: [true]", 
            "User: nginx: exists: matches expectation: [true]", 
            "User: nginx: home: matches expectation: [\"/var/lib/nginx\"]", 
            "User: nginx: groups: matches expectation: [[\"nginx\"]]", 
            "User: nginx: shell: matches expectation: [\"/sbin/nologin\"]", 
            "Package: nginx: installed: matches expectation: [true]", 
            "Package: keepalived: installed: matches expectation: [true]", 
            "", 
            "", 
            "Total Duration: 0.041s", 
            "Count: 7, Failed: 0, Skipped: 0"
        ]
    }
    ok: [glb-001.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:49.944775', '_ansible_no_log': False, u'stdout': u'Port: tcp:80: listening: matches expectation: [false]\nService: nginx: enabled: matches expectation: [true]\nService: nginx: running: matches expectation: [false]\n\n\nTotal Duration: 0.012s\nCount: 3, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_host_glb-001.example.com.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_host_glb-001.example.com.yml', u'delta': u'0:00:00.285448', '_ansible_item_label': u'/tmp/molecule/goss/test_host_glb-001.example.com.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_host_glb-001.example.com.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Port: tcp:80: listening: matches expectation: [false]', u'Service: nginx: enabled: matches expectation: [true]', u'Service: nginx: running: matches expectation: [false]', u'', u'', u'Total Duration: 0.012s', u'Count: 3, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:49.659327', '_ansible_ignore_errors': True, 'failed': False}) => {
        "msg": [
            "Port: tcp:80: listening: matches expectation: [false]", 
            "Service: nginx: enabled: matches expectation: [true]", 
            "Service: nginx: running: matches expectation: [false]", 
            "", 
            "", 
            "Total Duration: 0.012s", 
            "Count: 3, Failed: 0, Skipped: 0"
        ]
    }
    ok: [glb-002.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:49.944755', '_ansible_no_log': False, u'stdout': u'Port: tcp:80: listening: matches expectation: [true]\nPort: tcp:80: ip: matches expectation: [["0.0.0.0"]]\nService: nginx: enabled: matches expectation: [true]\nService: nginx: running: matches expectation: [true]\n\n\nTotal Duration: 0.006s\nCount: 4, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_host_glb-002.example.com.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_host_glb-002.example.com.yml', u'delta': u'0:00:00.275222', '_ansible_item_label': u'/tmp/molecule/goss/test_host_glb-002.example.com.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_host_glb-002.example.com.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Port: tcp:80: listening: matches expectation: [true]', u'Port: tcp:80: ip: matches expectation: [["0.0.0.0"]]', u'Service: nginx: enabled: matches expectation: [true]', u'Service: nginx: running: matches expectation: [true]', u'', u'', u'Total Duration: 0.006s', u'Count: 4, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:49.669533', '_ansible_ignore_errors': True, 'failed': False}) => {
        "msg": [
            "Port: tcp:80: listening: matches expectation: [true]", 
            "Port: tcp:80: ip: matches expectation: [[\"0.0.0.0\"]]", 
            "Service: nginx: enabled: matches expectation: [true]", 
            "Service: nginx: running: matches expectation: [true]", 
            "", 
            "", 
            "Total Duration: 0.006s", 
            "Count: 4, Failed: 0, Skipped: 0"
        ]
    }
    
    TASK [Fail when tests fail] ****************************************************
    Wednesday 16 January 2019  10:45:50 +0100 (0:00:00.528)       0:00:22.382 *****
    skipping: [glb-001.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:48.962033', '_ansible_no_log': False, u'stdout': u'Group: nginx: exists: matches expectation: [true]\nUser: nginx: exists: matches expectation: [true]\nUser: nginx: home: matches expectation: ["/var/lib/nginx"]\nUser: nginx: groups: matches expectation: [["nginx"]]\nUser: nginx: shell: matches expectation: ["/sbin/nologin"]\nPackage: keepalived: installed: matches expectation: [true]\nPackage: nginx: installed: matches expectation: [true]\n\n\nTotal Duration: 0.032s\nCount: 7, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_default.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_default.yml', u'delta': u'0:00:00.307828', '_ansible_item_label': u'/tmp/molecule/goss/test_default.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_default.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Group: nginx: exists: matches expectation: [true]', u'User: nginx: exists: matches expectation: [true]', u'User: nginx: home: matches expectation: ["/var/lib/nginx"]', u'User: nginx: groups: matches expectation: [["nginx"]]', u'User: nginx: shell: matches expectation: ["/sbin/nologin"]', u'Package: keepalived: installed: matches expectation: [true]', u'Package: nginx: installed: matches expectation: [true]', u'', u'', u'Total Duration: 0.032s', u'Count: 7, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:48.654205', '_ansible_ignore_errors': True, 'failed': False}) 
    skipping: [glb-001.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:49.944775', '_ansible_no_log': False, u'stdout': u'Port: tcp:80: listening: matches expectation: [false]\nService: nginx: enabled: matches expectation: [true]\nService: nginx: running: matches expectation: [false]\n\n\nTotal Duration: 0.012s\nCount: 3, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_host_glb-001.example.com.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_host_glb-001.example.com.yml', u'delta': u'0:00:00.285448', '_ansible_item_label': u'/tmp/molecule/goss/test_host_glb-001.example.com.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_host_glb-001.example.com.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Port: tcp:80: listening: matches expectation: [false]', u'Service: nginx: enabled: matches expectation: [true]', u'Service: nginx: running: matches expectation: [false]', u'', u'', u'Total Duration: 0.012s', u'Count: 3, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:49.659327', '_ansible_ignore_errors': True, 'failed': False}) 
    skipping: [glb-002.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:48.987570', '_ansible_no_log': False, u'stdout': u'Group: nginx: exists: matches expectation: [true]\nUser: nginx: exists: matches expectation: [true]\nUser: nginx: home: matches expectation: ["/var/lib/nginx"]\nUser: nginx: groups: matches expectation: [["nginx"]]\nUser: nginx: shell: matches expectation: ["/sbin/nologin"]\nPackage: nginx: installed: matches expectation: [true]\nPackage: keepalived: installed: matches expectation: [true]\n\n\nTotal Duration: 0.041s\nCount: 7, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_default.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_default.yml', u'delta': u'0:00:00.314446', '_ansible_item_label': u'/tmp/molecule/goss/test_default.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_default.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Group: nginx: exists: matches expectation: [true]', u'User: nginx: exists: matches expectation: [true]', u'User: nginx: home: matches expectation: ["/var/lib/nginx"]', u'User: nginx: groups: matches expectation: [["nginx"]]', u'User: nginx: shell: matches expectation: ["/sbin/nologin"]', u'Package: nginx: installed: matches expectation: [true]', u'Package: keepalived: installed: matches expectation: [true]', u'', u'', u'Total Duration: 0.041s', u'Count: 7, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:48.673124', '_ansible_ignore_errors': True, 'failed': False}) 
    skipping: [glb-002.example.com] => (item={'_ansible_parsed': True, 'stderr_lines': [], '_ansible_item_result': True, u'end': u'2019-01-16 09:45:49.944755', '_ansible_no_log': False, u'stdout': u'Port: tcp:80: listening: matches expectation: [true]\nPort: tcp:80: ip: matches expectation: [["0.0.0.0"]]\nService: nginx: enabled: matches expectation: [true]\nService: nginx: running: matches expectation: [true]\n\n\nTotal Duration: 0.006s\nCount: 4, Failed: 0, Skipped: 0', u'cmd': [u'/usr/local/bin/goss', u'-g', u'/tmp/molecule/goss/test_host_glb-002.example.com.yml', u'validate', u'--format', u'documentation'], u'rc': 0, 'item': u'/tmp/molecule/goss/test_host_glb-002.example.com.yml', u'delta': u'0:00:00.275222', '_ansible_item_label': u'/tmp/molecule/goss/test_host_glb-002.example.com.yml', u'stderr': u'', u'changed': True, u'invocation': {u'module_args': {u'warn': True, u'executable': None, u'_uses_shell': False, u'_raw_params': u'/usr/local/bin/goss -g /tmp/molecule/goss/test_host_glb-002.example.com.yml validate --format documentation', u'removes': None, u'creates': None, u'chdir': None, u'stdin': None}}, 'stdout_lines': [u'Port: tcp:80: listening: matches expectation: [true]', u'Port: tcp:80: ip: matches expectation: [["0.0.0.0"]]', u'Service: nginx: enabled: matches expectation: [true]', u'Service: nginx: running: matches expectation: [true]', u'', u'', u'Total Duration: 0.006s', u'Count: 4, Failed: 0, Skipped: 0'], u'start': u'2019-01-16 09:45:49.669533', '_ansible_ignore_errors': True, 'failed': False}) 
    
    PLAY RECAP *********************************************************************
    glb-001.example.com        : ok=8    changed=6    unreachable=0    failed=0
    glb-002.example.com        : ok=8    changed=6    unreachable=0    failed=0
    
    Wednesday 16 January 2019  10:45:50 +0100 (0:00:00.241)       0:00:22.623 *****
    ===============================================================================
    Download and install Goss ----------------------------------------------- 9.59s
    Gathering Facts --------------------------------------------------------- 3.51s
    Copy Goss tests to remote ----------------------------------------------- 3.39s
    Execute Goss tests ------------------------------------------------------ 2.10s
    Register test files ----------------------------------------------------- 1.20s
    Create Molecule directory for test files -------------------------------- 1.19s
    Display details about the Goss results ---------------------------------- 0.53s
    Find Goss tests on localhost -------------------------------------------- 0.48s
    debug ------------------------------------------------------------------- 0.29s
    Fail when tests fail ---------------------------------------------------- 0.24s
    
Verifier completed successfully.
--> Scenario: 'default'
--> Action: 'destroy'
    
    PLAY [Destroy] *****************************************************************
    
    TASK [Destroy molecule instance(s)] ********************************************
    Wednesday 16 January 2019  10:45:52 +0100 (0:00:00.156)       0:00:00.156 *****
    changed: [localhost] => (item=None)
    changed: [localhost] => (item=None)
    changed: [localhost]
    
    TASK [Wait for instance(s) deletion to complete] *******************************
    Wednesday 16 January 2019  10:45:55 +0100 (0:00:02.686)       0:00:02.843 *****
    changed: [localhost] => (item=None)
    changed: [localhost] => (item=None)
    changed: [localhost]
    
    TASK [Delete docker network(s)] ************************************************
    Wednesday 16 January 2019  10:45:56 +0100 (0:00:00.970)       0:00:03.813 *****
    skipping: [localhost]
    
    PLAY RECAP *********************************************************************
    localhost                  : ok=2    changed=2    unreachable=0    failed=0
    
    Wednesday 16 January 2019  10:45:56 +0100 (0:00:00.111)       0:00:03.925 *****
    ===============================================================================
    Destroy molecule instance(s) -------------------------------------------- 2.69s
    Wait for instance(s) deletion to complete ------------------------------- 0.97s
    Delete docker network(s) ------------------------------------------------ 0.11s
    
```

