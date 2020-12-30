from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents', "https://www.googleapis.com/auth/drive"]



# The ID of a sample document.
DOCUMENT_ID = '1qOQmwivV1PaSI7wqx3zH_sRiUx4oHGuLO2gugoAvIfQ'

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    vols = [
        # 1,
        # 2
        # 3
        # 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
        # 22, 23, 24, 25, 26, 27, 28, 29, 30,
        # 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        # 41, 
        42, 43, 44, 45, 46, 47, 48, 49, 50,
        51, 52, 53, 54
    ]

    results = {}

    for vol in vols:
        print(vol)

        title = str(vol).zfill(2)
        body = {
            'title': title
        }

    
        doc = service.documents() \
            .create(body=body).execute()
        print('Created document with title: {0}'.format(
            doc.get('title')))

        results[str(vol).zfill(2)] = doc.get("documentId")

    print(results)

        


if __name__ == '__main__':
    main()