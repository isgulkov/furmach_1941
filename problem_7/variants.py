from os import path

import csv

def get_data_by_variant_number(v):
	csv_filename = path.join(path.dirname(__file__), '_variant_data.csv')

	data_rows = []

	with open(csv_filename, 'rb') as f:
		csv_reader = csv.reader(f, delimiter=';')

		for row in csv_reader:
			data_rows.append(row[1:])

	return (data_rows[(v - 1) * 2], data_rows[(v - 1) * 2 + 1], )
