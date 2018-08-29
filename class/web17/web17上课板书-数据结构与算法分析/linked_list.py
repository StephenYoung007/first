class Node(object):
    def __init__(self, element=-1):
        self.element = element
        self.next = None


"""
不完整的链表实现, 自行补全
"""
class LinkedList(object):
    def __init__(self):
        self.head = None

    # O(1)
    def is_empty(self):
        return self.head is None

    def length(self):
        index = 0
        node = self.head
        while node is not None:
            index += 1
            node = node.next
        return index

    def find(self, element):
        index = 1
        node = self.head
        while node is not None:
            if node.element == element:
                break
            node = node.next
            index += 1
        return index

    def _node_at_index(self, index):
        i = 0
        node = self.head
        while node is not None:
            if i == index:
                return node
            node = node.next
            i += 1
        return None

    def element_at_index(self, index):
        node = self._node_at_index(index-1)
        return node.element


    def insert_before_index(self, position, element):
        node = Node(element)
        if position > 1:
            node_before = self._node_at_index(position -2)
            node.next = self._node_at_index(position-1)
            node_before.next = node
        else:
            node_head = self.head
            self.head = node
            self.head.next = node_head
        return self.element_at_index(position)

    # O(n)
    def insert_after_index(self, position, element):
        node = Node(element)
        node_before = self._node_at_index(position - 1)
        node.next = self._node_at_index(position)
        node_before.next = node
        return self.element_at_index(position + 1)

    # O(1)
    def first_object(self):
        return self.head

    # O(n)
    def last_object(self):
        return self._node_at_index(self.length() - 1)

    # O(n)
    def _append(self, node):
        if self.head is None:
            self.head = node
        else:
            last_node = self.last_object()
            last_node.next = node
            # node.front = last_node

    def __repr__(self):
        st = []
        node = self.head
        while node is not None:
            st.append(node.element)
            node = node.next
        s = ' '.join(str(ele) for ele in st)
        return s

def test():
    list = LinkedList()
    list._append(Node(6))
    print(list, list.length())
    list._append(Node(7))
    print(list)
    list._append(Node(2))
    print(list)
    list.insert_after_index(1, 5)
    print(list)
    list.insert_before_index(1, 4)
    print(list)
    print(list.length())
    print(list.last_object().element)
    print(list.element_at_index(5))
    print(list.find(2))

if __name__ == '__main__':
    test()
