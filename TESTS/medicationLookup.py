# https://open.fda.gov/apis/drug/ndc/
# https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory

import csv

from medication_barcode import MedicationBarcode


def read_tab_delimited_file(file_path):
    """Reads a tab-delimited file and returns a list of dictionaries."""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def search_data(data, search_term):
    """Searches the data for a given search term."""
    result = []
    for row in data:
        for value in row.values():
            if search_term in value:
                result.append(row)
                break
    return result

def different_test(file_path, search_term):
    with open(file_path, 'r') as f:
        for line in f:
            fields = line.split("\t")
            if len(fields) > 19:
                field = fields[1]

                if field == search_term:
                    print(line)

if __name__ == '__main__':
    file_path = '../db/ndctext/producta.txt'  # Replace with your file path
    # data = read_tab_delimited_file(file_path)

    # imageName = 'IMG_1147a.jpg'
    imageName = 'IMG_1146.jpg'

    medicationBarcode = MedicationBarcode('/mnt/c/projects/obsidianSync/assets/newPhotos/', imageName)
    [type, decoded] = medicationBarcode.run()

    search_term = ''

    if type == 'DATAMATRIX':
        search_term = decoded
        different_test(file_path, search_term)
        # search_term = 'your_search_term'  # Replace with your search term
        # result = search_data(data, search_term)
        # print(result)
    else:
        different_test(file_path, decoded)



