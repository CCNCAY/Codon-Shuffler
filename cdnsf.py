#last update 13-02-2024

import random
import argparse
import datetime
import sys
import re
import os


DEFAULT_CUTOFF = 9
RECOMMENDED_MAX_CUTOFF = 13
TOP_CUTOFF = 21
DEFAULT_SP = "human"
DEFAULT_N = 3
DEFAULT_I = "sample.txt"

#These are all the prompt and help messages.
messages = {"exit": "Exiting with user command.",
            "file_not_found":"File not found. Try another one [human, mouse, ecoli] or press x to exit program: ",
            "argparser" : "Creates reverse translation DNA of protein in 1 to 3 versions.",
            "help-n": "Number of DNA versions. Default is 3.",
            "help-sp": "Species for codon usage. Default: human, built-in options: mouse, ecoli. To add custom, check readme.txt",
            "help-co":"Cut-off percentage of codon usage (excluding codons below). Default: 9. Turn off: 0. Not recommended above 13. Anything above 21 is reset to 21.",
            "help-i":"The program reads the input from file (default: sample.txt). Tries first in samples/ folder an then in its own. Use -i - for command line input."
            }

#Parsing the command line arguments.
parser = argparse.ArgumentParser(description=messages["argparser"])
parser.add_argument("-n", default=DEFAULT_N, help=messages["help-n"], type=int)
parser.add_argument("-sp", default=DEFAULT_SP, help=messages["help-sp"], type=str)
parser.add_argument("-co", default=DEFAULT_CUTOFF, help= messages["help-co"], type=float)
parser.add_argument("-i", default=DEFAULT_I, help= messages["help-i"], type=str)
args = parser.parse_args()


#--------------------------------- Class definitions ---------------------------------------------


class Aminoacid():
    """
    A class to create an aminoacid and its codon distributions. A codon distribution is the percentage of different codons coding that aminoacid.
    The distributions are read from file during the program run, processed and given in a form of dictionary such as:
    {codon1: x%, codon2: y%, etc}. Inside the class there is a cutoff method that discards percentages below the treshold defined by the cutoff paramater,
    and actualizes the distribution accordingly so that the leftovers new value is adjusted to total of 1.
    """

    def __init__(self, name, distribution, cutoff):
        self.name = name
        self.distribution = distribution
        self.cutoff = cutoff
        self.distribution = self.reset_distribution()
        self.codons = self.get_codons()
        self.flag = self.set_flag()
        self.codon_subsets = self.set_codon_subsets()

    def __str__(self):
        return f"Aminoacid {self.name}"

    def get_name(self):
        return self.name

    def get_distribution(self):
        return self.distribution

    def get_cutoff(self):
        return self.cutoff

    def reset_distribution(self):
        int_dict = self.distribution.copy()
        for codon in int_dict:
            if int_dict[codon] < self.cutoff:
                self.distribution.pop(codon)
        total_values = 0
        for codon in self.distribution:
            total_values += self.distribution[codon]
        for codon in self.distribution:
            self.distribution[codon] *= 100/total_values
        return self.distribution

    def get_codons(self):
        codon_list = list(self.distribution.keys())
        return codon_list


    def set_flag(self):
        if len(self.codons) > 3:
            for i in range(len(self.codons[1:])):
                if self.codons[0][0] != self.codons[i][0]:
                    return True
        return False

    def set_codon_subsets(self):
        out = [[],[]]
        if self.flag:
            for i in range(len(self.codons)):
                if self.codons[0][0] == self.codons[i][0]:
                    out[0].append(self.codons[i])
                else:
                    out[1].append(self.codons[i])
            return out
        else:
            return False


#----------------------------- function definitions except main() ---------------------------------
#-- base functions (setters, file openers)  --

def command_input():
    """
    Continues to take input in command line until the user stops it.
    """
    out =["Command line input.",""]
    while True:
        print("Please paste your input peptide below and press enter. Add more peptides, or press enter in the empty line to stop.")
        new = input("Sequence: ")
        if new:
            out[1] += new.replace(" ", "")
        else:
            print("End of  collecting sequences.")
            return out


def file_input(filename):
    """
    Tries to open a file first in /inputs then in the own folder.
    Tested on mac and win.
    """
    out = ["", ""]
    try:
        with open(os.path.join("./inputs", filename)) as in_file:

            # open(f"/inputs/{filename}", "r") as in_file:
            for line in in_file:
                out[1] += line.replace(" ", "")
    except FileNotFoundError:
        try:
            with open(os.path.join("./", filename)) as in_file:
                for line in in_file:
                    out[1] += line.replace(" ", "")
        except FileNotFoundError:
            return False
    if out[1]:
        temp_lines = out[1].split("\n")
        if temp_lines[0].startswith(">"):
            out[0] += temp_lines[0]
            temp_lines = temp_lines[1:]
        out[1] = ""
        for l in temp_lines:
            out[1] += l
    return out


def write_report(report, timestamp):
    """
    Generates output file in result subfolder using the second (planned as a timestamp) string as file name.
    """
    with open(f"results/{timestamp}.txt", "w") as out_file:
        for line in report:
            out_file.write(line)

def set_source(source):
    """
    This returns the source of the codon tables. Either the built-ins or added by user.
    """
    if source in ["human", "mouse", "ecoli"]:
        return f"{source}.txt"
    else:
        return f"{source}"

def set_number(n):
    """
    Returns the number given if it is 1/2/3 or 3 if it is either. Returns 3 even if the user gives a non-number.
    """
    if n in [1,2,3]:
        return n
    else:
        return 3

def set_cutoff(n):
    if float(n) > TOP_CUTOFF:
        return float(21)
    else:
        return float(n)


def source_opener(source):
    out = []
    prompt = ""
    while prompt != "x":
        try:
            with open(os.path.join("./codonatbles", source)) as source_file:
                     #open(source, "r") as source_file:
                for line in source_file:
                    out.append(line)
            return out
        except FileNotFoundError:
            prompt = input(messages["file_not_found"]).lower()
            source = set_source(prompt)
    sys.exit(messages["exit"])


#-- Functions to handle input file format and build up internal datasets--


def base_data_parser(codon, aa, ratio,):
    """
    This is a helper function for line_parser and eventually all_codon_parser.
    """
    return {aa:{codon:float(ratio)*100}}

def line_parser(line):
    """
    This is a helper function for all_codon_parser.
    """
    finds = re.findall(r"(?:([A-Z]{3}) +([A-Z]|\*) +(\d\.\d{1,2}) )", line)
    out = []
    for base_data in finds:
        out.append( base_data_parser(*base_data))
    return out

def all_codon_parser(codon_table):
    """
    Hard coded all aminoacid letters. Handles the aminoacid codons and their codon frequencies.
    Otput is all the 20+1 aminoacid (+ stop) objects.
    Assumes that the input is formatted in the strict way of kazusa.or.jp
    """
    all_aminoacids = {"A":{}, "C":{}, "D":{}, "E":{},
                      "F": {}, "G":{}, "H":{}, "I":{},
                      "K" :{}, "L": {}, "M":{}, "N":{},
                      "P":{}, "Q":{}, "R": {}, "S": {},
                      "T": {}, "V": {}, "W": {}, "Y": {}, "*": {}}
    all_codons = []
    for line in codon_table:
        if line != "\n":
            all_codons.append(line_parser(line))
    for four_set in all_codons:                     #ex. [{"A":{"TTT": 25}}, {{}}, , , 4x]
        for aa_dict in four_set:                    #ex. {"A":{"TTT": 25}}
            for aa_key in aa_dict:                  #ex. "A" >> {"TTT": 25}
                 for codon in (aa_dict[aa_key]):    #ex. "TTT"  >>> 25
                     all_aminoacids[aa_key][codon] = aa_dict[aa_key][codon]
    return all_aminoacids




def sorter(aminoacid, n):
    """
    This is a complicated one because biology is weird. Param n is the required output number, 1, 2 or 3.
    n==1 is essentially different from 2 and 3, and is basically just a reverese translation that accounts for
    codon frquency.
    An aminoacid can have any number of coding codons from 1 to 6. If it has more than 4, then they necessarily
    fall in 2 goups. If n==2 or 3, frequencies matter less than shuffling, therefore different frequencies
    are disregarded and all have the same schance to be added to the DNA output.
    Some aminoacids are flagged for having two main groups of codons. These are handled separately ensuring that
    both groups are represented instead of just any 3 codons (which may mean 3 similar codons).
    """
    dist = aminoacid.distribution
    rnd = random.randint(0,100)
    if n == 1:
        sum = 0.0
        for codon in dist:
            if rnd <= sum+dist[codon]:
                return [codon]
            else:
                sum += dist[codon]
        return list(codon)
    codonlist = aminoacid.codons.copy()
    if len (codonlist) == 1:
        if n == 2:
            return [codonlist[0], codonlist[0]]
        else:
            return [codonlist[0], codonlist[0], codonlist[0]]
    elif len(codonlist) == 2:
        flip = random.randint(0,1)
        if n == 2:
            return [codonlist[flip], codonlist[1-flip]]
        else:
            reflip = random.randint(0,1)
            return [codonlist[flip], codonlist[1-flip], codonlist[reflip]]
    elif aminoacid.flag:
        if len(aminoacid.codon_subsets[0]) > len(aminoacid.codon_subsets[1]):
            codonlist0 = aminoacid.codon_subsets[0].copy()
            codonlist1 = aminoacid.codon_subsets[1].copy()
        else:
            codonlist0 = aminoacid.codon_subsets[1].copy()
            codonlist1 = aminoacid.codon_subsets[0].copy()
        random.shuffle(codonlist0)
        random.shuffle(codonlist1)
        if n == 2:
            return [codonlist0[0], codonlist1[0]]
        else:
            return [codonlist0[0], codonlist1[0], codonlist0[1]]
    else:
        random.shuffle(codonlist)
        if n == 2:
            return [codonlist[0], codonlist[1]]
        else:
            return [codonlist[0], codonlist[1], codonlist[2]]

def u_to_t(rna_seq):
    out = ""
    for letter in rna_seq.upper():
        if letter == "U":
            out += "T"
        else:
            out += letter
    return out


def aa_letter_check(input):
    out = set()
    for aa in input:
        if aa.upper() not in "ACDEFGHIJKLMNPQRSTVWYZ*":
            out.add(aa)
    return out



def dna_generator(peptide, n, aa_list):
    report = ""
    out = ["","",""]
    for ch in peptide:
        aa = aa_list[ch]
        for i in range(n):
            out[i] += sorter(aa, n)[i]
    for i in enumerate(out):
        if i[1]:
            report += f"\n\n>Seq{i[0]+1}:\n{u_to_t(i[1])}"
    return report




#----------------------------- end function definitions except main() ---------------------------------


def main():
    species = args.sp
    output_number = set_number(args.n)
    cut_off = set_cutoff(args.co)
    sample_file = args.i
    now = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_")
    report = f"Codons Shuffler cdnsf.py report. \nFile name: {now}.txt.\n\n"
    report += f"Report sequence(s) for {output_number} semi-randomly generated DNA sequences.\n\n\nCut-off: {cut_off}. Species of codon table: {species}.\n\n"
    if args.co > RECOMMENDED_MAX_CUTOFF:
        report += f"WARNING: cut-off was greater than the recommended maximum of {RECOMMENDED_MAX_CUTOFF}.\n"
    report += f"============== Input peptide: ==============\n\n"

    if sample_file == "-":
        primary_input = command_input()
    elif file_input(sample_file):
        primary_input = file_input(sample_file)
    else:
        primary_input = ["",""]
    if primary_input[0]:
        report += f"{primary_input[0]}\n"
    if primary_input[1] == "":
        report += "<<Empty input.>>"
        write_report(report, now)
        sys.exit()
    else:
        report += primary_input[1]

    if aa_letter_check(primary_input[1]):
        report += "\n\nThe following non-peptide letters were found (may be invisible characters):\n"
        for element in aa_letter_check(primary_input[1]):
            report += f"This: {element}. "
        write_report(report, now)
        sys.exit()

    output_number = set_number(args.n)
    cut_off = set_cutoff(args.co)
    codon_input = all_codon_parser(source_opener(set_source(species)))
    aminoacids = {}
    for aa_key in codon_input:
        aminoacids[aa_key] = Aminoacid(aa_key, codon_input[aa_key], cut_off)


    report += "\n\n============== Output DNA(s): =============="

    report += dna_generator(primary_input[1].upper(), output_number, aminoacids)

    write_report(report, now)






if __name__ == "__main__":
    main()
