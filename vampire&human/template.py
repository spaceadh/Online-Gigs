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
        boolean: returns True if the file exists and False otherwise.
    """
    return True

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
    participants = []
    days = []
    return (participants,days)

# Section 4
def pretty_print_infiltration_data(data):
    """ Your comments here """
    pass

# Section 5
def contacts_by_time(participant, time, contacts_daily):
    """ Your comments here """
    return []

# Section 6
def create_initial_vk(participants):
    """ Your comments here """
    dict = {}
    return dict

def pretty_print_vampire_knowledge(vk):
    """ Your comments here """
    pass

# Done by professors
def pretty_print_vks(vks):
    print(f'Vampire Knowledge Tables')
    for i in range(len(vks)):
        print(f'Day {str_time(i)}:')
        pretty_print_vampire_knowledge(vks[i])
    print(f'End Vampire Knowledge Tables')

# Section 7
def update_vk_with_tests(vk, tests):
    """ Your comments here """
    return vk

# Section 8
def update_vk_with_vampires_forward(vk_pre, vk_post):
    """ Your comments here """
    return vk_post

# Section 9
def update_vk_with_humans_backward(vk_pre, vk_post):
    """ Your comments here """
    return vk_pre

# Section 10
def update_vk_overnight(vk_pre, vk_post):
    """ Your comments here """
    return vk_post

# Section 11
def update_vk_with_contact_group(vk_pre, contacts, vk_post):
    """ Your comments here """
    return vk_post

# Section 12
def find_infection_windows(vks):
    """ Your comments here """
    windows = {}
    return windows

def pretty_print_infection_windows(iw):
    """ Your comments here """
    pass

# Section 13
def find_potential_sires(iw, groups):
    """ Your comments here """
    sires = {}
    return sires

def pretty_print_potential_sires(ps):
    """ Your comments here """
    pass

# Section 14
def trim_potential_sires(ps,vks):
    """ Your comments here """
    return ps

# Section 15
def trim_infection_windows(iw,ps):
    """ Your comments here """
    return iw

# Section 16
def update_vks_with_windows(vks,iw):
    """ Your comments here """
    changes = 0
    return (vks,changes)

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
    return (originals,unclear_vamps,newborns)
 
def pretty_print_vampire_strata(originals, unclear_vamps, newborns):
    """ Your comments here """
    pass

# Section 19: vampire sire sets
def calculate_sire_sets(ps):
    """ Your comments here """
    ss = {}
    return ss

def pretty_print_sire_sets(ss,iw,vamps,newb):
    """ Your comments here """
    pass

# Section 20: vampire sire sets
def find_hidden_vampires(ss,iw,vamps,vks):
    """ Your comments here """
    changes = 0
    return (vks,changes)

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
    # pretty_print_sire_sets(ss,iw,unkns,False)
    # pretty_print_sire_sets(ss,iw,newbs,True)  

    pretty_print_sire_sets(ss, iw, unkns, False)
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
    pretty_print_sire_sets(ss,iw,u,False)
    pretty_print_sire_sets(ss,iw,n,True)
    pretty_print_vks(vks)       
    
if __name__ == "__main__":
    main()
