import zipfile 

def unzip(file: str, dir: str):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        print(f'Unzipping {file} to {dir}')
        zip_ref.extractall(dir)