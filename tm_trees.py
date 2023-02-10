"""
Assignment 2: Trees for Treemap

=== CSC148 Summer 2022 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # Below is not needed as the folders should be collapsed and expand_all
        # will expand the files.
        # You will change this in Task 5
        # if len(self._subtrees) > 0:
        #     self._expanded = True
        # else:
        #     self._expanded = False

        self._expanded = False  # All the trees start collapsed

        # TO-DO: (Task 1) Complete this initializer by doing two things:
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.

        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))

        # if self._subtrees is not None or self._subtrees != []:
        #     sum_size = 0
        #     for sub in self._subtrees:
        #         sum_size += sub.data_size
        #         sub._parent_tree = self
        #     self.data_size = sum_size
        # else:
        #     self.data_size = data_size

        self.data_size = data_size
        self._helper_size()

        for sub in self._subtrees:
            sub._parent_tree = self

    def _helper_size(self) -> int:
        """helper for the data_size, it will return the total size of subtree.
        designed to be recursive and reach the leaves of each subtree.
        """
        if not self._subtrees:
            pass
        elif self.is_empty():
            self.data_size = 0
        else:
            total = sum(sub._helper_size() for sub in self._subtrees)
            self.data_size = total
        return self.data_size

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # TO-DO: (Task 2) Complete the body of this method.
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        if not self._expanded or not self._subtrees:
            self.rect = rect

        elif self.data_size == 0 or self.is_empty():
            return

        else:
            self.rect = rect
            x, y, width, height = rect
            if width > height:
                x, y = self._helper_width_greater(x, y, width, height)

            else:
                x, y = self._helper_height_greater(x, y, width, height)

    def _helper_width_greater(self, x: int, y: int, width: int, height: int) ->\
            tuple[int, int]:
        """Helper function when width is greater than height.
        """
        for sub in self._subtrees:
            if self.data_size == 0:
                percent = 0
            else:
                percent = sub.data_size / self.data_size
            new_width = math.floor(width * percent)
            new_height = height
            new_x = x + new_width
            new_y = y
            if sub is not self._subtrees[-1]:
                sub.update_rectangles((x, y, new_width, new_height))
            else:
                new_width = width - x + self.rect[0]
                new_height = height
                new_x = x + new_width
                new_y = y
                sub.update_rectangles((x, y, new_width, new_height))
            x = new_x
            y = new_y
        return x, y

    def _helper_height_greater(self, x: int, y: int, width: int, height: int)\
            -> tuple[int, int]:
        """ Helper function when height is greater than equal to width
        """
        for sub in self._subtrees:
            if self.data_size == 0:
                percent = 0
            else:
                percent = sub.data_size / self.data_size
            new_width = width
            new_height = math.floor(height * percent)
            new_x = x
            new_y = y + new_height
            if sub is not self._subtrees[-1]:
                sub.update_rectangles((x, y, new_width, new_height))
            else:
                new_width = width
                new_height = height - y + self.rect[1]
                new_x = x
                new_y = y + new_height
                sub.update_rectangles((x, y, new_width, new_height))
            x = new_x
            y = new_y
        return x, y

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        # TO-DO: (Task 2) Complete the body of this method.
        if self._expanded:
            if not self._subtrees:
                return [(self.rect, self._colour)]
            elif self.is_empty():
                return []
            else:
                final = []
                for sub in self._subtrees:
                    final.extend(sub.get_rectangles())
                return final
        else:
            return [(self.rect, self._colour)]

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        # TO-DO: (Task 3) Complete the body of this method

        given_x, given_y = pos

        x, y, width, height = self.rect

        if not self._expanded or not self._subtrees:
            if given_x in range(x, x + width + 1) and \
                    given_y in range(y, y + height + 1):
                return self
            return None

        elif self.is_empty():
            return None

        else:
            return self._helper_get_position(pos)

    def _helper_get_position(self, pos: Tuple[int, int], ) -> Optional[TMTree]:
        """Helper function for the get_tree_at_position.
        """
        finds = []
        for sub in self._subtrees:
            if sub.get_tree_at_position(pos) is not None:
                finds.append(sub.get_tree_at_position(pos))

        if len(finds) + 1 > 2:
            best = finds[0]
            for tree in finds:
                if best.rect[0] > tree.rect[0]:
                    best = tree
                elif best.rect[1] > tree.rect[1]:
                    best = tree
            return best

        elif len(finds) + 1 == 2:
            return finds[0]

        else:
            return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        # TO-DO: (Task 4) Complete the body of this method.
        return self._helper_size()

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        # TO-DO: (Task 4) Complete the body of this method.
        if destination._subtrees != [] and not self._subtrees:
            parent = self.get_parent()
            parent._subtrees.remove(self)
            parent.update_data_sizes()
            destination._subtrees.append(self)
            destination.update_data_sizes()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        # TO-DO: (Task 4) Complete the body of this method
        if not self.is_empty() and not self._subtrees:
            change = math.ceil(factor * self.data_size)
            self.data_size += change
            self._parent_tree.update_data_sizes()

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """
        # TO-DO: (Task 4) Complete the body of this method
        if self.get_parent():
            parent = self.get_parent()
            parent._subtrees.remove(self)
            parent.update_data_sizes()
            return True
        else:
            return False

    # TO-DO: (Task 5) Write the methods expand, expand_all, collapse, and
    # TO-DO: collapse_all, and add the displayed-tree functionality to the
    # TO-DO: methods from Tasks 2 and 3
    def expand(self) -> None:
        """Expand the tree to show subtrees if not expanded already.
        If expanded do nothing.
        """
        if not self._subtrees or self._expanded:
            return
        self._expanded = True
        self.update_rectangles(self.rect)

    def expand_all(self) -> None:
        """Expand the tree and all subtrees if not expanded.
        If expanded do nothing.
        """
        if not self._subtrees or self._expanded:
            return
        self._expanded = True
        for sub in self._subtrees:
            sub.expand_all()
        self.update_rectangles(self.rect)

    def collapse(self) -> None:
        """Collapse current tree.
        Do nothing if the tree is a root (no parent)
        """
        if not self.get_parent():
            return
        parent = self.get_parent()
        parent._expanded = False

    def collapse_all(self) -> None:
        """Collapse all the trees

        """
        if not self.get_parent():
            root = self
        else:
            curr = self.get_parent()
            while curr.get_parent():
                curr = curr.get_parent()
            root = curr
        root._helper_collapse_all()

    def _helper_collapse_all(self) -> None:
        """Recursive function for the collapse all.
        """
        self._expanded = False
        if not self._subtrees:
            return
        for sub in self._subtrees:
            sub._helper_collapse_all()

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree\
                       .get_path_string() + self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        >>> file = FileSystemTree('/Users/mohamadsabagh/Desktop/School Work/A 2021-2022@UTM/SUMMER 2022/CSC148/csc148 Pycharm/assignments/a2/example-directory/workshop/prep/reading.md')
        >>> file.data_size
        6
        >>> file._name
        'reading.md'
        >>> file.update_rectangles((1,1,1,1))
        >>> file._expanded = True
        >>> file.get_rectangles()
        [((1, 1, 1, 1), (20, 226, 19))]
        >>> net = FileSystemTree('/Users/mohamadsabagh/Desktop/School Work/A 2021-2022@UTM/SUMMER 2022/CSC148/csc148 Pycharm/assignments/a2/example-directory/workshop/prep/images')
        >>> net.data_size
        16
        >>> net._name
        'images'
        >>> net.update_rectangles((2,2,2,2))
        >>> net._expanded = True
        >>> net.get_rectangles()
        [((2, 2, 2, 2), (237, 101, 183))]
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        # TO-DO: (Task 1) Implement the initializer
        sub_tree = []
        if os.path.isdir(path):

            for name in os.listdir(path):
                sub_item = os.path.join(path, name)
                sub_tree.append(FileSystemTree(sub_item))

        super().__init__(os.path.basename(path), sub_tree,
                         os.path.getsize(path))

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
