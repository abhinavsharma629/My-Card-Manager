from .models import *
import random, sys

# What fields shall be populated?
target_fields = {"Name":True,
                 "FullName":True,
                 "Organization":True,
                 "Address":True,
                 "Title":True,
                 "Phone":True,
                 "Email":True,}

# Data that we'll use to populate the cards' fields.
first_names = []
last_names = []
streets = []
orgs = []
titles = []
phones = []
emails = []

################################## Actions ###################################

class CardFiller:
    def __init__(self, first_names, last_names, streets, orgs, titles, phones, emails):
        self.first_names = first_names
        self.last_names = last_names
        self.streets = streets
        self.orgs = orgs
        self.titles = titles
        self.phones = phones
        self.emails = emails

    def fill_card(self, target_fields, position):
        new_card = ["BEGIN:VCARD", "VERSION:2.1",]
        if "Name" in target_fields:
            namefield = "N:"
            namefield += str(self.last_names[position % len(self.last_names)])
            namefield +=";"
            namefield += str(self.first_names[position % len(self.first_names)])
            new_card.append(namefield)
        if "FullName" in target_fields:
            fnamefield = "FN:"
            fnamefield += str(self.first_names[position % len(self.first_names)])
            fnamefield += " "
            fnamefield += str(self.last_names[position % len(self.last_names)])
            new_card.append(fnamefield)
        if "Organization" in target_fields:
            orgfield = "ORG:"
            orgfield += str(self.orgs[position % len(self.orgs)])
            new_card.append(orgfield)
        if "Title" in target_fields:
            titlefield = "TITLE:"
            titlefield += str(self.titles[position % len(self.titles)])
            new_card.append(titlefield)
        if "Phone" in target_fields:
            phonefield = "TEL;WORK;VOICE:("
            phonefield += str(self.phones[position % len(self.phones)])
            new_card.append(phonefield)
        if "Address" in target_fields:
            addrfield = "ADR;WORK:;;"
            addrfield += str(self.streets[position % len(self.streets)])
            new_card.append(addrfield)
        if "Email" in target_fields:
            emailfield = "EMAIL;PREF;INTERNET:"
            emailfield += str(self.emails[position % len(self.emails)])
            new_card.append(emailfield)
        new_card.append("REV:%d" % random.randrange(100,500))
        new_card.append("END:VCARD")
        return new_card


def rolodex_engine(card_limit, target_fields):
    """Iterates over a range to generate a list of strings that can be
    sent to file or to stdout and which constitute a valid vcard file.
    Most programs that read vcards can accept a file that contains
    multiple vcards - all you have to do is concatenate them."""
    card_engine = CardFiller(first_names, last_names, streets, orgs, titles, phones, emails)
    # card_engine.prepare()
    rolodex = []
    for i in range(1, card_limit + 1):
        new_card = card_engine.fill_card(target_fields, i)
        for line in new_card:
            rolodex.append(line)
    return rolodex

################################### Execution ##################################

def vcf_card(obj):
    card_limit = 1
    card_export_file = obj.user.user.username + ".vcf"

    first_names.append(obj.user.user.first_name)
    last_names.append(obj.user.user.last_name)
    streets.append(obj.address1)
    phones.append(obj.user.mobile)
    emails.append(obj.user.user.email)
    if(obj.company):
        orgs.append(obj.company.name)
    else:
        orgs.append("")
    titles.append(obj.profession)

    with open("./%s" % card_export_file, "w") as rolodex_file:
        rolodex = rolodex_engine(card_limit, target_fields)
        for c in rolodex:
            rolodex_file.write(c)
            rolodex_file.write("\n")
    return card_export_file
