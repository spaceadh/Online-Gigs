import sys
import os.path
from format_list import format_list, format_list_or, str_time, is_initial, period_of_time, day_of_time, time_of_day

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
            lines = [line.strip() for line in file]

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
            test_results = {name.strip(): result.strip() for item in test_line for name, result in [item.split(':')]}

            # Update counts
            counts['H'] += sum(1 for result in test_results.values() if result == 'H')
            counts['V'] += sum(1 for result in test_results.values() if result == 'V')

            # Extract contact groups
            contact_groups = [group.split(',') for group in lines[current_line + 1: current_line + 1 + int(lines[current_line + 1])]]

            print("test_results",test_results)
            print("contact_groups",contact_groups)
            # Update data structure
            days.append((test_results, contact_groups))

            # Move to the next day
            current_line += 2 + int(lines[current_line + 1])

        for participant in participants:
            status = test_results.get(participant)
            if status is not None:
                print(f"{participant}: {status}")
            else:
                 print(f"{participant}: Status not available for the last day")

        # Print counts of humans and vampires
        print(f"\nTotal number of humans (H): {counts['H']}")
        print(f"Total number of vampires (V): {counts['V']}")

        return participants, days, counts

    except Exception as e:
        print("Error found in file, aborting.")
        sys.exit()

# Section 4
def pretty_print_infiltration_data(data):
    """Print the vampire infiltration data in a human-readable format.

    Parameters:
        data (tuple): A tuple consisting of a list of participants, a list of pairs for each day,
                     and a dictionary with counts of humans and vampires.

    Returns:
        None: Prints the formatted output.
    """
    participants, days, counts = data

    print("Vampire Infiltration Data")
    print(f"{len(days)} days with the following participants: {format_list(participants)}.")

    for i, (tests, groups) in enumerate(days, start=1):
        print(f"Day {i} has {len(tests)} vampire {'tests' if len(tests) != 1 else 'test'} "
              f"and {len(groups)} contact {'groups' if len(groups) != 1 else 'group'}.")

        # Print test results
        print(f"{len(tests)} test{'s' if len(tests) != 1 else ''}")
        for participant, result in sorted(tests.items()):
            print(f"    {format_list([participant])} is {'a vampire!' if result == 'V' else 'human.'}")

        # Print contact groups
        print(f"{len(groups)} group{'s' if len(groups) != 1 else ''}")
        for group in groups:
            print(f"    {format_list(group)}")

    print("End of Days")
    print(f"Total number of humans (H): {counts['H']}")
    print(f"Total number of vampires (V): {counts['V']}")


    print("End of Days")

# Section 5
def contacts_by_time(participant, time, contacts_daily):
    """Lookup function to get the contact list for a participant at a given time."""
    print(participant)
    day = day_of_time(time)
    is_am = period_of_time(time)
    day_index = day - 1

    if is_initial(time):
        return []

    if day_index < len(contacts_daily):
        participant_contacts = []
        for group in contacts_daily[day_index]:
            if participant in group:
                participant_contacts.extend(group)

        participant_contacts = list(set(participant_contacts) - {participant})

        return participant_contacts

    return []

def create_initial_vk(participants):
    """Create the initial vampire knowledge data structure.

    Args:
        participants (list): List of participants.

    Returns:
        dict: Initial vampire knowledge data structure.
    """
    print("Participants and Initial Status:")
    for participant in participants:
        print(f"{participant}: 'U'")

    initial_vk = {participant: 'U' for participant in participants}

    # Print the initial_vk
    print("\nInitial Vampire Knowledge:")
    for participant, status in initial_vk.items():
        print(f"{participant}: {status}")

    # Print counts of humans and vampires
    count_humans = sum(1 for status in initial_vk.values() if status == 'H')
    count_vampires = sum(1 for status in initial_vk.values() if status == 'V')
    print(f"\nTotal number of humans (H): {count_humans}")
    print(f"Total number of vampires (V): {count_vampires}")

    return initial_vk
    
def pretty_print_vampire_knowledge(vk):
    """Print the vampire knowledge data structure in a human-readable format.

    Args:
        vk (dict): Vampire knowledge data structure.

    Returns:
        None: Prints the formatted output.
    """
    humans = format_list_or([participant for participant, status in vk.items() if status == 'H'])
    vampires = format_list_or([participant for participant, status in vk.items() if status == 'V'])
    unclear = format_list_or([participant for participant, status in vk.items() if status == 'U'])

    print("Humans:", humans)
    print("Unclear individuals:", unclear)
    print("Vampires:", vampires)

# Example usage:
# Step 1: Parse the file
filename = "1.txt"
participants, days, counts = parse_file(filename)

# Step 2: Pretty print the infiltration data
# pretty_print_infiltration_data((participants, days, counts))

# Step 3: Create the initial vampire knowledge data structure
initial_vk = create_initial_vk(participants)

# Step 4: Pretty print the vampire knowledge data structure
# pretty_print_vampire_knowledge(initial_vk)
