from ir import Op

header = """\
	// Assemble with
	// gcc source.s
	
	.intel_syntax noprefix
	.global main
	.text
main:
	mov	edi, 30000
	mov	rsi, 1
	call	calloc@plt
	mov	rbx, rax
"""

end = "ret\n"

# >/<
incptr = "	inc	rbx\n"
decptr = "	dec	rbx\n"
addptr = "	add	rbx, {}\n"

# +/-
incmem = "	inc	BYTE PTR [rbx+{}]\n"
decmem = "	dec	BYTE PTR [rbx+{}]\n"
addmem = "	add	BYTE PTR [rbx+{}], {}\n"
setmem = "	mov	BYTE PTR [rbx+{}], {}\n"

# .
putchr = """\
	mov	edi, [rbx+{0}]
	call	putchar@plt
"""

#,
getchr = """\
	call	getchar@plt
	mov	BYTE PTR [rbx+{0}], al
"""

# [
oparen = """\
	cmp	BYTE PTR [rbx], 0
	jz	end_{0}
start_{0}:
"""

# ]
cparen = """\
	cmp	BYTE PTR [rbx], 0
	jnz	start_{0}
end_{0}:
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
