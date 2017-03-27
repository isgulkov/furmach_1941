from os import path

import csv

def get_data_by_variant_number(v):
	csv_filename = path.join(path.dirname(__file__), '_variant_data.csv')

	with open(csv_filename, 'rb') as f:
		# The data file used is the original xls file that has undergone several transformations:
		# - transposed
		# - saved as csv with ';' delimiter
		# - decimal delimiter was changed from comma to dot

		csv_reader = csv.reader(f, delimiter=';')

		data_rows = []

		for row in csv_reader:
			new_data_row = map(float, row[1:])

			data_rows.append(new_data_row)

		xs = data_rows[(v - 1) * 2]
		ys = data_rows[(v - 1) * 2 + 1]

		return (xs, ys, )
