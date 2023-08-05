#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import os

_meta_folder_name = 'meta'
_config_file_name = 'aos_container.yml'


def run_bootstrap():
    _create_meta_folder()
    _init_conf_file()


def _create_meta_folder():
    if not os.path.isdir(_meta_folder_name):
        os.mkdir(_meta_folder_name)


def _init_conf_file():
    conf_file_path = os.path.join(_meta_folder_name, _config_file_name)
    if not os.path.isfile(conf_file_path):
        with open(conf_file_path) as cfp:
            cfp.write(_config_bootstrap)


_config_bootstrap = """
# Commented sections are optional. Uncomment them if you want to include them in config

#publisher: # General publisher info section
#    author: # Author info
#    company: # Company info

# How to build and sign package
build:
    os: string
    arch: string
    sign_key: private_key.pem
    sign_certificate: sp-client.pem
    remove_non_regular_files: True
    context: string, optional

# Information about publishing process (URI, cert, etc)
publish:
    url: localhost
    service_uid: fc791798-a4e7-4960-8e3c-ab82ce2864fa
    tls_key: private_key.pem
    tls_certificate: sp-client.pem

# Service configuration
configuration:
    state:
        filename: state.dat
        required: False

    # Strartup command
    cmd: string

    workingDir: string

    # Requested quotas
    quotas:
        cpu: 50
        mem: 2KB
        state: 64KB
        storage: 64KB
        upload_speed: 32Kb
        download_speed: 32Kb
        upload: 1GB
        download: 1GB
        temp: 32KB
        //TODO: extend

    # Alerts
    alerts:
        ram:
            minTime: string
            minThreshold: 10,
            maxThreshold: 150
        cpu:
            minTime: string
            minThreshold: 40,
            maxThreshold: 45
        storage:
            minTime: string
            minThreshold: 10,
            maxThreshold: 150
        upload:
            minTime: string
            minThreshold: 10,
            maxThreshold: 150
        download:
            minTime: string
            minThreshold: 10,
            maxThreshold: 150
"""
