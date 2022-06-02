# This code contains some errors ...

from abc import ABC


class TwoThreeTree(ABC):
    def is_nil(self):
        raise NotImplementedError()

    def is_one(self):
        raise NotImplementedError()

    def is_two(self):
        raise NotImplementedError()

    def is_three(self):
        raise NotImplementedError()

    def is_four(self):
        raise NotImplementedError()

    def is_tree(self):
        raise NotImplementedError()

    def ins(self, k):
        raise NotImplementedError()

    def restore(self):
        raise NotImplementedError()

    def grow(self):
        raise NotImplementedError()

    def insert(self, k):
        return self.ins(k).restore().grow()

    def member(self, k):
        raise NotImplementedError()

    def _grow(self):
        return self


class Nil(TwoThreeTree, ABC):
    def __init__(self):
        TwoThreeTree.__init__(self)

    def is_nil(self):
        return True

    def member(self, k):
        return False

    def ins(self, k):
        return Two(Nil(), k, Nil())


class Two(TwoThreeTree, ABC):
    def __init__(self, left, key, right):
        TwoThreeTree.__init__(self)
        self._left = left
        self._key = key
        self._right = right

    def is_two(self):
        return True

    def member(self, key):
        l, k, r = self._extract()
        if k == key:
            return True
        elif key < k:
            return l.member(key)
        elif key > self._key:
            return r.member(key)

    def ins(self, key):
        if self._key == key:
            return self

        if not isinstance(self._left, Nil) and not isinstance(self._right, Nil):
            if self._key < key:
                Two(self._left, self._key, self._right.ins(key)).restore()

            if key < self._key:
                return Two(self._left.ins(key), self._key, self._right).restore()

        if self._key < key:
            return Three(Nil(), self._key, Nil(), key, Nil())

        if key < self._key:
            return Three(Nil(), key, Nil(), self._key, Nil())

        assert False, f'Unbalanced node {self}'

    def restore(self):
        if not isinstance(self._left, Four) and not isinstance(self._right, Four):
            return self

        if isinstance(self._left, Four):
            return Three(Two(self._left.left, self._left.key_left, self._left.middle_left),
                         self._left.key_middle,
                         Two(self._left.middle_right, self._left.key_right, self._left.right),
                         self._key, self._right)

        if isinstance(self._right, Four):
            return Three(self._left, self._key,
                         Two(self._right.left, self._right.key_left, self._right.middle_left),
                         self._right.key_middle,
                         Two(self._right.middle_right, self._right.key_right, self._right.right))

    def _extract(self):
        return self._left, self._key, self._right


class Three(TwoThreeTree, ABC):
    def __init__(self, left, key_left, middle, key_right, right):
        TwoThreeTree.__init__(self)
        self._left = left
        self._key_left = key_left
        self._middle = middle
        self._key_right = key_right
        self._right = right

    def is_three(self):
        return True

    def member(self, key):
        l, key_left, m, key_right, r = self._extract()
        if key == key_left or key == key_right:
            return True
        if key < key_left:
            return l.member(key)
        if key_left < key < key_right:
            return m.member(key)
        if key_right < key:
            return self._right.member(key)

    def ins(self, key):
        if self._left == key or self._right == key:
            return self

        if not isinstance(self._left, Nil) \
                and not isinstance(self._middle, Nil) \
                and not isinstance(self._right, Nil):
            if key < self._left:
                return Three(self._left.ins(key), self._key_left, self._middle, self._key_right, self._right).restore()

            if self._left < key < self._key_right:
                return Three(self._left, self._key_left, self._middle.ins(key), self._key_right, self._right).restore()

            if self._key_right < key:
                return Three(self._left, self._key_left, self._middle, self._key_right, self._right.ins(key)).restore()

        if key < self._key_left:
            return Four(Nil(), key, Nil(), self._key_left, Nil(), self._key_right, Nil())

        if self._key_left < key < self._key_right:
            return Four(Nil(), self._key_left, Nil(), key, Nil(), self._key_right, Nil())

        if self._key_right < key:
            return Four(Nil(), self._key_left, Nil(), self._key_right, Nil(), key, Nil())

        assert False, f'Unbalanced node {self}'

    def restore(self):
        if not isinstance(self._left, Four) \
                and not isinstance(self._middle, Four) \
                and not isinstance(self._right, Four):
            return self

        if isinstance(self._left, Four):
            return Four(Two(self._left.left, self._left.key_left, self._left.middle_left),
                        self._left.key_middle,
                        Two(self._left.middle_right, self._left.key_right, self._left.right),
                        self._key_left, self._middle, self._key_right, self._right)

        if isinstance(self._middle, Four):
            return Four(self._left, self._key_left,
                        Two(self._left.left, self._left.key_left, self._left.middle_left),
                        self._left.key_middle,
                        Two(self._left.middle_right, self._left.key_right, self._left.right),
                        self._key_right, self._right)

        if isinstance(self._right, Four):
            return Four(self._left, self._key_left, self._middle, self._key_right,
                        Two(self._left.left, self._left.key_left, self._left.middle_left),
                        self._left.key_middle,
                        Two(self._left.middle_right, self._left.key_right, self._left.right))

        return self

    def _extract(self):
        return self._left, self._key_left, self._middle, self._key_right, self._right


class Four(TwoThreeTree, ABC):
    def __init__(self, left, key_left, middle_left, key_middle, middle_right, key_right, right):
        TwoThreeTree.__init__(self)
        self.left = left
        self.key_left = key_left
        self.middle_left = middle_left
        self.key_middle = key_middle
        self.middle_right = middle_right
        self.key_right = key_right
        self.right = right

    def is_four(self):
        return True

    def restore(self):
        return self

    def grow(self):
        return Two(Two(self.left, self.key_left, self.middle_left),
                   self.key_middle,
                   Two(self.middle_right, self.key_right, self.right))

    def _extract(self):
        return self.left, self.key_left, self.middle_left, self.key_middle, \
               self.middle_right, self.key_right, self.right
