import argparse
import csv
import os
import sys
import subprocess

def main():
    for i in range(1000000):
        # Using subprocess to call another Python script
        subprocess.run(['python', 'thirty-bw2-wcsv3.py','--csv', 'thirty-bw2-wcsv-try6.csv'])

    return 'done'

if __name__ == '__main__':
    # No need to pass sys.argv to main as it doesn't accept any arguments
    result = main()
    sys.exit(0 if result == 'done' else 1)

