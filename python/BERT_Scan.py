# BERT_Scan.py

import subprocess

def run():
    for x in range(50, 80, 10):
        output = subprocess.run(["./TrackerDAQ/scripts/BERT_Scan.sh", str(x)])
        print(output)
        #output = subprocess.check_output(["./TrackerDAQ/scripts/BERT_Scan.sh", "100"])
        #print(output)

def main():
    #output = subprocess.run(["echo", "why hello there"])
    #print(output)
    #output = subprocess.check_output(["echo", "Geeks for geeks"]) 
    #print(output)
    run()

if __name__ == "__main__":
    main()

