# branflakes-ng
An improved version of my older project "branflakes", an optimising brainfuck compiler.

My original [branflakes](https://github.com/DavidBuchanan314/branflakes) project was written in C,
and it compiled brainfuck to in-memory machine code before executing it. The code was a complete mess,
the optimising passes were incredibly complex to understand, and as a result there were several
obscure bugs which I never tracked down.

`branflakes-ng` attempts to fix these issues. The brainfuck code is converted into a relatively
flexible Intermediate Representation, which optimisations are then performed on.

Finally, one of several backends is chosen to generate output code, whether it be x86_64 assembly
or C source code.

## Performance

|          | [Beef](http://kiyuko.org/software/beef) | [copy.sh](https://copy.sh/brainfuck/) | Branflakes | branflakes-ng x86\_64 asm | branflakes-ng compiled c | [Tritium](https://github.com/rdebath/Brainfuck) |
|----------|-----------------------------------------|---------------------------------------|------------|---------------------------|--------------------------|-------------------------------------------------|
| mandel.b | 4m36.388s                               | 0m3.99s                               | 0m2.279s   | 0m1.690s                  | 0m1.538s                 | 0m1.084s                                        |

## TODO

- Optimise multiplications
