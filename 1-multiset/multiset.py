from skiplist import *


class MultiSet:

    '''MultiSet that contains only comparable types.'''

    # Representation of MultiSet constants
    REPR_START = "MultiSet(["
    REPR_DELIMETER = ', '
    REPR_END = "])"

    # Error customizations.
    INSERT_ERROR = "The element insertion was incomparable with set items."
    # A failed count shouold returen 0, i.e. not in there.
    COUNT_ERROR_SIZE = 0
    # An element with an incomparable type cannot be in the multiset.
    CONTAINS_ERROR = False

    def __init__(self, skip_list=None):
        '''(MultiSet [, SkipList]) -> NoneType
        Initializes this multiset, with a specific skip list if given.
        '''
        # This multiset is implemented with a skip list; it has a skip list.
        if skip_list is None:
            skip_list = SkipList()
        self._skip_list = skip_list

    def __contains__(self, elem):
        '''(MultiSet, obj) -> bool
        Returns true iff this multiset has atleast one occurence of given
        element.
        '''
        # Search for the element, convert None/obj to False/True.
        try:
            ret = bool(self._skip_list.search(elem))
        except TypeError:
            # For contain it is irrelevant about the TypeError; false assumed.
            ret = MultiSet.CONTAINS_ERROR
        return ret

    def count(self, elem):
        '''(MultiSet, obj) -> int
        Returns the number of occurences of a given element.
        '''
        # Delegate to skip list's count method.
        try:
            return self._skip_list.count(elem)
        except TypeError:
            # For count it is not req'd to state TypeError; return 0.
            return MultiSet.COUNT_ERROR_SIZE

    def insert(self, elem):
        '''(MultiSet, obj) -> NoneType
        Adds the given element to the multiset.

        REQ: type(elem) should be comparable to those that are already in the
        set, otherwise a type error will occur.
        RAISES: TypeError iff trying to insert an incomparable type.
        '''
        try:
            # Simply insert into skiplist.
            self._skip_list.insert(elem)
        except TypeError:
            # Incomparable type, the user must be notified.
            raise TypeError(MultiSet.INSERT_ERROR)

    def remove(self, elem):
        '''(MultiSet, obj) -> NoneType
        Removes the given element from this skip list.
        '''
        # Simply remove from skiplist.
        self._skip_list.remove(elem)

    def clear(self):
        '''(MultiSet) -> NoneType
        Clears this skip list from all elements.
        '''
        # Make a brand new Skiplist.
        self._skip_list = SkipList()

    def __len__(self):
        '''(MultiSet) -> int
        Returns an integer representing the length of this set.
        '''
        # The skiplist has a length method that will be suitable.
        return len(self._skip_list)

    def __repr__(self):
        '''(MultiSet) -> str
        Returns a developer-friendly string representation of the contents of
        this multiset, in the format MultiSet([x1, x2, ..., xn]) where each
        'xi' represents a single occurence of an element.
        '''
        # Start with 'MultiSet(['
        to_ret = MultiSet.REPR_START

        # Append each element's repr in the skip list
        for elem in self._skip_list:
            to_ret += repr(elem) + MultiSet.REPR_DELIMETER

        # Remove the last delimeter if it is there, add "])" and return it.
        return to_ret.strip(MultiSet.REPR_DELIMETER) + MultiSet.REPR_END

    def __eq__(self, mset2):
        '''(MultiSet, MultiSet) -> bool
        Returns true if and only if both multisets share the exact number of
        occurences and type of objects.
        '''
        # This is equivalent to the skip list comparison.
        return self._skip_list == mset2._skip_list

    def __le__(self, mset2):
        '''(MultiSet, MultiSet) -> bool
        Returns true if and only if every element in this multiset is also in
        the given multiset.
        '''
        # Determine if this is a subset by counting that each element in this
        # is less than or equal to the count in mset2.
        is_subset = True
        done = False

        # We continue checking until failure or completion.
        self_iter = self._skip_list.unique_iter()
        while is_subset and not done:
            try:
                elem = next(self_iter)
                is_subset = self.count(elem) <= mset2.count(elem)
            except StopIteration:
                done = True

        return is_subset

    def __sub__(self, mset2):
        '''(MultiSet, MultiSet) -> MultiSet
        Returns a multiset that contains every element found in this multiset
        less any element(s) that could be found in the given multiset.
        '''
        # Create a new multiset to place the subtracted information into.
        to_sub = MultiSet()

        # Grab an iterator in unique mode.
        for elem in self._skip_list.unique_iter():
            # Take the different in count between this and the operand, and
            # add that to the new list.
            diff = self.count(elem) - mset2.count(elem)
            for count in range(diff):
                to_sub.insert(elem)

        return to_sub

    def __isub__(self, mset2):
        '''(MultiSet, MultiSet) -> MultiSet
        Mutates this multiset by removing all elements from this set that are
        found in the given set.
        '''
        # Grab an iterator in unique mode on mset2.
        for elem in mset2._skip_list.unique_iter():
            elem_count = mset2.count(elem)

            # Try to remove as many as possible, note that the skip list
            # remove method returns true iff the remove was succesful.
            count = 0
            while count < elem_count and self._skip_list.remove(elem):
                count += 1

        return self

    def __add__(self, mset2):
        '''(MultiSet, MultiSet) -> MultiSet
        Returns a multiset that contains every element found in this multiset
        plus all elements (and all of their occurences) that are in the given
        multiset.
        '''
        # This is equivalent to adding the skip list in this multiset with the
        # given multiset's skip list.
        return MultiSet(skip_list=(self._skip_list + mset2._skip_list))

    def __iadd__(self, mset2):
        '''(MultiSet, MultiSet) -> MultiSet
        Adds to this multiset, all the elements of the given multiset.
        '''
        # This is equivalent to appending the skip list via list
        self._skip_list += mset2._skip_list
        return self

    def __and__(self, mset2):
        '''(MultiSet, MultiSet) -> MultiSet
        Returns the set-theory equivalent of an intersection between two sets,
        except multiple instances are also accounted for.
        '''
        # Determine which is smaller, and get unique iterator on that one; for
        # efficiency as len(intersection) is the minimum of the two lengths.
        if len(self) < len(mset2):
            itered = self
            other = mset2
        else:
            itered = mset2
            other = self

        # Create the intersection multiset which will be returned.
        intersection = MultiSet()

        # Now iterate on the smaller one, checking for occurences...
        for elem in itered._skip_list.unique_iter():
            # The minimum of the counts is what the intersection will yield.
            final_count = min(itered.count(elem), other.count(elem))

            # Now insert the min
            for i in range(final_count):
                intersection.insert(elem)

        return intersection

    def __iand__(self, mset2):
        '''(MultiSet, MultiSet) -> MultiSet
        Mutates this set to contain only those elements (and their occurences)
        that are common to both multisets.
        '''
        # Get all unique values of both this and the other set, conslidated
        # into one list, making sure that the second list does not add extras.
        both_unique = SkipList()
        for elem in self._skip_list.unique_iter():
            both_unique.insert(elem)
        for elem in mset2._skip_list.unique_iter():
            if elem not in both_unique:
                both_unique.insert(elem)

        # Iterate once on this new combined unique list.
        for elem in both_unique:
            # We want the intersection, thus the minimum count between the two.
            cur_count = self.count(elem)
            final_count = min(cur_count, mset2.count(elem))

            # So the amount we remove will be the different between cur_count,
            # and the final_count (always <= cur_count ==> remove_couunt >= 0)
            remove_count = cur_count - final_count

            # Remove the difference
            for count in range(remove_count):
                self.remove(elem)
        # Now operate the other way around.
        return self

    def isdisjoint(self, mset2):
        '''(MultiSet, MultiSet) -> bool
        Returns true iff the two sets share no common element.
        '''
        # This happens if there intersection is empty.
        return (len(self & mset2) == 0)