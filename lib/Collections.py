from collections import namedtuple

class SetStrAtrr:
    "Mixin class to add __str__ functionality to namedtuple"
    __slots__ = ()
    def __str__(self):
        return f"B{self.box}O{self.index}"

class GetCoordinates:
    __slots__ = ()
    @property
    def coordinates(self):
        coords = {
            1 : (x,y),
            2 : (x,y),
            3 : (x,y)
            }
        return coords[self.box]

class Options(
        namedtuple('Options', ['name', 'box', 'index', 'value', 'image', 'info', 'selected']), 
        SetStrAtrr, 
        GetCoordinates
        ):
    __slots__ = ()
    

class TestOptions(
        namedtuple('TestOptions', ['name', 'box', 'index', 'image', 'info', 'selected', 'test']),
        SetStrAtrr, 
        GetCoordinates
        ):
    __slots__ = ()
    @property
    def value(self):
        return self.test.cost()