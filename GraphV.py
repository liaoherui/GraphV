import re
import os,sys
import argparse
import subprocess

__author__="Liao Herui"

usage="GraphV - Identify RNA virus strains from long reads using genome graph."

def main():
	db_dir='GraphV_DB'
	identify_script='GraphV_bin'

	### Parameter Set
	parser=argparse.ArgumentParser(prog='GraphV.py',description=usage)
	parser.add_argument('-i','--input_reads',dest='input_read',type=str,required=True,help="Long reads in fastq format --- Required")
	parser.add_argument('-v','--virus_type',dest='virus_type',type=str,required=True,help="The type of virus. For example, \"-v SCOV2\" --- Required")
	parser.add_argument('-o','--output_dir',dest='output_dir',type=str,help='Output file dir (default: current workdir)')
	parser.add_argument('-p','--output_prefix',dest='output_prefix',type=str,help='The prefix of output name (default: GraphV)')
	parser.add_argument('-t','--threads',dest='thread',type=str,help='number of threads (int) (default 1)')
	parser.add_argument('-c','--unique_cov',dest='unique_cov',type=str,help='unique coverage output cutoff (float: 0.0-1.0) (default 0.9)')
	args=parser.parse_args()
	in_read=args.input_read
	vtype=args.virus_type
	out_dir=args.output_dir
	threads=args.thread
	ucc=args.unique_cov
	prefix=args.output_prefix

	if not out_dir:
		out_dir='GraphV'
	if not prefix:
		prefix='GraphV'
	if not threads:
		threads='1'
	if not ucc:
		ucc='0.9'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	##### Only 2 steps totally #####

	# 1. The first Step is to Run the GraphAligner
	graphAligner(db_dir,in_read,vtype,threads,out_dir,prefix)

	# 2. Identify the strains based on th alignment result
	identify(db_dir,identify_script,vtype,out_dir,prefix,ucc)


def identify(db_dir,identify_script,vtype,out_dir,prefix,ucc):
	print(':: GraphV - 2. Identify strains based on graph alignment res...\n')
	pwd=os.getcwd()
	if not re.search('/',out_dir):
		out_dir=pwd+'/'+out_dir
	os.chdir(identify_script)
	cmd='python GraphV_identify.py -d ../'+db_dir+' -i '+out_dir+'/'+prefix+'.json -c '+ucc+' -v '+vtype+' -g  ../'+db_dir+'/'+vtype+'/clean_recluster.gfa -p '+prefix+' -o '+out_dir
	p=subprocess.run(cmd,shell=True)
	print(':: GraphV - 2. Done.\n')
	return


def graphAligner(db_dir,in_read,vtype,threads,out_dir,prefix):
	print(':: GraphV - 1. Align all input reads to the genome graph...\n\n')
	cmd='GraphAligner -t '+threads+' -g '+db_dir+'/'+vtype+'/clean_recluster.vg -f '+in_read+' -a '+out_dir+'/'+prefix+'.json -x vg'
	p=subprocess.run(cmd,shell=True)
	print('\n:: GraphV - 1. Done.\n')
	return



if __name__=='__main__':
	sys.exit(main())
		
