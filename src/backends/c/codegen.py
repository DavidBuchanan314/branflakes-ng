from ir import Op

header = """\
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {
	uint8_t * ptr = calloc(30000, sizeof(*ptr));
"""

end = """\
	return 0;
}
"""

# >/<
incptr = "	ptr++;\n"
decptr = "	ptr--;\n"
addptr = "	ptr	+= {};\n"

# +/-
incmem = "	ptr[{}]++;\n"
decmem = "	ptr[{}]--;\n"
addmem = "	ptr[{}] += {};\n"
setmem = "	ptr[{}] = {};\n"

# .
putchr = """\
	putchar(ptr[{}]);
"""

#,
getchr = """\
	ptr[{}] = getchar();
"""

# [
oparen = """\
	while (*ptr) {{ // loop {}
"""

# ]
cparen = """\
	}} //  end loop {}
"""

def generate(instructions):
	output = []
	output.append(header)
	for inst in instructions:
		op = inst.op
		
		if op == Op.ADDPTR:
			if inst.n == 1:
				output.append(incptr)
			elif inst.n == -1:
				output.append(decptr)
			elif inst.n == 0:
				pass
			else:
				output.append(addptr.format(inst.n))
		
		elif op == Op.ADDMEM:
			if inst.n == 1:
				output.append(incmem.format(inst.offset))
			elif inst.n == -1:
				output.append(decmem.format(inst.offset))
			elif inst.n == 0:
				pass
			else:
				output.append(addmem.format(inst.offset, inst.n))
		
		elif op == Op.SETMEM:
			output.append(setmem.format(inst.offset, inst.n))
		
		elif op == Op.PUTCHR:
			output.append(putchr.format(inst.offset))
		
		elif op == Op.GETCHR:
			output.append(getchr.format(inst.offset))
		
		elif op == Op.OPAREN:
			output.append(oparen.format(inst.n))
		
		elif op == Op.CPAREN:
			output.append(cparen.format(inst.n))
		
		else:
			exit("UNIMPLEMENTED:\n" + str(inst))
	
	output.append(end)
	return "".join(output)
