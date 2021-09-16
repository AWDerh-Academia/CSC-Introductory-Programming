import random


class BaseNode:

    '''The barebone, abstract node implementation.'''

    # The base case for a BaseNode length call.
    BASE_NODE_LEN = 1

    # Base case for comparisons of a BaseNode
    BASE_CASE_COMPARISON = False

    # Base case for count
    COUNT_BASE_CASE = 0

    def __init__(self, below_node=None):
        '''(BaseNode [, BaseNode]) -> NoneType
        Initializes this base node with the default optional parameter of
        below node to None.
        '''
        # Set the below node to given value or None by default.
        self.set_below(below_node)

    def get_below_node(self):
        '''(BaseNode) -> BaseNode
        Retrieves the below node.
        '''
        return self._below_node

    def set_below(self, node_to_set):
        '''(BaseNode, BaseNode) -> NoneType
        Sets the below node.
        '''
        self._below_node = node_to_set

    def get_last_below_node(self):
        '''(BaseNode) -> BaseNode
        Returns the last level of nodes.
        '''
        # Recursively; if there is a below node, request a below node
        if self._below_node is not None:
            return self._below_node.get_last_below_node()
        # Base case; no more below nodes, so return itself.
        return self

    def __eq__(self, elem):
        '''(BaseNode, obj) -> bool
        Returns whether or not this BaseNode is equal to given element.
        '''
        # By base case def'n, always False.
        return BaseNode.BASE_CASE_COMPARISON

    def __gt__(self, elem):
        '''(BaseNode, obj) -> bool
        Returns whether or not this BaseNode is greater than given element.
        '''
        # By base case def'n, always False.
        return BaseNode.BASE_CASE_COMPARISON

    def __lt__(self, elem):
        '''(BaseNode, obj) -> bool
        Returns whether or not this BaseNode is less than given element.
        '''
        # By base case def'n, always False.
        return BaseNode.BASE_CASE_COMPARISON

    def __len__(self):
        '''(BaseNode) -> int
        Returns an integer representing the length of this node, which is
        one if it is the base node being queried.
        '''
        return BaseNode.BASE_NODE_LEN

    def count(self, elem):
        '''(TailNode) -> bool
        Serves as a base case to the ordered ascending count.
        '''
        return BaseNode.COUNT_BASE_CASE


class TailNode(BaseNode):

    '''The tail node acts like a sentinel and inherits the base below_node
    property of the BaseNode.'''

    # String output for base case of head node and tail nodes
    TAIL_NODE_STR = 'tail'

    def __init__(self, below_node=None):
        '''(TailNode [, BaseNode])
        Initializes this tail node with the below node being any node that
        is or extends BaseNode (which is every node in this module).
        '''
        # Ensure constructor of super class executes first.
        super().__init__(below_node)

    def __str__(self):
        '''(TailNode)
        Returns the string representation of this tail node, which is 'tail'.
        '''
        return TailNode.TAIL_NODE_STR


class HeadNode(TailNode):

    '''A head node is a tail node that also supports a next node pointer.'''

    # String representation of just this object.
    HEAD_NODE_STR = 'head'
    # String formatting constant
    NEW_LINE = '\n'

    def __init__(self, below_node=None, next_node=None):
        '''(HeadNode [, BaseNode, BaseNode]) -> NoneType
        Initializes a HeadNode whose optional parameters below_node and
        next_node are None and a new TailNode() by default.
        '''
        # Initialize the super constructor with given below node.
        super().__init__(below_node)

        # By default, a new TailNode is made.
        if next_node is None:
            next_node = TailNode()

        # Set next node to None by default, otherwise (implicit) given value.
        self._next_node = next_node

    def get_next_node(self):
        '''(HeadNode) -> BaseNode or NoneType
        Returns a node iff there is a next node, or else this function must
        return None.
        '''
        # Returns the next node if there is one; can return None.
        return self._next_node

    def set_next_node(self, node_to_set):
        '''(HeadNode, BaseNode) -> NoneType
        Sets the next node that this node shall point to.
        '''
        # Sets the next node.
        self._next_node = node_to_set

    def __str__(self):
        '''(HeadNode) -> str
        Returns a string representation of this object.
        '''
        # Just return saying Head.
        return HeadNode.HEAD_NODE_STR

    def level_to_str(self, node_sep=' -> '):
        '''(HeadNode) -> str
        Returns a string representation of this level starting at this node.
        '''
        # Cannot be done recursively o/wise recursion depth error
        # Thus loop through all nodes on the right and add.
        ret = str(self)
        h = self._next_node

        # Stop loop if h None or h is a TalNode
        while (h is not None) and (type(h) is not TailNode):
            # Append to ret the str() of this node and set to next.
            ret += node_sep + str(h)
            h = h._next_node

        return ret

    def levels_to_str(self, node_sep=' -> '):
        '''(HeadNode) -> str
        Returns a string representation of all levels starting at this level.
        '''
        # Get the entire level as a string
        ret = self.level_to_str()

        # Recursively request the next level.
        below = self.get_below_node()
        if below is not None:
            ret += HeadNode.NEW_LINE + below.levels_to_str(node_sep)

        return ret

    def __len__(self):
        '''(SkipList) -> int
        Returns an integer representing the length of this list.
        '''
        # Starting at one (which is this node)...
        length = 1

        # Add the length of all other nodes.
        if self._next_node:
            length += len(self._next_node)

        # Return the final accumulated length.
        return length


class ElementNode(HeadNode):

    '''This is a type of HeadNode that also contains elements.'''

    # Errors for a comparisons against incompatible type objects.
    ERROR_LT = ("This LESS_THAN comparison is not compatible with given "
                "node object, and element")
    ERROR_EQ = ("This EQUAL_TO comparison is not compatible with given "
                "node object, and element")
    ERROR_GT = ("This GREATER_THAN, >, comparison is not compatible with given"
                " node object, and element")

    def __init__(self, value, below_node=None, next_node=None):
        '''(HeadNode, obj [, BaseNode, BaseNode]) -> NoneType
        Constructs this element node with the given value and the optional
        parameters of below node and next node set to None by default.
        '''
        # The super constructor can handle both below and next nodes.
        super().__init__(below_node, next_node)

        # Set the value of this node (unique to this class vs extending class).
        self._value = value

    def __lt__(self, elem):
        '''(HeadNode, obj) -> bool
        Determines if this node is less than another object.

        RAISES TypeError if this value and the given value cannot be compared.
        '''
        # Try a comparison, raising a customized TypeError if not possible.
        try:
            return self._value < elem
        except(TypeError):
            raise TypeError(ElementNode.ERROR_LT)

    def __eq__(self, elem):
        '''(HeadNode, obj) -> bool
        Determines if this node is equal to another object.

        RAISES TypeError if this value and the given value cannot be compared.
        '''
        # Try a comparison, raising a customized TypeError if not possible.
        try:
            return self._value == elem
        except(TypeError):
            raise TypeError(ElementNode.ERROR_EQ)

    def __gt__(self, elem):
        '''(HeadNode, obj) -> bool
        Determines if this node is greater than another object.

        RAISES TypeError if this value and the given value cannot be compared.
        '''
        # Try a comparison, raising a customized TypeError if not possible.
        try:
            return self._value > elem
        except(TypeError):
            raise TypeError(ElementNode.ERROR_GT)

    def __str__(self):
        '''(ElementNode) -> str
        Returns the string representation of this element node.
        '''
        # Return str of value.
        return str(self._value)

    def get_value(self):
        '''(ElementNode) -> obj
        Accessor for the value of this node.
        '''
        return self._value

    def count(self, elem):
        '''(ElementNode) -> int
        Counts the instances of a given element.

        REQ: The list must be ordered in a non-descending fashion
        '''
        # Base case; If we've reached a node greater than element, return 0
        if self.get_value() > elem:
            return 0
        else:
            # Check if the node has a value equal to this element.
            ret = 0
            if self.get_value() == elem:
                ret += 1
            # Add the count of the next node as well (recursive step).
            return ret + self.get_next_node().count(elem)


class SkipList:

    '''Randomized skip-list implementation with only comparable types.'''

    # Probability parameter bounds and defaults.
    PROB_LOWER_BOUND = 0
    PROB_UPPER_BOUND = 1
    DEFAULT_PROBABILITY = 0.5

    # Empty list length and count constants.
    EMPTY_LIST_LEN = 0
    EMPTY_LIST_COUNT = 0

    # Skip list errors
    ERROR_TYPE_SEARCH = ("Cannot search with incomparable types.")
    ERROR_TYPE_INSERT = ("When inserting, the type must be comparable with "
                         + " whatever is already in the list.")

    # Nested exception class for appropriately making a SkipList module.
    class RandProbException(Exception):

        '''Thrown when a SkipList is initialized with a bad random
        probability parameter.
        '''

        FIXED_P_MINIMUM = "The probability parameter must be greater than 0."
        FIXED_P_MAXIMUM = "The probability parameter must be less than 1."

        def __init__(self, fixed_p):
            self._fixed_p = fixed_p

        def __str__(self):
            if self._fixed_p <= SkipList.PROB_LOWER_BOUND:
                return RandProbException.FIXED_P_MINIMUM
            else:
                return RandProbException.FIXED_P_MAXIMUM

    # Nested, private iterator helper class for encapsulation and modular code.
    class _SkipIterator:

        '''The iterator used for looping through all or unique elements in a
        singly-linked list, and it actively excludes the tail/sentinel.
        '''

        def __init__(self, cur_node, unique_mode=False):
            '''(_SkipIterator, HeadNode) -> NoneType
            Creates an iterator given the HeadNode to start iterating upon.
            (Note that since ElementNode extends HeadNode, it too is an
            acceptable init cur_node value.) It also takes a unique_mode
            parameter, where it passes over duplicates.
            '''
            # Save the current node as the loop node.
            self._loop_node = cur_node

            # Unique mode: only iterating through one occurence of each elem.
            self._unique_mode = unique_mode
            if self._unique_mode:
                self._last_elem = None

        def __iter__(self):
            '''(_SkipIterator) -> _SkipIterator
            Returns the iterator for this object (i.e. itself).
            '''
            return self

        def __next__(self):
            '''(_SkipIterator) -> obj
            Returns the next object in this list.
            '''
            # If the current loop node is a sentinel, stop as we've finished.
            if type(self._loop_node) is TailNode:
                raise StopIteration()
            else:
                # If the next node is not a sentinel then continue; else stop.
                next_node = self._loop_node.get_next_node()

                # If in unique mode, continue until unique element.
                if self._unique_mode:
                    while next_node == self._last_elem:
                        next_node = next_node.get_next_node()
                    # Update the last element.
                    self._last_elem = next_node

                # WE stop iff next node is a sentinel
                if type(next_node) is TailNode:
                    raise StopIteration()
                else:
                    # If it's not a sentinel, valid element node; return it.
                    self._loop_node = next_node
                    return next_node.get_value()

    def __init__(self, fixed_p=DEFAULT_PROBABILITY):
        '''(SkipList[, int]) -> NoneType
        Initializes the SkipList the coin-toss probability number given or
        default at 0.5.

        REQ: the list formed by the head node must be an appropriate skip list
        format: non-descending order with head as start, elements in between
        and tail on the end. fixed_p range is 0 < fixed_p < 1.

        RAISES RandProbException if fixed_P is not in said range.
        '''
        self._head = HeadNode()
        self._tail = self._head.get_next_node()
        self._length = 0

        # Probability parameter check w/ customized exceptions.
        if (fixed_p <= SkipList.PROB_LOWER_BOUND or
                fixed_p >= SkipList.PROB_UPPER_BOUND):
            # If bad probability given; raise customized exception.
            raise SkipList.RandProbException(fixed_p)
        else:
            # Good probability float, save it (privately) for later use.
            self._probability = fixed_p

    def search(self, elem):
        '''(SkipList, obj) -> obj
        Returns the element if it is found, otherwise returns None.

        RAISES TypeError if trying to search with incompatible types.
        '''
        # Try searching for the node before, returning None if not found.
        search_attempt = self._search_before(elem)
        if search_attempt is not None:
            # Found, so return the value of the next node.
            return search_attempt.get_next_node().get_value()
        return None

    def _search_before(self, elem):
        '''(SkipList, obj) -> NoneType or ElementNode
        Searches for the node that is before the one containing given element.
        Returns none if the node is not found.

        RAISES TypeError if there was an issue comparing elements.
        '''
        # Try recursively searching for the node
        try:
            # Start off the helper at the first linked list.
            return self._rec_search_before(elem, self._head)
        except(TypeError):
            # Thrown during a comparison error.
            raise TypeError(SkipList.ERROR_TYPE_SEARCH)

    def _search_before_level(self, elem, cur_node):
        '''(SkipList, obj, HeadNode, HeadNode) -> HeadNode or TailNode
        Searches the nodes on a level to return the node before the
        element sought after.

        REQ: call cur_node on the head, otherwise you may skip the first.
        '''
        # Must be iterative, long levels may cause an issue o/w.
        # We cannot do anything at a tail node.
        if type(cur_node) is not TailNode:
            # If not a tail node, keep looking until next == elem.
            next_node = cur_node.get_next_node()
            while next_node < elem:
                # Continue while the next node is less than the element.
                cur_node = next_node
                next_node = cur_node.get_next_node()

        # returns the current node which could be  head, tail or element.
        return cur_node

    def _rec_search_before(self, elem, cur_node):
        '''(SkipList, obj, obj) -> obj or NoneType
        Recursively searches for the node before the one containing the
        element sought after.
        '''
        # Recursively finds and searches the first level containing
        # Base case: if the level starts null, than element is not found...
        if cur_node is None:
            return None

        # Continue linearly until the next node is larger.
        cur_node = self._search_before_level(elem, cur_node)
        next_node = cur_node.get_next_node()

        # Iff the next node is equal to the element, return the current node.
        if next_node == elem:
            return cur_node
        else:
            # otherwise, recurse on the next level.
            return self._rec_search_before(elem, cur_node.get_below_node())

    def remove(self, elem):
        '''(SkipList, obj) -> bool
        Returns True iff the remove operation sucessfully found the element
        and removed it.
        '''
        # Get the node on the first level before the element.
        try:
            search_before = self._search_before(elem)
        except TypeError:
            # Trying to remove an element whose type is impossible to have.
            return False

        # Operate on a node only. The helper functions ensure this.
        # Returns true iff the removal was successful, otherwise false.
        if search_before is not None and search_before.get_next_node() == elem:
            # Recursively remove, which will return a node if rows were removed
            head = self._rec_removal(search_before, elem)

            # If rows were removed, take the first empty row.
            if head is not None:
                self._head = head

            # Decrement length of list; return successful remove.
            self._length -= 1
            return True

        # Element not found, remove not succesful.
        return False

    def _rec_removal(self, before_elem, elem):
        '''(SkipList, HeadNode, int) -> bool
        Recursively removes an element, given the element before to remove.

        REQ: before_elem is a head node or an element node
        '''
        if before_elem is not None:
            # Given the node before the one to remove, remove below level too.
            new_head_node = self._rec_removal(before_elem.get_below_node(),
                                              elem)

            if new_head_node is not None:
                # If the one below was empty, this one will be as well. To
                # discard the row, we will just return the new head.
                return new_head_node
            else:
                # The last row not empty; must remove an element:
                # we are guaranteed next is the one to remove, and after is
                # either value or sentinel (never none).
                before_elem = self._search_before_level(elem, before_elem)
                before_elem.set_next_node(
                    before_elem.get_next_node().get_next_node())

            # Return before elem if it is a head of a now-empty list.
            if (type(before_elem) is HeadNode
                    and type(before_elem.get_next_node()) is TailNode):
                return before_elem

        # Base case, the element before is none. This means all levels done.
        # Returns None if base case or if this row is not empty.
        return None

    def insert(self, elem):
        '''(SkipList, obj) -> NoneType
        Inserts an object into the skip list.

        REQ: elem must be comparable to types alreayd in the list; not req'd if
        list is empty.
        RAISES: TypeError if trying to add a non-comparable type (w/ those in
        the list).
        '''
        # Try to insert the element, which will fail for incomparable types.
        try:
            # Recursively insert to present levels, return last level inserted
            elem_below = self._rec_insert(self._head, elem)
            if elem_below is not None:
                # If the last level was inserted, then add levels
                self._head = self._rec_insert_level(elem, elem_below,
                                                    self._head)
        except TypeError:
            # Raise a customized message
            raise TypeError(SkipList.ERROR_TYPE_INSERT)

        # Increment length of list, since insert either works or crashes.
        self._length += 1

    def _rec_insert(self, before_node, elem):
        '''(SkipList, ElementNode, obj) -> obj or NoneType
        Helper for recursively inserting a element, given the node before it
        This function returns the a inserted Node or None if level did not pass
        the coin toss.

        REQ: before_node, elem not None. elem comparable with those in the
        list, otherwise a TypeError will be raised.
        '''
        # Insert on level after, to get details regarding how to insert on this
        # First, get the position to add to, by looping through all nodes
        # and finding the node before where to add.
        before_node = self._search_before_level(elem, before_node)

        # The place where we will add_before, can be used as a hint for the
        # level below. Leave the height as-is, since we don't know the depth
        # of the insertion.
        below_node = before_node.get_below_node()
        insert = None
        if below_node is not None:
            insert = self._rec_insert(below_node, elem)

        # Try insert if at last level, or below was inserted.
        if (insert is not None) or (below_node is None):
            # Perform a coin toss to determine if one should add, overriden
            # By if it is the last level.
            if (below_node is None) or (random.random() < self._probability):
                # Create the node to add to this level. Set "before" to it.
                to_add = ElementNode(elem, below_node=insert,
                                     next_node=before_node.get_next_node())
                before_node.set_next_node(to_add)

                # Return added node so previous frame can reference it below.
                return to_add

        # Base Case: when this level did not add a node.
        return None

    def _rec_insert_level(self, elem, elem_below, head_below):
        '''(SkipList, obj, ElementNode, HeadNode) -> HeadNode
        Recursively inserts levels, used after inserting when coin tosses are
        continuously succesful.
        '''
        # Perform a coin toss and add iff we get a value >= probability.
        if random.random() < self._probability:
            # Link node -> tail, then head -> node (-> tail)
            # Created given all links to the level below.
            elem_link = ElementNode(elem, below_node=elem_below,
                                    next_node=self._tail)
            list_head = HeadNode(below_node=head_below, next_node=elem_link)

            # Use this created level as the below pointers, and request another
            # level to be created recursively.
            return self._rec_insert_level(elem, elem_link, list_head)
        else:
            # On the last call, when all levels inserted, return new head
            return head_below

    def insert_all(self, iterable):
        '''(SkipList, dict or list or SkipList) -> NoneType
        Inserts all of a given iterable structure to this list.
        '''
        # Add ever element into this skip list.
        for elem in iterable:
            self.insert(elem)

    def count(self, elem):
        '''(SkipList, obj) -> int
        Returns the number of occurences of a given object in a skip list.
        '''
        # Must be iterative or else it may exceed rec. depth. Starting at 0.
        count = 0
        # Start at the bottom most level's first occurence of this element.
        start = self._search_before_level(elem,
                                          self._head.get_last_below_node())
        start = start.get_next_node()

        # count until start is no longer = to elem.
        while start == elem:
            start = start.get_next_node()
            count += 1

        return count

    def __str__(self):
        '''(SkipList) -> str
        Returns a string representation of this object, in the
        form '{Head_Node_Str} -> {Next_Node_str} -> ... -> {Tail_Node_Str}'
        - an example would be: 'head -> 1 -> 2 -> tail'.
        '''
        # Recursively get and print the levels, starting at the head.
        return self._head.levels_to_str()

    def __len__(self):
        '''(SkipList) -> int
        Returns an integer representing the length of this list.
        '''
        # Since the node structure is controlled, a recursive or iterative
        # count is not required to return the length, making this O(1).
        return self._length

    def __eq__(self, skiplist2):
        '''(SkipList) -> bool
        Returns whether or not two skiplists are equal. Determine if they have
        same elements and the same number of them.
        '''
        # Quick O(1) length check
        if (len(self) == len(skiplist2)):
            # Both are the same size, ordered. Comparing each element, compares
            # occurences... we start with getting (non-unique) iterators:
            self_iter = iter(self)
            s2_iter = iter(skiplist2)

            # Loop until failure or no more to loop on; return "not failure".
            done = False
            fail = False
            while not done and not fail:
                try:
                    # Failure is determined if a non-equal pair found.
                    fail = next(self_iter) != next(s2_iter)
                except StopIteration:
                    # we've finished. Both will finish at the same time.
                    done = True
            return not fail

        # Lengths where not equal, immediate failure.
        return False

    def __iter__(self):
        '''(SkipList) -> iterator
        Returns an iterator for iteration processes on this list.
        '''
        # Return a Non-None iterator iff the list is Non-empty.
        if self._head is not None:
            # The iterator to return is that of the first element in the
            # lowest level.
            return SkipList._SkipIterator(self._head.get_last_below_node())
        return None

    def unique_iter(self):
        '''(SkipList) -> iterator
        Returns an iterator for iteration processes on this list, in unique
        mode.
        '''
        # Return a Non-None iterator iff the list is Non-empty.
        if self._head is not None:
            # The iterator to return is that of the first element in the
            # lowest level.
            return SkipList._SkipIterator(self._head.get_last_below_node(),
                                          unique_mode=True)
        return None

    def new_averaged_skip_list(self, skiplist2):
        '''(SkipList, SkipList) -> SkipList
        Creates a SkipList for purposes of operations, which has the average
        of the two probabilities of given skiplists.
        '''
        # Take the average of the two probabilities for the new list
        ret_list_prob = (self._probability + skiplist2._probability) / 2
        ret_list = SkipList(fixed_p=ret_list_prob)

        return ret_list

    def __add__(self, skiplist2):
        '''(SkipList, SkipList) -> SkipList
        Returns a new skiplist which are both skip list's concatenated.
        '''
        # Create a skiplist with the average of two probabilities.
        sum_list = self.new_averaged_skip_list(skiplist2)

        # Now for each element in self, insert it.
        sum_list.insert_all(self)

        # Now for each element in skiplist2, insert it to new one.
        sum_list.insert_all(skiplist2)

        return sum_list

    def __iadd__(self, skiplist2):
        '''(SkipList, SkipList) -> NoneType
        Adds to this skiplist, all elements and the number of there occurencesw
        in the given skiplist.
        '''
        # Insert every element in given skip list to this one.
        self.insert_all(skiplist2)

        return self