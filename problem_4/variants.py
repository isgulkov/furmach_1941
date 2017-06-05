from os import path

import csv

def get_data_by_variant_number(v):
	csv_filename = path.join(path.dirname(__file__), '_variant_data.csv')

	with open(csv_filename, 'rb') as f:
		csv_reader = csv.reader(f, delimiter=';')

		data_rows = []

		for row in csv_reader:
			new_data_row = map(float, row[1:])

			data_rows.append(new_data_row)

		x2s = data_rows[(v - 1) * 4]
		x3s = data_rows[(v - 1) * 4 + 1]
		x4s = data_rows[(v - 1) * 4 + 2]
		ys = data_rows[(v - 1) * 4 + 3]

		return (x2s, x3s, x4s, ys, )
