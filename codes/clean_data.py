import os

for root, subFolders, files in os.walk(os.getcwd()):
    for file_ in files:
    	if file_.endswith(".txt") and file_.startswith("opensignals"):
    		print "Opened " + os.path.join(root, file_)
    		fr = open(os.path.join(root, file_), "r")
    		fw = open(os.path.join(root, "cleaned_"+file_), "w")
    		for line in fr:
    			if not line.startswith("#"):
    				fw.write(line.split('\t')[0] + "\t" + line.split('\t')[5] + "\n")
    		fw.close()
    		fr.close()
    		print "Writing Complete"
                
