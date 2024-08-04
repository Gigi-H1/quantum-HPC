import csv
from collections import defaultdict

def load_counts(filename):
    counts = {}
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for row in csvreader:
            state, count = row
            counts[state] = int(count)
    return counts

def combine_counts(counts1, counts2):
    combined_counts = defaultdict(int)
    for state1, count1 in counts1.items():
        for state2, count2 in counts2.items():
            combined_state = state1 + state2  # Combine states
            combined_counts[combined_state] += count1 + count2
    return combined_counts

def save_combined_counts(filename, combined_counts):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['State', 'Counts'])
        for state, count in combined_counts.items():
            csvwriter.writerow([state, count])

# Load counts from the individual 30-qubit simulations
counts1 = load_counts('simulation_results_3.csv')
counts2 = load_counts('simulation_results_4.csv')

# Combine counts
combined_counts = combine_counts(counts1, counts2)

# Save combined results
save_combined_counts('combined_simulation_results2.csv', combined_counts)

print("Combined simulation results saved to 'combined_simulation_results2.csv'.")

