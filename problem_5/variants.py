from os import path

import csv

def remove_columns_with_none_entries(rows):
	columns_for_deletion = []

	for i in xrange(min(map(len, rows)) - 1, -1, -1):
		if any(map(lambda x: x is None, [row[i] for row in rows])):
			for row in rows:
				del row[i]
	
def get_data_by_variant_number(v):
	csv_filename = path.join(path.dirname(__file__), '_variant_data.csv')

	data_rows = []

	with open(csv_filename, 'rb') as f:
		csv_reader = csv.reader(f, delimiter=';')

		for row in csv_reader:
			def float_or_none(s):
				try:
					return float(s)
				except ValueError:
					return None

			new_data_row = map(float_or_none, row[1:])

			data_rows.append(new_data_row)

	variant_rows = tuple([data_rows[(v - 1) * 11 + i] for i in xrange(10)])

	remove_columns_with_none_entries(variant_rows)

	return variant_rows
