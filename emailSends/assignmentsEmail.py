import os
import re
import pandas as pd
from sendEmail import send_email

# read in the assignments excel file 
assignments = pd.read_excel('path_to_file')

# Create a list of the new URMs
urms = assignments['Active URM'].unique()

# Some prospects were assigned to offices. This regular expression matches the format of the names of URMs that are actual people
urmName = r"(\w+.*, \w+.*)"

# Create a dictionary of each URM who is not an office and that URM's email address
urmEmails = {urm: assignments.loc[assignments['Active URM'] == urm, ['URM Email']].values[0][0]
             for urm in urms if re.match(urmName, urm)}

# Create a dictionary of each URM who is not an office and that URM's assignments
urmAssignments = {urm: assignments.loc[assignments['Active URM'] == urm, 'Prospect Name':'Lifetime Household Recognition']
                  for urm in urms if re.match(urmName, urm)}

# Loop through the urms and assignments in the URM assignments dictionary
for urm, assignment in urmAssignments.items():
    
    # Open the email template
    message = open("assignmentsEmail.txt", "r").read()
    
    # Grab the current URM's email
    email = urmEmails[urm]
    
    # Grab the URM's first name
    firstName = urm.split(',')[1].split(' ')[1]
    
    # Enforce that the Lifetime Household Recognition for prospects that have not given shows up as 0
    assignment['Lifetime Household Recognition'] = assignment['Lifetime Household Recognition'].fillna(0)
    
    # Enforce that any other missing data shows up as a blank space
    assignment = assignment.fillna('')
    
    # Format Lifetime Household Recognition as currency
    assignment['Lifetime Household Recognition'] = assignment.apply(
        lambda x: "${:,.0f}".format(x['Lifetime Household Recognition']), axis=1)
    
    # Insert the URM's first name and assignments into the email template
    message = message.format(firstName, assignment.to_html(index=False))
    
    # Send the email to the current URM 
    send_email(sender='sender', recipient=email, subject='Newly Assigned Prospects', message=message, cc=['cc_addresses'])
