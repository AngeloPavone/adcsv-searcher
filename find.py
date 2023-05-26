# input csv file should follow this format
# DistinguishedName,Enabled,GivenName,Name,ObjectClass,ObjectGUID,SamAccountName,SID,Surname,UserPrincipalName

import csv
import re

input_file = 'ad_titles.csv'
output_file = 'new.csv'

dn_string = ""


class DistinguishedName:
    def __init__(self, common_name, organizational_unit_name, street_address):
        self.common_name = common_name
        self.organizational_unit_name = organizational_unit_name
        self.street_address = street_address


class User:
    def __init__(self, distinguished_name, enabled, given_name, name, object_class, object_GUID, sam_account_name, sid, surname, title, user_principal_name):
        self.distinguished_name = distinguished_name
        self.enabled = enabled
        self.given_name = given_name
        self.name = name
        self.object_class = object_class
        self.object_GUID = object_GUID
        self.sam_account_name = sam_account_name
        self.sid = sid
        self.surname = surname
        self.title = title
        self.user_principal_name = user_principal_name


def parse_distinguished_name(dn_string) -> DistinguishedName | None:
    # match the OU= and DC= and CN= and capture the following string until the next ","
    pattern = r"(?:OU|DC|CN)=([^,]+)"
    matches = re.findall(pattern, dn_string)
    organizational_unit_name = ""

    # if there is a match parse out DistinguishedName with different lengths to ensure that we get the OU we want
    if matches:
        street_address = []
        common_name = matches[0]
        if len(matches) == 4:
            organizational_unit_name = matches[1]
        if len(matches) == 5:
            organizational_unit_name = matches[1]
        if len(matches) == 6:
            organizational_unit_name = matches[1]
            street_address = matches[2]
        if len(matches) == 7:
            organizational_unit_name = matches[1]
            street_address = matches[2]

        dn = DistinguishedName(
            common_name, organizational_unit_name, street_address)
        return dn

    return None


def parse_csv(input_file) -> list:
    users = []

    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        # read in the rows of the csv into a class
        for row in csv_reader:
            dn_string = row[0]
            dn = parse_distinguished_name(dn_string)

            if dn:
                enabled = row[1]
                given_name = row[2]
                name = row[3]
                object_class = row[4]
                object_guid = row[5]
                sam_account_name = row[6]
                sid = row[7]
                surname = row[8]
                title = row[9]
                user_principal_name = row[10]

                user = User(dn, enabled, given_name, name, object_class,
                            object_guid, sam_account_name, sid, surname, title, user_principal_name)
                users.append(user)

    return users


def main():
    users = parse_csv(input_file)
    count = 0

    # how you want to search the output you can then pipe the output into a .txt file using the > operator in your terminal
    for user in users:
        if (("Receptionist" in user.title) or ("Billing" in user.distinguished_name.organizational_unit_name)) and user.enabled == "True":
            count += 1
            print("User Information:")
            print("CN:", user.distinguished_name.common_name)
            print("OU:", user.distinguished_name.organizational_unit_name)
            print("Site:", user.distinguished_name.street_address)
            print("enabled:", user.enabled)
            print("givenName:", user.given_name)
            print("name:", user.name)
            print("objectClass:", user.object_class)
            print("objectGUID:", user.object_GUID)
            print("samAccountName:", user.sam_account_name)
            print("sid:", user.sid)
            print("surname:", user.surname)
            print("title:", user.title)
            print("userPrincipalName:", user.user_principal_name)
            print("---------------------")
    print("Count: ", count)


if __name__ == "__main__":
    main()
