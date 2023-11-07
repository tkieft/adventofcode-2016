import sys


class Computer:
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}

    def execute(self, instruction: str) -> int:
        opcode, operand = instruction.split(maxsplit=1)

        if opcode == "cpy":
            src, dest = operand.split()
            self.registers[dest] = int(src) if src.isdigit() else self.registers[src]
        elif opcode == "inc":
            self.registers[operand] += 1
        elif opcode == "dec":
            self.registers[operand] -= 1
        elif opcode == "jnz":
            x, y = operand.split()
            if (int(x) if x.isdigit() else self.registers[x]) != 0:
                return int(y)
        else:
            raise ValueError(f"Improper opcode {opcode}")

        return 1

    def run(self, filename: str):
        with open(filename) as f:
            instructions = [line.strip() for line in f.readlines()]

        pc = 0
        while pc < len(instructions):
            pc += self.execute(instructions[pc])


def day12(filename: str):
    # Part 1
    c = Computer()
    c.run(filename)
    print(c.registers["a"])

    # Part 2
    c = Computer()
    c.registers["c"] = 1
    c.run(filename)
    print(c.registers["a"])


if __name__ == "__main__":
    day12(sys.argv[1])
