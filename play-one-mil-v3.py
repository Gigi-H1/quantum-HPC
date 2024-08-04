import sys
import subprocess

def main():
    for i in range(1):
        # Example of generating a CSV filename for each iteration
        csv_file = f'csv_files6/mil-30q_{i}.csv'
        result = subprocess.run(['python', 'thirty-bw2-wcsv4.py', '--csv', csv_file])
        if result.returncode != 0:
            print(f"Error: Script failed at iteration {i}")
            return 'error'

    return 'done'

if __name__ == '__main__':
    result = main()
    sys.exit(0 if result == 'done' else 1)

