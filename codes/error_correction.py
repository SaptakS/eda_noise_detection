import numpy as np

def replace_error(rows, error, replace_val):
	rows[rows.index(error)] = replace_val
	return rows

def std_error_correct(rows, error):
	start = error["start"]
	end = error["end"]
	length = end - start
	mid = start + (length / 2)
	replace_start = ((start / 1000) - 1) * 1000
	for i in range(start, end + 1):
		rows[i] = rows[replace_start]
		replace_start += 1
	return rows
