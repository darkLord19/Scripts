#!/usr/bin/env python3

""pip install oauthclient2 google-api-python-client

def upload_file_to_drive(filename, path):
    from apiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file, client, tools
    from apiclient.http import MediaFileUpload

    # Setup the Drive v3 API
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    folder_id = '1l9qOkLyTfEfNvAejpr-Yu28CmYFsdEHX'

    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    full_path = path + filename
    media = MediaFileUpload(full_path,
                            mimetype='text/html',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    filelocal = open('success/'+filename, 'w')
    time = datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')
    filelocal.write('File ID: %s' % file.get('id') + 'on' + time )
    filelocal.close()
    return

import datetime
import subprocess

current = datetime.datetime.now()
filename = current.strftime('%Y%m%d-%H%M%S')
result = subprocess.run(['pg_dump','blog'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

if result.returncode == 0:
    path = 'backups/'
    filename = 'blog-' + filename
    full_path = path + filename
    file = open(full_path, 'w')
    file.write(result.stdout)
    file.close()
    upload_file_to_drive(filename, path)
else:
	filename = 'log/'+filename+'.log'
	file = open(filename, 'w')
	file.write(result.stderr)