import sys
import os
import importlib
from ir import *

os.chdir(sys.path[0])

available_backends = sorted(os.listdir("backends"))

if len(sys.argv) != 2:
	print("USAGE: python3 {} BACKEND < source.bf > output".format(sys.argv[0]))
	print("")
	print("\n\t".join(["Available backends:"] + available_backends))
	exit()

backend = sys.argv[1]

if backend not in available_backends:
	exit("Backend {} is not available.".format(repr(backend)))

# This is kinda hacky...
codegen = importlib.import_module("backends.{}.codegen".format(backend))

instructions = []

# parse input
for char in sys.stdin.read():
	if char == ">":
		instructions.append(Instruction(Op.ADDPTR, 1))
	elif char == "<":
		instructions.append(Instruction(Op.ADDPTR, -1))
	elif char == "+":
		instructions.append(Instruction(Op.ADDMEM, 1))
	elif char == "-":
		instructions.append(Instruction(Op.ADDMEM, -1))
	elif char == ".":
		instructions.append(Instruction(Op.PUTCHR))
	elif char == ",":
		instructions.append(Instruction(Op.GETCHR))
	elif char == "[":
		instructions.append(Instruction(Op.OPAREN))
	elif char == "]":
		instructions.append(Instruction(Op.CPAREN))


# assign a unique id to each bracket pair:
stack = []
n = 0
for i in range(len(instructions)):
	if instructions[i].op == Op.OPAREN:
		instructions[i].n = n
		n += 1
		stack.append(i)
	elif instructions[i].op == Op.CPAREN:
		if not stack:
			exit("FATAL: Unexpected symbol ]")
		instructions[i].n = instructions[stack.pop()].n

if stack:
	exit("FATAL: Unexpected symbol EOF") # maybe these errors will make people think my parser is fancier than it is ;)


# collapse repeated ADDMEM/ADDPTRs:
i = 0
while i < len(instructions)-1:
	if instructions[i].op == instructions[i+1].op == Op.ADDMEM \
		or instructions[i].op == instructions[i+1].op == Op.ADDPTR:
		instructions[i].n += instructions.pop(i+1).n
	else:
		i += 1


# Replace [+], [-] with SETMEM
i = 0
while i < len(instructions)-3:
	if instructions[i].op == Op.OPAREN and instructions[i+1].op == Op.ADDMEM and instructions[i+2].op == Op.CPAREN:
		# XXX: If, for example [++] was encountered, it may or may not halt. We ignore these scenarios.
		instructions.pop(i+1)
		instructions.pop(i+1)
		n = 0
		if instructions[i+1].op == Op.ADDMEM:
			n = instructions[i+1].n
			instructions.pop(i+1)
		instructions[i] = Instruction(Op.SETMEM, n)
	i += 1


# Use local offsets where possible
i = 0
offset = 0
while i < len(instructions):
	op = instructions[i].op
	if op == Op.ADDPTR:
		offset += instructions[i].n
		instructions.pop(i)
	elif op == Op.OPAREN or op == Op.CPAREN:
		instructions.insert(i, Instruction(Op.ADDPTR, offset))
		offset = 0
		i += 2
	else:
		instructions[i].offset = offset
		i += 1

print(codegen.generate(instructions))
