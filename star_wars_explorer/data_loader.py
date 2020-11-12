import petl as etl


def load_data(data_path):
    table = etl.fromcsv(data_path)

    return table
