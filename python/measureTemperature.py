# measureTemperature.py

from tools import getTempRD53B

def main():
    voltage = int(input("Enter a positive integer voltage (mV): "))
    temperature = getTempRD53B(voltage)
    print("Temperature (C): {0:.2f}".format(temperature))

if __name__ == "__main__":
    main()

