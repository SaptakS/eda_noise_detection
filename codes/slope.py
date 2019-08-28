# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math

fr = open('D:/Brain Signals/Amritesh/noise/1/opensignals_201510266286_2016-09-14_18-29-05.txt', 'r+')
fw = open('D:/Brain Signals/Amritesh/noise/1/slope.txt', 'w+')
data = []
for line in fr:
     data.append(line.split('\t')[5])
#print data
window_size = 1000

for i in range(0, len(data), window_size / 2):
    if len(data[i:i + window_size]) < window_size:
        break
    window_data = data[i:i + window_size]
    first_maxima = max(window_data[0:9])
    first_maxima_index = window_data[0:9].index(first_maxima)
    second_maxima = max(window_data[91:100])
    second_maxima_index = 91 + window_data[91:100].index(second_maxima)
    height = int(first_maxima) - int(second_maxima)
    base = first_maxima_index - second_maxima_index
    tan_theta = float(height) / float(base)
    angle = math.degrees(math.atan(tan_theta))
    #print tan_theta, angle
    
    fw.write('{}\t{}\n'.format('{0:.2f}'.format(tan_theta), '{0:.2f}'.format(angle)))
fw.close()
fr.close()
