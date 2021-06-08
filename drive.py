import os.path

from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_gdrive_service():
    """
    """
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)    


def search(service:Resource, query:str):
    # search for the file
    result = []
    page_token = None
    while True:
        response = service.files().list(q=query,
                                        spaces="drive",
                                        fields="nextPageToken, files(id, name, mimeType)",
                                        pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            result.append((file["id"], file["name"], file["mimeType"]))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result

def create_folder(service:Resource, name:str) -> str:
    """Create a folder and returns its id
    """

    folder_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=folder_metadata, fields='id').execute()
    return file.get('id')


def upload(service:Resource, folder_id:str, filepath:str, filename:str, mimetype:str) -> str:
    with open('history.csv', 'r') as f:
            lines = f.readlines()
            for line in lines:
                name = line.split(',')[3]
                if name == filename:
                    raise Exception('File already uploaded')

    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    
    return file.get('id')


if __name__ == "__main__":
    service = get_gdrive_service()
    # print(search(service, f"mimeType='application/vnd.google-apps.folder'"))
    # print(search(service, "name='papers'"))
    # upload(service, '1gR-nIrJ7EPTxHgr1jfxO46uLfd5ovHja')
    create_folder(service, 'papers')