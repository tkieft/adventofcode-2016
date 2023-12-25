import sys


class Computer:
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    instructions: list[list[str]]

    def execute(self, pc: int, output: list[int]) -> int:
        opcode, operand = self.instructions[pc]

        if opcode == "cpy":
            src, dest = operand.split()
            self.registers[dest] = (
                self.registers[src] if src in self.registers else int(src)
            )
        elif opcode == "inc":
            self.registers[operand] += 1
        elif opcode == "dec":
            self.registers[operand] -= 1
        elif opcode == "mul":
            x, y, d = operand.split()
            self.registers[d] += self.registers[x] * self.registers[y]
        elif opcode == "jnz":
            x, y = operand.split()
            if (int(x) if x.isdigit() else self.registers[x]) != 0:
                return self.registers[y] if y in self.registers else int(y)
        elif opcode == "out":
            output += [int(operand) if operand.isdigit() else self.registers[operand]]
        else:
            raise ValueError(f"Improper opcode {opcode}")

        return 1

    def run(self, filename: str):
        with open(filename) as f:
            self.instructions = [
                line.strip().split(maxsplit=1) for line in f.readlines()
            ]

        pc = 0
        output = []
        while pc < len(self.instructions) and len(output) < 100:
            pc += self.execute(pc, output)
            if len(output) > 0 and (
                len(output) == 1
                and output[0] != 0
                or len(output) > 1
                and output[-1] == output[-2]
            ):
                return False
            if len(output) == 100:
                break

        return True


def day25(filename: str):
    x = 0
    while True:
        c = Computer()
        c.registers["a"] = x
        if c.run(filename):
            break
        x += 1
    print(x)


if __name__ == "__main__":
    day25(sys.argv[1])
