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
