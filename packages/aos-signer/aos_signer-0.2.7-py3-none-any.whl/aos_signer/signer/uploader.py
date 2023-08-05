#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

from aos_signer.service_config.service_config_parser import ServiceConfigParser
import requests


def run_upload():
    config = ServiceConfigParser('meta/conf.yaml')

    key = config.publish.tls_key
    if not key:
        key = config.build.sign_key

    cert = config.publish.tls_certificate
    if not cert:
        cert = config.build.sign_certificate

    service_uid = config.publish.service_uid
    domain = config.publish.url

    resp = requests.post(
        'https://{}:10000/api/v1/services/versions/'.format(domain),
        files={'file': open('service.tar.gz', 'rb')},
        data={'service': service_uid},
        cert=('meta/' + cert, 'meta/' + key),
        verify=False)

    if resp.status_code == 201:
        print('Uploaded')
    else:
        print('Error while uploading:')
        print(resp.text)
