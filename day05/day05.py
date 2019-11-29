import hashlib
import sys

def hash(door_id, index):
    return hashlib.md5((door_id + str(index)).encode('ascii')).hexdigest()

def day05(door_id):
    password1 = ""
    password2 = ["" for i in range(8)]
    index = 0

    while "" in password2:
        h = hash(door_id, index)
        if h.startswith("00000"):
            # Part 1
            if len(password1) < 8:
                password1 += h[5]

            # Part 2
            if h[5] < '8':
                pos = int(h[5])
                if password2[pos] == "":
                    password2[pos] = h[6]
        index += 1

    print(password1)
    password2 = ''.join(password2)
    print(password2)

if __name__ == "__main__":
    day05(sys.argv[1])
