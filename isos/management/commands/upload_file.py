import os
import sys
import requests
import random
import string

from time import sleep
from requests_toolbelt import MultipartEncoder

from isos_parser import settings

if not settings.DEBUG:
    sys.path.append('/home/tim_baiguzhinov/')
    from authenticate import authentication
else:
    pass


def upload_file(file_dir, file_name):
    data = open(os.path.join(file_dir, file_name), 'rb')
    fields = {
        'file': (
            file_name,
            data,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    }

    m = MultipartEncoder(
        fields=fields,
        boundary='----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters+string.digits, 16)))

    token = authentication()

    response = requests.post(
        'https://eu.core.resolver.com/creation/import',
        headers={
            'Connection': 'keep-alive',
            'Content-Type': m.content_type,
            'Authorization': f'bearer {token}',
        },
        params={
            'dryRun': 'false',
            'usingExternalRefIds': 'true',
            'deferPostProcessing': 'false',
        },
        data=m
    )
    response.raise_for_status()
    jobId = response.json()['jobId']

    status = 1
    while status == 1:
        token = authentication()
        response = requests.get(
            f'https://eu.core.resolver.com/object/job/{jobId}',
            headers={
                'Authorization': f'bearer {token}',
            },
        )
        response.raise_for_status()
        status = response.json()['status']
        sleep(15)
