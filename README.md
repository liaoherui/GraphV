# GraphV - An RNA virus strain-level identification tool using long reads and genome graph.

### E-mail: heruiliao2-c@my.cityu.edu.hk
### Version: V1.0
---------------------------------------------------------------------------
### Dependencies:
* Python >=3.6
* GraphAligner 1.0.10 (https://github.com/maickrau/GraphAligner)

Make sure these programs have been installed and added in path.

### Install (Only for linux)

####
`git clone https://github.com/liaoherui/GraphV.git`<BR/>
####
Then, you need to download the genome graph database for 8 RNA viruses. Run:<BR/>
`cd GraphV`<BR/>
`sh download.sh`<BR/>
### Usage

Use `python GraphV.py -h` to check the usage.

A demo real data of Sars-Cov-2 is included in GraphV folder, which can be uesd for test.

A running demo: (Result will be generated in the folder called `"GraphV"` by default)

`python GraphV.py -i Data/SRR10948550_801.fastq -v SCOV2`

The table about virus name and virus_type parameter:

| Virus Name | virus_type parameter |
|------|-------------|
| SARS-Cov-2  | `SCOV2`     |
| HIV  | `HIV`      |
| HCV  | `HCV`     |
| Ebolavirus  | `EBV`        |
| Zika virus  | `ZKV` |
| Dengue virus  | `DGV`        |
| Lassa virus  | `LSV`        |
| Enterovirus  | `ETVA`        |

### Output file

There will be 5 output files of GraphV.

1. `*.json` file --- The alignment result file from GraphAligner.

2. `*_Most_possible_Strain_report.txt` --- The final report generated bu GraphV.

3. `*_All_Cov.txt` --- The GraphV result file which is sorted by the descending order of alignment coverage.

4. `*_All_Cov_by_length.txt` --- The GraphV result file which is sorted by the descending order of alignment length.

5. `*_Unique_Cov.txt` --- The GraphV result file which is sorted by the descending order of unique coverage.

Note: <BR/><BR/>
For 3, 4, the meaning of each column in the file is: `Strain name, alignment length, genome length, alignment coverage`.<BR/>
For 5, the meaning of each column in the file is: `Strain name, alignment length, genome length, unique coverage, strain name in database`.

