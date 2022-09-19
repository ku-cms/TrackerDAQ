# CompareRD53AB.py 

import tools
import csv

def plot(input_csv, output_name):
    data = tools.getCSVData(input_csv)
    for row in data: 
        print(row)

def main():
    input_csv   = "CompareRD53AB/BERT_TAP0_Scan_Comparison_v1.csv"
    output_name = "CompareRD53AB/Comparison_v1"
    plot(input_csv, output_name)

if __name__ == "__main__":
    main()

