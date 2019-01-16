Role Name
=========

Install epel-release and nginx from package.

Requirements
------------

nginx.yml
- epel-release
- nginx

Role Variables
--------------

handlers/main.yml
- nginx restart and validate nginx config
tasks/main.yml
- Installation epel-release and nginx package

Dependencies
------------

First epel-release is needed then nginx can be install.

Example Playbook
----------------

playbook: nginx.yml

License
-------

Author Information
-----------------
