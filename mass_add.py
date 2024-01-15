from getpass import getpass
from Crypto.Util import Counter
import manager

def read(file : str):
    with open(file, "r", encoding="utf-8") as f:
        data = f.readlines()
    for i in range(len(data)-1):
        data[i] = data[i][:-1]
    for i in range(len(data)//4):
        data[i] = [data[i], data[i+1], data[i+2], data[i+3]]
        for _ in range(3):
            data.pop(i+1)
    return data

def add_data(data : list, seed):
    for e in data:
        ctr = Counter.new(128)
        length, encoded = manager.encode_data(e[0], e[1], e[2], e[3], seed, ctr)
        manager.add_data(encoded, length)

def main():
    seed = None
    while not seed:
        try:
            seed = bytes(getpass("key: "), encoding="utf-8")
        except ValueError:
            print("Dies ist keine valide Eingabe. Ein Seed ist vom Typ bytes mit 16 Elementen.")
    
    data = read("passwords.txt")
    add_data(data, seed)

if __name__ == "__main__":
    main()