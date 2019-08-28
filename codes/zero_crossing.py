import numpy as np
import matplotlib.pyplot as plt
import os
import error_detection as ed
import error_correction as ec

def std_zero_crossing_fixed_window(rows, window_size, fw):
	for i in range(0, len(rows), window_size):
		temp = []
		temp1 = []
		avg = 0
		if len(rows) - i >= window_size:
			avg = (sum(rows[i: (i + window_size - 1)])) / window_size;
			temp = rows[i: i + window_size];
		else:
			avg = (sum(rows[i: len(rows)])) / (len(rows) - i);
			temp = rows[i: len(rows)];

		for j in range(0, len(temp) - 1):
			temp1.append(temp[j] - avg) 

		count = 0
		if temp1[0] > 0:
			flag = 1
		else:
			flag = 0

		for j in range(1, len(temp1) - 1):
			if temp1[j] > 0 and flag == 1:
				flag = 1
				count = count + 1
			elif temp1[j] < 0 and flag == 0:
				flag = 0
				count = count + 1
		std = np.std(np.array(temp))
		fw.write('{}\t{}\n'.format('{0:.4f}'.format(std), count))
	fw.close()

def std_zero_crossing_slide_window(rows, window_size, fw):
	for i in range(0, len(rows), window_size / 2):
		temp = []
		temp1 = []
		avg = 0
		if len(rows) - i >= window_size:
			avg = (sum(rows[i: (i + window_size - 1)])) / window_size;
			temp = rows[i: i + window_size];
		else:
			avg = (sum(rows[i: len(rows)])) / (len(rows) - i);
			temp = rows[i: len(rows)];

		for j in range(0, len(temp) - 1):
			temp1.append(temp[j] - avg) 

		count = 0
		if temp1[0] > 0:
			flag = 1
		else:
			flag = 0

		for j in range(1, len(temp1) - 1):
			if temp1[j] > 0 and flag == 1:
				flag = 1
				count = count + 1
			elif temp1[j] < 0 and flag == 0:
				flag = 0
				count = count + 1
		std = np.std(np.array(temp))
		fw.write('{}\t{}\n'.format('{0:.4f}'.format(std), count))
	fw.close()

if __name__ == '__main__':
	for root, subFolders, files in os.walk("/home/saptaks/Downloads/brain/Brain_Signal_Data/data/"):
	    for file_ in files:
	    	if file_.endswith(".txt") and file_.startswith("cleaned"):
				print "\n\nOpened ", str(os.path.join(root, file_)).split('/')[7], " Data"
				fr = open(os.path.join(root, file_), "r")
				fw1 = open(os.path.join(root, "1000_fixed_"+file_), "w")

				rows = [int(line.split("\t")[1]) for line in fr]
				
				#Detect Device Error
				error_device_arr = ed.device_error_detect(rows)
				device_error_removed_arr = rows
				for (error, replace_val) in error_device_arr:	
					#Display Device Error
					print "\nDevice Error Detected"
					print "Error at ", rows.index(error) / 1000.0, "seconds"
					print "Error Value: ", error
					print "-------------------------------------------------------------"
					#Remove Device Error
					fw_device = open(os.path.join(root, "device_err_corr_" + file_), "w")
					device_error_removed_arr = ec.replace_error(rows, error, replace_val)

					for i in range(0, len(device_error_removed_arr)):
						fw_device.write('{}\n'.format(device_error_removed_arr[i]))
					fw_device.close()

					print "Device Error Removed"
					print "Replaced Value: ", replace_val
					print "Corrected Data written in ", os.path.join(root, "device_err_corr_" + file_)
					print "______________________________________________________________"

				window_size = 1000
				std_zero_crossing_fixed_window(device_error_removed_arr, window_size, fw1)

				#Detect Artefacts
				artefact_std_errors = ed.std_error_detect(device_error_removed_arr, \
							open(os.path.join(root, "1000_fixed_"+file_), "r"))

				#Display Artefacts
				artefact_error_removed_arr = device_error_removed_arr
				for error in artefact_std_errors:
					print "\nArtefact Error Detected"
					print "Error at ", error["time"]
					#Remove Artefact Error
					fw_artefact = open(os.path.join(root, "artefact_err_corr_" + file_), "w")
					artefact_error_removed_arr = ec.std_error_correct(device_error_removed_arr, error)

					for i in range(0, len(artefact_error_removed_arr)):
						fw_artefact.write('{}\n'.format(artefact_error_removed_arr[i]))
					fw_artefact.close()

					print "Artefact Error Removed"
					print "Corrected Data written in ", os.path.join(root, "artefact_err_corr_" + file_)
					print "______________________________________________________________"

				fw2 = open(os.path.join(root, "1000_fixed_corr_"+file_), "w")
				std_zero_crossing_fixed_window(artefact_error_removed_arr, window_size, fw2)

				#Save Plot of STD
				fig = plt.figure()
				f1_std = open(os.path.join(root, "1000_fixed_"+file_), "r")
				f2_std = open(os.path.join(root, "1000_fixed_corr_"+file_), "r")
				rows1 = [float(line.split("\t")[0]) for line in f1_std]
				rows2 = [float(line.split("\t")[0]) for line in f2_std]
				plt.plot(rows1)
				plt.plot(rows2)
				fig.savefig(os.path.join(root, "std_plot.png"), dpi=fig.dpi)

				print "Done...."

