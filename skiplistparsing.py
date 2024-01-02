#pull all fasta entries using a list-infasta and out fasta. Enter info from the command line. 
import sys
import re

list_filename = "skiplist.txt"
input_filename = "locations_of_upstream_regions_per_gene.tab"
output_filename = "locations_of_upstream_regions_per_gene.tab.skipped"


listofnames = open(list_filename)
withmatchedid = open(output_filename, "a")
infile = open(input_filename)
read = infile.read()
#cleaninfile = read.replace("\n","")
#rep = cleaninfile.replace (">","\n>")
splitrep = read.split("\n")
#print splitrep
#NAMES_DICT = {}
listofnames_read = listofnames.read()
listofnames_split = listofnames_read.split("\n")
for lines in splitrep:

    #print lines
    
    #print clean
    found = 0
    for line in listofnames_split:
        if len(line)>0:
            
        #print line
            if line + "." in lines:
                print (line)
                found = 1
    if found<1:
        withmatchedid.write(lines  +"\n")

        #print (clean)
##    if clean.startswith("M"):
##        #print (clean)
##        x = 0
##        s = re.search(clean,cleaninfile)
##        e = re.search(clean+".*>M",cleaninfile)
##        print str(s.start()) +"   " +str(e.end())
##        #print "\n"+cleaninfile[s.start()-1:e.end()-1]
##        #e = re.search(line+"*>",read)
##        #print read[s.start():e.end()-1]
##        #withmatchedid.write(line)
##            
listofnames.close()
withmatchedid.close()
infile.close()
