import json
arrayOfBaddies = []

#https://developers.google.com/gmail/api/quickstart/python
#get your credentials file here. save as credentials.json



#ALWAYS CHANGE LINE 11 LINE 24 AND LINE 105 109

f = open('/Users/pavelfrolikov/canvas_automated_grading/manual_inspections/Study Group 1 Week 1 Report.json')
data = json.load(f)
print(data)
for x in data:
    arrayOfBaddies.append((x.get('name'), x.get('email_ids')))
    print(x.get('name'))
    print(x.get('email_ids'))




arrayOfNamesAndEmails = []
import csv
with open("Study Group 1.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            parsedString = row[2]
            print("HERE")
            parsedString = parsedString[2:-1]
            listOfEmails = parsedString.split("', '")
            listOfEmails[-1] = listOfEmails[-1][0:-1]
            parsedString = row[1]
            parsedString = parsedString[2:-1]
            listOfNames = parsedString.split("', '")
            listOfNames[-1] = listOfNames[-1][0:-1]
            arrayOfNamesAndEmails.append((listOfNames, listOfEmails))
            print(f'{row[1]} {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')


newArrayOfPeopleToEmail = []
for x in arrayOfBaddies:
    for group in arrayOfNamesAndEmails:
        if x[0] in group[0]:
            print(x[0]+ "is in the group")
            newEmail = group[1]
            print(group[0])
            print(group[1])
            newEmail.remove(x[1])
            newArrayOfPeopleToEmail.append((x[0], newEmail))
            print(x[0]+ "did not work with")
            print(newEmail)



for w in newArrayOfPeopleToEmail:
    print(w[0])
    print(w[1])



import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://mail.google.com/']
creds = None

if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
        # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    #replace 0 with newArrayOfPeopleToEmail
    for x in 0:#newArrayOfPeopleToEmail
        baddie = x[0]
        print(baddie)
        message_text = "Hi, did you guys meet up with: " + baddie + " for last week's study groups?(Please use reply all feature so msgs don't get lost) "+baddie+" is not on this email thread.\n\n~Pavel"
        sender = "frolikov@ucdavis.edu"
        to = x[1]
        subject = "Study Group 1 - Teammate question"

        message = EmailMessage()
        message.set_content(message_text)


        message["to"] = to
        message["from"] = sender
        message["subject"] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {
                        'raw': encoded_message
        }
        if to:
            print(message["to"])
            print(to)
            draft = (service.users().messages().send(userId="me",
                                                        body=create_message).execute())
            print(F'Draft id: {draft["id"]}\n')



except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f'An error occurred: {error}')
