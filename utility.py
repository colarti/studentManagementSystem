from zipfile import ZipFile



def unzip_file(file):
    with ZipFile(file) as zip:
        zip.extractall()


if __name__ == '__main__':
    unzip_file('icons.zip')