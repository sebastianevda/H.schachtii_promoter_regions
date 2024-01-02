
#requires input of several files - gff grepped for gene - gff grepped for start codon - and gff grepped for transcript.
#output is a tab file with locations.

from_feature = "CDS"
to_feature = "gene"

outfile = "locations_of_upstream_regions_per_gene.tab"
outfile_opened = open(outfile,"w")

outstring = ""

grep_transcript_file = "H_sch_gene_calls_v1_Apollo_with_gene.gff.grep.transcript"
grep_transcript_file_opened = open(grep_transcript_file)
grep_transcript_file_read = grep_transcript_file_opened.read()
grep_transcript_file_read_split = grep_transcript_file_read.split("\n")

grep_start_codon_file = "H_sch_gene_calls_v1_Apollo_with_gene.gff.grep.start_codon_per_transcript"
grep_start_codon_file_opened = open(grep_start_codon_file)
grep_start_codon_file_read = grep_start_codon_file_opened.read()
grep_start_codon_file_read_split = grep_start_codon_file_read.split("\n")

grep_gene_file = "H_sch_gene_calls_v1_Apollo_with_gene.gff.grep.gene"
grep_gene_file_opened = open(grep_gene_file)
grep_gene_file_read = grep_gene_file_opened.read()
grep_gene_file_read_split = grep_gene_file_read.split("\n")
skiplist = ""
skip = 0
#this gets general info about the genes.
for line in grep_transcript_file_read_split:
    if len(line) >1:
        #print (line)
        linesplit = line.split ("\t")
        scaffold = linesplit[0]
        direction = linesplit[6]
        pre_transcript_name = linesplit[8]
        pre_transcript_name_split = pre_transcript_name.split(";")
        transcript_name_with_ID = pre_transcript_name_split[0]
        transcript_name = transcript_name_with_ID[3:]
        #print (transcript_name)
        transcript_name_split = transcript_name.split(".")
        gene_name = transcript_name_split[0]
        #print (gene_name)
        gene_name_splitz = gene_name.split("_")
        gene_name_base = gene_name_splitz[0]+"_"+gene_name_splitz[1]+"_"
        gene_name_number = int(gene_name_splitz[2])
        #print (gene_name_base)
        #print (str(gene_name_number))
        
        ###this gets the start location from the star_codon_file (and is correct with direction).
        for lines in grep_start_codon_file_read_split:
            fail = 0
            if len(lines) >1:
                #print (lines)
                #print (transcript_name_with_ID)
                if transcript_name in lines:
                    #print lines
                    linessplit = lines.split ("\t")
                    direction = linessplit[6]
                    if direction is "-":
                        start_location = linessplit[4]
                        start_location_inc_codon = linessplit[3]
                        new_gene_number = gene_name_number +1
                        upstream_gene_name = gene_name_base+ str(new_gene_number)
                        #print (str(gene_name) + " "+ str(upstream_gene_name))
                        
                    if direction is "+":
                        start_location = linessplit[3]
                        start_location_inc_codon = linessplit[4]
                        upstream_gene_name = gene_name_base + str(gene_name_number -1)
                        new_gene_number = gene_name_number -1
                        #upstream_gene_name = gene_name_base+ str(new_gene_number)
                        #print gene_name
                        #print upstream_gene_name
                     
                        #print direction
                        #print start_location
                    #print ("gene name " + gene_name + ", transcript name " + transcript_name + ", start location " + start_location + "\n" + "old_line = " + lines)

                     

                    for liners in grep_gene_file_read_split:
                        if len (liners) >1:
                            #print (liners)
                            #print (upstream_gene_name)
                            linerssplit = liners.split ("\t")
                            scaffold = linesplit[0]
                            if liners.endswith(upstream_gene_name):
                                scaff_of_upstream = linerssplit[0]
                                #print ("\n")
                                #print ("gene_name = " + gene_name)
                                #print ("direction = " + direction)
                                #print (scaffold)
                                #print (lines)

                                #print ("upstream gene_name = " + upstream_gene_name)
                                #print (scaff_of_upstream)
                                
                                if scaff_of_upstream.endswith(scaffold):
                                    #print liners
                                    if direction is "-":
                                        end_location = linerssplit[3]
                                        #print ("interval is " + start_location + " to " + end_location + "\n")
                                        first_number = int(start_location_inc_codon)-1
                                        #if do not want ATG then first_number = start_location - also change in else belwo for when at end of scaff
                                        second_number = int(end_location)-1
                                        if int(first_number) > int(second_number):
                                            print ("warning - "  + transcript_name + " " + str(first_number) + " " + str(second_number))
                                            skip = 1
                                            new_gene_number = gene_name_number +2
                                            upstream_gene_name = gene_name_base+ str(new_gene_number)
                                            for liners in grep_gene_file_read_split:
                                                if len (liners) >1:
                                                    #print liners
                                                    linerssplit = liners.split ("\t")
                                                    scaffold = linesplit[0]
                                                    if liners.endswith(upstream_gene_name):
                                                        scaff_of_upstream = linerssplit[0]
                                                        #print "\n"
                                                        #print "gene_name = " + gene_name
                                                        #print "direction = " + direction
                                                        #print scaffold
                                                        #print lines

                                                        #print "upstream gene_name = " + upstream_gene_name
                                                        #print scaff_of_upstream
                                                        
                                                        if scaff_of_upstream.endswith(scaffold):
                                                            #print liners
                                                            if direction is "-":
                                                                end_location = linerssplit[3]
                                                                #print "interval is " + start_location + " to " + end_location + "\n"
                                                                first_number = int(start_location_inc_codon)-1
                                                                #if do not want ATG then first_number = start_location - also change in else belwo for when at end of scaff
                                                                second_number = int(end_location)-1
                                                                print ("warning fixed - "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                                if int(first_number) > int(second_number):
                                                                    print ("second warning - "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                                    new_gene_number = gene_name_number +3
                                                                    upstream_gene_name = gene_name_base+ str(new_gene_number)
                                                                    for liners in grep_gene_file_read_split:
                                                                        if len (liners) >1:
                                                                            #print liners
                                                                            linerssplit = liners.split ("\t")
                                                                            scaffold = linesplit[0]
                                                                            if liners.endswith(upstream_gene_name):
                                                                                scaff_of_upstream = linerssplit[0]
                                                                                #print "\n"
                                                                                #print "gene_name = " + gene_name
                                                                                #print "direction = " + direction
                                                                                #print scaffold
                                                                                #print lines

                                                                                #print "upstream gene_name = " + upstream_gene_name
                                                                                #print scaff_of_upstream
                                                                                
                                                                                if scaff_of_upstream.endswith(scaffold):
                                                                                    #print liners
                                                                                    if direction is "-":
                                                                                        end_location = linerssplit[3]
                                                                                        #print "interval is " + start_location + " to " + end_location + "\n"
                                                                                        first_number = int(start_location_inc_codon)-1
                                                                                        #if do not want ATG then first_number = start_location - also change in else belwo for when at end of scaff
                                                                                        second_number = int(end_location)-1
                                                                                        print ("second warning fixed - "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                                                        if int(first_number) > int(second_number):
                                                                                            print ("third warning " + gene_name)
                                                                                            new_gene_number = gene_name_number +4
                                                                                            upstream_gene_name = gene_name_base+ str(new_gene_number)
                                                                                            for liners in grep_gene_file_read_split:
                                                                                                if len (liners) >1:
                                                                                                    #print liners
                                                                                                    linerssplit = liners.split ("\t")
                                                                                                    scaffold = linesplit[0]
                                                                                                    if liners.endswith(upstream_gene_name):
                                                                                                        scaff_of_upstream = linerssplit[0]
                                                                                                        #print "\n"
                                                                                                        #print "gene_name = " + gene_name
                                                                                                        #print "direction = " + direction
                                                                                                        #print scaffold
                                                                                                        #print lines

                                                                                                        #print "upstream gene_name = " + upstream_gene_name
                                                                                                        #print scaff_of_upstream
                                                                                                        
                                                                                                        if scaff_of_upstream.endswith(scaffold):
                                                                                                            #print liners
                                                                                                            if direction is "-":
                                                                                                                end_location = linerssplit[3]
                                                                                                                #print "interval is " + start_location + " to " + end_location + "\n"
                                                                                                                first_number = int(start_location_inc_codon)-1
                                                                                                                #if do not want ATG then first_number = start_location - also change in else belwo for when at end of scaff
                                                                                                                second_number = int(end_location)-1
                                                                                                                print ("thrid warning fixed - "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                                                                                if int(first_number) > int(second_number):
                                                                                                                    print ("fourth warning " + gene_name)
                                                                                                        else:
                                                                                                            #print ("not on same scaff!!")
                                                                                                            #here need to set location as the end of the scaff then depending on direction either 1, or whatever is length of scaff.
                                                                                                            if direction is "+":
                                                                                                                first_number = str(1)
                                                                                                                second_number = start_location_inc_codon
                                                                                                            if direction is "-":
                                                                                                                second_number = "X"
                                                                                                                first_number = int(start_location_inc_codon)-1
                                                                                else:
                                                                                    #print ("not on same scaff!!")
                                                                                    #here need to set location as the end of the scaff then depending on direction either 1, or whatever is length of scaff.
                                                                                    if direction is "+":
                                                                                        first_number = str(1)
                                                                                        second_number = start_location_inc_codon
                                                                                    if direction is "-":
                                                                                        second_number = "X"
                                                                                        first_number = int(start_location_inc_codon)-1
                                                        else:
                                                            #print ("not on same scaff!!")
                                                            #here need to set location as the end of the scaff then depending on direction either 1, or whatever is length of scaff.
                                                            if direction is "+":
                                                                first_number = str(1)
                                                                second_number = start_location_inc_codon
                                                            if direction is "-":
                                                                second_number = "X"
                                                                first_number = int(start_location_inc_codon)-1
                                                            
                                                                
                                    if direction is "+":
                                        end_location = linerssplit[4]
                                        first_number = end_location
                                        second_number = start_location_inc_codon
                                        if int(first_number) > int(second_number):
                                            print ("warning + "  + transcript_name + " " + str(first_number) + " " + str(second_number))
                                            skip = 1
                                            new_gene_number = gene_name_number -2
                                            upstream_gene_name = gene_name_base+ str(new_gene_number)
                                            for liners in grep_gene_file_read_split:
                                                if len (liners) >1:
                                                    #print liners
                                                    linerssplit = liners.split ("\t")
                                                    scaffold = linesplit[0]
                                                    if liners.endswith(upstream_gene_name):
                                                        scaff_of_upstream = linerssplit[0]
                                                        #print "\n"
                                                        #print "gene_name = " + gene_name
                                                        #print "direction = " + direction
                                                        #print scaffold
                                                        #print lines

                                                        #print "upstream gene_name = " + upstream_gene_name
                                                        #print scaff_of_upstream
                                                        
                                                        if scaff_of_upstream.endswith(scaffold):
                                                            #print liners
                                                            if direction is "+":
                                                                end_location = linerssplit[3]
                                                                #print "interval is " + start_location + " to " + end_location + "\n"
                                                                first_number = int(end_location)
                                                                #if do not want ATG then first_number = start_location - also change in else belwo for when at end of scaff
                                                                second_number = int(start_location_inc_codon)
                                                                print ("warning fixed + "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                            
                                                                skip = 1
                                                                if int(first_number) > int(second_number):
                                                                    print ("second warning + "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                                    new_gene_number = gene_name_number -3
                                                                    upstream_gene_name = gene_name_base+ str(new_gene_number)
                                                                    for liners in grep_gene_file_read_split:
                                                                        if len (liners) >1:
                                                                            #print liners
                                                                            linerssplit = liners.split ("\t")
                                                                            scaffold = linesplit[0]
                                                                            if liners.endswith(upstream_gene_name):
                                                                                scaff_of_upstream = linerssplit[0]
                                                                                #print "\n"
                                                                                #print "gene_name = " + gene_name
                                                                                #print "direction = " + direction
                                                                                #print scaffold
                                                                                #print lines

                                                                                #print "upstream gene_name = " + upstream_gene_name
                                                                                #print scaff_of_upstream
                                                                                
                                                                                if scaff_of_upstream.endswith(scaffold):
                                                                                    #print liners
                                                                                    if direction is "+":
                                                                                        end_location = linerssplit[3]
                                                                                        #print "interval is " + start_location + " to " + end_location + "\n"
                                                                                        first_number = int(end_location)
                                                                                        #if do not want ATG then first_number = start_location - also change in else belwo for when at end of scaff
                                                                                        second_number = int(start_location_inc_codon)
                                                                                        print ("second warning fixed + "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                                                        if int(first_number) > int(second_number):
                                                                                            print ("third warning " + gene_name)
                                                                                            new_gene_number = gene_name_number -4
                                                                                            upstream_gene_name = gene_name_base+ str(new_gene_number)
                                                                                            for liners in grep_gene_file_read_split:
                                                                                                if len (liners) >1:
                                                                                                    #print liners
                                                                                                    linerssplit = liners.split ("\t")
                                                                                                    scaffold = linesplit[0]
                                                                                                    if liners.endswith(upstream_gene_name):
                                                                                                        scaff_of_upstream = linerssplit[0]
                                                                                                        #print "\n"
                                                                                                        #print "gene_name = " + gene_name
                                                                                                        #print "direction = " + direction
                                                                                                        #print scaffold
                                                                                                        #print lines

                                                                                                        #print "upstream gene_name = " + upstream_gene_name
                                                                                                        #print scaff_of_upstream
                                                                                                        
                                                                                                        if scaff_of_upstream.endswith(scaffold):
                                                                                                            #print liners
                                                                                                            if direction is "+":
                                                                                                                end_location = linerssplit[3]
                                                                                                                #print "interval is " + start_location + " to " + end_location + "\n"
                                                                                                                first_number = int(end_location)
                                                                                                                #if do not want ATG then first_number = start_location - also change in else belwo for when at end of scaff
                                                                                                                second_number = int(start_location_inc_codon)
                                                                                                                print ("thrid warning fixed + "  + gene_name + " " + str(first_number) + " " + str(second_number))
                                                                                                                if int(first_number) > int(second_number):
                                                                                                                    print ("fourth warning " + gene_name)
                                                                                                        else:
                                                                                                            #print ("not on same scaff!!")
                                                                                                            #here need to set location as the end of the scaff then depending on direction either 1, or whatever is length of scaff.
                                                                                                            if direction is "+":
                                                                                                                first_number = str(1)
                                                                                                                second_number = start_location_inc_codon
                                                                                                            if direction is "-":
                                                                                                                second_number = "X"
                                                                                                                first_number = int(start_location_inc_codon)-1
                                                                                else:
                                                                                    #print ("not on same scaff!!")
                                                                                    #here need to set location as the end of the scaff then depending on direction either 1, or whatever is length of scaff.
                                                                                    if direction is "+":
                                                                                        first_number = str(1)
                                                                                        second_number = start_location_inc_codon
                                                                                    if direction is "-":
                                                                                        second_number = "X"
                                                                                        first_number = int(start_location_inc_codon)-1
                                                        else:
                                                            #print ("not on same scaff!!")
                                                            #here need to set location as the end of the scaff then depending on direction either 1, or whatever is length of scaff.
                                                            if direction is "+":
                                                                first_number = str(1)
                                                                second_number = start_location_inc_codon
                                                            if direction is "-":
                                                                second_number = "X"
                                                                first_number = int(start_location_inc_codon)-1
                                        #if do not want ATG then second_number = start_location - also change in else belwo for when at end of scaff
                                        #print "interval is " + end_location + " to " + start_location
                                    
                                else:
                                    #print ("not on same scaff!!")
                                    #here need to set location as the end of the scaff then depending on direction either 1, or whatever is length of scaff.
                                    if direction is "+":
                                        first_number = str(1)
                                        second_number = start_location_inc_codon
                                    if direction is "-":
                                        second_number = "X"
                                        first_number = int(start_location_inc_codon)-1
                                if skip is 0:
                                    #print "Direction of\t" + transcript_name + "\tis\t" + direction+ "\t and its on scaff\t" + scaffold + "\t" + str(first_number) + "\tto\t" + str(second_number)      
                                    outstring = outstring + "Direction of\t" + transcript_name + "\tis\t" + direction+ "\t and its on scaff\t" + scaffold + "\t" + str(first_number) + "\tto\t" + str(second_number) + "\n"
                                    
                                else:
                                    skiplist = skiplist + gene_name + "\n"
                                    print ("skipped " + transcript_name)
                                    skip = 0
outstringsplit = outstring.split("\n")
old = ""
newstring = ""
for x in range(len(outstringsplit)):
    if outstringsplit[x] in old:
        donothing = 1
    else:
        newstring = newstring + outstringsplit[x] + "\n"
    old = outstringsplit[x]
outfile_opened.write(newstring)
outfile_opened.close()
print (skiplist)

outfileskip = "skiplist.txt"
outfile_openedsk = open(outfileskip,"w")
outfile_openedsk.write(skiplist)
outfile_openedsk.close()
#dont forget to remove all genes from skiplist from file using  extract_expression_from_tabular_keep_order_of_list_with_zeros_opposite.py
#so print this to a file - and then go through it later.
#firstly if there are two or more transcripts that have the exact same upstream region, then just use one.
#then go through fasta and print them off line by line.
#and later could do only the .t1s if I wanted.

