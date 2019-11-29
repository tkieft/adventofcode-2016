import itertools
import re
import sys

IPADDR_FORMAT = re.compile(r"\w+")
ABBA_FORMAT = re.compile(r"(?=(\w)(\w)\2\1)")
ABA_FORMAT = re.compile(r"(?=(\w)(\w)\1)")

def parse(ipaddr):
    supernets = []
    hypernets = []

    i = 0

    for net in re.finditer(IPADDR_FORMAT, ipaddr):
        if i % 2 == 0:
            supernets.append(net[0])
        else:
            hypernets.append(net[0])
        i += 1

    return (supernets, hypernets)

def has_abba(net):
    matches = ABBA_FORMAT.findall(net)
    for match in matches:
        if match[0] != match[1]:
            return True
    return False

def supports_tls(ipaddr):
    (supernets, hypernets) = parse(ipaddr)

    for h in hypernets:
        if has_abba(h):
            return False
    
    for s in supernets:
        if has_abba(s):
            return True

def supports_ssl(ipaddr):
    (supernets, hypernets) = parse(ipaddr)
    abas = list(itertools.chain.from_iterable(ABA_FORMAT.findall(s) for s in supernets))
    babs = list(itertools.chain.from_iterable(ABA_FORMAT.findall(h) for h in hypernets))

    for a in abas:
        if a[0] != a[1] and (a[1], a[0]) in babs:
            return True
    
    return False

def day07(filename):
    with open(filename) as f:
        ipaddrs = [line.rstrip() for line in f]

    print(len(list(filter(supports_tls, ipaddrs))))
    print(len(list(filter(supports_ssl, ipaddrs))))

if __name__ == "__main__":
    day07(sys.argv[1])
