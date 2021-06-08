#!/usr/bin/env python3

import os
import time

from datetime import datetime
from drive import upload, create_folder, search, get_gdrive_service
from utils import read_config


def main(pathname:str):
    service = get_gdrive_service()

    docs = os.listdir(pathname)
    files = []
    for doc in docs:
        if doc.split('.')[-1] == 'pdf':
            files.append(doc)
    print(f"Files found: \n{files}")

    folder_name = pathname.split('/')[-1]
    ids = search(service,
                 query=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'")

    if len(ids) > 0:
        folder_id = ids[0]
    else:
        folder_id = create_folder(service, name=folder_name)
        with open('history.csv', 'a') as f:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            f.write(f'{timestamp},folder,create,{folder_name},{folder_id}\n')
    
    # upload the files
    for filename in files:
        try:
            file_id = upload(service, folder_id, filepath=f'{pathname}/{filename}',
                             filename=filename, mimetype='application/pdf')
            
            with open('history.csv', 'a') as f:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                f.write(f'{timestamp},file,upload_file,{filename},{file_id}\n')
        except:
            print(f'{filename} already uploaded')


if __name__ == '__main__':
    config = read_config()

    while True:
        time.sleep(int(config['interval']))
        print(f"Checking {config['name']}")
        main(config['local'])