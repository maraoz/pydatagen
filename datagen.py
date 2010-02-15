

import random
import re

from ga import CrossoverGeneticAlgorithm


length = len
lowercase = lowercases = 'abcdefghijklmnopqrstuvwxyz'
uppercase = uppercases = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter = letters = lowercase + uppercase
digit = number = digits = numbers = '0123456789'
symbol = specialcharacter = symbols = specialcharacters = \
         """~!@#$%^&*()_+|}{":?<>`-=[]\;',./"""
space = spaces = " "
characters = symbols+digits+letters



def contains(container,lower = None, upper = None, containee = characters):
    lower = lower or -1
    upper = upper or 10**100

    count = 0
    for c in container:
        if c in containee:
            count += 1
    return lower < count < upper

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
                lwr = nr.findall(cond_sfx)[0]
                upr = None
                containee = cond_sfx.replace(lwr,"")
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

def get_types(conds):
    return {'x': int, 'sex': str, 'y': int, 'password': str, "age": int}

def get_random_string(min_length=3,max_length=10, chrs=[]):
    rlength = random.randint(min_length, max_length)

    addon = ''.join(str(list(chrs))[1:-1].replace("'","").replace(",","").replace(" ","").replace('"',""))*100


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
        
    def fitness(chromosome):
        total = 0
        env = chromosome.copy()
        for k,v in globals().items():
            env[k] = v
        for k,v in locals().items():
            env[k] = v
        #env['contains'] = contains
        for cond in conds:
            try:
                result = eval(cond, env)
            except IndexError:
                print "Skipping index error in fitness evaluation"
                result = False
                
            if result is True:
                total += 1
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
            random_chromosome, mate, mutate, max_generations = 5,
            population_size = 250)

    best = ga.run()
    return best




if __name__ == "__main__":
    for x in preprocess([
        "password contains 1 letter",
        "password contains 1 number+symbol",
        "lala_popo contains 1 to 10 symbols",
        "loooooot contains 100000 to 20 ['M','x']"
        ]):
        print x
        print contains("llala",1,None,letter)
    


