#!/usr/bin/python3
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def callback(request_id, response, exception):
    if exception:
        # Handle error
        print (exception)
    else:
        print ("Permission Id: %s" % response)


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


'''
page_token = None
while True:
    response = drive_service.files().list(q="mimeType='image/jpeg'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        print 'Found file: %s (%s)' % (file.get('name'), file.get('id'))
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break
'''



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    #id_resp = service.permissions().getIdForEmail(email='angelmazorra@gmail.com').execute()
    #print(id_resp['id'])
    #results = service.files().list(q="'angelmazorra@gmail.com' in writers and name  contains 'pruebadeficheroraronousar' ",
    #    pageSize=10,fields="nextPageToken, files(id, name)").execute()
    page_token = None
    while True:
        results = service.files().list(q="'angelmazorra@gmail.com' in writers",
            pageSize=1000,fields="nextPageToken, files(id, name)",pageToken=page_token).execute()

        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))
                file_id=item['id']
                '''
                perms = service.permissions().list(fileId=file_id).execute()
                p = perms.get('items',[])
                print(perms)
                '''
                
                batch = service.new_batch_http_request(callback=callback)
                user_permission = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': 'cicamazorra@gmail.com'
                }
                batch.add(service.permissions().create(
                        fileId=file_id,
                        body=user_permission,
                        fields='id',
                        sendNotificationEmail=False
                ))

                batch.add(service.permissions().delete(fileId=file_id,permissionId='08043516404169648689'))
                batch.execute()
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break

if __name__ == '__main__':
    main()