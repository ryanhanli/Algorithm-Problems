import fileinput


class Node(object):
    def __init__(self):
        self.guide = None
        # guide points to max key in subtree rooted at node


class InternalNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.child0 = None
        self.child1 = None
        self.child2 = None
        # child0 and child1 are always non-none
        # child2 is none iff node has only 2 children

    def tlist(self):
        children = self.child0.tlist()
        children.extend(self.child1.tlist())
        if not self.child2 is None:
            children.extend(self.child2.tlist())
        offset = ["               " + i for i in children]
        offset.insert(1, self.guide)
        return offset

    def __str__(self):
        return "\n".join(self.tlist())


class LeafNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.value = None
        # guide points to the key

    def tlist(self):
        return [str(self.guide) + " " + str(self.value)]

    def __str__(self):
        return "\n".join(self.tlist())


class TwoThreeTree:
    def __init__(self):
        self.root = None
        self.height = -1


class WorkSpace:
    def __init__(self):
        self.newNode = None
        self.offset = None
        self.guideChanged = None
        self.scratch = [None] * 4


def insert(key, value, tree):
    # insert a key value pair into tree (overwrite existsing value
    # if key is already present)

    h = tree.height

    if h == -1:
        newLeaf = LeafNode()
        newLeaf.guide = key
        newLeaf.value = value
        tree.root = newLeaf
        tree.height = 0

    else:
        ws = doInsert(key, value, tree.root, h)

        if ws != None and ws.newNode != None:
            # create a new root

            newRoot = InternalNode()
            if ws.offset == 0:
                newRoot.child0 = ws.newNode
                newRoot.child1 = tree.root

            else:
                newRoot.child0 = tree.root
                newRoot.child1 = ws.newNode

            resetGuide(newRoot)
            tree.root = newRoot
            tree.height = h + 1


def doInsert(key, value, p, h):
    # auxiliary recursive routine for insert

    if h == 0:
        # we're at the leaf level, so compare and
        # either update value or insert new leaf

        leaf = p  # downcast (unnecessary in python)
        cmp = 0
        if key < leaf.guide:
            cmp = -1
        elif key > leaf.guide:
            cmp = 1

        if cmp == 0:
            leaf.value = value
            return None

        # create new leaf node and insert into tree
        newLeaf = LeafNode()
        newLeaf.guide = key
        newLeaf.value = value

        offset = 1
        if cmp < 0:
            offset = 0
        # offset == 0 => newLeaf inserted as left sibling
        # offset == 1 => newLeaf inserted as right sibling

        ws = WorkSpace()
        ws.newNode = newLeaf
        ws.offset = offset
        ws.scratch = [None] * 4

        return ws

    else:
        q = p  # downcast (unnecessary in python)
        pos = 2
        ws = None

        if key <= q.child0.guide:
            pos = 0
            ws = doInsert(key, value, q.child0, h - 1)

        elif key <= q.child1.guide or q.child2 is None:
            pos = 1
            ws = doInsert(key, value, q.child1, h - 1)

        else:
            pos = 2
            ws = doInsert(key, value, q.child2, h - 1)
        if ws != None:
            if ws.newNode != None:
                # make ws.newNode child # pos + ws.offset of q
                sz = copyOutChildren(q, ws.scratch)

                ws.scratch.insert(pos + ws.offset, ws.newNode)

                if sz == 2:
                    ws.newNode = None
                    ws.guideChanged = resetChildren(q, ws.scratch, 0, 3)
                else:
                    ws.newNode = InternalNode()
                    ws.offset = 1
                    resetChildren(q, ws.scratch, 0, 2)
                    resetChildren(ws.newNode, ws.scratch, 2, 2)

            elif ws.guideChanged:
                ws.guideChanged = resetGuide(q)

        return ws


def copyOutChildren(q, x):
    # copy children of q into x, and return # of children

    sz = 2
    x[0] = q.child0
    x[1] = q.child1
    if q.child2 != None:
        x[2] = q.child2
        sz = 3

    return sz


def resetGuide(q):
    # reset q.guide, and return true if it changes.

    oldGuide = q.guide
    if q.child2 != None:
        q.guide = q.child2.guide
    else:
        q.guide = q.child1.guide

    return q.guide != oldGuide


def resetChildren(q, x, pos, sz):
    # reset q's children to x[pos..pos+sz), where sz is 2 or 3.
    # also resets guide, and returns the result of that

    q.child0 = x[pos]
    q.child1 = x[pos + 1]

    if sz == 3:
        q.child2 = x[pos + 2]
    else:
        q.child2 = None

    return resetGuide(q)


# P=ROOT, X=KEY, H=HEIGHT

def compareTo(self, that):
    return ((self > that) - (self < that))


def printAll(p, h):
    if h == 0:
        print(p.guide + ' ' + p.value)
    else:
        printAll(p.child0, h - 1)
        printAll(p.child1, h - 1)
        if p.child2 != None:
            printAll(p.child2, h - 1)


def printLE(x, p, h):
    if h == 0:
        if (p != None and compareTo(p.guide, x) <= 0):
            print(p.guide + ' ' + p.value)
        return
    node = p
    if (compareTo(x, node.child0.guide) <= 0):
        printLE(x, node.child0, h - 1)
    elif (node.child2 == None or compareTo(x, node.child1.guide) <= 0):
        printAll(node.child0, h - 1)
        printLE(x, node.child1, h - 1)
    else:
        printAll(node.child0, h - 1)
        printAll(node.child1, h - 1)
        printLE(x, node.child2, h - 1)


def printGE(x, p, h):
    if h == 0:
        if (p != None and compareTo(p.guide, x) >= 0):
            print(p.guide + ' ' + p.value)
        return
    node = p
    if (compareTo(x, node.child0.guide) <= 0):
        printGE(x, node.child0, h - 1)
        printAll(node.child1, h - 1)
        if (node.child2 != None):
            printAll(node.child2, h - 1)
    elif (node.child2 == None or compareTo(x, node.child1.guide) <= 0):
        printGE(x, node.child1, h - 1)
        if (node.child2 != None):
            printAll(node.child2, h - 1)
    else:
        printGE(x, node.child2, h - 1)


def printRange(p, x, y, h):
    if h == 0:
        if x <= p.guide and p.guide <= y:
            print(p.guide + ' ' + p.value)
        elif y <= p.child0.guide:
            printRange(p.child0, x, y, h - 1)
        elif p.child2 == None or y <= p.child1.guide:
            if x <= p.child0:
                printGE(x, p.child0, h - 1)
                printLE(y, p.child1, h - 1)
        else:
            printRange(p.child1, x, y, h - 1)
    else:
        if x <= p.child0.guide:
            printGE(x, p.child0, h - 1)
            printAll(p.child1, h - 1)
            printLE(y, p.child2, h - 1)
        elif x <= p.child1:
            printGE(x, p.child1, h - 1)
            printLE(y, p.child2, h - 1)
        else:
            printRange(p.child2, x, y, h - 1)


def printRange2(x, y, p, h):
    if (h == 0):
        if (p != None and compareTo(p.guide, x) >= 0 and compareTo(p.guide, y) <= 0):
            print(p.guide + " " + p.value)
        return
    node = p
    if (compareTo(y, node.child0.guide) <= 0):
        printRange2(x, y, node.child0, h - 1)
    elif (node.child2 == None or compareTo(y, node.child1.guide) <= 0):
        if (compareTo(x, node.child0.guide) <= 0):
            printGE(x, node.child0, h - 1)
            printLE(y, node.child1, h - 1)
        else:
            printRange2(x, y, node.child1, h - 1)
    else:
        if (compareTo(x, node.child0.guide) <= 0):
            printGE(x, node.child0, h - 1)
            printAll(node.child1, h - 1)
            printLE(y, node.child2, h - 1)
        elif (compareTo(x, node.child1.guide) <= 0):
            printGE(x, node.child1, h - 1)
            printLE(y, node.child2, h - 1)
        else:
            printRange2(x, y, node.child2, h - 1)


inputlist = []
TwoThreeTree = TwoThreeTree()

for line in fileinput.input():
    inputlist.append(line.strip())

# print(inputlist)

nodenumber = (int)(inputlist[0])
for each in range(1, nodenumber + 1):
    filler = inputlist[each].split()
    # print(filler)
    insert(filler[0], (filler[1]), TwoThreeTree)

# printAll(TwoThreeTree.root,TwoThreeTree.height)
# printRange(TwoThreeTree.root,'earth','jupiter',TwoThreeTree.height)
# printRange(TwoThreeTree.root,'earth','venus',TwoThreeTree.height)

NofI = (int)(inputlist[nodenumber + 1])
inputlist2 = inputlist[nodenumber + 2:]
# print(inputlist2)
for each in range(0, NofI):
    list = inputlist2[each].split()
    start = list[0]
    end = list[1]
    if start > end:
        temp = start
        start = end
        end = temp
    printRange2(start, end, TwoThreeTree.root, TwoThreeTree.height)
# print(NofI)

# printGE('a',TwoThreeTree.root,TwoThreeTree.height)
