

import random
import re
from keyword import iskeyword
import string

from tokenize import generate_tokens
from StringIO import StringIO

from ga import CrossoverGeneticAlgorithm


length = len
lowercase = lowercases = 'abcdefghijklmnopqrstuvwxyz'
uppercase = uppercases = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter = letters = lowercase + uppercase
digit = number = digits = numbers = '0123456789'
symbol = special = specials = specialcharacter = symbols = specialcharacters = \
         """~!@#$%^&*()_+|}{":?<>`-=[]\;',./"""
space = spaces = " "
character = characters = symbols+digits+letters
true = True
false = False



VARIABLE = 1
add_kw = ['None', "True", "False", 'true', 'false', "contains", "length",
          "lowercase", "lowercases", "uppercase", "uppercases", 'letter',
          'letters', 'lowercase', 'uppercase', 'digit', 'number', 'digits',
          'numbers', 'symbol', 'specialcharacter', 'symbols',
          'specialcharacters', 'space', 'spaces', 'character',
          'characters', 'range', 'does_not_repeat', 'no', 'special',
          'specials']

def is_keyword(varname):
    return iskeyword(varname) or varname in add_kw
    

def contains(container,lower = None, upper = None, containee = characters, v=False):

    if lower is None:
        lower = -1
    if upper is None:
        upper = 10**100


    count = 0
    for c in container:
        if v:
            print ord(c)
        if c in containee:
            if v:
                print c, "in", containee

            count += 1
            if count > upper:
                return False
    #print lower ,"<=", count, "<=" ,upper
    return lower <= count 

def does_not_repeat(something):
    for i in xrange(len(something)-1):
        if something[i] == something[i+1]:
            return False
    return True

def preprocess(conds):
    new_conds = []

    for cond in conds:
        cond = cond.strip()
        sp = cond.split("contains")

            
        if len(sp) == 1:
            sp2 = cond.split(" does not repeat")
            if len(sp2) == 1:
                synth_cond = cond
            else:
                synth_cond = "does_not_repeat(%s)" % (sp2[0])

        elif len(sp) > 2:
            raise SyntaxError, "Condition can't consist of more than one \
                                    'contains' statement"
        else:
            cond_sfx = sp[1]
            r = re.compile("[0-9]+ +to +[0-9]+")
            fall = r.findall(cond_sfx)
            if len(fall) == 0:
                nr = re.compile(" [0-9]+ ")
                fall2 = nr.findall(cond_sfx)
                if len(fall2) == 1:
                    lwr = fall2[0]
                    upr = None
                    containee = cond_sfx.replace(lwr,"")
                elif 'no' in cond_sfx:
                    lwr = 0
                    upr = 0
                    containee = cond_sfx.replace("no","")
                    
                    
            elif len(fall) == 1:
                reinsh = fall[0]
                nr = re.compile("[0-9]+")
                lwr, upr = tuple(nr.findall(reinsh))
                containee = cond_sfx.replace(reinsh,"")
            else:
                raise SyntaxError, "Condition can't contain more than one \
                                        range (N to M)"
            
            synth_cond = "contains(%s,%s,%s,%s)" % (sp[0], lwr, upr, containee)
        new_conds.append(synth_cond)

    return new_conds


type_hints = ['length','contains',"'","repeat", "lowercase","uppercase",
              "letter", "digit", "number", "symbol", "specialcharacter",
              "space", "character"]



def get_types(conds):

    d = {}

    for cond in conds:
        for ttype, varname, _, _, _ in generate_tokens(StringIO(cond).readline):
            if ttype == VARIABLE and not is_keyword(varname):
                for hint in type_hints:
                    if hint in cond:
                        print "Our guess is that",varname,"is a string."
                        d[varname] = str
                        break
                else:
                    print "Our guess is that",varname,"is an integer."
                    d[varname] = int

    return d
                    


def get_random_string(min_length=3,max_length=10, chrs=[]):
    rlength = random.randint(min_length, max_length)

    addon = ''.join(str(list(chrs))[1:-1].replace("'","").\
                    replace(",","").replace(" ","").replace('"',""))*100


    res = ''.join(random.sample(
        characters+addon,
        rlength)
        )
    return res

def range_guess(conds):
    final = []
    r = re.compile("[0-9]+")
    for cond in conds:
        final += [int(x) for x in r.findall(cond)]

    if len(final) is 0:
        return 0,100
    mmin, mmax = min(final), max(final)
    delta = (mmax - mmin) or 5
        
    
    return mmin - delta, mmax + delta

def str_guess(conds):
    final = []
    chrs = set()
    r = re.compile("""\'[a-zA-z]+\'""")
    r2 = re.compile("""[0-9]+""")
    for cond in conds:
        faaa = r.findall(cond)
        final += [len(x) for x in faaa ]
        for occ in faaa:
            for c in occ:
                chrs.add(c)

    if len(final) is 0:
        return 0,30,chrs

    mmin, mmax = min(final), max(final)
    delta = (mmax - mmin) or 5
        
    mmmin = (mmin - delta) if mmin >= delta else 0
    mmmax = mmax + delta
    return mmmin, mmmax , chrs


def get_data(conds):
    """ Generates test data from conditions """

    # flatten input
    if type(conds) is str:
        conds = [conds]
    elif type(conds) is not list:
        raise TypeError, "Conditions must be a string or list of strings, but \
                received %s" % type(conds)


    conds = preprocess(conds)
    typedict = get_types(conds)

    a,b = range_guess(conds)

    sa, sb, chrs= str_guess(conds)

    def random_chromosome():
        c = dict()
        for (name, tyype) in typedict.items():
            if tyype is int:
                c[name] = random.randint(a,b)
            elif tyype is str:
                c[name] = get_random_string(sa, sb, chrs)
            else:
                raise TypeError, "chromosome shouldn't contain \
                    element of type %s" % tyype
        return c


    def only_ascii(chromo):
        for k,v in chromo.items():
            if typedict[k] == str:
                for c in v:
                    if c not in string.printable:
                        return False
        return True
    
    def fitness(chromosome):
        total = 0
        env = chromosome.copy()
        for k,v in globals().items():
            env[k] = v
        for k,v in locals().items():
            env[k] = v

        for cond in conds:
            try:
                result = eval(cond, env)
            except IndexError:
                result = False
                
            if result is True:
                total += 1
        if not only_ascii(chromosome):
            return total/2
        return total**2


    def chrom2bin(chromo):
        byte = ''
        for k, v in chromo.items():
            if type(v) is str:
                for c in v:
                    byte += format(ord(c),'08b')
                byte += '00000000'
            else:
                byte += format(v,'08b')
        return byte

    def bin2chrom(byte_str):
        d = dict()
        i = 0
        for name, tyype in typedict.items():
            if tyype is int:
                try:
                    d[name] = int(byte_str[i*8:(i+1)*8], 2)
                except:
                        d[name] = 0
                i += 1
            else:
                s = ''
                while(True):
                    chunk = byte_str[i*8:(i+1)*8]
                    if len(chunk) is not 8:
                        break
                    i += 1
                    if chunk == '00000000':
                        break
                    try:
                        s += chr(int(chunk, 2))
                    except:
                        s += '0'

                d[name] = s
        return d
                    
            
            
            

    def mate(chromo1, chromo2):
        s1 = chrom2bin(chromo1)
        s2 = chrom2bin(chromo2)

        crossover_point1 = random.randint(0,(len(s1)-1)/8)
        crossover_point2 = random.randint(0,(len(s2)-1)/8)

        child_bin = s1[:crossover_point1] + s2[crossover_point2:]
        
        return bin2chrom(child_bin)

    MU = 0.05
    def mutate(chromosome):
        s = chrom2bin(chromosome)
        new_s = ''

        for c in s:
            if random.random() < MU:
                new_s += '0' if c == '1' else '1'
            else:
                new_s += c
            
        
        return chromosome

    ga = CrossoverGeneticAlgorithm(len(conds)**2, fitness,
            random_chromosome, mate, mutate, max_generations = 50,
            population_size = 250)

    best, best_fitness = ga.run()
    time = 0
    fail_messages = [
        "We couldn't find a solution, let us try again...",
        "Yikes! This one seems a hard one. Let's try again.",
        "Hmm... This is strange, we still can't find a solution...",
        "OK, this is our last chance, I swear! We'll try something new."
        ]
    while(best_fitness != len(conds)**2):
        print fail_messages[time]
        if time == 3:
            ga = CrossoverGeneticAlgorithm(len(conds)**2, fitness,
                    random_chromosome, mate, mutate, max_generations = 100,
                    population_size = 250)
        best, best_fitness = ga.run()
        time += 1
        if time == 4:
            break

    if time == 4 and best_fitness != len(conds)**2:
        print "I'm afraid there might be no solution to this constraints"
        print "Anyway, this is the best that I could manage to get."
        return best
    print "Yippie! We found data that satisfies all the constraints!"
    return best





if __name__ == "__main__":
    conds = [

            "name contains 4 to 18 letters",
            "name contains no special+number",
            "name[0] in uppercase",

            "password contains 1 number",
            "password does not repeat",
            "password contains 10 to 30 characters",
            ]

    data = get_data(conds)
    print "Values generated:"
    for k,v in data.items():
        print k+":", v
    


