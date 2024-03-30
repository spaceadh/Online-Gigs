#!/usr/bin/env python3
"""Analyse a vampire infiltration.
   Vampire Hunting v1.4.0

   Student number:
"""

import sys
import os.path
from format_list import format_list, format_list_or, str_time, is_initial, period_of_time, day_of_time, time_of_day

# Section 2
def file_exists(file_name):
    """Verify that the file exists.

    Args:
        file_name (str): name of the file

    Returns:
    - bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_name)

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

# Section 4
def pretty_print_infiltration_data(data):
    """Print the vampire infiltration data in a human-readable format.

    Parameters:
        data (tuple): A tuple consisting of a list of participants, a list of pairs for each day,
                     and a dictionary with counts of humans and vampires.

    Returns:
        None: Prints the formatted output.
    """
    participants, days = data
    # participants, days, counts = data

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

    # print(f"Total number of humans (H): {counts['H']}")
    # print(f"Total number of vampires (V): {counts['V']}")
    print("End of Days")

# Section 5
def contacts_by_time(participant, time, contacts_daily):
    """Lookup function to get the contact list for a participant at a given time."""
    # print(participant)
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

# Section 6
def create_initial_vk(participants):
    """ Your comments here """
    # dict = {}
    # for participant in participants:
    #     dict[participant] = "U"
    # return dict
    dict = {participant: 'U' for participant in participants}
    # print(dict)
    return dict

def pretty_print_vampire_knowledge(vk):
    """
    Print the vampire knowledge data structure in a human-readable format.

    Parameters:
        vk (dict): Vampire knowledge data structure.

    Returns:
        None: Prints the formatted output.
    """
    humans = format_list([k for k, v in vk.items() if v == "H"])
    unclear = format_list([k for k, v in vk.items() if v == "U"])
    vampires = format_list([k for k, v in vk.items() if v == "V"])

    print("Humans:", humans if humans else "(None)")
    print("Unclear individuals:", unclear if unclear else "(None)")
    print("Vampires:", vampires if vampires else "(None)")

# Done by professors
def pretty_print_vks(vks):
    print(f'Vampire Knowledge Tables')
    for i in range(len(vks)):
        print(f'Day {str_time(i)}:')
        pretty_print_vampire_knowledge(vks[i])
    print(f'End Vampire Knowledge Tables')

# Section 7
def update_vk_with_tests(vk, tests):
    # print("VK structure before update:", vk)
    # print("Test results:", tests)

    # Iterate over participants in tests
    for participant, test_result in tests.items():
        # Check if participant is in VK structure
        if participant not in vk:
            # print(f"Warning: Participant '{participant}' not in VK structure. Skipping.")
            continue

        current_status = vk[participant]

        # Update participant status based on test result
        if current_status == "U":
            vk[participant] = "V" if test_result else "H"
        elif current_status == "H" and test_result:
            print("Error found in data: humans cannot be vampires; aborting.")
            sys.exit()
        elif current_status == "V" and not test_result:
            print("Error found in data: vampires cannot be humans; aborting.")
            sys.exit()

    # print("VK structure after update:", vk)
    return vk

# Section 8
def update_vk_with_vampires_forward(vk_pre, vk_post):
    """Update vk_post by pushing vampire status forward from vk_pre."""
    for participant, status_pre in vk_pre.items():
        if status_pre == "V":
            # If participant is a vampire in vk_pre
            if participant not in vk_post or vk_post[participant] == "U":
                # Update vk_post to mark participant as a vampire
                vk_post[participant] = "V"
        elif status_pre == "H":
            # If participant is a definite human in vk_pre, print an error and exit
            print("Error found in data: vampires cannot be humans; aborting.")
            sys.exit()

    return vk_post

# Section 9
def update_vk_with_humans_backward(vk_pre, vk_post):
    """Update vk_pre by pushing human status backwards from vk_post."""
    # print("VK structure before update:", vk_pre)
    # print("VK structure after update:", vk_post)
    # print("VK items:", vk_pre.items())
   
    for participant, status_post in vk_post.items():
        # Check if participant is in vk_pre
        # print(participant)
        # print(status_post)
        if participant not in vk_pre:
            # If participant is not in vk_pre, add them with the status from vk_post
            vk_pre[participant] = status_post
        else:
            # Check if participant is confirmed human in vk_post
            if status_post == "H":
                # If confirmed human, update vk_pre to human
                vk_pre[participant] = "H"
            elif status_post == "V":
                # If confirmed vampire, print an error and continue
                vk_pre[participant] = "V"
                # print("Error found in data: humans cannot be vampires; continuing.")
    
    return vk_pre

# Section 10
# Section 10
def update_vk_overnight(vk_pre, vk_post):
    """Update vk_post by propagating human/vampire status forward overnight from vk_pre."""
    # print("VK structure before update:", vk_pre)
    # print("VK structure after update:", vk_post)

    for participant, status_pre in vk_pre.items():
        # Check if participant is in vk_post
        if participant not in vk_post:
            # If participant is not in vk_post, add them with the status from vk_pre
            vk_post[participant] = status_pre
        else:
            status_post = vk_post[participant]

            # Check if participant was a definite human in the afternoon and tested as vampire in the morning
            if status_pre == "H" and status_post == "V":
                print("Error found in data: humans cannot be vampires; aborting.")
                sys.exit()
            
            # Check if participant was a definite vampire in the afternoon and tested as human in the morning
            elif status_pre == "V" and status_post == "H":
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()

            # Propagate statuses forward
            vk_post[participant] = status_pre

    return vk_post

# Section 11
def update_vk_with_contact_group(vk_pre, contacts, vk_post):
    """Update vk_post by approximating contact results from vk_pre."""
    # print("VK structure before update:", vk_pre)
    # print("Contact groups:", contacts)
    # print("VK structure after update:", vk_post)

    # Part 1: Check for errors and propagate vampirism forward
    for participant, status_pre in vk_pre.items():
        # Check if participant is in vk_post
        if participant not in vk_post:
            # If participant is not in vk_post, add them with the status from vk_pre
            vk_post[participant] = status_pre
        else:
            status_post = vk_post[participant]

            # Check if participant was a definite vampire in the afternoon and is somehow a human in the evening
            if status_pre == "V" and status_post == "H":
                print("Error found in data: vampires cannot be human; aborting.")
                sys.exit()

            # Propagate statuses forward
            vk_post[participant] = status_pre

    # Part 2: Propagate humanness forward based on contact groups
    for contact_group in contacts:
        all_human_pre = all(vk_pre[participant] == "H" for participant in contact_group if participant in vk_pre)
        all_unknown_pre = all(vk_pre[participant] == "U" for participant in contact_group if participant in vk_pre)

        for participant in contact_group:
            # Check if participant is in vk_pre and vk_post
            if participant in vk_pre and participant in vk_post:
                status_pre = vk_pre[participant]
                status_post = vk_post[participant]

                # Check for errors: human in pre but somehow a vampire in post
                if status_pre == "H" and status_post == "V":
                    print("Error found in data: humans cannot be vampires; aborting.")
                    sys.exit()

                # Propagate humanness forward only if all_human_pre and no definite vampires or unknown in the group
                if all_human_pre and status_pre == "H" and status_post == "U":
                    vk_post[participant] = "H"

    return vk_post

# Section 12
def find_infection_windows(vks):
    """Find infection windows for definite vampires in the VK structures."""
    windows = {}

    for t in range(len(vks)):
        vk = vks[t]

        # Identify definite vampires on the last day
        definite_vampires = {participant: t for participant, status in vk.items() if status == "V"}

        # Update infection windows
        for vampire, last_human_time in definite_vampires.items():
            if vampire not in windows:
                windows[vampire] = (last_human_time, t)

    return windows

def pretty_print_infection_windows(iw):
    """Prints a readable format for the infection windows."""
    for participant, (start, end) in sorted(iw.items()):
        start_time_str = str_time(start)
        end_time_str = str_time(end)
        print(f"{participant} was turned between {start_time_str} and {end_time_str}.")

# Section 13
def find_potential_sires(iw, groups, vks):
    """Find potential sires based on infection windows, contact groups, and vampire knowledge structures."""
    sires = {}

    for vampire, (start, end) in iw.items():
        contact_list = []

        for t in range(start, end + 1):
            if t % 2 == 1:  # Only consider PM time units
                contacts = groups[t // 2] if t // 2 < len(groups) else []
                contact_list.append((t, contacts))

        sires[vampire] = contact_list

    return sires

def pretty_print_potential_sires(ps):
    """Print the potential sires structure nicely."""
    for vampire, contact_list in sorted(ps.items()):
        print(f"{vampire}:")
        if contact_list:
            for time_unit, contacts in contact_list:
                day_str = str_time(time_unit)
                contact_str = format_list_or(contacts)
                print(f"On {day_str}, met with {contact_str}.")
        else:
            print("(None)")

# Section 14
def trim_potential_sires(ps, vks):
    """Trim the potential sires structure based on logical principles."""
    trimmed_ps = {}

    for vampire, contact_list in ps.items():
        trimmed_contacts = []

        for time_unit, contacts in contact_list:
            if time_unit not in vks or vampire not in vks[time_unit] or vks[time_unit][vampire] == "V":
                # Remove empty contact days and the (eventual) vampire
                continue

            trimmed_contacts.append((time_unit, [contact for contact in contacts if contact not in vks[time_unit] or vks[time_unit][contact] != "H"]))

        if trimmed_contacts:
            trimmed_ps[vampire] = trimmed_contacts

    return trimmed_ps

# Section 15
def trim_infection_windows(iw, ps):
    """Tighten infection windows based on potential sire information."""
    trimmed_iw = {}

    for vampire, (start, end) in iw.items():
        trimmed_start = start
        trimmed_end = end

        if vampire in ps:
            for time_unit, _ in ps[vampire]:
                trimmed_start = max(trimmed_start, time_unit)

        trimmed_iw[vampire] = (trimmed_start, trimmed_end)

    return trimmed_iw

# Section 16
def update_vks_with_windows(vks, iw):
    """Update vk structures with infection window data."""
    changes_count = 0
    # print(vks)
    print(iw)
    # Iterate over participants in infection window
    for participant, window in iw.items():
        start, end = window
        for t in range(start, end + 1):
            # Check if participant is in vk structure
            if participant in vks[t]:
                current_status = vks[t][participant]
                print(current_status)
                print(participant)
                # Update participant status based on infection window
                if current_status == "U":
                    vks[t][participant] = "V"
                    changes_count += 1
                elif current_status == "H":
                    print(f"Warning: Attempted to update '{participant}' to vampire, but they are already known to be human.")
                elif current_status == "V":
                    print(f"Warning: Attempted to update '{participant}' to human, but they are already known to be a vampire.")

    return vks, changes_count

# Section 17; done by professors
def cyclic_analysis(vks,iw,ps):
    count = 0
    changes = 1
    while(changes != 0):
        ps = trim_potential_sires(ps,vks)
        iw = trim_infection_windows(iw,ps)
        (vks,changes) = update_vks_with_windows(vks,iw)
        count = count + 1
    return (vks,iw,ps,count)

# Section 18: vampire strata
def vampire_strata(iw):
    """ Your comments here """
    originals = set()
    unclear_vamps = set()
    newborns = set()

    for vampire, window in iw.items():
        start, end = window

        if start == 0 and end == 0:
            originals.add(vampire)
        elif start > 0 and end == 0:
            newborns.add(vampire)
        elif start > 0 and end > 0:
            unclear_vamps.add(vampire)
            
    return (originals,unclear_vamps,newborns)
 
def pretty_print_vampire_strata(originals, unclear_vamps, newborns):
    """Pretty print vampire stratas."""
    print("Original vampires:", ", ".join(sorted(originals)) if originals else "(None)")
    print("Unknown strata vampires:", ", ".join(sorted(unclear_vamps)) if unclear_vamps else "(None)")
    print("Newborn vampires:", ", ".join(sorted(newborns)) if newborns else "(None)")


# Section 19: vampire sire sets
def calculate_sire_sets(ps):
    """Calculate sets of possible sires for vampires."""
    ss = {}
    # print("Debug - ps:", ps)  # Add this line
    for vampire, contacts_list in ps.items():
        sire_set = set()
        for time_unit, contacts in contacts_list:
            # Update sire_set with contacts for the current time_unit
            sire_set.update(contacts)
        # Remove the vampire itself from the sire_set
        sire_set.discard(vampire)
        ss[vampire] = sire_set
    # print("Debug - ss:", ss)  # Add this line
    return ss

def pretty_print_sire_sets(ss, iw, vamps, newb):
    """Print the sets of possible sires for vampires."""
    if newb:
        print("Newborn vampires:")
    else:
        print("Vampires of unknown strata:")
        # print("ss:", ss)  # Add this line

    print(vamps)
    for vampire in sorted(vamps):
        sire_set = ss[vampire]

        if not sire_set:
            print(f"{vampire} was sired by None.")
        else:
            start, end = iw[vampire]

            if start == end:
                print(f"{vampire} was sired by {format_list_or(sire_set)} on {str_time(start, True)}.")
            else:
                print(f"{vampire} could have been sired by {format_list_or(sire_set)} "
                      f"between {str_time(start, True)} and {str_time(end, True)}.")


# Section 20: Find hidden vampire sires
def find_hidden_vampires(ss, iw, vamps, vks):
    """Update vk structures based on hidden vampire sires."""
    changes_count = 0

    for vampire in vamps:
        sire_set = ss[vampire]

        if len(sire_set) == 1:
            sire = next(iter(sire_set))  # Get the only element in the set

            # Get the infection window of the newborn vampire
            start, end = iw[vampire]

            # Check if the sire was a vampire during the entire infection window
            if all(vks[t][sire] == "V" for t in range(start, end + 1)):
                # Extend the vampire status of the sire one time unit further back
                start -= 1

                # Update vk structures
                for t in range(start, end + 1):
                    if vks[t][vampire] == "U":
                        vks[t][vampire] = "V"
                        changes_count += 1

                    if vks[t][sire] == "H":
                        print("Error found in data: vampires cannot be humans; aborting.")
                        sys.exit()

    return vks, changes_count

# Section 21; done by professor
def cyclic_analysis2(vks,groups):
    count = 0
    changes = 1
    while(changes != 0):
        iw = find_infection_windows(vks)
        ps = find_potential_sires(iw, vks, groups)
        vks,iw,ps,countz = cyclic_analysis(vks,iw,ps)
        o,u,n = vampire_strata(iw)
        ss = calculate_sire_sets(ps)
        vks,changes = find_hidden_vampires(ss,iw,n,vks)        
        count = count + 1
    return (vks,iw,ps,ss,o,u,n,count)

def main():
    """Main logic for the program.  Do not change this (although if 
       you do so for debugging purposes that's ok if you later change 
       it back...)
    """
    filename = ""
    # Get the file name from the command line or ask the user for a file name
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()

    # Section 2. Check that the file exists
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    # Section 3. Create contacts dictionary from the file
    # Complete function parse_file().
    data = parse_file(filename)
    participants, days = data
    tests_by_day = [d[0] for d in days]
    groups_by_day = [d[1] for d in days]

    # Section 4. Print contact records
    pretty_print_infiltration_data(data)

    # Section 5. Create helper function for time analysis.
    print("********\nSection 5: Lookup helper function")
    if len(participants) == 0:
        print("  No participants.")
    else:
        p = participants[0]
        if len(days) > 1:
            d = 2
        elif len(days) == 1:
            d = 1
        else:
            d = 0
        t = time_of_day(d,False)
        t2 = time_of_day(d,True)
        print(f"  {p}'s contacts for time unit {t} (day {day_of_time(t)}) are {format_list(contacts_by_time(p,t,groups_by_day))}.")
        print(f"  {p}'s contacts for time unit {t2} (day {day_of_time(t)}) are {format_list(contacts_by_time(p,t2,groups_by_day))}.")
        assert(contacts_by_time(p,t,groups_by_day) == contacts_by_time(p,t2,groups_by_day))

    # Section 6.  Create the initial data structure and pretty-print it.
    print("********\nSection 6: create initial vampire knowledge tables")
    vks = [create_initial_vk(participants) for i in range(1 + (2 * len(days)))]
    pretty_print_vks(vks)

    # Section 7.  Update the VKs with test results.
    print("********\nSection 7: update the vampire knowledge tables with test results")
    for t in range(1,len(vks),2):
        vks[t] = update_vk_with_tests(vks[t],tests_by_day[day_of_time(t)-1])
    pretty_print_vks(vks)

    # Section 8.  Update the VKs to push vampirism forwards in time.
    print("********\nSection 8: update the vampire knowledge tables by forward propagation of vampire status")
    for t in range(1,len(vks)):
        vks[t] = update_vk_with_vampires_forward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Section 9.  Update the VKs to push humanism backwards in time.
    print("********\nSection 9: update the vampire knowledge tables by backward propagation of human status")
    for t in range(len(vks)-1, 0, -1):
        vks[t-1] = update_vk_with_humans_backward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Sections 10 and 11.  Update the VKs to account for contact groups and safety at night.
    print("********\nSections 10 and 11: update the vampire knowledge tables by forward propagation of contact results and overnight")
    for t in range(1, len(vks), 2):
        vks[t+1] = update_vk_with_contact_group(vks[t],groups_by_day[day_of_time(t)-1],vks[t+1])
        if t + 2 < len(vks):
            vks[t+2] = update_vk_overnight(vks[t+1],vks[t+2])
    pretty_print_vks(vks)

    # Section 12. Find infection windows for vampires.
    print("********\nSection 12: Vampire infection windows")
    iw = find_infection_windows(vks)
    pretty_print_infection_windows(iw)

    # Section 13. Find possible vampire sires.
    print("********\nSection 13: Find possible vampire sires")
    ps = find_potential_sires(iw, vks, groups_by_day)
    pretty_print_potential_sires(ps)

    # Section 14. Trim the potential sire structure.
    print("********\nSection 14: Trim potential sire structure")
    ps = trim_potential_sires(ps,vks)
    pretty_print_potential_sires(ps)

    # Section 15. Trim the infection windows.
    print("********\nSection 15: Trim infection windows")
    iw = trim_infection_windows(iw,ps)
    pretty_print_infection_windows(iw)

    # Section 16. Update the vk structures with infection windows.
    print("********\nSection 16: Update vampire information tables with infection window data")
    (vks,changes) = update_vks_with_windows(vks,iw)
    pretty_print_vks(vks)
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 17.  Cyclic analysis for sections 14-16 
    print("********\nSection 17: Cyclic analysis for sections 14-16")
    vks,iw,ps,count = cyclic_analysis(vks,iw,ps)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print('Potential sires:')
    pretty_print_potential_sires(ps)
    print('Infection windows:')
    pretty_print_infection_windows(iw)
    pretty_print_vks(vks)       

    # Section 18.  Calculate vampire strata
    print("********\nSection 18: Calculate vampire strata")
    (origs,unkns,newbs) = vampire_strata(iw)
    pretty_print_vampire_strata(origs,unkns,newbs)

    # Section 19.  Calculate definite sires
    print("********\nSection 19: Calculate definite vampire sires")
    ss = calculate_sire_sets(ps) 
    pretty_print_sire_sets(ss, iw, newbs, True)   

    # Section 20.  Find hidden vampires
    print("********\nSection 20: Find hidden vampires")
    (vks, changes) = find_hidden_vampires(ss,iw,newbs,vks)
    pretty_print_vks(vks)           
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 21.  Cyclic analysis for sections 14-20
    print("********\nSection 21: Cyclic analysis for sections 14-20")
    (vks,iw,ps,ss,o,u,n,count) = cyclic_analysis2(vks,groups_by_day)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print("Infection windows:")
    pretty_print_infection_windows(iw)
    print("Vampire potential sires:")
    pretty_print_potential_sires(ps)
    print("Vampire strata:")
    pretty_print_vampire_strata(o,u,n)
    print("Vampire sire sets:")    
    pretty_print_sire_sets(ss,iw,n,True)
    pretty_print_vks(vks)       
    
if __name__ == "__main__":
    main()