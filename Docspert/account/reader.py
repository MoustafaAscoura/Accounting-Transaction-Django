import csv
import json
import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Account


class UnsupportedFileExtension(Exception):
    pass


class UnsupportedFileFormat(Exception):
    pass


def map_data_into_account_format(data_object):
    return {
        "id": data_object.get("ID"),
        "balance": data_object.get("Balance"),
        "name": data_object.get("Name")
    }


def read_raw_data_from_file(uploaded_file: InMemoryUploadedFile) -> iter:
    split_tup = os.path.splitext(uploaded_file.name)
    file_extension = split_tup[1]

    if file_extension == ".csv":
        decoded_file = uploaded_file.read().decode('utf-8')
        reader = csv.DictReader(decoded_file.splitlines())
        headers = list(sorted(reader.fieldnames))
        if headers != ["Balance", "ID", "Name"]:
            raise UnsupportedFileFormat("File Column Names do not match Balance, ID, Name")

        data = map(map_data_into_account_format, reader)
    elif file_extension == ".json":
        try:
            data = json.load(uploaded_file)
            data = map(map_data_into_account_format, data)
        except json.JSONDecodeError:
            raise UnsupportedFileFormat("Invalid JSON or invalid Keys Balance, ID, Name")
    else:
        raise UnsupportedFileExtension(f"{file_extension} files are not supported")

    return data


def open_file_and_load_content_into_database(uploaded_file: InMemoryUploadedFile) -> list:
    data = read_raw_data_from_file(uploaded_file)
    failed = []
    for record in data:
        try:
            new_account = Account.objects.create(**record)
            new_account.asave()

        except:
            failed.append(record)

    return failed
