import zipfile 

def unzip(file: str, dir: str):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dir)