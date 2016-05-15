from collections import defaultdict
import random

class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)

    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', 'hw1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def gen_random(self, symbol):
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        sentence = ''

        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '

        return sentence


def main():
    cfg1 = CFG()
    cfg1.add_prod('S', 'NP  VP')
    cfg1.add_prod('VP', 'Verb NP')
    cfg1.add_prod('NP', 'Det Noun')
    cfg1.add_prod('NP', 'NP PP')
    cfg1.add_prod('PP', 'Prep NP')
    cfg1.add_prod('Noun', 'Adj Noun')

    cfg1.add_prod('Verb', 'I | he | she | Joe')
    cfg1.add_prod('Det', 'a | the | every')
    cfg1.add_prod('Noun', 'president | sandwich | pickle | floor| chief of staff')
    cfg1.add_prod('Adj', 'fine | delicious | perplexed | pickled')
    cfg1.add_prod('Prep', 'with | on | under | in')

    for i in xrange(10):
        print cfg1.gen_random('S')

if __name__ == "__main__":
    main()
