#Creates fat edges (inward, because the caller takes the outer edge for boundary) around the call 
# boundaries, intersects with segdups and reports pct coverage. 
import sys,os,string
import argparse


def fat_edge(inp,side,outb,pad):
	openbed = open(inp,"r").readlines()
	if side == "L":
		leftout = args.inputbed.strip()+"_left.bed"		
		lwrite = open(leftout,"a+")	
		lwrite.truncate()
		for intervals in openbed:
	
			splitinterval = intervals.split('\t')
			#print splitinterval
			chrom,start,end  = splitinterval[0:3]
			#print  chrom,start,end 
			#max_size = sizes[chrom]
			fatstart = int(start)  #Assuming a 10kb padding
			fatend = int(start) + pad
			if fatstart < 1 : fatstart = 1
			#if fatend > max_size: fatend = chrom_size
			returnstr = chrom + "\t" + str(fatstart) + "\t" + str(fatend)+"\t"
			newbed = returnstr +''.join (''.join(x+"\t") for x in splitinterval[3:])
			#print "newbed:\n" ,newbed
			lwrite.write(returnstr.strip()+"\n")
		lwrite.close()
	if side == "R":
                rightout = args.inputbed.strip()+"_right.bed"
		rwrite = open(rightout,"a+")
		rwrite.truncate()
                for intervals in openbed:

                        splitinterval = intervals.split('\t')
                        #print splitinterval
                        chrom,start,end  = splitinterval[0:3]
                        #print  chrom,start,end
                        #max_size = sizes[chrom]
                        fatstart = int(end) - pad #Assuming a 10kb padding
                        fatend = int(end) 
                        if fatstart < 1 : fatstart = 1
                        #if fatend > max_size: fatend = chrom_size
                        returnstr = chrom + "\t" + str(fatstart) + "\t" + str(fatend)+"\t"
                        newbed = returnstr +''.join (''.join(x+"\t") for x in splitinterval[3:])
                        #print "newbed:\n" ,newbed
			rwrite.write(returnstr.strip()+"\n")
		rwrite.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(usage="Create padded bediles for the boundaries of your call\nusage: makeFatEdge.py [-h] -i <input bedfile> -p <pad size>\n")
	parser.add_argument("-i",dest="inputbed",help="Input bedfile",required=True)
	parser.add_argument("-p", dest="pad",help="Pad edges by this many basepairs")
	args = parser.parse_args()
	leftout = args.inputbed.strip('bed')+"_left.bed"
	rightout = args.inputbed.strip('bed')+"_right.bed"
	pad = int(args.pad)
	fat_edge(args.inputbed,"L",leftout,pad)
	fat_edge(args.inputbed,"R",rightout,pad)

