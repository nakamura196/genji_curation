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

    title = 'My Document'
    body = {
        'title': title
    }

    '''
    doc = service.documents() \
        .create(body=body).execute()
    print('Created document with title: {0}'.format(
        doc.get('title')))

    print(doc)

    '''

    text1 = "665-01 [YG2100000300]としかはりて宮の御はてもすきぬれは世中いろあらたまりてころもかへのほと\n"
    text2 = "665-02 なともいまめかしきをましてまつりのころはおほかたの空のけしき心ちよけな\n"
    text3 = "ccc"

    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text1
            }
        },
        {
            'insertText': {
                'location': {
                    'index': 1 + len(text1),
                },
                'text': text2
            }
        }
    ]

    body = {
        "content": [
            {
                "endIndex": 1,
                "sectionBreak": {
                    "sectionStyle": {
                        "columnSeparatorStyle": "NONE",
                        "contentDirection": "LEFT_TO_RIGHT",
                        "sectionType": "CONTINUOUS"
                    }
                }
            },
            {
                "endIndex": 17,
                "paragraph": {
                    "elements": [
                        {
                            "endIndex": 17,
                            "startIndex": 1,
                            "textRun": {
                                "content": "aaaaaaaaaaaaaaa\n",
                                "textStyle": {}
                            }
                        }
                    ],
                    "paragraphStyle": {
                        "direction": "LEFT_TO_RIGHT",
                        "namedStyleType": "NORMAL_TEXT"
                    }
                },
                "startIndex": 1
            }
        ]
    }

    id = "1I_p1J5pFdCCUICHNmKmEgzxXXXZYNuSODfqgk0a5Tw0"
    result = service.documents().batchUpdate(
        documentId=id, body={'requests': requests}).execute()


if __name__ == '__main__':
    main()