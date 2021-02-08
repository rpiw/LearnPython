class SelectableList(list):  # Linear Selectable container
    u"""Linear containers with selectable items. Like list, but with one item 'selected' and additional methods."""
    def __init__(self, linear_container=None, chain=False):
        if linear_container is None:
            linear_container = []
        if not isinstance(linear_container, list):
            raise TypeError

        super(SelectableList, self).__init__(linear_container)

        self._item = None
        self._type = type(self._item)
        self._index = None
        self._iterator = None
        self.restart_iterator()

        self._chain = chain

        if super():
            self.selected_index = 0

    def restart_iterator(self):
        self._iterator = super(SelectableList, self).__iter__()

    @property
    def selected_index(self):
        return self._index

    @selected_index.setter
    def selected_index(self, new_index: int):
        if not isinstance(new_index, int):
            raise TypeError
        self._index = new_index
        self._item = super().__getitem__(self._index)

    @property
    def value(self):
        return self._item

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, self._type):
            raise TypeError
        self._item = new_value
        self._index = super().index(self._item)

    def __len__(self):
        return super().__len__()

    def __next__(self):
        try:
            next(self._iterator)
        except StopIteration:
            if self._chain:  # are we cyclic?
                self.restart_iterator()
                next(self._iterator)
            else:
                raise StopIteration

        self.selected_index = (self._index + 1) % super().__len__()
        print(f"Selected: {self.selected_index}")
