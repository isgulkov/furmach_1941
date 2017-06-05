from os import path

import csv

def get_data_by_variant_number(v):
	csv_filename = path.join(path.dirname(__file__), '_variant_data.csv')

	with open(csv_filename, 'rb') as f:
		csv_reader = csv.reader(f, delimiter=';')

		data_rows = []

		for row in csv_reader:
			def float_or_none(s):
				try:
					return float(s)
				except ValueError:
					return None

			new_data_row = map(float_or_none, row[1:])

			data_rows.append(new_data_row)

		return tuple([data_rows[(v - 1) * 11 + i] for i in xrange(10)])
