"""
This file implements skip list.
Skip list can do search, insert and delete in O(lg n) time,
in O(n) space, with high probability
"""
from __future__ import annotations

from random import randrange
from typing import List, Optional, Tuple


class SkipListNode:
    def __init__(self, value: int = -1):
        self.value: int = value
        self.next: Optional[SkipListNode] = None
        self.pre: Optional[SkipListNode] = None
        self.down: Optional[SkipListNode] = None
        self.up: Optional[SkipListNode] = None

    def search(self, x: int, path: List[SkipListNode]) \
            -> Tuple[Optional[SkipListNode], List[SkipListNode]]:
        """
        search and return the node with value x
        (node, predecessor, successor)
        """
        if self.value == x:
            # item found, go to level 0 to find the position
            if self.down is None:
                # item found
                return self, path
            else:
                # go down
                path.append(self)
                return self.down.search(x, path)

        if self.down is None:
            # level 0, linear search
            if self.next is None or self.next.value > x:
                # hit list end or larger value at level 0, return None
                return None, path
            else:
                return self.next.search(x, path)

        if self.next is None or self.next.value > x:
            # hit list end or larger value, go down level
            path.append(self)
            return self.down.search(x, path)
        else:
            return self.next.search(x, path)

    def search_node_right_before(self, x: int, path: List[SkipListNode]) \
            -> Tuple[SkipListNode, List[SkipListNode]]:
        """
        search the node right before the value x should be inserted
        """
        if self.value == x:
            return self.search(x, path)
        if self.down is None:
            # level 0, linear search
            if self.next is None or self.next.value > x:
                return self, path
            else:
                return self.next.search_node_right_before(x, path)
        if self.next is None or self.next.value > x:
            path.append(self)
            return self.down.search_node_right_before(x, path)
        return self.next.search_node_right_before(x, path)

    def insert_after(self, x: int) -> SkipListNode:
        """
        insert a node as successor of current node
        """
        new_node = SkipListNode(value=x)
        new_node.next = self.next
        new_node.pre = self
        self.next = new_node
        if new_node.next is not None:
            new_node.next.pre = new_node
        return new_node

    def insert_above(self) -> SkipListNode:
        new_node = SkipListNode(value=self.value)
        new_node.down = self
        self.up = new_node
        return new_node

    def delete(self) -> None:
        if self.up is not None:
            self.up.delete()
        self.pre.next = self.next
        if self.next is not None:
            self.next.pre = self.pre


class SkipList:
    def __init__(self) -> None:
        self.node_list: List[SkipListNode] = list()

    def is_empty(self) -> bool:
        return len(self.node_list) == 0

    def top_list_node(self) -> SkipListNode:
        return self.node_list[len(self.node_list) - 1]

    def search(self, x: int) -> bool:
        n, _ = self.top_list_node().search(x, [])
        return n is not None

    def insert(self, x: int) -> None:
        print(f"inserting {x}")
        if self.is_empty():
            # if the list is empty
            self.node_list.append(SkipListNode(value=x))
            return
        if self.node_list[0].value > x:
            # insert the first element
            new_node = SkipListNode(x)
            new_node.next = self.node_list[0]
            self.node_list[0].pre = new_node
            self.node_list[0].up = None
            self.node_list[0] = new_node
            if len(self.node_list) > 1:
                self.node_list[0].up = self.node_list[1]
                self.node_list[1].down = self.node_list[0]
            for node in self.node_list:
                node.value = x
            return

        node, path = self.top_list_node().search_node_right_before(x, [])
        last_node = node.insert_after(x)

        for path_node in path:
            if randrange(2) == 0:
                break
            new_node = path_node.insert_after(x)
            new_node.down = last_node
            last_node.up = new_node
            last_node = new_node
        else:
            while True:
                if randrange(2) == 0:
                    break
                start_node = self.top_list_node().insert_above()
                new_node = last_node.insert_above()
                self.node_list.append(start_node)
                start_node.next = new_node
                new_node.pre = start_node
                last_node = new_node

    def delete(self, x: int) -> bool:
        print(f'deleting {x}')
        if self.node_list[0].value == x:
            # delete first element
            self.node_list[0] = self.node_list[0].next
            old_up = self.node_list[0].up
            if len(self.node_list) > 1:
                self.node_list[0].up = self.node_list[1]
                self.node_list[1].down = self.node_list[0]
            for node in self.node_list:
                node.value = self.node_list[0].value

            if old_up is not None:
                old_up.delete()
            return True

        node, path = self.top_list_node().search(x, [])
        if node is None:
            return False
        node.delete()
        return True

    def show(self):
        first_row: List[SkipListNode] = []
        process_node = self.node_list[0]
        while process_node is not None:
            first_row.append(process_node)
            process_node = process_node.next

        node_matrix: List[List[Optional[SkipListNode]]] = [[None for _ in first_row] for _ in
                                                           self.node_list]
        node_matrix[0] = first_row
        for i, node in enumerate(first_row):
            node = node.up
            for j in range(1, len(self.node_list)):
                if node is None:
                    break
                node_matrix[j][i] = node
                node = node.up
        value_matrix = '\n'.join(
            ["\t".join([str(n.value) if n is not None else "" for n in row]) for row in
             node_matrix]) + '\n'
        return value_matrix


if __name__ == '__main__':
    ll = SkipList()
    ll.insert(1)
    ll.insert(5)
    ll.insert(10)
    ll.insert(20)
    ll.insert(15)
    ll.insert(25)
    print(ll.show())

    ll.delete(15)
    print(ll.show())
    ll.delete(1)
    print(ll.show())

    ll.insert(1)
    print(ll.show())

    ll.insert(30)
    print(ll.show())
