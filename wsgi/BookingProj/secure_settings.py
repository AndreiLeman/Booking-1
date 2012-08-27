# SECURE and LOCAL INFO
# Pull real data from outside Git repo:
# i.e. from git-repo/../data persistent dir
# i.e. OPENSHIFT_DATA_DIR
#############################################

import json
import os

# settings to determine if running on OpenShift
ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

blank_settings = {
    "EMAIL_HOST" : '',
    "EMAIL_PORT" : 0,
    "EMAIL_HOST_USER" : '',
    "EMAIL_HOST_PASSWORD" : ''
    }

try:
    if ON_OPENSHIFT:
        with open(os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'secure_settings.json'), 'r') as fin:
            settings = json.loads(fin.read())        
    else:
        #automatically gets the abs path of dir containing this secure_settings.py file
        #assumes secure_settings.py is in project root dir
        secure_settings_dir = os.path.dirname(__file__)
        PROJECT_ROOT = os.path.abspath(secure_settings_dir)
    
        with open(os.path.join(PROJECT_ROOT, '..', '..', '..', 'data_not_in_git_repo', 'secure_settings.json')) as fin:
            settings = json.loads(fin.read())
except IOError as e:
    print 'secure_settings.json cannot be opened. Using blank email settings.'
    settings = blank_settings

SECURE_SETTINGS = {
    "EMAIL_HOST" : settings['EMAIL_HOST'],
    "EMAIL_PORT" : settings['EMAIL_PORT'],
    "EMAIL_HOST_USER" : settings['EMAIL_HOST_USER'],
    "EMAIL_HOST_PASSWORD" : settings['EMAIL_HOST_PASSWORD'],
    "EMAIL_USE_TLS" : True
    }

