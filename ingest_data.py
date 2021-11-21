import urllib.request
import os.path


ingest_directory = 'data/ingest'
ingest_manifest = 'ingest_urls.csv'


class IngestDataFile:
    def __init__(self, filename, url):
        self.filename = filename
        self.url = url
        self.data = ''

    def ingest(self):
        self.data = urllib.request.urlopen(self.url).read()
        return self.data

    def write(self, directory):
        full_filename = os.path.join(directory, self.filename)
        with open(full_filename, 'wb') as output_file:
            output_file.write(self.data)


def get_ingest_files(directory):
    full_filename = os.path.join(directory, ingest_manifest)
    with open(full_filename, 'r') as ingest_file:
        ingest_file_rows = [row.split(',') for row in ingest_file.read().split('\n') if row.strip()]
    header = ingest_file_rows[0]
    ingest_file_rows = ingest_file_rows[1:]
    ingest_file_manifest = []
    for ingest_row in ingest_file_rows:
        ingest_file_manifest.append(IngestDataFile(ingest_row[header.index('Filename')], ingest_row[header.index('Url')]))
    return ingest_file_manifest


if __name__ == '__main__':
    for ingestion_file_object in get_ingest_files(ingest_directory):
        ingestion_file_object.ingest()
        ingestion_file_object.write(ingest_directory)
