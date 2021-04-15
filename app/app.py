import os
from skpy import Skype

username = os.environ["SKYPE_USERNAME"]
password = os.environ["SKYPE_PASSWORD"]

sk = Skype(username, password)

contacts = sk.contacts
for contact in contacts:
    print(contact)
