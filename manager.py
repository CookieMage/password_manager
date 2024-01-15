import aes
from Crypto.Util import Counter
from getpass import getpass
import sys
from os.path import isfile

def encode_data(platform, account_user_name, account_mail, account_password, seed, counter):
    text = platform + ":"
    text += " Username: " + account_user_name + " Mail: " + account_mail
    text += " PW: " + account_password
    text = aes.encrypt(seed, text, counter)
    length = len(text)
    length = '{0:016b}'.format(length).encode()
    return length, text

def add_data(text, length, write_file = "passwords.bin"):
    with open(write_file, "ba") as f:
        f.write(length)
        f.write(text)

def read_data(read_file = "passwords.bin"):
    with open(read_file, "rb") as f:
        data = [f.read()]
    length = []
    segment = 0
    while len(data[0]) != 0:
        length.append(int(data[0][:16], 2))
        data.append(data[0][16:16+length[segment]])
        data[0] = data[0][16+length[segment]:]
        segment += 1
    data.pop(0)
    return data

def decode_data(data, seed, counter):
    text = aes.decrypt(seed, data, counter)
    return text.decode() # "iso-8859-1"

def add_entry(counter):
    platform = input("Für welche Plattform soll ein Eintrag erstellt werden?   ")
    account_user_name = input("Wie lautet der Account-Name?                             ")
    account_mail = input("Wie lautet die Account-Mail?                             ")
    account_password = input("Wie lautet das Account-Paswort?                          ")
    seed = input("Wie lautet der Verschlüsselungsseed?                     ")
    length, encoded = encode_data(platform, account_user_name, account_mail, account_password, seed, counter)
    add_data(encoded, length)

def search_entry(entry, seed, counter):
    entry = entry.lower()
    data = []
    headings = []
    data = read_data()
    for e in data:
        headings += [decode_data(e, seed, counter).split(":")[0]]
    no_hit = []
    for i,e in enumerate(headings):
        if entry not in e.lower():
            no_hit += [i]
    for e in reversed(no_hit):
        headings.pop(e)
        data.pop(e)

    for i,e in enumerate(data):
        data[i] = decode_data(e, seed, counter)

    for i,e in enumerate(headings):
        data[i] = data[i][len(e)+2:]

    while len(data) > 1:
        text = "The following entries have been found:\n"
        for i,e in enumerate(headings):
            text += f"    {i}) {e}\n"
        text += "Please choose one of these entries.\n"
        choice = input(text)
        try:
            data = [data[int(choice)]]
        except (ValueError, IndexError):
            for i,e in enumerate(headings):
                if e.lower() == choice.lower():
                    data = [data[i]]
                    headings = [headings[i]]
                    break
            if len(data) > 1:
                print("The platform you meant could not be identified. Please try again.")

    if len(headings) == 0:
        raise IndexError

    return headings[0], data[0]



def decode_entry(entry, seed, counter):
    try:
        platform, data = search_entry(entry, seed, counter)
    except IndexError as exc:
        raise exc
    data = data.split()
    text = platform + ":"
    for i in range(0, 5, 2):
        text += "\n    " + data[i] + " " + data[i+1]
    text = "\n" + text + "\n"
    print(text)




def main():
    try:
        file = sys.argv[1]
    except IndexError:
        file = input("What file do you want to look at?\n")

    while not isfile(file):
        file = input("This file does not exist. Please enter a valid path.\n")

    directions = "If you want to quit, type 'quit'. Do you want to 'add' or 'read' an entry?\n"
    mode = input(directions).lower()
    ctr = Counter.new(128)
    while mode != "quit":
        if mode == 'read':
            platform = input("Which entry are you looking for?\n")
            seed = None
            while not seed:
                try:
                    seed = bytes(getpass("What is your key?\n"), encoding="utf-8")
                except ValueError:
                    print("Dies ist keine valide Eingabe. Ein Seed ist vom Typ bytes mit 16 Elementen.")
            try:
                decode_entry(platform, seed, ctr)
            except IndexError:
                print("\nThe platform you are looking for could not be found. Please try again.")
            mode = input(directions).lower()
        elif mode == 'add':
            platform = input("platform: ")
            account_user_name = input("user_name: ")
            account_mail = input("mail: ")
            account_password = input("password: ")
            seed = None
            while not seed:
                try:
                    seed = bytes(getpass("key: "), encoding="utf-8")
                except ValueError:
                    print("Dies ist keine valide Eingabe. Ein Seed ist vom Typ bytes mit 16 Elementen.")
            length, text = encode_data(platform, account_user_name, account_mail, account_password, seed, ctr)
            add_data(text, length)
            mode = input(directions).lower()
        else:
            mode = input("Command could not be found. " + directions).lower()

if __name__ == "__main__":
    main()
