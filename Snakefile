#snakemake to check for num of bases in segdup regions 
import sys,os 

configfile : "config.json"
#INBED = config["input_bed"]
#print (INBED)
INBEDS = config["input_bed"]
PAD = int(config["padEdge"])

rule all: 
	input: expand("{INBED}_boundary_SGcoverage.bed",INBED=INBEDS)


rule combine_left_right_bou:
	input: R="{INBED}_right_pctSG.bed", L="{INBED}_left_pctSG.bed", INP="{INBED}"
	output: temp("tmp"),"{INBED}_boundary_SGcoverage.bed"
	shell: """ cut -f 4,5 {input.L} | paste {input.INP} - > {output[0]}; cut -f 4,5 {input.R} | paste {output[0]}  - > {output[1]} """

rule right_percent:
        input: "{INBED}_right_nosSG.bed"
        output: "{INBED}_right_pctSG.bed"
        shell : """ awk '{{print $0,($4/($3-$2))}}'  {input}  | tr ' ' '\t' >  {output} """

rule left_percent: 
	input: "{INBED}_left_nosSG.bed"
	output: "{INBED}_left_pctSG.bed"
	shell : """ awk '{{print $0,($4/($3-$2))}}' {input} | tr ' ' '\t' >  {output} """

rule right_intersect:
        input: "{INBED}_right.bed", MSD= "merged_segdups.bed"
        output: temp("{INBED}_right_nosSG.bed")
        shell : """ bedtools intersect -a {input[0]} -b {input.MSD} -wao | bedtools groupby -g 1,2,3 -c 7 -o sum > {output} """


rule left_intersect:
	input: "{INBED}_left.bed", MSD= "merged_segdups.bed"
	output: temp("{INBED}_left_nosSG.bed")
	shell : """ bedtools intersect -a {input[0]} -b {input.MSD} -wao | bedtools groupby -g 1,2,3 -c 7 -o sum > {output} """

rule mergebed:
	input : SD=config["segdup_file"]
	output: "merged_segdups.bed"	
	shell : """ cut -f1,2,3 {input.SD} | sort -k1,1 -k2,2n -k3,3n | bedtools merge > {output} """

rule fatten_edge: 
	input: INP="{INBED}"
	output: temp("{INBED}_left.bed"), temp("{INBED}_right.bed")
	shell: """ python makeFatEdge.py -i {input.INP} -p {PAD}"""

