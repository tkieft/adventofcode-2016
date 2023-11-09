import re
import sys
from hashlib import md5


class HashStorage:
    salt: str
    stretch: bool
    _storage: dict[int, str]

    def __init__(self, salt: str, stretch: bool):
        self.salt = salt
        self.stretch = stretch
        self._storage = {}

    def _generate(self, index: int):
        hash = md5(bytes(f"{self.salt}{index}", "utf8")).hexdigest()
        if self.stretch:
            for _ in range(2016):
                hash = md5(bytes(hash, "utf8")).hexdigest()
        return hash

    def get(self, index: int):
        if index not in self._storage:
            self._storage[index] = self._generate(index)
        return self._storage[index]


def find_index(salt: str, stretch: bool) -> int:
    hashes = HashStorage(salt, stretch)
    regex = re.compile(r"(.)\1\1+")

    found_keys = 0
    index = 0

    while True:
        if match := regex.search(hashes.get(index)):
            new_search = str(match.group(1)) * 5
            for i in range(index + 1, index + 1001):
                if new_search in hashes.get(i):
                    found_keys += 1
                    break

        if found_keys == 64:
            return index

        index += 1


def day14(salt: str):
    print(find_index(salt, False))
    print(find_index(salt, True))


if __name__ == "__main__":
    day14(sys.argv[1])
