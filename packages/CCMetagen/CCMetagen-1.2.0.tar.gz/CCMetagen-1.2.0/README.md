# CCMetagen

CCMetagen processes sequence alignments produced with [KMA](https://bitbucket.org/genomicepidemiology/kma), which implements the ConClave sorting scheme to achieve highly accurate read mappings. The pipeline is fast enough to use the whole NCBI nt collection as reference, facilitating the inclusion of understudied organisms, such as microbial eukaryotes, in metagenome surveys. CCMetagen produces ranked taxonomic results in user-friendly formats that are ready for publication or downstream statistical analyses.

If you this tool, please cite the CCMetagen preprint and the original KMA paper:

  * [CCMetagen, please cite: Marcelino VR, Clausen PT, Buchman J, Wille M, Iredell JR, Meyer W, Lund O, Sorrell T, Holmes EC. 2019. CCMetagen: comprehensive and accurate identification of eukaryotes and prokaryotes in metagenomic data. bioRxiv. doi: https://doi.org/10.1101/641332.](https://doi.org/10.1101/641332)

  * [Clausen PT, Aarestrup FM, Lund O. 2018. Rapid and precise alignment of raw reads against redundant databases with KMA. BMC bioinformatics. 2018 Dec;19(1):307.](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2336-6)

Besides the guidelines below, we also provide a tutorial to reproduce our metagenome clasisfication analyses of the microbiome of wild birds [here](https://github.com/vrmarcelino/CCMetagen/tree/master/tutorial).

The guidelines below will guide you in using the command-line version of the CCMetagen pipeline.

CCMetagen is also available as a web service at https://cge.cbs.dtu.dk/services/ccmetagen/.
Note that we recommend using this command-line version to analyze data exceeding 1.5Gb.

## Requirements and Installation

Make sure you have the dependencies below installed and accessible in your $PATH.
The guidelines below are for Unix systems.

  * If you do not have it already, download and install [Python 3.6](https://www.python.org/downloads/)
CCMetagen requires Python modules [pandas (>0.23)](https://pandas.pydata.org/) and [ETE3](http://etetoolkit.org/). The easiest way to install these modules is via conda or pip:

`conda install pandas`

  * You need a C-compiler and zlib development files to install KMA:

`sudo apt-get install libz-dev`

  * Download and install [KMA](https://bitbucket.org/genomicepidemiology/kma):
```
git clone https://bitbucket.org/genomicepidemiology/kma.git
cd kma && make
```

  * [Krona](https://github.com/marbl/Krona) is required for graphs. To install Krona it in the local folder:
```
wget https://github.com/marbl/Krona/releases/download/v2.7/KronaTools-2.7.tar
tar xvf KronaTools-2.7.tar 
cd  KronaTools-2.7
./install.pl --prefix . 
```

  * Then download CCMetagen and add it to your path.
If you have git:
```
git clone https://github.com/vrmarcelino/CCMetagen
```
This will download CCMetagen and the tutorial files.
You can also just download the python files from this folder (CCMetagen.py, CCMetagen_merge.py) and the ones in the ccmetagen folder if you rather avoid downloading all other files.

Then add the CCMetagen python scripts to the path, temporarily or permanently. For example:
`PATH=$PATH<your_folder>/CCMetagen`

To update CCMetagen, go to the CCMetagen folder and type: `git pull`


## Databases

**Option 1** Download the indexed (ready-to-go) nt database either [here](http://dx.doi.org/10.25910/5cc7cd40fca8e) or [here](http://www.cbs.dtu.dk/public/CGE/databases/CCMetagen/).
Download the ncbi_nt_kma.zip file (96GB zipped file, 165GB uncompressed).
Unzip the database: `unzip ncbi_nt_kma`.
This database contains the whole in NCBI nucleotide collection (of of Jan 2018), and therefore is suitable to identify a range of microorganisms, including prokaryotes and eukaryotes.

**Option 2** We have indexed a more recent version of the ncbi nucleotide collection (June 2019) that does not contain environemntal or artificial sequences. The file ncbi_nt_no_env_11jun2019.zip can be found [here](http://dx.doi.org/10.25910/5cc7cd40fca8e) and contains all ncbi nt entries excluding the descendants of environmental eukaryotes (taxid 61964), environmental prokaryotes (48479), unclassified sequences (12908) and artificial sequences (28384).

**Option 3:** Build your own reference database.
Follow the instructions in the [KMA website](https://bitbucket.org/genomicepidemiology/kma) to index the database.
It is important that taxids are incorporated in sequence headers for processing with CCMetagen.
We provide scripts to rename sequences in the nt database [here](https://github.com/vrmarcelino/CCMetagen/tree/master/benchmarking/rename_nt).

If you want to use the RefSeq database, the format is similar to the one required for Kraken. The [Opiniomics blog](http://www.opiniomics.org/building-a-kraken-database-with-new-ftp-structure-and-no-gi-numbers/) describes how to download sequences in an adequate format. Note that you still need to build the index with KMA: `kma_index -i refseq.fna -o refseq_indexed -NI -Sparse -` or `kma_index -i refseq.fna -o refseq_indexed -NI -Sparse TG` for faster analysis.


## Quick Start

  * First map sequence reads (or contigs) to the database with **KMA**.

For paired-end files:
```
kma -ipe $SAMPLE_R1 $SAMPLE_R2 -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and -apm f
```

For single-end files:
```
kma -i $SAMPLE -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and
```

If you intend to calculate abundance in reads per million (RPM), add the flag -ef (extended features:
```
kma -ipe $SAMPLE_R1 $SAMPLE_R2 -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and -apm f -ef
```

Where:

$db is the path to the reference database
$th is the number of threads
$SAMPLE_R1 is the path to the mate1 of a paired-end metagenome/metatranscriptome sample (fastq or fasta)
$SAMPLE_R2 is the path to the mate2 of a paired-end metagenome/metatranscriptome sample (fastq or fasta)
$SAMPLE is the path to a single-end metagenome/metatranscriptome file (reads or contigs)


  * Then run **CCMetagen**:
```
CCMetagen.py -i $sample_out_kma.res -o results
```
Where $sample_out_kma.res is alignment results produced by KMA.

Note that if you are running CCMetagen from the local folder (instead of adding it to your path), you may need to add 'python' before CCMetagen: `python CCMetagen.py -i $sample_out_kma.res -o results`

Done! This will make an additional quality filter and output a text file with ranked taxonomic classifications and a krona graph file for interactive visualization.

An example of the CCMetagen output can be found [here (.csv file)](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res.csv) and [here (.html file)](https://htmlpreview.github.io/?https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res.html).

<img src=tutorial/figs_tutorial/krona_photo.png width="500" height="419.64">

In the .csv file, you will find the depth (abundance) of each match. Depth can be estimated in three ways: by counting the number of nucleotides matching the reference sequence (use flag --depth_unit nc, by applying an additional correction for template length (default in KMA and CCMetagen), or by calculating depth in Reads Per Million (RPM, use flag --depth_unit rpm). If you want RPM values, you will need to suply the .mapstats file generated with KMA.

You can adjust the stringency of the taxonomic assignments by adjusting the minimum coverage (--coverage), the minimum abundance (--depth), and the minimum level of sequence similarity (--query_identity).

If you change the default depth unit, we recommend adjusting the minimum abundance (--depth) to remove taxa found in low abundance accordingly. For example, you can use -d 200 (200 nucleotides) when using --depth_unit nc, which is similar to -d 0.2 when using the default '--depth_unit kma' option. If you choose to calculate abundances in RPM, you may want to adjust the minimum abundance according to your sequence depth.
For example, to calculate abundances in RPM, and filter out all matches with less than one read per million:

```
CCMetagen.py -i $sample_out_kma.res -o results --depth_unit rpm --mapstat $sample_out_kma.mapstat --depth 1
```


**Understanding the ranked taxonomic output of CCMetagen:** The taxonomic classifications reflect the sequence similarity between query and reference sequences, according to default or user-defined similarity thresholds. For example, if a match is 97% similar to the reference sequence, the match will not get a species-level classification. If the match is 85% similar to the reference sequence, then the species, genus and family-level classifications will be 'none'.
Note that this is different from identifications tagged as unk_x (unknown taxa). These unknowns indicate taxa where higher-rank classifications have not been defined (according to the NCBI taxonomy database), and it is unrelated to sequence similarity.


For a list of options to customize your analyze, type:
```
CCMetagen.py -h
```

  * To get the abundance of each taxon, and/or summarize results for multiple samples, use **CCMetagen_merge**:
```
CCMetagen_merge.py -i $CCMetagen_out
```

Where $CCMetagen_out is the folder containing the CCMetagen taxonomic classifications.
The results must be in .csv format (default or '--mode text' output of CCMetagen), and no other csv file should be present in the folder.

The flag '-t' define the taxonomic level to merge the results. The default is species-level.

You can also filter out specific taxa, at any taxonomic level:

Use flag -kr to keep (k) or remove (r) taxa.
Use flag -l to set the taxonomic level for the filtering.
Use flag -tlist to list the taxa to keep or remove (separated by comma).

EX1: Filter out bacteria: `CCMetagen_merge.py -i $CCMetagen_out -kr r -l Kingdom -tlist Bacteria`

EX2: Filter out bacteria and Metazoa: `CCMetagen_merge.py -i $CCMetagen_out -kr r -l Kingdom -tlist Bacteria, Metazoa`

EX3: Merge results at family-level, and remove Metazoa and Viridiplantae taxa at Kingdom level:
```
CCMetagen_merge.py -i $CCMetagen_out -t Family -kr r -l Kingdom -tlist Metazoa,Viridiplantae -o family_table
```

For species-level filtering (where there is a space in taxa names), use quotation marks.
Ex 4: Keep only _Escherichia coli_ and _Candida albicans_:
```
CCMetagen_merge.py -i 05_KMetagen/ -kr k -l Species -tlist "Escherichia coli,Candida albicans"
```

If you only have one sample, you can also use CMetagen_merge to get one line per taxa.

To see all options, type:
```
CCMetagen_merge.py -h
```
This file should look like [this](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Bird_family_table_filtered.csv).

**Check out our [tutorial](https://github.com/vrmarcelino/CCMetagen/tree/master/tutorial) for an applied example of the CCMetagen pipeline.**


## FAQs

* Error taxid not found.
  You probably need to update your local ETE3 database, which contains the taxids and lineage information:
```
python
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()
quit()
```

* TypeError: concat() got an unexpected keyword argument 'sort'.
  If you get this error, please update the python module pandas:
```
pip install pandas --upgrade --user
```

* WARNING: no NCBI's taxid found for accession [something], this match will not get taxonomic ranks

  This is not an error, this is just a warning indicating that one of your query sequences matchs to a genbank record for which the NCBI taxonomic identifier (taxid) is not known. CCMetagen therefore will not be able to assign taxonomic ranks to this match, but you will still be able to see it in the output file.

* KeyError: "['Superkingdom' 'Kingdom' 'Phylum' 'Class' 'Order' 'Family' .... ] not in index"
  Make sure that the output of CCMetagen ends in '.csv'.

* The results of the CCMetagen_merge.py at different taxonomic levels do not sum up.
  As explained above, this script merges all unclassified taxa at a given taxonomic level. For example, if you have 20 matches to the genus _Candida_, but only 2 matches were classified at the species level, the output of CCMetagen_merge.py -t Species (default) will only have the abundances of two classified _Candida_ species, while the others will be merged with the "Unclassified" taxa. The output of CCMetagen_merge.py -t Genus however will contain all 20 matches. 
  If this behaviour is undesirable, one option is to disable the similarity thresholds (use flag -off) - so that all taxonomic levels are reported regardless of their similarity to the reference sequence. Alternatively, you can cluster species at the 'Closest_match' (using the flag --tax_level Closest_match).


## Complete option list

CCMetagen:
```
usage: CCMetagen.py [-h] [-m MODE] -i RES_FP [-o OUTPUT_FP]
                    [-r REFERENCE_DATABASE] [-du DEPTH_UNIT] [-map MAPSTAT]
                    [-d DEPTH] [-c COVERAGE] [-q QUERY_IDENTITY] [-p PVALUE]
                    [-st SPECIES_THRESHOLD] [-gt GENUS_THRESHOLD]
                    [-ft FAMILY_THRESHOLD] [-ot ORDER_THRESHOLD]
                    [-ct CLASS_THRESHOLD] [-pt PHYLUM_THRESHOLD]
                    [-off TURN_OFF_SIM_THRESHOLDS] [--version]

optional arguments:
  -h, --help            show this help message and exit
  
  -m MODE, --mode MODE  what do you want CCMetagen to do? Valid options are
                        'visual', 'text' or 'both': text: parses kma, filters
                        based on quality and output a text file with taxonomic
                        information and detailed mapping information visual:
                        parses kma, filters based on quality and output a
                        simplified text file and a krona html file for
                        visualization both: outputs both text and visual file
                        formats. Default = both

  -i RES_FP, --res_fp RES_FP
                        Path to the KMA result (.res file)
  -o OUTPUT_FP, --output_fp OUTPUT_FP
                        Path to the output file. Default = CCMetagen_out
  -r REFERENCE_DATABASE, --reference_database REFERENCE_DATABASE
                        Which reference database was used. Options: UNITE,
                        RefSeq or nt. Default = nt

  -du DEPTH_UNIT, --depth_unit DEPTH_UNIT
                        Desired unit for Depth(abundance) measurements.
                        Default = kma (KMA default depth, which is the number
                        of nucleotides overlapping each template, divided by
                        the lengh of the template). Alternatively, you can
                        have abundance calculated in Reads Per Million (RPM,
                        option 'rpm'), or simply count the number of
                        nucleotides overlaping the template (option 'nc'). If
                        you use the 'nc' or 'rpm' options, remember to change
                        the default --depth parameter accordingly. Valid
                        options are nc, rpm and kma
  -map MAPSTAT, --mapstat MAPSTAT
                        Path to the mapstat file produced with KMA when using
                        the -ef flag (.mapstat). Required when calculating
                        abundances in RPM.
  -d DEPTH, --depth DEPTH
                        minimum sequencing depth. Default = 0.2. If you use
                        --depth_unit nc, change this accordingly. For example,
                        -d 200 (200 nucleotides) is similar to -d 0.2 when
                        using the default '--depth_unit kma' option.

  -c COVERAGE, --coverage COVERAGE
                        Minimum coverage. Default = 20
  -q QUERY_IDENTITY, --query_identity QUERY_IDENTITY
                        Minimum query identity (Phylum level). Default = 50
  -p PVALUE, --pvalue PVALUE
                        Minimum p-value. Default = 0.05.
  -st SPECIES_THRESHOLD, --species_threshold SPECIES_THRESHOLD
                        Species-level similarity threshold. Default = 98.41
  -gt GENUS_THRESHOLD, --genus_threshold GENUS_THRESHOLD
                        Genus-level similarity threshold. Default = 96.31
  -ft FAMILY_THRESHOLD, --family_threshold FAMILY_THRESHOLD
                        Family-level similarity threshold. Default = 88.51
  -ot ORDER_THRESHOLD, --order_threshold ORDER_THRESHOLD
                        Order-level similarity threshold. Default = 81.21
  -ct CLASS_THRESHOLD, --class_threshold CLASS_THRESHOLD
                        Class-level similarity threshold. Default = 80.91
  -pt PHYLUM_THRESHOLD, --phylum_threshold PHYLUM_THRESHOLD
                        Phylum-level similarity threshold. Default = 0 - not
                        applied
  -off TURN_OFF_SIM_THRESHOLDS, --turn_off_sim_thresholds TURN_OFF_SIM_THRESHOLDS
                        Turns simularity-based filtering off. Options = y or
                        n. Default = n

  --version             show program's version number and exit
 ```

CCMetagen_merge:
 ```
usage: CCMetagen_merge.py [-h] -i INPUT_FP [-t TAX_LEVEL] [-o OUTPUT_FP]
                          [-kr KEEP_OR_REMOVE] [-l FILTERING_TAX_LEVEL]
                          [-tlist TAXA_LIST]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FP, --input_fp INPUT_FP
                        Path to the folder containing CCMetagen text results.
                        Note that files must end with ".csv" and the folder
                        should not contain other .csv files
  -t TAX_LEVEL, --tax_level TAX_LEVEL
                        Taxonomic level to merge the results. Options:
                        Closest_match (includes different genes for the same
                        species), Species (Default), Genus, Family, Order,
                        Class, Phylum, Kingdom and Superkingdom
  -o OUTPUT_FP, --output_fp OUTPUT_FP
                        Path to the output file. Default = merged_samples
  -kr KEEP_OR_REMOVE, --keep_or_remove KEEP_OR_REMOVE
                        keep or remove taxa. Options = k (keep), r (remove)
                        and n (none, default)
  -l FILTERING_TAX_LEVEL, --filtering_tax_level FILTERING_TAX_LEVEL
                        level to perform taxonomic filtering, default = none
  -tlist TAXA_LIST, --taxa_list TAXA_LIST
                        list taxon names (comma-separated) that you want to
                        keep or exclude
 ```


