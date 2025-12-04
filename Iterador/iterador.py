# ============================================================
#   PATRÓN ITERATOR - PROGRAMA 2
# ============================================================

# ------------------------------------------------------------
#   INTERFACES
# ------------------------------------------------------------

class IteratorInterface:
    def has_next(self):
        raise NotImplementedError()

    def next(self):
        raise NotImplementedError()


class IterableStructure:
    def create_iterator(self):
        raise NotImplementedError()


# ------------------------------------------------------------
#   ARRAY / LISTA
# ------------------------------------------------------------

class ArrayStructure(IterableStructure):
    def __init__(self, data):
        self.data = data

    def create_iterator(self):
        return ArrayIterator(self.data)


class ArrayIterator(IteratorInterface):
    def __init__(self, data):
        self.data = data
        self.index = 0

    def has_next(self):
        return self.index < len(self.data)

    def next(self):
        elemento = self.data[self.index]
        self.index += 1
        return elemento


# ------------------------------------------------------------
#   MATRIZ 2D
# ------------------------------------------------------------

class MatrixStructure(IterableStructure):
    def __init__(self, matrix):
        self.matrix = matrix

    def create_iterator(self):
        return MatrixIterator(self.matrix)


class MatrixIterator(IteratorInterface):
    def __init__(self, matrix):
        self.matrix = matrix
        self.fila = 0
        self.col = 0

    def has_next(self):
        return self.fila < len(self.matrix)

    def next(self):
        valor = self.matrix[self.fila][self.col]

        self.col += 1
        if self.col >= len(self.matrix[self.fila]):
            self.col = 0
            self.fila += 1

        return valor


# ------------------------------------------------------------
#   ÁRBOL BINARIO
# ------------------------------------------------------------

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTreeStructure(IterableStructure):
    def __init__(self, root):
        self.root = root

    def create_iterator(self):
        return BinaryTreeIterator(self.root)


class BinaryTreeIterator(IteratorInterface):
    """Recorrido IN-ORDER usando una pila."""
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def has_next(self):
        return len(self.stack) > 0

    def next(self):
        nodo = self.stack.pop()
        valor = nodo.value

        if nodo.right:
            self._push_left(nodo.right)

        return valor


# ------------------------------------------------------------
#   CLIENTE / PRINTER
# ------------------------------------------------------------

class Printer:
    @staticmethod
    def print_all(structure: IterableStructure):
        iterator = structure.create_iterator()
        print("Recorriendo estructura:")

        while iterator.has_next():
            print(f"- {iterator.next()}")


# ------------------------------------------------------------
#   MAIN DE PRUEBA
# ------------------------------------------------------------

if __name__ == "__main__":
    # Array
    arr = ArrayStructure([10, 20, 30])
    Printer.print_all(arr)

    # Matriz
    mat = MatrixStructure([[1, 2], [3, 4], [5, 6]])
    Printer.print_all(mat)

    # Árbol binario
    """
            4
           / \
          2   6
         / \  / \
        1  3 5  7
    """
    root = Node(4,
                Node(2, Node(1), Node(3)),
                Node(6, Node(5), Node(7)))

    tree = BinaryTreeStructure(root)
    Printer.print_all(tree)




# ============================================================
#   POSIBLES ESTRUCTURAS EXTRA QUE EL PROFESOR PUEDE PEDIR
#   TODAS ESTÁN LISTAS PARA USARSE SI SE DESCOMENTAN
# ============================================================


# ------------------------------------------------------------
#   1. LISTA ENLAZADA (Linked List)
# ------------------------------------------------------------

# class LinkedNode:
#     def __init__(self, value, next=None):
#         self.value = value
#         self.next = next
#
#
# class LinkedListStructure(IterableStructure):
#     def __init__(self, head):
#         self.head = head
#
#     def create_iterator(self):
#         return LinkedListIterator(self.head)
#
#
# class LinkedListIterator(IteratorInterface):
#     def __init__(self, head):
#         self.actual = head
#
#     def has_next(self):
#         return self.actual is not None
#
#     def next(self):
#         val = self.actual.value
#         self.actual = self.actual.next
#         return val
#
# # Ejemplo de uso:
# # n1 = LinkedNode(1, LinkedNode(2, LinkedNode(3)))
# # lista = LinkedListStructure(n1)
# # Printer.print_all(lista)


# ------------------------------------------------------------
#   2. COLA (Queue)
# ------------------------------------------------------------

# class QueueStructure(IterableStructure):
#     def __init__(self, items):
#         self.items = items
#
#     def create_iterator(self):
#         return QueueIterator(self.items)
#
#
# class QueueIterator(IteratorInterface):
#     def __init__(self, items):
#         self.items = items
#         self.index = 0
#
#     def has_next(self):
#         return self.index < len(self.items)
#
#     def next(self):
#         val = self.items[self.index]
#         self.index += 1
#         return val
#
# # Ejemplo:
# # q = QueueStructure(["A", "B", "C"])
# # Printer.print_all(q)


# ------------------------------------------------------------
#   3. PILA (Stack)
# ------------------------------------------------------------

# class StackStructure(IterableStructure):
#     def __init__(self, items):
#         self.items = items
#
#     def create_iterator(self):
#         return StackIterator(self.items)
#
#
# class StackIterator(IteratorInterface):
#     def __init__(self, items):
#         self.items = items
#         self.index = len(items) - 1
#
#     def has_next(self):
#         return self.index >= 0
#
#     def next(self):
#         val = self.items[self.index]
#         self.index -= 1
#         return val
#
# # Ejemplo:
# # stack = StackStructure([5, 10, 15])
# # Printer.print_all(stack)


# ------------------------------------------------------------
#   4. DICCIONARIO (Map)
# ------------------------------------------------------------

# class DictStructure(IterableStructure):
#     def __init__(self, d):
#         self.d = d
#
#     def create_iterator(self):
#         return DictIterator(self.d)
#
#
# class DictIterator(IteratorInterface):
#     def __init__(self, d):
#         self.items = list(d.items())
#         self.index = 0
#
#     def has_next(self):
#         return self.index < len(self.items)
#
#     def next(self):
#         val = self.items[self.index]
#         self.index += 1
#         return val
#
# # Ejemplo:
# # dic = DictStructure({"a": 1, "b": 2, "c": 3})
# # Printer.print_all(dic)


# ------------------------------------------------------------
#   5. RANGO NUMÉRICO (tipo range)
# ------------------------------------------------------------

# class RangeStructure(IterableStructure):
#     def __init__(self, start, end, step=1):
#         self.start = start
#         self.end = end
#         self.step = step
#
#     def create_iterator(self):
#         return RangeIterator(self.start, self.end, self.step)
#
#
# class RangeIterator(IteratorInterface):
#     def __init__(self, start, end, step):
#         self.current = start
#         self.end = end
#         self.step = step
#
#     def has_next(self):
#         return self.current <= self.end
#
#     def next(self):
#         val = self.current
#         self.current += self.step
#         return val
#
# # Ejemplo:
# # r = RangeStructure(1, 10, 2)
# # Printer.print_all(r)


# ------------------------------------------------------------
#   6. ÁRBOL N-ARIO
# ------------------------------------------------------------

# class NNode:
#     def __init__(self, value, children=None):
#         self.value = value
#         self.children = children if children else []
#
#
# class NAryTreeStructure(IterableStructure):
#     def __init__(self, root):
#         self.root = root
#
#     def create_iterator(self):
#         return NAryTreeIterator(self.root)
#
#
# class NAryTreeIterator(IteratorInterface):
#     def __init__(self, root):
#         self.stack = [root] if root else []
#
#     def has_next(self):
#         return len(self.stack) > 0
#
#     def next(self):
#         nodo = self.stack.pop()
#         for hijo in reversed(nodo.children):
#             self.stack.append(hijo)
#         return nodo.value
#
# # Ejemplo:
# # root = NNode(1, [NNode(2), NNode(3, [NNode(4), NNode(5)])])
# # tree = NAryTreeStructure(root)
# # Printer.print_all(tree)


# ------------------------------------------------------------
#   7. GRAFO (BFS)
# ------------------------------------------------------------

# from collections import deque
#
# class GraphStructure(IterableStructure):
#     def __init__(self, adj_list, start):
#         self.adj = adj_list
#         self.start = start
#
#     def create_iterator(self):
#         return GraphBFSIterator(self.adj, self.start)
#
#
# class GraphBFSIterator(IteratorInterface):
#     def __init__(self, adj, start):
#         self.adj = adj
#         self.queue = deque([start])
#         self.visited = set()
#
#     def has_next(self):
#         return len(self.queue) > 0
#
#     def next(self):
#         node = self.queue.popleft()
#         self.visited.add(node)
#         for neigh in self.adj[node]:
#             if neigh not in self.visited:
#                 self.queue.append(neigh)
#         return node
#
# # Ejemplo:
# # grafo = GraphStructure({
# #     1: [2, 3],
# #     2: [4],
# #     3: [4],
# #     4: []
# # }, start=1)
# # Printer.print_all(grafo)


# ------------------------------------------------------------
#   8. ARCHIVO DE TEXTO (línea por línea)
# ------------------------------------------------------------

# class FileStructure(IterableStructure):
#     def __init__(self, filename):
#         self.filename = filename
#
#     def create_iterator(self):
#         return FileIterator(self.filename)
#
#
# class FileIterator(IteratorInterface):
#     def __init__(self, filename):
#         self.file = open(filename, "r")
#         self.lines = self.file.readlines()
#         self.index = 0
#
#     def has_next(self):
#         return self.index < len(self.lines)
#
#     def next(self):
#         val = self.lines[self.index].strip()
#         self.index += 1
#         return val
#
# # Ejemplo:
# # texto = FileStructure("archivo.txt")
# # Printer.print_all(texto)


# ------------------------------------------------------------
#   9. LISTA CIRCULAR
# ------------------------------------------------------------

# class CircularNode:
#     def __init__(self, value):
#         self.value = value
#         self.next = None
#
# class CircularListStructure(IterableStructure):
#     def __init__(self, head, length):
#         self.head = head
#         self.length = length  # para evitar bucle infinito
#
#     def create_iterator(self):
#         return CircularListIterator(self.head, self.length)
#
#
# class CircularListIterator(IteratorInterface):
#     def __init__(self, head, length):
#         self.actual = head
#         self.remaining = length
#
#     def has_next(self):
#         return self.remaining > 0
#
#     def next(self):
#         val = self.actual.value
#         self.actual = self.actual.next
#         self.remaining -= 1
#         return val
#
# # Ejemplo:
# # a = CircularNode(1)
# # b = CircularNode(2)
# # c = CircularNode(3)
# # a.next = b; b.next = c; c.next = a
# # lista = CircularListStructure(a, 3)
# # Printer.print_all(lista)
