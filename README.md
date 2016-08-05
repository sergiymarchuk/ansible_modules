# Ansible module to download file.

## Development environment:
Ansible versions: 2.1

OS: CentOS 7

## Update Ansible configuration file: /etc/ansible/ansible.cfg 
```
library        = /root/my-ansible-modules/
```
Create directory /root/my-ansible-modules/
Create module file /root/my-ansible-modules/download_file.py

```
#!/usr/bin/python
# Date: 2016-08-05

DOCUMENTATION = '''
---
module: download_file
short_description: Downloads file via URL
description:
  - This module downloads file via url to local destination.
  - It also checks if file already exists and can overwrite file or skip.
options:
  url:
    description:
      - URL to download file.
    required: true
  dest:
    description:
      - Local file destination
    required: true
  overwrite:
    description:
      - Should module overwrite existing file or not.
    required: true
'''

EXAMPLES = '''
- name: Download file
  download_file: url='https://www.kernel.org/doc/linux/README' dest='/tmp/README' overwrite=yes
'''

from ansible.module_utils.basic import *
import urllib
import os

def main():

    module = AnsibleModule(
        argument_spec = dict(
            url       = dict(required=True),
            dest      = dict(required=True),
            overwrite = dict(default='yes', choices=['yes', 'no']),
        )
    )

    url = module.params.get('url')
    dest = module.params.get('dest')
    overwrite = module.params.get('overwrite')

    try:
        if not os.path.isfile(dest):
            urllib.urlretrieve(url, dest)
            res_txt = "Downloaded"
            change_status = True
        else:
            if overwrite == "yes":
                urllib.urlretrieve(url, dest)
                res_txt = "Overwritten"
                change_status = True
            else:
                res_txt = "File exists"
                change_status = False
    except:
        module.fail_json(msg="Downloading failed. URL or DEST is wrong.")

    response = {"Message": res_txt }
    module.exit_json(changed=change_status, meta=response)

if __name__ == '__main__':  
    main()

```

## Make file executable:
```
chmod +x /root/my-ansible-modules/download_file.py
```

## Create playbook file /root/play.yml

```
---
- hosts: app-servers
  tasks:
    - name: Download file
      download_file: url='https://www.kernel.org/doc/linux/README' dest='/tmp/README' overwrite=yes
      register: result
    - debug: var=result
```

## Create inventory file /root/my-inventory:
```
[app-servers]
192.168.1.111
```

## Run playbook:
```
ansible-playbook -i my-inventory play.yml
```

## Output example:
```
PLAY [app-servers] *************************************************************

TASK [setup] *******************************************************************
ok: [192.168.1.111]

TASK [Download file] ***********************************************************
changed: [192.168.1.111]

TASK [debug] *******************************************************************
ok: [192.168.1.111] => {
    "result": {
        "changed": true, 
        "meta": {
            "Message": "Downloaded"
        }
    }
}

PLAY RECAP *********************************************************************
192.168.1.111              : ok=3    changed=1    unreachable=0    failed=0   
```

## "download-file" module documentation:

```
[ansible-server]# ansible-doc download_file
> DOWNLOAD_FILE

  This module downloads file via url to local destination. It also checks if file
  already exists and can overwrite file or skip.

Options (= is mandatory):

= dest
        Local file destination

= overwrite
        Should module overwrite existing file or not.

= url
        URL to download file.

EXAMPLES:
- name: Download file
  download_file: url='https://www.kernel.org/doc/linux/README' dest='/tmp/README' overwrite=yes
```
