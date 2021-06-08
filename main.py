#!/usr/bin/env python3

import os

from drive import upload, create_folder, search, get_gdrive_service

def main(pathdir:str):
    service = get_gdrive_service()

    docs = os.listdir(pathdir)
    files = []
    for doc in docs:
        if doc.split('.')[-1] == 'pdf':
            files.append(doc)

    folder_name = pathdir.split('/')[-1]
    ids = search(service,
                 query=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'")

    if len(ids) == 1:
        folder_id = ids[0]
    else:
        folder_id = create_folder(service, name=folder_name)
    
    # upload the files
    for filename in files:
        file_id = upload(service, folder_id, filepath=f'{pathdir}/{filename}',
               filename=filename, mimetype='application/pdf')
        print(f'Uploaded {filename} : file_id {file_id}')


if __name__ == '__main__':
    main('/home/achraf/Documents/Resources/papers')