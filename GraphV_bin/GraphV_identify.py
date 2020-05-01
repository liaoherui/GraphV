import re
import os
import json
import getopt
import sys


opts,args=getopt.getopt(sys.argv[1:],"g:i:o:p:d:c:v:")

graph=''
input_json=''
out=''
prefix=''
default_db_dir=''
uniquq_cov=''
virus_type=''

for opt,arg in opts:
	if opt=='-g':
		graph=arg
	elif opt=='-i':
		input_json=arg
	elif opt=='-o':
		out=arg
	elif opt=='-p':
		prefix=arg
	elif opt=='-d':
		default_db_dir=arg
	elif opt=='-c':
		unique_cov=arg
	elif opt=='-v':
		virus_type=arg


#default_db_dir='../All_other_db'
name_pre={}
# Load Name <-> prefix dict
#fm=open('/mnt/d/My_Research/Graph_Genome/GraphV_GraphC/GraphC_Tem_SCOV2/map_id_name.txt','r')
#fm=open('/mnt/d/My_Research/Graph_Genome/GraphV_GraphC/GraphC_Tem_LSV/map_id_name.txt','r')
fm=open(default_db_dir+'/'+virus_type+'/map_id_name.txt','r')
while True:
	line=fm.readline().strip()
	if not line:break
	ele=line.split('\t')
	name_pre[ele[1]]=ele[0]

#strain='HIV_8067'

f=open(graph,'r')

node={}   # all node
path_node={}
path_length={}
target_node={}
path_direction={}
node_count={}
node_path={}


while True:
	line=f.readline().strip()
	if not line:break
	if line[0]=='S':
		ele=line.split('\t')
		node[ele[1]]=ele[-1]
	if line[0]=='P':
		ele=line.split('\t')
		all_node=re.split(',',ele[-1])
		path_node[ele[1]]={}
		path_direction[ele[1]]=[]
		for n in all_node:
			if re.search('\+',n):
				path_direction[ele[1]].append('+')
			else:
				path_direction[ele[1]].append('-')
			n=re.sub('\+','',n)
			n=re.sub('\-','',n)
			if n not in node_path:
				node_path[n]={}
				node_path[n][ele[1]]=''
			else:
				node_path[n][ele[1]]=''
			if n not in node_count:
				node_count[n]=1
			else:
				node_count[n]+=1
			path_node[ele[1]][n]=''

# get path length and init covered dict
path_unique_covered_node={}
path_multiple_covered_node={}
path_all_covered_node={}

for p in path_node:
	path_unique_covered_node[p]={}
	path_multiple_covered_node[p]={}
	path_all_covered_node[p]={}
	path_length[p]=0
	for n in path_node[p]:
		path_length[p]+=len(node[n])


#f2=open('../HIV_L1500.json','r')
with open(input_json,'r') as aln_json:
	for line in aln_json:
		path_ref_length={} # Tem dict for output
		for p in path_node:
			path_ref_length[p]=0
		aln=json.loads(line)
		#print(aln['identity'])
		if float(aln['identity'])<0.9:continue
		path=aln['path']
		mapping=path['mapping']
		total_len=0
		alignment_node={} # all mapped nodes in this alignment
		for node_info in mapping:
			position=node_info['position']
			node_id=position['node_id']
			alignment_node[node_id]=''
			edit=node_info["edit"]
			'''
			seq_name=aln["name"]
			seq_name=re.split(';',seq_name)
			ch=re.sub('chromosome=','',seq_name[3])
			rid=re.sub('Read=','R',seq_name[0])
			seq_name=ch+'_'+rid
			'''
			from_len=0
			for aln_piece in edit:
				if 'from_length' in aln_piece:
					from_len+=int(aln_piece['from_length'])
			total_len+=from_len
			for p in node_path[node_id]:
				path_ref_length[p]+=from_len
		if total_len<500:continue # only consider alignment bigger than 500bp
		# Divide into 2 cases
		res=sorted(path_ref_length.items(),key=lambda d:d[1],reverse=True)
		if res[0][1]==res[1][1]:
			iden=1
		else:
			iden=0
		highest=res[0][1]
		for node_info in mapping:
			position=node_info["position"]
			node_id=position["node_id"]
			cutoff=int(0.9*highest)
			for r in res:
				if r[1]<cutoff:break
				if node_id in path_node[r[0]]:
					path_all_covered_node[r[0]][node_id]=''
			if not iden==1:
				if node_id in path_node[res[0][0]]:
					path_unique_covered_node[res[0][0]][node_id]=''
					#path_all_covered_node[res[0][0]][node_id]=''
			'''
			else:
				for r in res:
					if r[1]<cutoff:break
					if node_id in path_node[r[0]]:
						path_multiple_covered_node[r[0]][node_id]=''
						#path_all_covered_node[r[0]][node_id]=''
			'''





path_unique_cov={}
#path_multiple_cov={}
path_unique_length={}
#path_multiple_length={}
path_all_cov={}
path_all_length={}

#o=open(out+'_Multiple_Cov.txt','w+')
#o2=open(out+'_Multiple_Cov_by_length.txt','w+')
out=out+'/'+prefix
o4=open(out+'_All_Cov.txt','w+')
o5=open(out+'_All_Cov_by_length.txt','w+')
o3=open(out+'_Unique_Cov.txt','w+')
o1=open(out+'_Most_possible_Strain_report.txt','w+')


for p in path_node:
	path_unique_cov[p]=0
	#path_multiple_cov[p]=0
	path_all_cov[p]=0


	#pc_m=0
	pc_u=0
	pc_a=0
	'''
	if not len(path_multiple_covered_node[p])==0:
		for n in path_multiple_covered_node[p]:
			pc_m+=len(node[n])
	'''
	if not len(path_unique_covered_node[p])==0:
		for n in path_unique_covered_node[p]:
			pc_u+=len(node[n])
	if not len(path_all_covered_node[p])==0:
		for n in path_all_covered_node[p]:
			pc_a+=len(node[n])
	
	path_unique_length[p]=int(pc_u)
	#path_multiple_length[p]=int(pc_m)
	path_all_length[p]=int(pc_a)

	#path_multiple_cov[p]=float(pc_m)/float(path_length[p])
	path_unique_cov[p]=float(pc_u)/float(path_length[p])
	path_all_cov[p]=float(pc_a)/float(path_length[p])

'''
res=sorted(path_multiple_cov.items(),key=lambda d:d[1],reverse=True)
for r in res:
	o.write(r[0]+'\t'+str(path_multiple_length[r[0]])+'\t'+str(path_length[r[0]])+'\t'+str(r[1])+'\n')'

res2=sorted(path_multiple_length.items(),key=lambda d:d[1],reverse=True)
for r in res2:
	o2.write(r[0]+'\t'+str(r[1])+'\t'+str(path_length[r[0]])+'\t'+str(path_multiple_cov[r[0]])+'\n')
'''

unique_res=[]
res3=sorted(path_unique_cov.items(),key=lambda d:d[1],reverse=True)
for r in res3:
	if r[1]>=float(unique_cov):unique_res.append(r[0])
	o3.write(r[0]+'\t'+str(path_unique_length[r[0]])+'\t'+str(path_length[r[0]])+'\t'+str(r[1])+'\t'+name_pre[r[0]]+'\n')


res4=sorted(path_all_cov.items(),key=lambda d:d[1],reverse=True)
for r in res4:
	o4.write(r[0]+'\t'+str(path_all_length[r[0]])+'\t'+str(path_length[r[0]])+'\t'+str(r[1])+'\n')


res5=sorted(path_all_length.items(),key=lambda d:d[1],reverse=True)
for r in res5:
	o5.write(r[0]+'\t'+str(r[1])+'\t'+str(path_length[r[0]])+'\t'+str(path_all_cov[r[0]])+'\n')


top1_al=[]
top5_al=[]
t=0

top1_al.append(res5[0][0])
for r in res5[:5]:
	top5_al.append(r[0])
	

# Report part
o1.write('>>>>>Result1 <-----> Based on feature: Alignment length<<<<<\n\n')
o1.write('[The most possible strains in dataset (Top1)]:\n')
o1.write('[Strain_prefix]\t[Strain_Name]\n')
o1.write(top1_al[0]+'\t'+name_pre[top1_al[0]]+'\n\n')
o1.write('[The most possible strains in dataset (Top5)]:\n')
o1.write('[Strain prefix]\t[Alignment Length]\t[Alignment Coverage]\t[Strain_Name]\n')
for a in top5_al:
	o1.write(a+'\t'+str(path_all_length[a])+'\t'+str(path_all_cov[a])+'\t'+name_pre[a]+'\n')
o1.write('\n------------------------------------------------------------------------\n')
o1.write('>>>>>Result2 <-----> Based on feature: Unique Coverage<<<<<\n\n')
o1.write('[Other possibble strains in dataset (unique coverage cutoff: 90%)]\n')
o1.write('[Strain prefix]\t[Unique Coverage]\t[Strain_Name]\n')
if not len(unique_res)==0:
	for a in unique_res:
		o1.write(a+'\t'+str(path_unique_cov[a])+'\t'+name_pre[a]+'\n')

