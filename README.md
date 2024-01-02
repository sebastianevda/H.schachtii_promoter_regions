Prepare necessary files:
Cam_Hsc_genome1.2.fa

gff grepped for "gene\t"
gff grepped for "start codon\t"
gff grepped for "transcript\t"

run "extract_upstream_regions_moded_without_gene_in_gene.py"
creates "locations_of_upstream_regions_per_gene.tab" and "skiplist.txt"

then run "skiplistparsing.py"
creates "locations_of_upstream_regions_per_gene.tab.skipped"

then run "using_locations_extract_upstream_Regions_From_fasta_all_transcript_variants.py"
creates many files (upstream regions from 200 bp to 3800 bp) - can be modified - for each direction (plus or minus on the genome)

then reverse complement the minuses using the following command, and merge with the pluses
cat input.fa | while read L; do  echo $L; read L; echo "$L" | rev | tr "ATGC" "TACG" ; done

Using these upstream regions files, can pull out genes of interest for comparisons.
