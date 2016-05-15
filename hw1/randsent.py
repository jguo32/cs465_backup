from collections import defaultdict
import random
import argparse
import sys

class CFG(object):
    def __init__(self):
        self.rules = defaultdict(list)

    def gen_random(self, symbol):
        sentence = ''
        sym_sum = 0

        # select one grammar of this symbol randomly

        for rule in self.rules[symbol]:
            sym_sum += float(rule[-1])

        sample = random.random() * sym_sum

        i = 0
        while i < len(self.rules[symbol]):
            rule = self.rules[symbol][i]

            if sample > 0:
                sample -= float(rule[-1])
                i += 1
            else:
                break

        rule = self.rules[symbol][i - 1]
        rand_symbols = rule[: -1]

        for sym in rand_symbols:
            # for non-terminals, recurse
            if sym in self.rules:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '

        return sentence

    def gen_tree(self, symbol):
        words = []
        sentence = []
        sym_sum = 0

        # select one grammar of this symbol randomly
        for rule in self.rules[symbol]:
            sym_sum += float(rule[-1])

        sample = random.random() * sym_sum

        i = 0
        while i < len(self.rules[symbol]):
            rule = self.rules[symbol][i]

            if sample > 0:
                sample -= float(rule[-1])
                i += 1
            else:
                break

        rule = self.rules[symbol][i - 1]
        rand_symbols = rule[:-1]

        flag = False

        for sym in rand_symbols:
            # for non-terminals, recurse
            if sym in self.rules:
                words.append((sym, self.gen_tree(sym)))
                flag = True
        if not flag:
            return ' '.join(rand_symbols)

        return tuple(words)

    @classmethod
    def printTree(cls, sentence, indent, peren):
        """
        Print the sentence as a tree structure.
        :param sentence: multi-layer list
        :param indent: (int) the space before the printed words
        """
        if not sentence:
            return

        if sentence[1] is None:  # this is a single string, not a grammar
            print sentence[0],
            return
        else:
            print "(" + sentence[0],
            if type(sentence[1]) is str:        # it is a leaf, so print a new line after printing the current grammar
                words = sentence[1].split()
                if len(words) > 1:              # the sentence contains several words, print them to different lines
                    for i in range(len(words)):
                        if i < len(words) - 1:
                            print words[i]
                            print " " * (indent + 1 + len(sentence[0])),
                        else:
                            print words[i] + ")",
                else:
                    print sentence[1] + ")",
                return

        # for every child, print the child recursively
        for i in range(len(sentence[1])):
            cls.printTree(sentence[1][i], indent + 2 + len(sentence[0]), peren + 1)
            if i < len(sentence[1]) - 1:
                print ""
                print " " * (indent + 1 + len(sentence[0])),
        sys.stdout.write(")")

    def read_file(self, filename):
        f = open(filename, 'r')
        for line in f:
            if "#" not in line and line.strip():
                split = line.split('\t')

                self.rules[split[1]].append(tuple((split[2] + ' ' + split[0]).split()))


def main():
    # Get the parameters from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='output tree', action='store_true')
    parser.add_argument('grammar', help='grammar file')
    parser.add_argument('count', type=int, help="produces trees instead of strings")
    # parser.add_argument('grammar', help = 'grammar file')

    parser.parse_args()
    args = parser.parse_args()

    input_file = args.grammar
    sen_num = args.count

    cfg = CFG()
    cfg.read_file(input_file)
    if args.t:
        for i in xrange(sen_num):
            sentence = ('ROOT', cfg.gen_tree('ROOT'))
            cfg.printTree(sentence, 0, 0)
    else:
        for i in xrange(sen_num):
            print cfg.gen_random('ROOT')


if __name__ == "__main__":
    main()