import sys

def parse_file(file_name):
    """Read the input file, parse the contents, and return data structures.

    Args:
        file_name (str): The name of the file.

    Returns:
        participants (list): List of participants.
        days (list): List of pairs; the first element is the test results
            (dictionary from participants to "H"/"V"); the second is a list of
            contact groups (list of lists of participants).
        counts (dict): Dictionary with counts of humans and vampires.
    """
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Remove leading and trailing whitespaces from each line
        lines = [line.strip() for line in lines]

        # Extract preamble data
        participants = lines[0].split(',')
        num_days = int(lines[1])

        # Initialize data structure
        days = []
        counts = {'H': 0, 'V': 0}  # Initialize counters for humans and vampires

        # Process days
        current_line = 2
        for _ in range(num_days):
            # Extract test results
            test_line = lines[current_line].split(',')
            test_results = {name: result.strip() for item in test_line for name, result in [item.split(':')]}

            # Update counts
            counts['H'] += sum(1 for result in test_results.values() if result == 'H')
            counts['V'] += sum(1 for result in test_results.values() if result == 'V')

            # Extract contact groups
            contact_groups = [group.split(',') for group in lines[current_line + 1: current_line + 1 + int(lines[current_line + 1])]]

            # Update data structure
            days.append((test_results, contact_groups))

            # Move to the next day
            current_line += 2 + int(lines[current_line + 1])

        # return participants, days, counts
        # print(counts)
        return participants, days

    except Exception as e:
        print("Error found in file, aborting.")
        sys.exit()

# Section 3. Create contacts dictionary from the file
# Complete function parse_file().
data = parse_file('1.txt')
participants, days = data
tests_by_day = [d[0] for d in days]
groups_by_day = [d[1] for d in days]

print(participants)
print(days)
print(tests_by_day)
print(groups_by_day)