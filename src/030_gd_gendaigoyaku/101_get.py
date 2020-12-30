from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from bs4 import BeautifulSoup

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents', "https://www.googleapis.com/auth/drive"]

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text

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
        # 2,
        3,
        # 4, 
        # 5, 6, 7, 8, 9, 10, 11, 
        # 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
        # 16
    ]

    with open("data/ids.json") as f:
        ids = json.load(f)

    itaiji = {}

    import csv

    with open('../001_scripto/data2/itaiji.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            key = row[1]
            text = row[2]
            elements = text.split("　")
            for e in elements:
                itaiji[e] = key

    for vol in vols:
        print(vol)

        vol = str(vol).zfill(2)

        from bs4 import BeautifulSoup
        with open('/Users/nakamurasatoru/git/d_genji/kouigenjimonogatari.github.io/tei/'+vol+'.xml') as doc:
            soup = BeautifulSoup(doc, "xml") # 第2引数でパーサを指定

        gid = ids[vol]

        document = service.documents().get(documentId=gid).execute()

        doc_content = document.get('body').get('content')
        text = read_strucutural_elements(doc_content)

        for key in itaiji:
            text = text.replace(key, itaiji[key])

        text = text.replace("(か)", "")
        text = text.replace("(む)", "")

        # print(text)
        texts = text.split("\n")

        #-----------

        for text in texts:
            tmp = text.split(" ")

            id = tmp[0]

            uri = "https://w3id.org/kouigenjimonogatari/api/items/"+id+".json"

            if len(tmp) != 2:
                print("text", text)
                continue
            
            t = tmp[1]

            t = t.replace("[", "<anchor corresp='https://genji.dl.itc.u-tokyo.ac.jp/data/tei/yosano/"+vol+".xml#").replace("]", "'/>")

            ans = '<seg corresp="'+uri+'">'+t+'</seg>'

            soup.find("seg", {"corresp" : uri}).replace_with(BeautifulSoup(ans,'xml'))

        
        f = open("data/gd/"+vol+".xml", "w")
        f.write(soup.prettify())
        f.close()
        

if __name__ == '__main__':
    main()