import bisect
from graphviz import Digraph

class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.next = None  # Only for leaf nodes

class BPlusTree:
    def __init__(self, order=4):
        if order < 3:
            raise ValueError("Order must be at least 3")
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order
        self.min_keys = (order - 1) // 2

    def insert(self, key, value):
        if len(self.root.keys) >= self.order - 1:
            new_root = BPlusTreeNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            self._insert_into_leaf(node, key, value)
        else:
            self._insert_into_internal(node, key, value)

    def _insert_into_leaf(self, node, key, value):
        idx = bisect.bisect_left(node.keys, key)
        if idx < len(node.keys) and node.keys[idx] == key:
            node.children[idx] = value  # Update existing
        else:
            node.keys.insert(idx, key)
            node.children.insert(idx, value)
            if len(node.keys) > self.order - 1:
                self._split_leaf(node)

    def _insert_into_internal(self, node, key, value):
        idx = bisect.bisect_right(node.keys, key)
        child = node.children[idx]
        if len(child.keys) >= self.order - 1:
            self._split_child(node, idx)
            if key > node.keys[idx]:
                idx += 1
        self._insert_non_full(node.children[idx], key, value)

    def _split_leaf(self, node):
        if len(node.keys) < 2:  # Ensure enough keys to split
            return
            
        split_idx = len(node.keys) // 2
        new_node = BPlusTreeNode(is_leaf=True)
        
        new_node.keys = node.keys[split_idx:]
        new_node.children = node.children[split_idx:]
        new_node.next = node.next
        
        promote_key = new_node.keys[0]
        node.keys = node.keys[:split_idx]
        node.children = node.children[:split_idx]
        node.next = new_node
        
        if node == self.root:
            self._handle_root_split(node, new_node, promote_key)
        else:
            return promote_key, new_node

    def _split_child(self, parent, index):
        child = parent.children[index]
        if child.is_leaf:
            result = self._split_leaf(child)
            if result:
                promote_key, new_node = result
                parent.keys.insert(index, promote_key)
                parent.children.insert(index + 1, new_node)
        else:
            split_idx = len(child.keys) // 2
            if split_idx == 0:  # Prevent empty splits
                return
                
            promote_key = child.keys[split_idx]
            new_node = BPlusTreeNode(is_leaf=False)
            
            new_node.keys = child.keys[split_idx+1:]
            new_node.children = child.children[split_idx+1:]
            
            child.keys = child.keys[:split_idx]
            child.children = child.children[:split_idx+1]
            
            parent.keys.insert(index, promote_key)
            parent.children.insert(index + 1, new_node)

    def _handle_root_split(self, left, right, promote_key):
        new_root = BPlusTreeNode(is_leaf=False)
        new_root.keys = [promote_key]
        new_root.children = [left, right]
        self.root = new_root
# searching 
    def search(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        for i, item in enumerate(node.keys):
            if item == key:
                return node.children[i]
        return None

    def range_query(self, start_key, end_key):
        result = []
        node = self.root

        # Traverse to the correct leaf node
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and start_key >= node.keys[i]:
                i += 1
            node = node.children[i]

        # Collect values within the range
        while node:
            for i, key in enumerate(node.keys):
                if start_key <= key <= end_key:
                    result.append((key, node.children[i]))
                elif key > end_key:
                    return result
            node = node.next

        return result

    def delete(self, key):
        self._delete(self.root, key)

    # Shrink root if needed
        if not self.root.keys and not self.root.is_leaf:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        if node.is_leaf:
            if key in node.keys:
                idx = node.keys.index(key)
                node.keys.pop(idx)
                node.children.pop(idx)
            return

    # Find the child to descend into
        idx = 0
        while idx < len(node.keys) and key >= node.keys[idx]:
            idx += 1

        child = node.children[idx]

    # Recursive delete
        self._delete(child, key)

    # If child underflows, fix it
        if len(child.keys) < (self.order - 1) // 2:
            self._fix_underflow(node, idx)

    def _fix_underflow(self, parent, idx):
        child = parent.children[idx]

    # Try left sibling
        if idx > 0 and len(parent.children[idx - 1].keys) > (self.order - 1) // 2:
            self._borrow_from_prev(parent, idx)

    # Try right sibling
        elif idx < len(parent.children) - 1 and len(parent.children[idx + 1].keys) > (self.order - 1) // 2:
            self._borrow_from_next(parent, idx)

    # Otherwise merge
        else:
            if idx < len(parent.children) - 1:
                self._merge(parent, idx)
            else:
                self._merge(parent, idx - 1)

    def _borrow_from_prev(self, parent, idx):
        child = parent.children[idx]
        left_sibling = parent.children[idx - 1]

        if child.is_leaf:
        # Move last key/value from left sibling to front of child
            child.keys.insert(0, left_sibling.keys.pop(-1))
            child.children.insert(0, left_sibling.children.pop(-1))
            parent.keys[idx - 1] = child.keys[0]
        else:
        # Internal node: borrow key from parent
            child.keys.insert(0, parent.keys[idx - 1])
            parent.keys[idx - 1] = left_sibling.keys.pop(-1)
            child.children.insert(0, left_sibling.children.pop(-1))

    def _borrow_from_next(self, parent, idx):
        child = parent.children[idx]
        right_sibling = parent.children[idx + 1]

        if child.is_leaf:
        # Move first key/value from right sibling to end of child
            child.keys.append(right_sibling.keys.pop(0))
            child.children.append(right_sibling.children.pop(0))
            parent.keys[idx] = right_sibling.keys[0]
        else:
        # Internal node: borrow key from parent
            child.keys.append(parent.keys[idx])
            parent.keys[idx] = right_sibling.keys.pop(0)
            child.children.append(right_sibling.children.pop(0))

    def _merge(self, parent, idx):
        left = parent.children[idx]
        right = parent.children[idx + 1]

        if left.is_leaf:
            left.keys.extend(right.keys)
            left.children.extend(right.children)
            left.next = right.next
        else:
            left.keys.append(parent.keys[idx])
            left.keys.extend(right.keys)
            left.children.extend(right.children)

        parent.keys.pop(idx)
        parent.children.pop(idx + 1)


    def get_all(self):
        result = []
        node = self.root

        # Go to leftmost leaf
        while not node.is_leaf:
            node = node.children[0]

        while node:
            for i in range(len(node.keys)):
                result.append((node.keys[i], node.children[i]))
            node = node.next
        return result

    def visualize_tree(self):
        from graphviz import Digraph
        dot = Digraph()
        self._add_nodes(dot, self.root)
        self._add_edges(dot, self.root)
        return dot

    def _add_nodes(self, dot, node):
        node_id = str(id(node))
        label = '|'.join(map(str, node.keys))
        shape = 'record'
        dot.node(node_id, label=label, shape=shape)
        if not node.is_leaf:
            for child in node.children:
                self._add_nodes(dot, child)

    def _add_edges(self, dot, node):
        node_id = str(id(node))
        
    def _add_edges(self, dot, node):
        node_id = str(id(node))
        if not node.is_leaf:
            for child in node.children:
                child_id = str(id(child))
                dot.edge(node_id, child_id)
                self._add_edges(dot, child)
        else:
        # Draw dashed line to next leaf node (linked list style)
            if node.next:
                next_id = str(id(node.next))
                dot.edge(node_id, next_id, style='dashed')