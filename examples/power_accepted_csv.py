"""Generate csv file containing accepted power at frequency.
"""

import csv

def write_accepted_powers(filename, accepted_powers):
    """Save list of accepted powers to csv file.
    """
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', 
                               quoting = csv.QUOTE_MINIMAL)
        csvwriter.writerow(accepted_powers)

def display_accepted_powers(filename):
    """Load and display the csv file.
    """
    with open(filename, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))

if "__main__" == __name__:
    filename = 'accepted_powers.csv'
    accepted_powers = [
        0.99953098, 0.99960789, 0.99969136, 0.99969799,
        0.99932407, 0.99956244, 0.99969353, 0.99967368,
        0.99953662, 0.99969774, 0.99968834, 0.99966301,
        0.99935933, 0.99967862, 0.99969800, 0.99969748,
        ]
    write_accepted_powers(filename, accepted_powers)
    print('Writing accepted powers...')
    print('Displaying accepted powers...')
    display_accepted_powers(filename)
    print('\nDone.')
