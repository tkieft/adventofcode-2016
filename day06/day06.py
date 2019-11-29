import sys

def most_frequent(letters):
    return max(set(letters), key=letters.count)

def least_frequent(letters):
    return min(set(letters), key=letters.count)

def day06(filename):
    with open(filename) as f:
        messages = [line.rstrip() for line in f if line]

    message_len = len(messages[0])
    print(''.join([most_frequent([message[i] for message in messages]) for i in range(message_len)]))
    print(''.join([least_frequent([message[i] for message in messages]) for i in range(message_len)]))


if __name__ == "__main__":
    day06(sys.argv[1])