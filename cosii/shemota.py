MAX = 2 ** 4
start = 0

base = 'b'
width = 4


def main():
    with open('input_vectors.txt', 'w') as file:
        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            A = in_res[9:]
            B = in_res[3:9]
            s1 = in_res[2]
            s0 = in_res[1]
            opt = in_res[0]

            Y = 0
            oper = 0
            int_A = int(A, 2)
            int_B = int(B, 2)

            if opt == '0':
                if s0 == '0' and s1 == '0':
                    Y = A
                    if int_A == 0:
                        oper = 1
                elif s0 == '0' and s1 == '1':
                    Y = B
                    if int_B == 0:
                        oper = 1
                elif s0 == '1' and s1 == '0':
                    Y = int_A & int_B
                    Y = f'{Y: {6}{base}}'.replace(' ', '0')
                    oper = 'Z'
                elif s0 == '1' and s1 == '1':
                    Y = '0' * 6
                    oper = '0'
            else:
                if s0 == '0' and s1 == '0':
                    Y = ''.join(['0' if i == '1' else '1' for i in A])
                    if int_A == 0:
                        oper = 1
                elif s0 == '0' and s1 == '1':
                    Y = ''.join(['0' if i == '1' else '1' for i in B])
                    if int_B == 0:
                        oper = 1
                elif s0 == '1' and s1 == '0':
                    Y = int_A & int_B
                    Y = f'{Y: {6}{base}}'.replace(' ', '0')
                    Y = ''.join(['0' if i == '1' else '1' for i in Y])
                    oper = 'Z'
                elif s0 == '1' and s1 == '1':
                    Y = 'Z' * 6
                    oper = 'Z'

            out_res = f'{oper}{Y[-6:]}'
            # out_res = f'{oper}{"".join([i for i in Y[-1::-1]])}'
            file.write(f'{in_res} {out_res}\n')


def main_2():
    with open('input_vectors.txt', 'w') as file:
        mr = 0
        pl = 0
        cpu = 0
        cpd = 0
        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{cpu}{0}{in_res}\n')
            file.write(f'{mr}{pl}{cpu}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{cpd}{in_res}\n')
            file.write(f'{mr}{pl}{1}{cpd}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{0}{in_res}\n')
            file.write(f'{mr}{pl}{1}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{1}{in_res}\n')
            file.write(f'{mr}{pl}{1}{0}{in_res}\n')

        mr = 1
        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{cpu}{0}{in_res}\n')
            file.write(f'{mr}{pl}{cpu}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{cpd}{in_res}\n')
            file.write(f'{mr}{pl}{1}{cpd}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{0}{in_res}\n')
            file.write(f'{mr}{pl}{1}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{1}{in_res}\n')
            file.write(f'{mr}{pl}{1}{0}{in_res}\n')

        pl = 1
        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{cpu}{0}{in_res}\n')
            file.write(f'{mr}{pl}{cpu}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{cpd}{in_res}\n')
            file.write(f'{mr}{pl}{1}{cpd}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{0}{in_res}\n')
            file.write(f'{mr}{pl}{1}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{1}{in_res}\n')
            file.write(f'{mr}{pl}{1}{0}{in_res}\n')

        mr = 0
        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{cpu}{0}{in_res}\n')
            file.write(f'{mr}{pl}{cpu}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{cpd}{in_res}\n')
            file.write(f'{mr}{pl}{1}{cpd}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{0}{in_res}\n')
            file.write(f'{mr}{pl}{1}{1}{in_res}\n')

        for num in range(MAX):
            in_res = f'{num:{width}{base}}'.replace(' ', '0')

            file.write(f'{mr}{pl}{0}{1}{in_res}\n')
            file.write(f'{mr}{pl}{1}{0}{in_res}\n')


if __name__ == '__main__':
    # main()
    main_2()
