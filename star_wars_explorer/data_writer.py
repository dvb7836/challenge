import os
import csv
import uuid

from challenge.settings import FETCHED_DATA_PATH
from star_wars_explorer.models import Collection


def save_collection(filename):
    collection = Collection(filename=filename)
    collection.save()


def save_to_disk(data):
    filename = "{}.csv".format(uuid.uuid4())
    filepath = os.path.join(FETCHED_DATA_PATH, filename)

    with open(filepath, "w", newline="") as csvfile:
        fieldnames = sorted(data[0].keys(), reverse=True)
        fieldnames.append(fieldnames.pop(0))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    return filename
