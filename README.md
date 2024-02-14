# Codon-Shuffler
This was my CS50P final project. 
Welcome to Codon Shuffle or CDNSF
To unbore your DNA.

TLDR: Watch the short intro video instead: https://youtu.be/grccqGhYsBU

ToC.:

1. INTRO
2. REQUIREMENTS
3. HOW TO USE
   3.1 Number of runs
   3.2 Cut-off
   3.3 Input (file and command line)
   3.4 Codon table, species
4. REPORT
5. TROUBLE SHOOTING
5. MISC



**1. INTRO**


The purpose of Codon Shuffler is to create DNA sequences that code for repetitive aminoacid sequences but are as little repetitive on the DNA level as possible. Why is it important. Gene synthesis is a modern way to create any coding DNA of artificial genes. However, repetitions in the DNA may impair the success rate of DNA synthesis. Many genes of interest nowadays consist of multiplication (dimer, trimer or higher degree of multimer) of a protein or domain. To cretae coding DNA for trimer via syntesis, one needs a DNA design that has as little similraties as possible.

How it is done. Codon Shuffler takes an aminoacid sequence and returns up to three reverse translated DNA sequences. The first DNA is random for each codon. Te second is random from the leftover codons, and certainly different if possible. The third one is random from the leftover and again, different from the previous one if possible. If only one repeat is requetsed, then the program also considers the codon frequency. 

Some examples. Let's looke at the short example sequence

    MGCG. 
    
Let's assume the user wanted 3 DNA outputs. The program takes the first amino acid, M (Methionine). It is coded by only ATG, so each of the three outputs is started as ATG:

    Output DNA 1: ATG
    Output DNA 2: ATG
    Output DNA 3: ATG

The prgram then takes G (Glycine). It is coded by GGA, GGT, GGG and GGC. The program takes a ramdom (say, GGG) for the first DNA. Then a random from the other three (say GGC). And finally picks a random from the leftover let's sad GGA. The output now looks like:

    Output DNA 1: ATGGGG
    Output DNA 2: ATGGGC
    Output DNA 3: ATGGGA


The next aminoacid is Y (Tyrosine) coded by two codons TAT, TAC. Codon Shuffler picks one for the first DNA and the other for the second. Unfortunately the options are out so either one of them is (randomly) repeated on the third DNA. The W (Tryptophane) is even worse, having one option, TGG.

    Output DNA 1: ATGGGGTACTGG
    Output DNA 2: ATGGGCTATTGG
    Output DNA 3: ATGGGATATTGG

The program continoues this way, producing 3 different DNA outputs for the same peptide input. Note that the next Glycin (or any next aminoacid) is independent from the previous, so the codons will be added in different order. As the program uses random to reverse translate the aminoacid sequence, the outcome is different in every run. 
The user may get less versions of DNA (see chapter 3.1), discard rare codons (see chapter 3.2), chose the way of input (see chapter 3.3) or use codon frequency tables from different species (see chapter 3.4).



**2. REQUIREMENTS**

The program was written in Python 3. No extra libraries are needed as dependency, but the Python 3 itself needs to be installed. Some operating systems come with python. If you try to run the program but an error comes back such as "unknown command" or similar, then the Python 3 should be installed first. Codon Shuffler can be in any folder, but requires to have a subfolder called /codontables in its own folder. This subfolder must contain the codontables under the names of human.txt, mouse.txt and ecoli.txt in the exact format it comes with. It may also contain other txt files.
The human, mouse and ecoli files come with the program. If the files are missing or tampered with, the program will not run and/or run into an error. More on these files in the HOW TO USE chapter. The program also requires a /results folder where the results are saved and an /inputs folder too. These folders and files must be named exactly as described here.



**3. HOW TO USE**


Codon Shuffler can be used in command-line with customization options or instead, by double clicking, without customoization (a.k.a default). To use in command line, use the terminal window (called command prompt in windows) to navigate into the folder containing cdnsf.py. For example 
    
    C:/User/Documents/Codon Shuffler 

Then type in the command line:

    python cdnsf.py

Depending on your system it is possible that instead of the "python" part, "python3" should be typed. Make sure that the program file is cdnsf.py, or if it was renamed, type the new name after "python". The new name must end with the extension ".py", and cannot have white space in it (i.e. "codon shuffler.py"). After the file name, command line arguments can be added. Command line arguments can be combined and any number can be added. Codon Shuffler uses the following arguments:

    -n          Number of requested DNA. Use with a whole number of 1 or 2 or 3, such as -n 2
    -co         Cut-off. Use with a number, such as -co 10
    -i          Input file. Use with a filename such as -i example.txt or with an dash character for command line input: -i -
    -sp         Species. Use with a built-in species such as -sp mouse or a filename -sp arabidopsis.txt

Using the -h argument offers help. The arguments, except -h can be combined and used in any order. For example the following setup is valid:

    python cdnsf.py -n 2 -co 15 -sp ecoli -i myfile.txt

In this case the program will output 2 DNA sequences (-n 2), using a cut-off of 15% (-co 15), and using the E. coli built-in codon frequency table (-sp ecoli), and the peptide sequence comes from a file (-file myfile.txt). The chapters below explain all settings one by one in detail. The default values are:

    python cdnsf.py -n 3 -co 9 -sp human -i sample.txt

Arguments that are the same as default are not necessary to be typed in.
Codon shuffler generates a report file after every run (unless something causes a crashing). Some problems are expected and dealt with, such as invalid characters in the input. In such case the program still generates a report. Report files appear in the /reports folder. If this folder does not exist (i.e. deleted accidentally), no report can be generated.


*3.1 Number of runs*


    Usage by: -n, # where # is either 1, 2 or 3.
    Example: -n 3
    Default: 3, if any number but 1 to 3 is given (for example 52 or -2), the default 3 is used instead.


The main goal of Codon Shuffler is to generate as different copies of DNA as possible. The number of copies requested can be either 1, 2 or 3. If only 2 is needed, it is still recommended to use the setting 3 and use the two best options. What the program in fact does: it looks at each aminoacid in the input and randomly takes one codon for the first output and the other one for the second. Since many aminoacids have only two codons (such as Histidine: CAC or CAT), the third output will be the same as either one of the codons. If a third codon is available (shuch as Glycine that is encoded by
GGA, GGT, GGC or GGG), the third output is also guaranteed to be different. 
That however comes with a sacrifice. Usual reverse tranlation programs take into considerartion the codon usage bias that is specific for each species. For example in mouse 50% of the Isoleucines are coded by ATC, 34% is ATT and the rest (16%) is ATA. It is usually recommended, for high performance protein expression, to not overrepresent rare codons i.e. in this example do not use the ATA codon for more than 16 of all isoleucines in the target protein. Codon Shuffler however does overrepresent rare codons, because it takes, in this example, all Isoleucine codons at 33%. To counter that, it is possible to exclude the really rare codons (those with 5-6%), and the program comes with such setting options called cut-off see more anbout it in chapter 3.2.

In fact, to maximise codon variability, Codon shuffler handles every codon at the same odds. For example if an aminoacid has
4 codons (such as Glycine), then codon shuffler will take one at 25% for the first output DNA, regardless of the real codon
bias, then picks one from the remaining 3 at a probability of 33%, and finally picks from the other two at 50%. That
ensures that all three DNA is as dissimilar as possible.
In some cases an aminoacid comes with 6 codons that fall into two main categories. For example, Serine is encoded by: TCA,
TCT, TCG, TCC, AGT and AGC. The two groups are the TCN and the AGY (Y being the shortcut for T or C), in such case the
program takes the first output codon from the larger group (at equal probability among those), the second from the smaller
group, and the third from the larger again.

Codon shuffler also can be used as a simple reverse translation program for only 1 output, by using -n 1. In this case the
program will consider the codon bias and gives a random reverse translation where the codons are taken at their own odds.
I.e. with the above examples, ~50% of the Isoleucines are expected to be ~34% is expected to be ATT and the rest is ATA,
within deviation of the random generator itself.


*3.2 Cut-off.*

    Usage by: -co # where # is a number.
    Example for setting 5, type in the command line python cdnsf.py -co 5
    Default: 10
    Turn off: use -n 0

Codon Shuffler applies a cut-off to exclude rare codons, such as the Ser codon TCG that is used in many mammals only at around 5% of all Ser codons. In proetin production it is often recommended to avoid such codons (i.e use them even at lower occurance than they are used by nature or not at all) as they can be the bottleneck in terms of protein yield. To cut-off a given rare codon, a setting that is HIGHER (equal NOT included) must be used. For example to cut off codons that are as rare as 5, 6, or 7%, the setting 8 shall be used. Codons with 8% or higher occurance will not be cut off.
The program will by default apply a setting of 9 that cuts out the human TCG (ser), CTA & TTA (Leu) and CGT (Arg). To turn it off use 0 as a setting. Negative numbers will be automatically used as 0, non-numbers cause the program to run in an error and stop. Numbers larger than 21 will be automatically reset to 21. This is because in human the next setting would cut off all Arginine codons. Ir is highly not recommended though to use a setting where aminoacids are reduced to two codons, such as setting 13 in human or setting 14 in mouse where they have 2 Leucine codons left
(respectively).

The prgram handles fraction numbers so theoretically a 5.5 can be used to put a cut-off between 5% and 5.8%, but it is only there to give the program more robustness. It does not bring too much biological sense.


*3.2.1 About cut-off settings*


The table below lists which setting will cause which codon, in mouse, human or E. coli, are excluded as they do not make the cut-off. The format of the table is as follows. The leftmost number is the setting. For example at setting 8, the human column lists
    
    7.9 Leu TTA (4 left)
    
In this example **7.9** means the actual usage percentage of that codon, followed by the 3-letter code of the amoniacid (**Leu**) and which exact codon (**TTA**) excluded by this setting. And finally a detail on how many codons of the given aminoacid are still there at this setting. Please note that at every setting the previous numbers are cut off too.

There is a trade-off between using "good" or frequent codons, and resulting as highly shuffled results as possible. To my experience sticking with only the good codons can result in DNA that is too repetitive for synthesis. It is not reecommended to use cut-off settings where an aminoacid that originally had more than two codon options, is reduced to two or less, as this reduces the DNA versatility. (Note that many aminoacids alread come with only 1 or 2 options that can reduce versatility of some regions alredy.) If the human codon table is used, the first occurance of such case is cut-off of 13, where Leu is reduced to two codons.

I also recommend to keep in mind the excluded codons, and hand-edit them back in a targeted, low occurance way if the resulting DNA is too difficult for syntesis. Or, re-run the program at a lower setting of cut-off. Please note that aminoacid clusters high in Trp and Met will always be difficult to produce in a dimer or trimer, as tehese aminoacids have only 1 codon each.


    Setting           human                      mouse                            E. coli
    --------------------------------------------------------------------------------------------------
     4                                                                       4.0 Leu CTA (5 left)    |
                                                                             3.0 Arg AGG (5 left)    |
     6        5.0 Ser TCG (5 left)          5.0 Ser (5 left)                 5.0 Arg AGA (4 left)    |
     7        6.9 Leu CTA (5 left)                                                                    \ DEFAULT
     8        7.9 Leu TTA (4 left)          7.0 Leu TTA (5 left)             7.0 Arg CGA (7.0)        / SETTING
     9        8.1 Arg CGT (5 left)          8.0 Leu CTA (4  left)                                    |
                                            8.0 Arg CGT (5 left)                                     |
    --------------------------------------------------------------------------------------------------
    10                                      9.1 Ala GCG (3 left)             9.1 Ile ATA (2 left)
    11      10.9 Ala GCG (3 left)          10.0 Pro CCG (3 left)            10.0 Leu CTC (4 left)
                                           10.1 Thr ACG (3 left)
    12      11.0 Pro CCG (3 left)                                           11.0 Leu CTT (3 left)
            11.1 Arg CGA (4 left)                                           11.1 Arg CGG (3 left)
            11.0 Thr ACG (3 left)
    13      12.8 Leu TTG, CTT (2 left)     12.0 Arg CGA (4 left)            12.0 Gly GGA (3 left)
            12.0 Val GTA (3 left)
    14                                     13.0 Leu TTG, CTT (2 left)       13.0 Leu TTA, TTG (1 left)
                                                                            13.0 Pro CCC (3 left)
                                                                            13.8 Ser TCT, TCA (4 left)
    15                                     14.0 Ser TCA (3 left)            14.8 Ser TCC, TCG (2 left)
    16      15.0 Ser AGT, TCA (3 left)     16.0 Ser AGT (2 left)            15.8 Ser AGT (1 left)
                                                                            15.0 Thr ACA (3 left)
    17      16.0 Gly GGT (3 left)                                           16.0 Ala GCT (3 left)
                                                                            16.0 Gly GGG (2 left)
                                                                            16.0 Val GTA (3 left)
    18      17.0 Ile ATA (2 left)          17.0 Ile ATA (2 left)            17.0 Thr ACT (2 left)
                                           17.0 Arg CGC (3 left)
                                           17.0 GTT (2 left)
    19      18.2 Arg CGC (3 left)          18.0 Gly GGT (3 left)
            18.0 Val (2 left)
    20      19.0 Ser TCT (2 left)          19.0 Arg CGG (2 left)            19.0 Pro CCG (1 left)
    21      20.2 Arg CGG (2 left)          20.0 Leu CTC (1 left)
                                           20.0 Ser TCT (2 left)
    -----------------------------------------------------------------------------------------------> MAX
    22      21.2 Arg AGA, AGG (none left)




*3.3 Input.*

Codon shuffler requires a peptid as input to be reverse translated. The peptide must come as plain text, using the single-letter aminoacid codes. The peptide sequence can either be copied in command line or can be a file. Allowed characters: single-letter amino acids according to IUPAC (https://iupac.qmul.ac.uk/AminoAcid/A2021.html) except U, X, or Z. The input is case-insensitive (lower case or upper case equally okay, such as a, A, t, T, q, Q). Use asterisk (*) for stop. 

Do not use other letters such as ambiguos or non-aminoacids (Z, X, B, etc), missing aminoacids ( _ ), or any other stop character but asterisk. The program filters for wild space and line end characters, but other (even invisible) characters will stop it from running. If such characters are included, a report file is generated with the run details, including all input and the found non-peptide caharacters. Note that sequences copied from a word or other rich dext editor may contain characters that look like a normal space but they are not. Such characters may close the program to report invalid characters. See more on reports later, and check the trouble shooting in case if anything like that happens.


_3.3.1 File input_


    Usage by: -i xxxx.txt + where xxxx.txt is an existing raw text file.
    Example: -i my_input.txt

The default input method is reading data from the /inputs/input.txt file. This being default, the program can be run with double clicking, with every other parameters being default: **"-n 3", "-co 9" and "-sp human"**. To use the program this way, the content of input.txt must be updated before each run. (The file comes as an empty txt with the program, for a test please copy over the content of example.txt which contains the sequence of GFP.) It is also possible to run Codon Shuffler using different input files, but for that the program must be started from command line. If doing so, the -i argument and the file name must be given. The input file is first searched in the /inputs subfolder, and if any matching file, it is used. If not, the program tries to look for it in its own folder. If it is still unsuccessful, a report is generated and the program exits.

**IMPORTANT.** If started from command line, a file name cannot have a space character in it, or if it has, it must be sourrounded by quotation marks. I.e. My File.txt is not valid, but "My File.txt" is valid. Quotation marks and apostrophes cannot be in the file name at all. It is not a restriction of Codon Shuffler, but a restriction of command line in general. 

The input file can be fasta format or just the plain sequence. (More on fasta format: https://en.wikipedia.org/wiki/FASTA_format#Overview) Although empty lines are disregarded, the program does not support multiple peptide sequences in one file. If there are multiple sequences without separator, Codon Shuffler will concatenate them and handle as a single sequence (deleting any empty lines in between). A multiple fasta file with ">" symbols will cause an error but a report will be generated telling that ">" symbols were found. The drawings below illustrate the input, the lines are representing the text editor window.

An illustration of a fasta file how it shall look (the lines represent the text editor window.) Lower or upper-case letters can be mixed.

    _________________________________________________
    |>GFP #1.1 as from Dr Doe                               <==== This is the fasta header or title .
    |SKGEELFTGVVPILVELdgdVNGHKFSVSGEGEGDATYGKL                    line. Without the ">" symbol it 
    |TLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDF                    causes an error
    |FKSAMPEGYVqert*
    |
    |
    |


An example for WRONG input, it is missing the > symbol. Will cause an error. In case if there were no other symbols or numbers (#1.1 in this example),
the prgram will try to reverse translate the name of the protein, in this case "GFP" as aminoacids. It may lead to an error in the resulting DNA.
______________________________________________
|GFP #1.1                                               <==== Without the ">" symbol, the non-peptide characters (#, 1 and .) cause an error.
|SKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKL
|TLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDF
|FKSAMPEGYVQERT
|
|
|          WRONG!!!
|


A sequence without title line is also possible:
____________________________________________
|SKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKL
|TLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDF
|FKSAMPEGYVQERT
|
|
|


Several sequences separated by whitespaces or new lines will be merged as one:
____________________________________________
|SKGEELFTGVVPILVELDGDV
|
|
|NGHKFS VSGEGE GDATYGKL     TLKFICTTGKLPVPWPT          <====  Merged all as SKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPT
|                                                             Note that as a consequence, any intended name that comes without the ">"
|                                                             symbol but has only peptide letters (such as GFP, rDrP etc) will be
|                                                             reverse translated as if peptide.


Numbers will cause an error.

____________________________________________
|     5    10    15    20    25                        <==== Numbers cause an error.
|SKGEEL FTGVV PILVE LDGDV NGHKF
|
|
|          WRONG!!!
|
|


Sequences with non-aminoacid letters (B, X, etc), or any symbol other than * will cause an error.
A fasta separator is also not supported.
________________________________________________
|SKGEEL__GVVPILVELDGDVNGHKFSVSGEGEGDATYgklXXX
|TLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDF
|FKSAMPEGYVQERT.                                        <==== A report will be generated listing all invalid characters. a ">" is invalid
|                                                             except for the first line, very first character.
|>another fasta peptide
|MTGGDASSEGPPRG
|
|
|          WRONG!!!
|
|


If a wrong input is given, the program generates a report with the cause (such as all the bad characters found) and stops running.




        3.3.2 Command line input


Usage by: -i - (dash)
Default: file input from sample.txt

If ran in this mode, Codon Shuffler asks for an input in the command line unless a file is specified in command line argument.
Once the program is started this way, a message will appear on the command line:



Please paste your input peptide below and press enter. Add more peptides, or press enter in the empty line to stop.
Sequence:


Once a peptide sequence is placed and enter is pressed, the "Sequence: " message reappears until an enter is pressed without input.
Then a message appers "End of  collecting sequences." All inputs are merged together. This allows the user to copy-paste peptide
from different sources or in small pieces. Otherwise the same restictions apply as above.
While doing the command line input, one must make sure that there is no newline character (aka multiple lines) in the sequence,
as it may cause the loss of everything after the first line.

Once all sequenes are entered, the program runs and saves a report in the /reports folder.



                3.4 Codon tables, species



Usage by: -sp species (Where species is coming from the built-in list: human, mouse, ecoli, or a custom one as my_species.txt)
Example: -sp ecoli
Default: human


Codon usage frequencies (biases) depend on the species. It is usually recommended to use the codon choice of the organism in
which a protein will be expressed (regardless of the origin species). Therefore a protein that is intended to be expressed in
E. coli, should avoid the CTA codon of leucine because this codon codes 4% of all leucines in E. coli. In many cases the the
corresponding tRNA is also rare (in terms of concentration compared to the other codons), thus overusing a codon like that may
deplete the tRNA and stall the protein synthesis.
Codon Shuffler comes with 3 built-in species but more can be added. If used by clicking, the default human table will be used.
These three built-in species are represented by the files human.txt, mouse.txt and ecoli.txt. For the program to run correctly,
the files must be formatted as they come. If there is a doubt that the values are tampered with, please re-download the files.
If there are already custom added codon tables, they can be used by typing the FULL NAME of the file after the -sp argument,
such as:  -sp my_new_species.txt  Note that with custom species the file extension (such as txt) must be added while with the
built-ins, only the species (e.g. human).
A codon table is essential for the program to run. If the one given by the user is not found, a re-prompt appears. It comes until
a valid file is given or the user just types in a letter x and presses enter. In the latter case, the program exits.

Some important notes.

The codon tables used by the program contain the codons in RNA letters (U instead of T). The exact same format but with DNA letters
can also be used. The output is going to be DNA letters either way.

The codon tables store the codon percentage values in ratio format, so instead of 14% it is 0.14, or instead of 50% it is 0.50 and so
on. Codon shuffler converts and uses percrentages instead.

The sum of codon usage for any given aminoacid should be 1 or 100%. Due to rounding errors, in some cases, it is not exactly 100%.
For example the human Alanine has values of 0.27, 0.40, 0.23 and 0.11, which is 1.01 or 101%. Codon shuffler re-calculates the values
so it is now 100%, but it means that some aminoacids have sligthly different values than in the codon table. Hence, the GCG codon
for Alanine is 10.9 instead of 11, and that affects codon cut-off, as at setting 11 this is now cut off while 11 would not be.


        3.4.1 Adding more codon tables

Codon usage frequencies are measured, and stored in databases. The database used for Codon Shuffler is http://www.kazusa.or.jp
For example the human codon usage is copied over from: http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=9606&aa=1&style=N
At the time of release, Codon Shuffler comes with 3 built-in codon table choices but any number may be added. Here is how:

First go to http://www.kazusa.or.jp and search for your species of interest. Some species are listed as common name, but most of
them are with the Latin name. The result will be a list like the follwing (example search: Homo sapiens):


_______________________________________________________________________________
Answer for your query "Homo sapiens" (case: insensitive search).

mitochondrion Homo sapiens [gbpri]: 31745
Homo sapiens [gbpri]: 93487
_______________________________________________________________________________


Note that the list may contain organelles or parasites of the target species. Click on the correct one. Some lists may be long,
containing many versions and strains:

_______________________________________________________________________________
Answer for your query "Escherichia coli" (case: sensitive search).
Escherichia coli O157:H7 EDL933 [gbbct]: 5347
Escherichia coli O127:H6 [gbbct]: 1
Escherichia coli O111:H- [gbbct]: 7
Escherichia coli O157:H- [gbbct]: 34
Escherichia coli phage EH297 [gbphg]: 2                 <===== THIS IS A PHAGE OF E. COLI
Escherichia coli CFT073 [gbbct]: 5379
Escherichia coli O157:H45 [gbbct]: 4
Escherichia coli O55:H51 [gbbct]: 1                     <===== DO NOT USE ANY WITH A LOW NUMBER
Escherichia coli O26:H11 [gbbct]: 9
Escherichia coli O63:H6 [gbbct]: 1
Escherichia coli O153:H21 [gbbct]: 2
Escherichia coli EAEC 042 [gbbct]: 4
Escherichia coli W3110 [gbbct]: 4332
Escherichia coli Nissle 1917 [gbbct]: 199
Escherichia coli O63:HNM [gbbct]: 2
Escherichia coli 536 [gbbct]: 4629
Escherichia coli UTI89 [gbbct]: 5211
[...]
_______________________________________________________________________________


Notice the number at the end of each line. For the human above, it was 93487. In some E. coli strains it is above 4-5000, but in
many cases it is just a few. The number means the number of coding sequences analized. The lower the number is, the less reliable
the data becomes. At a number of 1 or 2, some codons are not even captured, and there will be gaps such as "ACG T 0.00  0.0 (     0)"
It would lead Codon Shuffler to skip that codon entirely. As distorted data will lead to distorted results, DO NOT USE
data from species where there wer not at least a few thousands of coding sequences analyzed.

Once found the species of interest, a preliminary table is shown. This is not the correct table yet. For human, here is how the
first couple of line would look. Note that the aminoacid names are missing.

_______________________________________________________________________________
Homo sapiens [gbpri]: 93487 CDS's (40662582 codons)
fields: [triplet] [frequency: per thousand] ([number])

UUU 17.6(714298)  UCU 15.2(618711)  UAU 12.2(495699)  UGU 10.6(430311)
UUC 20.3(824692)  UCC 17.7(718892)  UAC 15.3(622407)  UGC 12.6(513028)
UUA  7.7(311881)  UCA 12.2(496448)  UAA  1.0( 40285)  UGA  1.6( 63237)
UUG 12.9(525688)  UCG  4.4(179419)  UAG  0.8( 32109)  UGG 13.2(535595)
_______________________________________________________________________________


To get the correct table go down below the preliminary table and find the dopdown menu below the word "Format:", written "SELECT A CODE"

                        Format:
     THIS ====>        [SELECT A CODE ˇ]  Genetic codes (NCBI)

From this menu, select the 1st option "1: STANDARD" and click the SUBMIT button below. In the browser search bar, the address will change
like this (human example):



http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=9606&aa=1&style=N

|--------------------------------------------------|------------|-----------|
      base part, always the same                 your species ID    THIS must be exactly as is:   &aa=1&style=N

You must see the exact same link, except the species ID (1 to 6 digits) will change. Here is the correct table for E. coli, notice the ID
is 199310 instead of 9606, but the rest is the same:

http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=199310&aa=1&style=N


When looking up the correct codon usage table at kazusa.or.jp, this is the output format. There is a header with species info. The actual
data you need to copy over starts with "UUU F 0.# #.# (#####)"  (where # means numbers), and ends with GGG G 0.# #.# (#####). Example:

__________________________________________________________________________________________________________________________________
                                                                                                                      \
Homo sapiens [gbpri]: 93487 CDS's (40662582 codons)                                                                    >  DO NOT COPY
fields: [triplet] [amino acid] [fraction] [frequency: per thousand] ([number])                                        /

                                                                                                                     __
UUU F 0.46 17.6 (714298)  UCU S 0.19 15.2 (618711)  UAU Y 0.44 12.2 (495699)  UGU C 0.46 10.6 (430311)                 \
UUC F 0.54 20.3 (824692)  UCC S 0.22 17.7 (718892)  UAC Y 0.56 15.3 (622407)  UGC C 0.54 12.6 (513028)                  |
UUA L 0.08  7.7 (311881)  UCA S 0.15 12.2 (496448)  UAA * 0.30  1.0 ( 40285)  UGA * 0.47  1.6 ( 63237)                  |
UUG L 0.13 12.9 (525688)  UCG S 0.05  4.4 (179419)  UAG * 0.24  0.8 ( 32109)  UGG W 1.00 13.2 (535595)                  |
                                                                                                                        |
CUU L 0.13 13.2 (536515)  CCU P 0.29 17.5 (713233)  CAU H 0.42 10.9 (441711)  CGU R 0.08  4.5 (184609)                  |
CUC L 0.20 19.6 (796638)  CCC P 0.32 19.8 (804620)  CAC H 0.58 15.1 (613713)  CGC R 0.18 10.4 (423516)                  |
CUA L 0.07  7.2 (290751)  CCA P 0.28 16.9 (688038)  CAA Q 0.27 12.3 (501911)  CGA R 0.11  6.2 (250760)                   \
CUG L 0.40 39.6 (1611801)  CCG P 0.11  6.9 (281570)  CAG Q 0.73 34.2 (1391973)  CGG R 0.20 11.4 (464485)                  \  Copy only
                                                                                                                          /  this part
AUU I 0.36 16.0 (650473)  ACU T 0.25 13.1 (533609)  AAU N 0.47 17.0 (689701)  AGU S 0.15 12.1 (493429)                   /
AUC I 0.47 20.8 (846466)  ACC T 0.36 18.9 (768147)  AAC N 0.53 19.1 (776603)  AGC S 0.24 19.5 (791383)                  |
AUA I 0.17  7.5 (304565)  ACA T 0.28 15.1 (614523)  AAA K 0.43 24.4 (993621)  AGA R 0.21 12.2 (494682)                  |
AUG M 1.00 22.0 (896005)  ACG T 0.11  6.1 (246105)  AAG K 0.57 31.9 (1295568)  AGG R 0.21 12.0 (486463)                 |
                                                                                                                        |
GUU V 0.18 11.0 (448607)  GCU A 0.27 18.4 (750096)  GAU D 0.46 21.8 (885429)  GGU G 0.16 10.8 (437126)                  |
GUC V 0.24 14.5 (588138)  GCC A 0.40 27.7 (1127679)  GAC D 0.54 25.1 (1020595)  GGC G 0.34 22.2 (903565)                |
GUA V 0.12  7.1 (287712)  GCA A 0.23 15.8 (643471)  GAA E 0.42 29.0 (1177632)  GGA G 0.25 16.5 (669873)                 |
GUG V 0.46 28.1 (1143534)  GCG A 0.11  7.4 (299495)  GAG E 0.58 39.6 (1609975)  GGG G 0.25 16.5 (669768)              __/

                                                                                                                       \
Coding GC 52.27% 1st letter GC 55.72% 2nd letter GC 42.54% 3rd letter GC 58.55%                                         >  DO NOT COPY
Genetic code 1: Standard                                                                                               /
__________________________________________________________________________________________________________________________________


The codon usage data then must be saved as txt file into the /codontables subfolder. In the file name it is  recommended to use
only alphanumeric characters (including underscore _). Command lines usually do not support names with multiple words (i.e. space in it)
or characters such as # or <. Since you run your newly added species from command line, it is probably the best to have a simple name
like ara.txt for Arabidopsis. Once the new species is saved, you have access to the codon table by running Codon Shuffler from
command line by adding the argument such as -sp ara.txt or whatever the file name is.




                        4. REPORT


Codon Shuffler generates a report after every run and saves it the results folder. If the folder is missing (deleted accidentally),
the report is not generated and lost. In this case just create a report folder and re-run the program.

The name of the report is generated automatically, using the date (YYYY_MM_DD), followed by the time HH_MM_SS_ssssss, to the milliesconds
punctuality. This ensures unique name at all times, so the previous reports are safe from being overwritten.
The filename therefore looks like: 2024_02_12_10_55_50_870895.txt

The general layout of the report is as follows. (The lines arount the text represent the edge of the text window.)


______________________________________________________________________
|Codons Shuffler cdnsf.py report.
|File name: 2024_02_12_10_55_50_870895.txt.
|
|Report sequence(s) for 3 semi-randomly generated DNA sequences.
|                                                                       <====== Base data with the run parameters (such as cut-off used etc.)
|
|Cut-off: 0.0. Species of codon table: ecoli.
|
|============== Input peptide: ==============
|
|>Test123                              <====== The name of the sequence if a fasta was given
|GGAHALALALTTTMAA                      <====== The peptide sequence
|
|
|
|============== Output DNA(s): ==============
|
|>Seq1:
|GGGGGCGCACATGCACTTGCGCTTGCTCTAACTACCACAATGGCA
|
|>Seq2:
|GGCGGGGCGCACGCCTTGGCGTTGGCATTAACAACTACCATGGCT               <====== 1, 2, or 3 DNA output sequences.
|
|>Seq3:
|GGAGGGGCCCATGCTCTCGCACTAGCCCTTACTACAACCATGGCG
|
|
|__________________________________________________________________



There are a few possible errors that the program will name in the output (and there is no DNA showing up). These can be:
missing input file, empty input file or invalid characters in the input.


                4.1 Input problems

If either the specified file is missing or it has no data, the report will contain this, in the place of the input peptide:



============== Input peptide: ==============

<<Empty input.>>



If the input contains invalid characters, the report will show this:




============== Input peptide: ==============

>Test123
GG_AHA_LALALTTxTMA.X

The following non-peptide letters were found (may be invisible characters):
This: _. This: x. This: .. This: X.


Each wrong input character comes after the word This: and followed by a full stop. Therefore in the example above it is easy to see
that the program found underscore (_), dot (.), lower case x, and upper case X. If an invisible character caused trouble,
it would look like an empty sentence, such as "This:  . It may happen if the input was copied from a word document that had non standard
space characters or similar invisible characters. This can be avoided if the input comes from a raw text file.
Note that symbols are listed only once per kind (regardless of their actual amount) and not necessarily in their order of appearance.



                        5. TROUBLE SHOOTING

NOTE: If nothing helps, please download Codon Shuffler again, or contact me: https://www.linkedin.com/in/peterhorvath82/


Issue                                   Try this

The program crashes with weird,         1. The codon table may be corrupt: download it again.
cryptic message containing words        2. The program code was edited: download it again.
like ValueError, IndexError etc.        3. You managed to do something I never thought of: contact me.

The program stops with message like     1. The command line arguments must be the exact type of value they
"error: argument, invalid int value"       designed for. I.e. -n and -co must be a number, if it is not given
                                           a number, the program stops running.

I can't find a report.                  1. The report is saved in the subfolder /results, if this is
                                           deleted, no report is saved. Create the folder with this exact name.
                                        2. Try to re-order the files by name. Depending on the order,
                                           the newest one is either top or bottom. It should be there.
                                           The name is however based on the date-time setting of your
                                           computer, check if it is off.

I get an "empty input" in the           1. Make sure the name of the input file is correctly given.
report.                                    The full, exact name of the file must be used "my_file.txt".
                                           If your file has upper case letters, type it that way.
                                        2. The input file is first searched in the /inputs subfolder,
                                           THEN in the actual folder where the program is.
                                           If there is a file with the same /inputs without input,
                                           it may stop the program looking further.
                                           Files placed elswhere are not found at all.

The program keeps asking me for         1. The species files must be in the codontables subfolder, named
species. I keep saying human /             exactly as human.txt, mouse.txt, ecoli.txt. If the folder or
mosue / ecoli.                             the file is renamed or moved, the program keeps asking for it.
                                           Move and name back everything or download it all again.
                                           Your own files must be given with the full name (file.txt).

The program does not start.             1. The program needs the python3 running environment. Some
                                           computers come with it already, some computers may need
                                           to install it first. https://www.python.org/downloads/
                                        2. Maybe the program was renamed on your computer. If someone
                                           renamed cdnsf.py to sor example codon.py, then you must
                                           use the name as it is now (codon.py). The rest remains the
                                           same.

How do I know it does not have          1. Codon shuffler is open source program, you can even look
a virus?                                   into the code yourself. Ask someone who can read it. :)

I think I type everything correctly     1. Note that in command line the space separates the values.
yet I get error message.                   do not use commas, or double space. Do not use file names
                                           containing space (i.e. my file.txt). In such case the
                                           command line will try to take the "my" part as file.
                                        2. If in your country numbers use commas (like 1,5),
                                           use dot instead (1.5).
                                        3. Do not use non-english characters such as é or ł.

A codon is not cut off at the           1. If you look at the codon usage table and see, for example,
-co setting where it should be.            a codon usage of 0.10 meaning 10%, it is possible that
Or the other way round.                    Codon shuffler has a value of 11% for it. The reson is
                                           that often the values do not add up to 100% due to rounding
                                           errors. The program recalculates all values so it is now 100%
                                           It may result in some values to go up or down a little. Try a
                                           slightly different setting.



5. MISC

CDNSF aka Codon Shuffler can be used free of charge under the licence of Creative Commons licence at the users own responsibility.
It can be used in for-profit organisations but cannot be sold on its own, modified or unmodified, alone or as a part of a package
or paid service. This and all the legalese about the license is described here https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1
The author does not take responsibility for any damage (incl. misinterpreted or misused biological data). The user always must
ensure that the result fits their needs and any result shall be confirmed (such as translated back to the original peptide).

The author welcomes any ideas to improve, add, change and it may or may not be implemented in the future.

Please find me at https://www.linkedin.com/in/peterhorvath82/
Maybe there are other codes of mine at my github: https://github.com/CCNCAY/
