'''
Used to access project constants, many of which are user specific and
so are not included in the git repo.
These include file paths and earthdata passwords.

The user must create their own constants file using
define_constants_template.py

User will also need to specify the path to the constants.
'''

import json


def get_project_constants():
    f_path = '/sat_precip_trmm_3b42/sd_constants/project_constants.json'
    project_constants = json.load(open(f_path, 'r'))
    return project_constants
