from enum import Enum

# not all opcode types are currently in use
class Op(Enum):
	ADDPTR = 1
	ADDMEM = 2
	SETMEM = 3
	PUTCHR = 4
	GETCHR = 5
	OPAREN = 6
	CPAREN = 7

class Instruction:
	def __init__(self, op, n=None, offset=0):
		self.op = op
		self.n = n # multipurpose "argument"
		self.offset = offset # effective memory offset (currently unused)
	
	def __str__(self):
		output = "OP:	{}\n".format(self.op)
		output += "n:	{}\n".format(self.n)
		output += "offset:	{}\n".format(self.offset)
		return output
