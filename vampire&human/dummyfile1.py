import sys

# Section 3        
def parse_file(file_name):
    """Read the input file, parse the contents and return some data structures
    that contain the associated data for the vampire infiltration.

    Args:
        file_name (str): Contains the name of the file.

    Returns:
        participants: list of participants.
        days: list of pairs; the first element of a pair is the result of tests
          (dictionary from participants to "H"/"V"); the second is a list of
          contact groups (list of lists of participants)
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

        # Process days
        current_line = 2
        for _ in range(num_days):
            # Extract test results
            test_line = lines[current_line].split(',')
            test_results = {}
            for item in test_line:
                name, result = item.split(':')
                test_results[name.strip()] = result.strip()

            # Extract contact groups
            contact_groups = [group.split(',') for group in lines[current_line + 1: current_line + 1 + int(lines[current_line + 1])]]
            print(contact_groups)

            # Update data structure
            days.append((test_results, contact_groups))

            # Move to the next day
            current_line += 2 + int(lines[current_line + 1])
        print("participants:",participants)
        print("days:",days)

        return participants, days

    except Exception as e:
        print("Error found in file, aborting.")
        sys.exit()

# Example usage:
file_name = '1.txt'
participants, days = parse_file(file_name)
# print(participants)
# print(days)