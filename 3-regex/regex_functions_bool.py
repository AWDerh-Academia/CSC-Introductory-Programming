"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, Abdul Derh 2013, 2014,
# 2015. Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2015
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

# Single Length regex matches.
EMPTY_SYMBOL = 'e'
MATCH_ZERO = '0'
MATCH_ONE = '1'
MATCH_TWO = '2'

# Operator containers.
LEFT_BRACKET = '('
RIGHT_BRACKET = ')'

# Operators
AND_OP = '.'
OR_OP = '|'
ALL_OP = '*'

class InvalidRegexException(Exception):
    '''Thrown when a func'n needed a valid regex but an invalid one was given.
    '''

def is_regex(regex):
    '''(str, bool) -> bool
    Returns true iff the given string is a valid regular expression.

    >>> is_regex('e')
    True
    >>> is_regex('2*')
    True
    >>> is_regex('1**')
    True
    >>> is_regex('((1.(0|2)*).1)')
    True
    >>> is_regex('*1')
    False
    >>> is_regex('e*')
    True
    >>> is_regex('*(')
    False
    '''
    # Check if empty
    if (len(regex) > 0):
        # Base case: single length can only be 0,1,2 and e
        if len(regex) == 1:
            return (regex == EMPTY_SYMBOL or regex == MATCH_ONE
                    or regex == MATCH_TWO or regex == MATCH_ZERO)

        # The star pattern is a variant of the base case.
        elif regex[-1] == ALL_OP:
            return is_regex(regex[:-1])

        # Bracket case: evaluate r1 and r2 after bracket check and length check
        elif (len(regex) > 4 and regex[0] == LEFT_BRACKET and
              regex[-1] == RIGHT_BRACKET):

            # Working only w/inside text... find op first.
            inner = regex[1:-1]
            div = _find_operator(inner)

            # If a valid '.' or '|', now split and recurse on left and right.
            if div < len(regex):
                return is_regex(inner[:div]) and is_regex(inner[div+1:])

    # Occurs for: bad bracket match, bad start char, empty regex.
    return False


def _find_operator(regex):
    '''(str) -> int
    Retrieves the operator in a given expression.
    If the returned int == len(regex) then an operator was not found.

    >>> _find_operator('(0.1).1')
    5
    >>> _find_operator('010101')
    6
    '''
    # Starting at the first character, continue until op. found.
    count = 0
    found = False
    # We must keep track of brackets.
    brackets_open = 0
    while count < len(regex) and not found:
        # If a bracket is found, either add or remove the count.
        if regex[count] == LEFT_BRACKET:
            brackets_open += 1
        elif regex[count] == RIGHT_BRACKET:
            brackets_open -= 1

        # If operator found with all previous brackets closed: found op.
        if ((regex[count] == AND_OP or regex[count] == OR_OP)
            and brackets_open == 0):

            found = True
        # Otherwise, continue...
        else:
            count += 1

    # Either we fall off the list or we give the right index.
    return count

def all_regex_permutations(given_regex):
    '''(str) -> list of str
    Returns all valid permutations of a given regex.

    >>> all_regex_permutations('1')
    ['1']
    >>> all_regex_permutations('(0|2*)')
    ['(0|2*)', '(0|2)*', '(0*|2)', '(2|0*)', '(2|0)*', '(2*|0)']
    '''
    # Return a list of regexes from the permutation that are valid.
    return [regex for regex in _permute_str(given_regex) if is_regex(regex)]

def _permute_str(regex):
    '''(str) -> list of str
    Permutes a given string.

    REQ: len(s) >= 1

    >> _permute_str('1')
    ['1']
    >>> _permute_str('(*)')
    ['(*)', '()*', '*()', '*)(', ')(*', ')*(']
    '''
    # Base case with 1 length string.
    if len(regex) == 1:
        return [regex]

    # Keep a letter and permute the rest of them.
    ret = []
    for cut in range(len(regex)):

        # Permute everything but the current (cut) element.
        perms = _permute_str(regex[:cut] + regex[cut + 1:])
        # Append the cut element to the front of the permutations. Add to ret.
        ret += [regex[cut] + perm for perm in perms]

    return ret

def regex_match(regnode, check):
    '''(RegexTree, str) -> bool
    Returns true iff the given string passed the regex match.

    REQ: The given RegexTree is a valid one.

    >>> regex_match(RegexTree("e", []), '')
    True
    >>> regex_match(RegexTree("2", []), '1')
    False
    >>> regex_match(StarTree(RegexTree("1", [])), '11111111')
    True
    >>> regex_match(StarTree(RegexTree("1", [])), '111110111')
    False
    >>> regex_match(StarTree(RegexTree("1", [])), '')
    True
    >>> regex_match(DotTree(RegexTree('0', []), RegexTree('1', [])), '01')
    True
    >>> regex_match(DotTree(RegexTree('0', []), RegexTree('1', [])), '')
    False
    >>> regex_match(BarTree(RegexTree('0', []), RegexTree('1', [])), '')
    False
    '''
    return regex_match_helper(regnode, check) >= len(check)

def regex_match_helper(regnode, check):
    '''(RegexTree, str) -> int
    Returns the integer upon which this match failed. If it is >= then the
    len of the string, then it passed.

    REQ: The given regex tree must be a valid one.

    >>> regex_match_helper(RegexTree("e", []), '')
    1
    >>> regex_match_helper(RegexTree("e", []), '1')
    0
    >>> regex_match_helper(StarTree(RegexTree("1", [])), '11111111')
    8
    >>> regex_match_helper(StarTree(RegexTree("1", [])), '111110111')
    5
    >>> regex_match_helper(StarTree(RegexTree("1", [])), '')
    1
    >>> regex_match_helper(DotTree(RegexTree('0', []), RegexTree('1', [])), \
'01')
    2
    >>> regex_match_helper(BarTree(RegexTree('0', []), RegexTree('1', [])), \
'0')
    1
    '''
    # If the string is only one character long, only works with 1 regex.
    if (type(regnode) is RegexTree):
        # Valid iff regex tree and values match.
        return apply_basic_regex(regnode.get_symbol(), check)
    # If it s a star tree, we deligate to helper and check completion.
    elif (type(regnode) is StarTree):
        return apply_star_regex(regnode.get_child(), check)
    # If it is a bar tree, we check both children against the string using OR.
    elif (type(regnode) is BarTree):
        left, right = regnode.get_left_child(), regnode.get_right_child()
        return apply_bar_regex(left, right, check)
    # If it is a dot tree, we must
    elif (type(regnode) is DotTree):
        left, right = regnode.get_left_child(), regnode.get_right_child()
        return apply_dot_regex(left, right, check)
    return 1

def apply_basic_regex(symbol, check):
    '''(str, str) -> (int, bool)
    Applies the basic RegexTree (i.e. of length 1 and either 0,1,2 or e).
    Returns an index inside the length of the string (i.e. 0) if the match
    failed, otherwise 1. Note, this funcn only checks first character, but
    note that a sole basic comparison with length > 1 will always fail. The
    second return variable is to indicate whether or not the first value
    in the given string was the required one.

    REQ: len(check) > 0

    >>> apply_basic_regex('e', '')
    (1, True)
    >>> apply_basic_regex('e', ' ')
    (0, False)
    >>> apply_basic_regex('1', '1')
    (1, True)
    >>> apply_basic_regex('2', '1')
    (0, False)
    '''
    # Empty string we check only that the length is 0.
    if (symbol == EMPTY_SYMBOL):
        ret = len(check) == 0
        return (int(ret), ret)
    # For all else, we do an exact comparison on the first character.
    if len(check) > 0:
        ret = symbol == check[0]
        return (int(ret), ret)
    else:
        # REQ failed.
        return (0, False)

def apply_star_regex(child, check):
    '''(RegexTree, str) -> int
    Applies the StarTree given the child and the check to perform on. Returns
    the index for which the match has failed, which is not in the str if the
    entire string passed.

    >>> one = RegexTree('1', [])
    >>> apply_star_regex(one, '1111111')
    (7, True)
    >>> apply_star_regex(one, '')
    (1, True)
    >>> apply_star_regex(one, '222222')
    (0, False)
    >>> apply_star_regex(RegexTree('2', []), '222111')
    (3, True)
    '''
    # Empty strings always pass.
    if len(check) == 0:
        return (1, True)

    # We loop until a failed attempt or until end of line.
    start_char = 0
    attempt = True
    while attempt and start_char < len(check):
        # We procees the entire subsequence.
        ret = regex_match_helper(child, check[start_char:])

        # Now we determine if a subsequence was found. If so, we continue...
        attempt = ret[1]
        if attempt:
            start_char += ret[0]

    # We return start of invalid sequence and what the last attempt was.
    return (start_char, start_char > 0)

def apply_bar_regex(left_child, right_child, check):
    '''(RegexTree, RegexTree, str) -> int
    Applies the BarTree given the child and the check to perform on. Returns
    the integer index of the string, which is not in the string if the regex
    succeeded completely.

    >>> left = RegexTree(MATCH_ONE, [])
    >>> right = RegexTree(MATCH_ZERO, [])
    >>> apply_bar_regex(left, right, '1')
    (1, True)
    >>> apply_bar_regex(left, right, '0')
    (1, True)
    >>> apply_bar_regex(left, right, '2')
    (0, False)
    >>> apply_bar_regex(left, right, '')
    (0, False)
    >>> apply_bar_regex(RegexTree(MATCH_EMPTY), right, '')
    (0, True)
    '''
    # We force both matches, left and right.
    left = regex_match_helper(left_child, check)
    right = regex_match_helper(right_child, check)

    # We consider the one that traversed furthur as the correct index...
    if left[1] and right[1]:
        ret = (max(left[0], right[0]), True)
    # We send whichever one worked. If neither worked, it doesn't matter.        <--- CASE THIS
    elif left[1]:
        ret = left
    else:
        ret = right

    return ret

def apply_dot_regex(left, right, check):
    '''(RegexTree, RegexTree, str) -> (int, bool)
    Applies the dot regex on the given check string. Returns an integer
    representing the index that failed, which may be > len(check), this
    implies success.

    >>> left = RegexTree('1', [])
    >>> right = RegexTree('2', [])
    >>> apply_dot_regex(left, right, '12')
    (2, True)
    >>> apply_dot_regex(left, right, '122')
    (2, True)
    >>> left = StarTree(BarTree(RegexTree('0', []), RegexTree('1', [])))
    >>> apply_dot_regex(left, right, '10101010112')
    (11, True)
    >>> apply_dot_regex(left, right, '1010101011')
    (9, False)
    >>> apply_dot_regex(left, right, '')
    (0, False)
    '''
    # From left-right, continue until failure.
    ret = regex_match_helper(left, check)

    # Did we find what we were looking for on the left side? If not, quit...
    if not ret[1]:
        return ret

    # From failure index, work on right side, adding to return index.
    # But first make sure that non-star regex returned non-zero.
    if ((ret == 0) and (type(left) is not StarTree)):
        # Just like DotBar, this case could be an empty str, thus -1 is better.
        ret = -1
    else:
        # We add the index that the right side traverses after...
        rt = regex_match_helper(right, check[ret:])

        # We must ensure that the left traversal didn't make it impossible
        # for the right one to run. We only worry about non-star, '0' cases.
        if rt == 0 and type(right) is not StarTree:
            # Now we know the right-side was not satisfied. Fail the match.
            if ret >= len(check):
                ret = len(check) - 1
        else:
            ret += rt

    # The "return index" is the last character of success.
    return ret

def build_regex_tree(reg):
    '''(str) -> RegexTree
    Builds a regex tree given a valid regex string.

    REQ: valid regex.
    RAISES: InvalidRegexException - if a bad regex is presented.

    >>> build_regex_tree('0')
    RegexTree('0', [])
    >>> build_regex_tree('((0|1).2*)')
    DotTree(BarTree(RegexTree('0', []), RegexTree('1', [])), \
StarTree(RegexTree('2', [])))
    >>> build_regex_tree('(0.)*')
    Traceback (most recent call last):
        ...
    InvalidRegexException
    '''
    # Check that REQ is satisfied.
    if not is_regex(reg):
        raise InvalidRegexException()

    # Last letter is op: we build everything before it for the star tree to ret
    if (reg[-1] == ALL_OP):
        return StarTree(build_regex_tree(reg[:-1]))
    # Binary case: we delegate to the binary builder.
    elif (reg[0] == LEFT_BRACKET):
        return build_binary_tree(reg)
    # If we don't have a binary tree or star tree, then we have a basic tree.
    else:
        # We simply use the first (and supposedly ONLY) character to build.
        return RegexTree(reg[0], [])

def build_binary_tree(reg):
    '''(str) -> RegexTree
    Builds a binary tree given the regular expression with the outermost
    expression being a binary one (i.e. dot or bar).

    REQ: the given binary regex (i.e. ( . ) or ( | ) is valid)
    '''
    # Get the inner expression as well as operator index and type.
    inner = reg[1:-1]
    op_index = _find_operator(inner)
    op = inner[op_index]

    # Build left and right trees.
    left_tree = build_regex_tree(inner[:op_index])
    right_tree = build_regex_tree(inner[op_index + 1:])

    # Construct this tree using left and right.
    if op == OR_OP:
        ret = BarTree(left_tree, right_tree)
    else:
        ret = DotTree(left_tree, right_tree)
    return ret


if __name__ == "__main__":
    import doctest
    doctest.testmod()

# Exceptions for operators and bad regexes.
