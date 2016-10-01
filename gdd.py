
import random

# Declensions
DEF_ART_DECL = (("der", "den", "dem", "des"), ("das", "das", "dem", "des"), ("die", "die", "der", "der"), ("die", "die", "den", "der"))
STRONG_DET_DECL = (("er", "en", "em", "es"), ("es", "es", "em", "es"), ("e", "e", "er", "er"), ("e",  "e",  "en", "er"))
MIXED_DET_DECL =  (("",   "en", "em", "es"), ("",   "",   "em", "es"), ("e", "e", "er", "er"), ("e",  "e",  "en", "er"))

STRONG_ADJ_DECL = (("er", "en", "em", "en"), ("es", "es", "em", "en"), ("e", "e", "er", "er"), ("e",  "e",  "en", "er"))
MIXED_ADJ_DECL =  (("er", "en", "en", "en"), ("es", "es", "en", "en"), ("e", "e", "en", "en"), ("en", "en", "en", "en"))
WEAK_ADJ_DECL =   (("e",  "en", "en", "en"), ("e",  "e",  "en", "en"), ("e", "e", "en", "en"), ("en", "en", "en", "en"))

# Determiners
NUM = {"∅", "zwei", "drei", "vier"} # Invariable
ART_S = {"der", "dies", "jen", "welch", "jed", "manch", "solch"} # Strong declension
ART_M = {"ein", "mein", "dein", "sein", "ihr", "unser", "euer", "kein"} # Mixed declension
DET = ART_S | ART_M | NUM

# Adjectives
ADJ = {"weiß", "grau", "schwarz", "rot", "grün", "blau", "groß", "klein", "lang", "kurz", "gut", "neu", "jung", "alt", "schön", "gesund", "beste", "letzte", "stark", "schnell", "bestimmt", "froh", "komisch"}

# Nouns
NF = {("Nuss", "Nüsse"), ("Katze", "Katzen"), ("Hand", "Hände"), ("Kralle", "Krallen"),
         ("Haut", "Häute"), ("Mutter", "Mütter"), ("Pfote", "Pfoten"), ("Wand", "Wände"),
         ("Flasche", "Flaschen"), ("Fliege", "Fliegen"), ("Schlange", "Schlangen")}
NN = {("Pferd", "Pferde"), ("Wasser", "Wässer"), ("Ei", "Eier"), ("Ohr", "Ohren"),
         ("Auge", "Augen"), ("Buch", "Bücher"), "Feuer", ("Licht", "Lichter"),
         ("Haus", "Häuser"), ("Haar", "Haare"), ("Wildschwein", "Wildschweine")}
NM = {("Vogel", "Vögel"), ("Freund", "Freunde"), ("Hund", "Hunde"), ("Weg", "Wege"),
         "Dinosaurier", ("Geist", "Geiste"), ("Zahn", "Zähne"), ("Fuß", "Füße"),
         ("Apfel", "Äpfel"), ("Baum", "Bäume"), ("Schmetterling", "Schmetterlinge")}
NM_EN7 = {"Bär", "Drache", "Mensch", "Student"}

CASES = ("NOM", "ACC", "DAT", "GEN")
NUMS = ("SG", "PL") # Unused

def make_en7_pl(n):
    if n[-1] != 'e':
        n += 'e'
    return n + 'n'

def random_noun():
    n_nf = len(NF)
    n_nn = len(NN)
    n_nm = len(NM)
    n_en7 = len(NM_EN7)
    t = n_nf + n_nn + n_nm + n_en7
    rv = random.randint(0, t - 1)
    # We'll return a list of the form [noun_tuple, gender, has_genitive].
    if rv < n_en7:
        r = [list(NM_EN7)[rv], 'M', False]
        r[0] = (r[0], make_en7_pl(r[0]))
    elif rv < (n_en7 + n_nm):
        r = [list(NM)[rv - n_en7], 'M', True]
    elif rv < (n_en7 + n_nm + n_nn):
        r = [list(NN)[rv - (n_en7 + n_nm)], 'N', True]
    else:
        r = [list(NF)[rv - (n_en7 + n_nm + n_nn)], 'F', False]
    if not isinstance(r[0], tuple):
        r[0] = (r[0], r[0]) # The noun must be a pair tuple.
    return r

def adj_paradigm_from_art(art):
    if art in ART_S:
        return 'W'
    elif art in ART_M:
        return 'M'
    else:
        return 'S'

def decline_art(art, gender, num, case):
    if art == "der":
        paradigm = DEF_ART_DECL
        art = ""
    elif art in ART_S:
        paradigm = STRONG_DET_DECL
    elif art in ART_M:
        paradigm = MIXED_DET_DECL
    else:
        return art
    return art + paradigm[numgen_categ_index(gender, num)][CASES.index(case)]

def numgen_categ_index(gender, number):
    return ('M', 'N', 'F').index(gender) if number == "SG" else 3

def decline_adj(adj, paradigm, gender, num, case):
    if paradigm == 'S':
        paradigm = STRONG_ADJ_DECL
    elif paradigm == 'M':
        paradigm = MIXED_ADJ_DECL
    else:
        paradigm = WEAK_ADJ_DECL
    if adj[-1] == 'e':
        adj = adj[:-1]
    return adj + paradigm[numgen_categ_index(gender, num)][CASES.index(case)]

def decline_noun(noun, has_gen, num, case):
    if not isinstance(noun, tuple):
        return ""
    if noun[0] in NM_EN7 and not (case == "NOM" and num == "SG"):
        noun = noun[1]
    elif num == "SG":
        noun = noun[0]
    else:
        noun = noun[1]
    assert (isinstance(noun, str) and len(noun) > 0)
    if num == "SG" and case == "GEN" and has_gen:
        noun = add_gen(noun)
    elif num == "PL" and case == "DAT":
        noun = make_pl_dat(noun)
    return noun

def add_gen(n):
    if n[-1] in {'s', 'ß'}:
        n += "es"
    else:
        n += "s"
    return n
    
def make_pl_dat(n):
    if n[-1] == 'n':
        pass
    elif n[-1] in {'e', 'r', 'l'}:
        n += "n"
    else:
        n += "en"
    return n

# ============================================================================= #

def capitalize_first_letter(s):
    return (s[0].upper() + s[1:]) if len(s) > 0 else ""

q = False
while not q:
    rv = random.randint(0, 8)
    gcase = CASES[rv % 4]
    gnum = "SG" if rv < 4 else "PL"
    adj = list(ADJ)[random.randint(0, len(ADJ) - 1)]
    art = list(DET)[random.randint(0, len(DET) - 1)]
    if random.randint(0, 4) == 0:
        art = "der"
    if art in NUM:
        gnum = "PL"
    noun, gender, has_genitive = random_noun()
    query = (gcase + "." + gnum + ": " + art + ("-" if art not in {"der"} | NUM else "") +
             " + " + adj + " + " + noun[0])
    answer = (decline_art(art, gender, gnum, gcase) + ' '
           + decline_adj(adj, adj_paradigm_from_art(art), gender, gnum, gcase) + ' '
           + decline_noun(noun, has_genitive, gnum, gcase))
    print ("\n<< " + query)
    ip = input("")
    if ip == 'q':
        q = True
    else:
        print (">> " + capitalize_first_letter(answer))

