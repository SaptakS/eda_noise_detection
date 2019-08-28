import numpy as np
import math

def device_error_detect(rows, window_size=1000):
	bin_count = np.bincount(np.array(rows))
	non_zero_bin_values = np.nonzero(bin_count)[0]
	frequency_dist = zip(non_zero_bin_values, bin_count[non_zero_bin_values])

	possible_error_vals = []
	for (val, freq) in frequency_dist:
		if freq < 5:
			possible_error_vals.append(val)

	device_error = []
	for i in range(0, len(rows), window_size):
		for value in possible_error_vals:
			if value in rows[i: (i + window_size - 1)]:
				max_freq_val = np.bincount(rows[i: (i + window_size - 1)]).argmax()
				delta = value - max_freq_val
				if delta > 150:
					device_error.append((value, max_freq_val))

	return device_error

def std_error_detect(rows, fr, window_size=1000):
	standard_deviations = [float(line.split("\t")[0]) for line in fr]
	possible_error_vals = []
	pos = 0
	for i in range(0, len(standard_deviations), 5):
		window_max = max(standard_deviations[i: i + 4])
		window_min = min(standard_deviations[i: i + 4])
		window_delta = window_max - window_min
		if window_delta > 5:
			pos = standard_deviations[i: i + 4].index(window_max)
			possible_error_vals.append({'std_pos': i + pos})
			#print window_max, " at ", i + pos - 2, " - ", i + pos + 2, " sec"


	for error in possible_error_vals:
		start = 0
		end = 0
		std_pos = error['std_pos']
		std_old = np.std(rows[((std_pos - 2) * window_size): ((std_pos - 2) * window_size) + 1000])
		for i in range(((std_pos - 2) * window_size), ((std_pos + 1) * window_size), 200):
			std_new = np.std(rows[i: i + 1000])
			if math.floor(std_new) - math.floor(std_old) > 3:
				if start == 0:
					start = i
				end = i

		error["start"] = start
		error["end"] = end
		error["time"] = '{}-{} seconds'.format(start / 1000.0, end / 1000.0)
		#print "Replace ", start, " - ", end, "len ", (end - start)

	return possible_error_vals
