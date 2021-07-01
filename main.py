import operator as op
import random
from fpdf import FPDF
from pylatex import Document, Command, Enumerate, NoEscape
from pylatex.base_classes import Environment

OP = [
    ("+", op.add),
    ("-", op.sub),
    ("*", op.mul),
    ("/", op.truediv),
    ("**", op.pow)
]

MIN = 0 # min number in equation
MAX = 20 # max number in equation (division overrules this but final answer will be within range)
NUM = 5 # number of numbers in equation
NUMP = 10 # number of problems
MAXPOW = 2 # maximum exponent value
EXP = False # if exponents should be in the equation
NEG = True # if numbers can be negative

# complex question
def gen_cq(min, max, prevq, preva, num):
    num -= 1
    sym, func = random.choice(OP)
    n2 = random.randint(min, max)

    # random choice to make number negative if NEG True, 0 to make neg, 1 to not
    if NEG and random.randint(0, 1) == 0: n2 *= -1

    while (sym == "/" and preva == 0) or (sym == "**" and not EXP): sym, func = random.choice(OP)
    if sym == "/":
        while n2 == 0: n2 = random.randint(min, max)
        n3 = preva * n2
        if " " in prevq: q = "{} {} ({})".format(int(n3), sym, prevq)
        else: q = "{} {} {}".format(int(n3), sym, prevq)
    elif sym == "**":
        if " " in prevq: q = "({}){}{}".format(prevq, sym, random.randint(0, MAXPOW))
        else: q = "{}{}{}".format(prevq, sym, random.randint(0, MAXPOW))
    elif n2 < 0:
        q = "{} {} ({})".format(prevq, sym, n2)
    else:
        q = "{} {} {}".format(prevq, sym, n2)

    # random choice to add parentheses around the given q pair, 0 to add, 1 to not
    # addP = random.randint(0, 1)
    # if addP == 0: q = "({})".format(q)

    if num == 0:
        return q
    else:
        #print("{} = {}".format(q.replace("**", "^"), int(eval(q))))
        return gen_cq(min, max, q, eval(q), num)

# simple 2 number basic arithmetic equation
def gen_q(min, max):
    sym, func = random.choice(OP)
    n1, n2 = random.randint(min, max), random.randint(min, max)
    if sym == "/":
        if n2 == 0:
            while n2 == 0: n2 = random.randint(min, max)
        n1 *= n2
    q = "{} {} {}".format(n1, sym, n2)
    ans = int(func(n1, n2))
    return q, ans

class Alignat(Environment):
    aligns = 2
    escape = False
    numbering = False
    content_separator = "\n"

def main():
    # for i in range(5):
    #     q, ans = gen_q(0, 50)
    #     print("{} = {}".format(q, ans))
    qs = []
    anss = []

    for i in range(NUMP):
        start = random.randint(MIN, MAX)
        q = gen_cq(MIN, MAX, str(start), start, NUM)
        qs.append(q.replace("**", "^"))
        anss.append(int(eval(q)))

    ## LaTeX Generation
    doc = Document('basic')

    doc.preamble.append(Command('title', 'Problem Set'))
    if EXP: doc.preamble.append(Command('author', 'Exponents'))
    else: doc.preamble.append(Command('author', 'For Grace'))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Alignat()):
        for i in range(NUMP):
            line = "%d. \\(%s\\) = \n" % (i + 1, qs[i])
            doc.append(line)
            doc.append(NoEscape(r'\vspace{2.25in}'))

    doc.append(NoEscape(r'\newpage'))

    with doc.create(Alignat()):
        for i in range(NUMP):
            line = "%d. %s\n" % (i + 1, anss[i])
            doc.append(line)

    if EXP: doc.generate_pdf('exp', clean_tex=False, compiler='pdflatex')
    else: doc.generate_pdf('graceset', clean_tex=False, compiler='pdflatex')


    ## FPDF Generation
    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font('Arial', 'B', 16)
    # pdf.multi_cell(40, 10, '\nProblem Set')
    # pdf.set_font('Arial', '', 12)
    # for i in range(NUMP):
    #     pdf.multi_cell(190, 10, ' %d) %s = \n\n\n' % (i + 1, qs[i]), 1)
    # pdf.add_page()
    # pdf.set_font('Arial', 'B', 16)
    # pdf.multi_cell(40, 10, '\nAnswers')
    # pdf.set_font('Arial', '', 12)
    # for i in range(NUMP):
    #     pdf.multi_cell(40, 10, ' %d) %d' % (i + 1, anss[i]))
    # pdf.output('set1.pdf', 'F')

if __name__ == '__main__':
    main()
