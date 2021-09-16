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
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

# Single Length regex matches.
MATCH_EMPTY = 'e'
MATCH_ZERO = '0'
MATCH_ONE = '1'
MATCH_TWO = '2'

# Binary operator containers.
BINARY_LEFT = '('
BINARY_RIGHT = ')'

# Operators
AND_OP = '.'
OR_OP = '|'
ALL_OP = '*'


class InvalidRegexException(Exception):

    '''When a function needed a valid regex but an invalid one was given.'''


class InvalidRegexTreeException(Exception):

    '''When a bad regex tree is used for matching.'''


def is_regex(regex):
    '''(str) -> bool
    Returns true if the given string was found to be a valid regex. A valid
    regex is defined as:
    If regex is of length 1: then regex should be either '0', '1', '2', or 'e'
    Let x and y be valid regexes.
    A star operation is of the form: x*
    A binary operation like '.' or '|' is of the form: (x.y) or (x|y)
    If it is not a valid regex, false is returned.

    >>> is_regex('e')
    True
    >>> is_regex('(1.2)')
    True
    >>> is_regex('(e|0)')
    True
    >>> is_regex('1*')
    True
    >>> is_regex('((1.(0|2)*).1)')
    True
    >>> is_regex(')1*)')
    False
    >>> is_regex('-1')
    False
    >>> is_regex('(1.)')
    False
    >>> is_regex('*')
    False
    >>> is_regex('')
    False
    '''
    valid = False
    # Make sure regex is not empty...
    if (len(regex) > 0):
        # Base case: single length can only be 0,1,2 and e
        if (_is_leaf_symbol(regex)):
            valid = True
        # The star pattern is a variant of the base case. Process all b4 *.
        elif (regex[-1] == ALL_OP):
            valid = is_regex(regex[:-1])
        # Bracket case: when len is atleast 4, and first and last are '(', ')'
        elif (len(regex) > 4 and regex[0] == BINARY_LEFT and
              regex[-1] == BINARY_RIGHT):
            # check inside ones after bracket check and length check. find op.
            inner = regex[1:-1]
            div = _find_operator(inner)
            # If a valid '.' or '|', now split and recurse on left and right.
            if (div < len(regex)):
                valid = (is_regex(inner[:div]) and is_regex(inner[div + 1:]))

    # False for: bad bracket usage, bad Leaf sequence, empty regex.
    return valid


def _is_leaf_symbol(symb):
    '''(str) -> bool
    Returns true iff the given symbol is a valid leaf symbol, which in this
    program is a '1', '2', '0' or 'e'.

    >>> _is_leaf_symbol('e')
    True
    >>> _is_leaf_symbol('3')
    False
    >>> _is_leaf_symbol('e1')
    False
    '''
    # len > 1 are unknown to us. We check if it is e, 1, 2 or 0.
    return (len(symb) == 1 and (symb == MATCH_EMPTY or symb == MATCH_ONE
                                or symb == MATCH_TWO or symb == MATCH_ZERO))


def _find_operator(regex):
    '''(str) -> int
    Retrieves the operator in a given expression. If the returned int is equal
    to the length of the regex then an operator was not found.

    >>> _find_operator('(0.1).1')
    5
    >>> _find_operator('010101')
    6
    >>> _find_operator('')
    0
    '''
    # Starting at the first character, continue until op. found.
    index = 0
    found = False
    # We must keep track of brackets.
    brackets_open = 0
    while (index < len(regex) and not found):
        # For a left bracket, we increment the count.
        if (regex[index] == BINARY_LEFT):
            brackets_open += 1
        # For a right bracket, we decrement the count.
        elif (regex[index] == BINARY_RIGHT):
            brackets_open -= 1
        # If operator found with all previous brackets closed: found op.
        elif ((regex[index] == AND_OP or regex[index] == OR_OP)
              and brackets_open == 0):
            found = True

        # We continue iff we did not find the operator.
        if (not found):
            index += 1

    # Either we fall off the str or we give the right index.
    return index


def all_regex_permutations(given_str):
    '''(str) -> set of str
    Returns all permutations of a given string that are valid regexes.

    >>> all_regex_permutations('1')
    {'1'}
    >>> all_regex_permutations('')
    set()
    >>> ret = {'(0|2)*', '(0|2*)', '(0*|2)', '(2|0)*', '(2|0*)', '(2*|0)'}
    >>> all_regex_permutations(')0|2*(') == ret
    True
    '''
    # We permute the string, check each to be a regex and return only those.
    # Since _permute_str returns a set, we do not worry about multiple equal
    # perms caused by multiple occurences of leafs.
    return {perm for perm in _permute_str(given_str) if is_regex(perm)}


def _permute_str(regex):
    '''(str) -> set of str
    Returns the permutations of a given string, as a set of strings.

    >> _permute_str('1')
    {'1'}
    >>> _permute_str('')
    set()
    >>> ret = {'(*)', '()*', '*()', '*)(', ')(*', ')*('}
    >>> _permute_str('(*)') == ret
    True
    '''
    # Base case with length = 1 should just return it as the sole entry.
    if len(regex) == 1:
        return {regex}

    # Keep a letter, called cut, and permute the rest of them.
    all_perms = set()
    for cut in range(len(regex)):
        perms = _permute_str(regex[:cut] + regex[cut + 1:])
        # Add the cut element to the front of the permutations. Add to ret.
        for perm in perms:
            all_perms.add(regex[cut] + perm)

    return all_perms


def regex_match(regnode, check):
    '''(RegexTree, str) -> bool
    Returns True if and only if the given string matched the given regex. Which
    is defined by the following rules:
    A leaf will completely match a string of length 1 and equal to the leaf
    (but only on characters '0', '1', and '2'; 'e' is asking for empty match)
    A star operation will match iff the sequences within the string can be
    arranged in subsequences that match the regex inside the star & ammount to
    the entire string.
    A bar operation will match iff either the left matches the entire string
    or the right matches the entire string.
    A dot operation will match iff the string can be split in two such that
    the left regex matches the 'left' string and the right regex matches
    the 'right' string, where left or right strings could be empty.

    Refer to is_valid_tree to see what a valid RegexTree is defined to be.

    REQ: The given RegexTree is a valid one.
    RAISES InvalidRegexTreeException if the given tree was unsupported.

    >>> regex_match(Leaf('e'), '')
    True
    >>> regex_match(Leaf('2'), '1')
    False
    >>> regex_match(StarTree(Leaf('1')), '11111111')
    True
    >>> regex_match(StarTree(Leaf('1')), '111110111')
    False
    >>> regex_match(StarTree(Leaf('1')), '')
    True
    >>> regex_match(DotTree(Leaf('0'), Leaf('1')), '01')
    True
    >>> regex_match(DotTree(Leaf('0'), Leaf('1')), '')
    False
    >>> regex_match(DotTree(Leaf('0'), Leaf('1')), '0')
    False
    >>> regex_match(DotTree(Leaf('0'), Leaf('1')), '1')
    False
    >>> regex_match(DotTree(Leaf('e'), Leaf('1')), '1')
    True
    >>> regex_match(BarTree(Leaf('0'), Leaf('1')), '0')
    True
    >>> regex_match(BarTree(Leaf('0'), Leaf('1')), '1')
    True
    >>> regex_match(BarTree(Leaf('0'), Leaf('1')), '')
    False
    >>> regex_match(BarTree(Leaf('0'), Leaf('e')), '')
    True
    >>> compound = DotTree(BarTree(Leaf('0'), Leaf('1')), StarTree(Leaf('2')))
    >>> regex_match(compound, '022')
    True
    >>> regex_match(compound, '01')
    False
    >>> regex_match(Leaf('-1'), '-1')
    Traceback (most recent call last):
        ...
    InvalidRegexTreeException: Unsupported regex tree.
    '''
    # We ensure the regex tree is supported by this application.
    if (not is_valid_tree(regnode)):
        raise InvalidRegexTreeException("Unsupported regex tree.")

    # We do not check for the exception b/c it is implicitly handled above.
    res_index = _regex_match_helper(regnode, check)

    # Failure is defined as the empty set, or not passing entire sequence.
    return ((len(res_index) > 0) and (max(res_index) >= len(check)))


def is_valid_tree(node):
    '''(RegexTree) -> bool
    Returns True iff the given tree is a valid tree for this program. That is,
    a leaf will have no child, a Star will only have one child and a dot or
    bar will have two children. Finally, a leaf can be only '0', '1', '2' or
    'e'. This function will also check if the correct RegexTree class is used!

    >>> is_valid_tree(Leaf('2'))
    True
    >>> is_valid_tree(StarTree(Leaf('1')))
    True
    >>> is_valid_tree(DotTree(Leaf('0'), Leaf('1')))
    True
    >>> is_valid_tree(BarTree(Leaf('0'), Leaf('1')))
    True
    >>> is_valid_tree(Leaf("-1"))
    False
    >>> is_valid_tree(DotTree(Leaf('0'), None))
    False
    >>> is_valid_tree(StarTree(None))
    False
    >>> is_valid_tree(RegexTree('|', []))
    False
    >>> is_valid_tree(None)
    False
    '''
    valid = False
    # First we check that we're not given a bad object...
    if (isinstance(node, RegexTree)):
        # We work with symbols first, they are the best indicator of tree type.
        # We process in order of: star *, and ., or | and finally leaf symbols.
        children = node.get_children()
        num_children = len(children)
        symbol = node.get_symbol()
        # '*': we verify that it is a star tree and has only one child.
        if (symbol == ALL_OP):
            valid = (isinstance(node, StarTree) and num_children == 1)
        # '|': verify it is a BarTree and has two children.
        elif (symbol == OR_OP):
            valid = (isinstance(node, BarTree) and num_children == 2)
        # '.': Verify it is a DotTree and has two children.
        elif (symbol == AND_OP):
            valid = (isinstance(node, DotTree) and num_children == 2)
        # Must be a leaf, check it so. And ensure no child!
        elif (_is_leaf_symbol(symbol) and num_children == 0):
            valid = True

        # Now we check all of it's children, we quit as soon as one fails.
        iter_index = 0
        while valid and iter_index < num_children:
            valid = is_valid_tree(children[iter_index])
            iter_index += 1

    # Unrecognized symbol, bad structure, bad child, bad object will all fail.
    return valid


def _regex_match_helper(regnode, check):
    '''(RegexTree, str) -> set of int
    Returns the set of ints that correspond to the various subsequences that
    matched the entire given regex node, such that any integer i accepts all
    values before i to have matched the regex. If no integers are returned,
    this regex failed completely. In other words, the set of integers returned
    represent the various combinations of possible success. Obviously, the
    greatest integer tells you how far the match succeeds.

    Refer to regex_match for a definition of what will match and is_valid_tree
    to see what a valid RegexTree is defined to be.

    REQ: The given regex tree must be a valid one.
    RAISES InvalidRegexTreeException if the given tree was unsupported.

    >>> _regex_match_helper(Leaf('e'), '')
    {1}
    >>> _regex_match_helper(Leaf('e'), '1')
    {0}
    >>> _regex_match_helper(Leaf('1'), '2')
    set()
    >>> _regex_match_helper(StarTree(Leaf('1')), '11111111') == {0, 1, 2, 3, \
    4, 5, 6, 7, 8}
    True
    >>> _regex_match_helper(StarTree(Leaf('1')), '111110111') == {0, 1, 2, 3,\
    4, 5}
    True
    >>> _regex_match_helper(StarTree(Leaf('1')), '')
    {1}
    >>> _regex_match_helper(DotTree(Leaf('0'), Leaf('1')), '01')
    {2}
    >>> _regex_match_helper(BarTree(Leaf('0'), Leaf('1')), '0')
    {1}
    >>> _regex_match_helper(RegexTree('&', []), '-1')
    Traceback (most recent call last):
        ...
    InvalidRegexTreeException: Internal unsupported regex tree.
    '''
    # If the string is only one character long, it is a basic match.
    if (isinstance(regnode, Leaf)):
        # Valid iff regex tree and values match.
        return _apply_basic_regex(regnode.get_symbol(), check)
    # If it is a star tree, we delegate to helper to get all possibilities.
    elif (isinstance(regnode, StarTree)):
        return _apply_star_regex(regnode.get_child(), check)
    # If it is a bar tree, we get left and right then return helper.
    elif (isinstance(regnode, BarTree)):
        left, right = regnode.get_left_child(), regnode.get_right_child()
        return _apply_bar_regex(left, right, check)
    # If it is a dot tree, we also get left and right and return helper.
    elif (isinstance(regnode, DotTree)):
        left, right = regnode.get_left_child(), regnode.get_right_child()
        return _apply_dot_regex(left, right, check)

    # Unhandled case. No explicit 'try' b/c this is just a helper function.
    # Notice how this one says it is an "internal" issue.
    raise InvalidRegexTreeException("Internal unsupported regex tree.")


def _apply_basic_regex(symbol, check):
    '''(str, str) -> set of int
    Applies the basic RegexTree (i.e. of length 1 and either 0, 1, 2 or e).
    Returns the set of ints that correspond to the various subsequences that
    are matched, such that integer i accepts all values before i to have
    matched the regex. If no integers are returned, this regex failed
    completely. In particular, this function will return {1} for a completely
    valid pass, but a {0} may be returned to indicate that this sequence will
    match if one considers it as an empty string. Otherwise, an empty set is
    returned.

    >>> _apply_basic_regex('e', '')
    {1}
    >>> _apply_basic_regex('e', ' ')
    {0}
    >>> _apply_basic_regex('1', '1')
    {1}
    >>> _apply_basic_regex('2', '1')
    set()
    >>> _apply_basic_regex('2', '')
    set()
    >>> _apply_basic_regex('e', '2')
    {0}
    '''
    ret = set()
    # Empty string we check only that the length is 0...
    if (symbol == MATCH_EMPTY):
        # We return {1} to signify complete pass if str is empty ...
        if (len(check) == 0):
            ret = {1}
        # ... or {0} to signify this would pass if the string was 'empty'.
        else:
            ret = {0}
    # For lengths > 0, we do an exact comparison on the first character.
    elif (len(check) > 0):
        # Returning {1} iff the match was exact with the first character.
        if (symbol == check[0]):
            ret = {1}

    return ret


def _apply_star_regex(child, check):
    '''(RegexTree, str) -> set of int
    Applies the StarTree given the child and the check to perform on.
    Returns the indices of where subsequences start, which is the set of ints
    that correspond to the various subsequences that are matched, such that
    integer i accepts all values before i to have matched the regex. If no
    integers are returned, this regex failed completely. So i-th index means
    a match due to the various combinations of applications of given regexes on
    all characters before the ith one (thus exclusive). This will return a {0}
    if the empty string is a valid possibility or {1} if it was the empty
    string, in addition to other possible combinations if any.

    >>> one = Leaf('1')
    >>> _apply_star_regex(one, '')
    {1}
    >>> _apply_star_regex(one, '1') == {0, 1}
    True
    >>> _apply_star_regex(one, '111') == {0, 1, 2, 3}
    True
    >>> _apply_star_regex(Leaf('2'), '222111') == {0, 1, 2, 3}
    True
    >>> two = Leaf('2')
    >>> _apply_star_regex(DotTree(one, two), '12121211') == {0, 2, 4, 6}
    True
    '''
    # Empty strings always pass. The set with one signifies to move one index.
    if (len(check) == 0):
        return {1}

    # We ignore nested unary links of stars, by processing inwards.
    if (isinstance(child, StarTree)):
        return _apply_star_regex(child.get_child(), check)

    # We loop until a failed attempt or until end of line, assuming nothing.
    indices = [0]
    iter_index = 0
    while (iter_index < len(indices)):
        # We start at the next index (of combination) to validate.
        start_index = indices[iter_index]

        # We don't want to accidently create an empty match, we stay in the str
        if (start_index < len(check)):
            # We process the entire subsequence.
            match = _regex_match_helper(child, check[start_index:])

            # we honour each possibility and run on all of them.
            for passed_indices in match:
                # The index to iterate is the current index, start_index, plus
                # all of indices that are matched, called passed_indices. We
                # only iterate if we are not already scheduled to.
                to_iter = start_index + passed_indices
                if (to_iter not in indices):
                    indices.append(to_iter)

        iter_index += 1

    return set(indices)


def _apply_bar_regex(left_child, right_child, check):
    '''(RegexTree, RegexTree, str) -> set of int
    Applies the BarTree given the child and the check to perform on. Returns
    the set of ints that correspond to the various subsequences that are
    matched, such that integer i accepts all values before i to have matched
    the regex. If no integers are returned, this regex failed completely. In
    particular, this will match the left or right regex and append both
    possibilities to one set. This accounts for alternating matches for Star.

    >>> left = DotTree(Leaf('0'), Leaf('1'))
    >>> right = Leaf('1')
    >>> _apply_bar_regex(left, right, '01')
    {2}
    >>> _apply_bar_regex(left, right, '1')
    {1}
    >>> _apply_bar_regex(left, right, '02')
    set()
    >>> right = Leaf('0')
    >>> _apply_bar_regex(left, right, '01')
    {1, 2}
    '''
    # We force both matches, left and right.
    left = _regex_match_helper(left_child, check)
    right = _regex_match_helper(right_child, check)

    # All of the possibilities are the union of the two sets (all unique),
    # where any index is matched by either left OR right (or both).
    return left.union(right)


def _apply_dot_regex(left, right, check):
    '''(RegexTree, RegexTree, str) -> set of int
    Applies the dot regex on the given check string. Returns the set of ints
    that correspond to the various subsequences that are matched, such that
    integer i accepts all values before i to have matched the regex. In
    particular, it will match the left and right, accumulating all the possible
    ways for this to be done. An empty set means complete failure.

    >>> left = StarTree(BarTree(Leaf('0'), Leaf('1')))
    >>> right = Leaf('1')
    >>> _apply_dot_regex(left, right, '2')
    set()
    >>> _apply_dot_regex(left, right, '0')
    set()
    >>> _apply_dot_regex(left, right, '01')
    {2}
    >>> _apply_dot_regex(left, right, '111') == {1, 2, 3}
    True
    '''
    # We want to return the intersection of where left AND right work.
    intrsection = set()

    # We get the set of all indices that can work with the left, we start here.
    left_indices = _regex_match_helper(left, check)

    # We apply the right side on every left index, adding only those that work
    for left_index in left_indices:
        right_indices = _regex_match_helper(right, check[left_index:])

        # The resultant intersection is where the right side worked (and left).
        for right_index in right_indices:
            # We add left and right together to get the resultant pass index.
            resultant_index = left_index + right_index
            intrsection.add(resultant_index)

    return intrsection


def build_regex_tree(reg):
    '''(str) -> RegexTree
    Builds a regex tree given a valid regex string.

    REQ: valid regex string.
    RAISES: InvalidRegexException if a bad regex string is presented.

    >>> build_regex_tree('0')
    Leaf('0')
    >>> build_regex_tree('((0|1).2*)')
    DotTree(BarTree(Leaf('0'), Leaf('1')), StarTree(Leaf('2')))
    >>> build_regex_tree('(0.)*')
    Traceback (most recent call last):
        ...
    InvalidRegexException: Unsupported regex format.
    '''
    # Check that REQ is satisfied.
    if (not is_regex(reg)):
        raise InvalidRegexException("Unsupported regex format.")

    # Delegate to helper (it does not validate).
    return _build_regex_tree(reg)


def _build_regex_tree(reg):
    '''(str) -> RegexTree
    Returns a regex tree corresponding to the given (valid) regex.

    REQ: valid regex string. This helper function will not raise an exception
    on a bad regex string. Unsafe for external use.

    >>> _build_regex_tree('0')
    Leaf('0')
    >>> _build_regex_tree('((0|1).2*)')
    DotTree(BarTree(Leaf('0'), Leaf('1')), StarTree(Leaf('2')))
    '''
    # Last letter is oper., build everything before it for the star tree to ret
    if (reg[-1] == ALL_OP):
        return StarTree(_build_regex_tree(reg[:-1]))
    # Binary case (when first char is '('): we delegate to the binary builder.
    elif (reg[0] == BINARY_LEFT):
        return _build_binary_tree(reg)
    # If we don't have a binary tree or star tree, then we have a basic tree.
    else:
        # We simply use the (supposedly ONLY) character to build.
        return Leaf(reg)


def _build_binary_tree(reg):
    '''(str) -> RegexTree
    Builds a binary tree given the regular expression with the outermost
    expression being a binary one (i.e. dot or bar).

    REQ: the given binary regex (i.e. (   .   ) or (   |   )) is a valid
    binary regex, and not a unary one. Since this is a helper function,
    failure to meet this REQ may be fatal, without a specific exception. When
    used internally, this will never be an issue. Unsafe for external use!

    >>> _build_binary_tree('(1.0)')
    DotTree(Leaf('1'), Leaf('0'))
    >>> _build_binary_tree('(e|1)')
    BarTree(Leaf('e'), Leaf('1'))
    >>> _build_binary_tree('((0.1).(2|0))')
    DotTree(DotTree(Leaf('0'), Leaf('1')), BarTree(Leaf('2'), Leaf('0')))
    '''
    # Get the inner expression as well as operator index and type.
    inner = reg[1:-1]
    op_index = _find_operator(inner)
    op = inner[op_index]

    # Build left and right trees, we do not need to validate.
    left_tree = _build_regex_tree(inner[:op_index])
    right_tree = _build_regex_tree(inner[op_index + 1:])

    # Construct this tree using left and right.
    if (op == OR_OP):
        ret = BarTree(left_tree, right_tree)
    # Since this is an internal helper, we know the other op is AND.
    else:
        ret = DotTree(left_tree, right_tree)

    return ret


# Some main testing code.
if (__name__ == "__main__"):
    import doctest
    doctest.testmod()
