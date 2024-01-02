#requires output of previous script + fasta file of genome.
#creates two files (one for each direction) of upstream regions - the minus needs to be rev comped (i think)

genome_file = "Cam_Hsc_genome1.2.fa"
genome_file_opened = open(genome_file)
genome_file_read = genome_file_opened.read()
genome_file_read_split = genome_file_read.split(">")

coord_file = "locations_of_upstream_regions_per_gene.tab.skipped"
coord_file_opened = open(coord_file)
coord_file_read = coord_file_opened.read()
coord_file_read_split = coord_file_read.split("\n")

outstring_plus = ""
outstring_minus = ""


for line in genome_file_read_split:
    if len(line)>0:
        linesplit = line.split("\n")
        name = linesplit[0]
        entry = ""
        seq = entry.join(linesplit[1:])
        scaffold_length = len(seq)
        #print scaffold_length
        for lines in coord_file_read_split:
            if len(lines)>0:
                slinessplit = lines.split("\t")
                #print lines
                direction = slinessplit[3]
                scaffold = slinessplit[5]
                location_1 = slinessplit[6]
                location_2 = slinessplit[8]
                upstream_of_which_transcript = slinessplit[1]
                if name.endswith(scaffold):
                    if location_2 is "X":
                        location_2 = scaffold_length
                    #print direction
                    #print scaffold
                    #print location_1
                    #print location_2
                    if direction is "+":
                        outstring_plus = outstring_plus + ">" + scaffold + "_" + str(location_1) + "_to_"+ str(location_2)+"_" + direction + "_of_"+ upstream_of_which_transcript+ "\n" + seq[int(location_1):int(location_2)] + "\n"
                    if direction is "-":
                        outstring_minus = outstring_minus + ">" + scaffold + "_" + str(location_1) + "_to_"+ str(location_2)+"_" + direction + "_of_"+ upstream_of_which_transcript+ "\n" + seq[int(location_1):int(location_2)] + "\n"
                    #print ">"+scaffold+"_"+upstream_of_which_transcript + "\n" + seq[int(location_1):int(location_2)]
print ("sorted out the upstream regions - next step is to iterate through to make sub-sets by length")
#sort out the different lengths files from the original ArithmeticError outstring.

outstring_plus_split = outstring_plus.split(">")
length = 200
for x in range(20):
    new_outstring = ""
    if x >0:
        length_to_print = int(length*x)
        print ("plus strand - "+str(length_to_print))
        outfileplus = "upstream_regions_plus_"+str(length_to_print)+".fa"
        outfileplus_opened = open(outfileplus,"w")
        for liner in outstring_plus_split:
            if len(liner)>0:
                linersplit = liner.split("\n")
                name = linersplit[0]
                seq = linersplit[1]
                length_of_seq = len(seq)
                length_to_use_finally = length_to_print
                if length_to_print>length_of_seq:
                    length_to_use_finally = length_of_seq
                new_outstring = new_outstring + ">"+name + "\n" + seq[length_of_seq-length_to_use_finally:] + "\n"
        outfileplus_opened.write(new_outstring)
        outfileplus_opened.close()



outstring_minus_split = outstring_minus.split(">")
length = 200
for x in range(20):
    new_outstring = ""
    if x >0:
        length_to_print = int(length*x)
        print ("minus strand - "+str(length_to_print))
        outfileminus = "upstream_regions_minus_"+str(length_to_print)+".fa"
        outfileminus_opened = open(outfileminus,"w")
        for liner in outstring_minus_split:
            if len(liner)>0:
                linersplit = liner.split("\n")
                name = linersplit[0]
                seq = linersplit[1]
                length_of_seq = len(seq)
                length_to_use_finally = length_to_print
                if length_to_print>length_of_seq:
                    length_to_use_finally = length_of_seq
                new_outstring = new_outstring + ">"+name + "\n" + seq[:length_to_use_finally] + "\n"
        outfileminus_opened.write(new_outstring)
        outfileminus_opened.close()
              
            
            
        
                        
