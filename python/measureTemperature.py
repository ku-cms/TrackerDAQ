# measureTemperature.py

from tools import getTempRD53B

def measure():
    # Get temperature for RD53B; input: voltage (mV), output: temperature (C)
    voltage = int(input("Enter a positive integer voltage (mV): "))
    temperature = getTempRD53B(voltage)
    print("Temperature (C): {0:.2f}".format(temperature))

def main():
    measure()

if __name__ == "__main__":
    main()

