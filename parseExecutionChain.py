# Quick, dirty, brittle py code to parse (most) execution chains from files in repos like @pr0xylife's excellent Qakbot and other collections: https://github.com/pr0xylife?tab=repositories&q=&type=source&language=&sort=
# Outputs execution chains in format "file extension > file extension" into a .csv file
import argparse
import glob
import os
import csv
import re

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folder', action='store', dest='input_folder', default='Qakbot',
                        required=False, help='Input the name of the file folder containing the TXT files to parse')

args = parser.parse_args()
inputFolder = args.input_folder

files = glob.glob(os.path.join(inputFolder, '**/*.txt'), recursive=True)
outfile = open('parsedExecutionChains.csv', 'w', encoding='utf-8', newline='')
writer = csv. writer(outfile)
writer.writerow(['Execution Chain'])
reg = re.compile('[a-fA-F0-9]{64}')

for file in files:
    with open(file, 'r', encoding='utf-8') as infile:
        filelines = infile.readlines()
        executionChainElements = []
        for fileline in filelines:
            match = re.findall(reg, fileline)
            if match:
                chainElementCandidate = fileline.split(' ')[0]
                if len(chainElementCandidate) == 4 or len(chainElementCandidate) == 5:
                    executionChainElements.append(chainElementCandidate)
            elif '.url ' in fileline:
                executionChainElements.append(fileline.split(' ')[0])

        try:
            executionChainString = executionChainElements[0]
            for executionChainElement in executionChainElements[1:]:
                executionChainString += ' > ' + executionChainElement
            writer.writerow([executionChainString])
        except IndexError:
            continue
