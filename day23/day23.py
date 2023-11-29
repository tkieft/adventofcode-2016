import sys


class Computer:
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    instructions: list[list[str]]

    def execute(self, pc: int) -> int:
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
        elif opcode == "tgl":
            offset = self.registers[operand]
            if pc + offset in range(0, len(self.instructions)):
                tgt_opcode, tgt_operand = self.instructions[pc + offset]
                if tgt_opcode == "inc":
                    self.instructions[pc + offset] = ["dec", tgt_operand]
                elif tgt_opcode == "dec" or tgt_opcode == "tgl":
                    self.instructions[pc + offset] = ["inc", tgt_operand]
                elif tgt_opcode == "jnz":
                    self.instructions[pc + offset] = ["cpy", tgt_operand]
                elif tgt_opcode == "cpy":
                    self.instructions[pc + offset] = ["jnz", tgt_operand]
        else:
            raise ValueError(f"Improper opcode {opcode}")

        return 1

    def run(self, filename: str):
        with open(filename) as f:
            self.instructions = [
                line.strip().split(maxsplit=1) for line in f.readlines()
            ]

        pc = 0
        while pc < len(self.instructions):
            pc += self.execute(pc)


def day23(filename: str):
    c = Computer()
    c.registers["a"] = 7
    c.run(filename)
    print(c.registers["a"])

    c = Computer()
    c.registers["a"] = 12
    c.run(filename)
    print(c.registers["a"])


if __name__ == "__main__":
    day23(sys.argv[1])
