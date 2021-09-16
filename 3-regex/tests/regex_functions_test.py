import unittest
from regextree import *
import regex_functions as rf

class TestIsRegex(unittest.TestCase):

    def test_all(self):
        f = open('is_regex.txt', 'r')
        i = 1
        for line in f:
            line = line.strip()
            if not line.startswith('#') and len(line) != 0:
                line = line.split()
                check = True
                if line[1] == 'F':
                    check = False
                self.assertEqual(rf.is_regex(line[0]), check,
                                 "Failed: " + line[0])
                i += 1
        print()
        print("Is Regex Ran: " + str(i) + " cases.")
        print()
        f.close()

class BuildRegex(unittest.TestCase):

    def test_all(self):
        f = open('build_regex.txt', 'r')
        i = 1
        for line in f:
            line = line.strip()
            if not line.startswith('#') and len(line) != 0:
                ind = line.index(' ')
                case = line[:ind]
                check = line[ind + 1:]

                build = rf.build_regex_tree(case)
                self.assertEqual(str(build), check, "Failed: #" + str(i) + " " + str(case))
            i += 1
        f.close()


class MatchRegex(unittest.TestCase):

    def test_all(self):
        print()
        print("Testing matches... Good luck.")
        f = open('match_regex.txt', 'r')
        i = 1
        total = 0
        for line in f:
            line = line.strip()
            if not line.startswith('#') and len(line) != 0:
                line = line.split(' ')
                case = line[0]


                if rf.is_regex(case):
                    build = rf.build_regex_tree(case)
                else:
                    print("Error with test case.", case)
                    continue

                cases = []
                # Get cases as tuples...
                for i10 in range(1, len(line), 2):
                    cases.append((line[i10], line[i10+1]))

                i2 = 0
                for case, val in cases:
                    if val == 'T':
                        val = True
                    else:
                        val = False

                    if case == 'E':
                        case = ''

                    mtch = rf.regex_match(build, case)
                    try:
                        self.assertEqual(mtch, val)
                    except AssertionError:
                        print("Failed: #" + str(i) + " '" + str(case) + "' #" + str(i2))
                    i2 += 1
                total += i2
            i += 1
        f.close()
        print ("Ran: ", str(total), " total tests.")

if __name__ == '__main__':
    unittest.main(exit = False)
