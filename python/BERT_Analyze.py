# BERT_Analyze.py

from BERT_Plot import plot

def getData(input_file):
    f = open(input_file, 'r')
    x_values = []
    y_values = []
    for line in f:
        # TAP0 DAC Setting (x values)
        if "CML_TAP0_BIAS" in line:
            array = line.split()
            # must remove " before using int()
            x = int(array[-1].replace('"', ''))
            x_values.append(x)
            #print(line)
            #print(array)
            #print(x)
        # Total error counter (y values)
        if "Final counter" in line:
            # get all numbers in string
            numbers = [int(s) for s in line.split() if s.isdigit()]
            y = numbers[0]
            y_values.append(y)
            #print(line)
            #print(numbers)
    
    return [x_values, y_values]

def analyze(input_file, plot_dir, output_file):
    data = getData(input_file)
    x_values = data[0]
    y_values = data[1]
    plot(plot_dir, output_file, x_values, y_values)

def main():
    plot_dir    = "plots"
    data_dir    = "data/BERT_Scan_SingleDP_Data"
    
    output_file = "BERT_scan_001"
    input_file  = "{0}/scan_001.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    output_file = "BERT_scan_002"
    input_file  = "{0}/scan_002.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)
    
    output_file = "BERT_scan_003"
    input_file  = "{0}/scan_003.log".format(data_dir)
    analyze(input_file, plot_dir, output_file)

if __name__ == "__main__":
    main()

