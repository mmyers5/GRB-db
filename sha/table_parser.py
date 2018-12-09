import pandas

SHA_FILES_LIST = (
    'sha_results_table_1543989340_0.tbl',
    'sha_results_table_1543989340_1.tbl',
    'sha_results_table_1543989340_2.tbl',
    'sha_results_table_1543989340_3.tbl'
)

SHA_FILES_OUT = 'sha_results_table_1543989340.csv'

def get_header(sha_file):
    with open(sha_file, 'r') as f:
        for line in f:
            if line.startswith('|'):
                header = line
                break
    return header

def get_colspecs(sha_file):
    header = get_header(sha_file)
    delim_idx = [loc for loc, val in enumerate(header) if val == '|']
    colspecs  = []
    start = 0
    for delim in delim_idx:
        if delim == 0:
            continue
        else:
            end = delim
            colspecs.append((start, end))
            start = delim
    return colspecs   

def read_table(sha_file):
    header = get_header(sha_file)
    colspecs = get_colspecs(sha_file)
    file_data = pandas.read_fwf(
        sha_file, comment='\\', colspecs=colspecs, skiprows=[17,18])
    return file_data

def read_many_tables(SHA_FILES_LIST):
    data = pandas.DataFrame()
    for sha_file in SHA_FILES_LIST:
        file_data = read_table(sha_file)
        data = data.append(file_data)
    return data

def data_to_csv(data):
    raw_cols = data.columns.values
    parsed_cols = [col.strip('|') for col in raw_cols]
    data.to_csv(SHA_FILES_OUT, header=parsed_cols, index=False)
