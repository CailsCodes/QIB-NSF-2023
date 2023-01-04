from collections import namedtuple


class SetStrAtrr:
    "Mixin class to add __str__ functionality to namedtuple"
    __slots__ = ()
    def __str__(self):
        return f"B{self.box}O{self.index}" # type: ignore


class OptionProperties:
    __slots__ = ()

    @property
    def coordinates(self):
        coords = {
            1 : (50,240),
            2 : (50,515),
            3 : (50,800)
            }
        return coords[self.box] # type: ignore

    @property
    def width(self):
        widths = {
            1 : 641,
            2 : 1036,
            3 : 918
            }
        return widths[self.box] # type: ignore


class Options(
        namedtuple('Options', ['name', 'box', 'index', 'value', 'image', 'selected']), 
        SetStrAtrr, 
        OptionProperties
        ):
    __slots__ = ()

    """
    Options is an extended namedtuple class for handling properties associated with each selectable option in a box (question).

    ....

    Attributes
    ----------
    name : str
        The text value seen on screen (this information is not used internally)

    box : int
        The box associated with the option (index). Options are 1 to 3.
    
    index : int
        The position an option is in the order. Options are 0 to 3. 0 is used to indicate that the user has not yet selected an option

    value : int
        The value given by selecting this option.

    image : pygame.surface
        The image file / pygame surface handling the visual element of the option.

    selected : bool
        Indicates whether the user has selected this option, True if option is selected.

    coordinates : tuple[int, int]
        x, y coordinates of option on screen
    
    width : int
        The width of the box in pixels

    """
    

class TestOptions(
        namedtuple('TestOptions', ['name', 'box', 'index', 'image', 'selected', 'test']),
        SetStrAtrr, 
        OptionProperties
        ):
    __slots__ = ()

    """
    Options is an extended namedtuple class for handling properties associated with each selectable option in a box (question).

    ....

    Attributes
    ----------
    name : str
        The text value seen on screen (this information is not used internally)

    box : int
        The box associated with the option (index). Options are 1 to 3.
    
    index : int
        The position an option is in the order. Options are 0 to 3. 0 is used to indicate that the user has not yet selected an option

    value : int
        The value given by selecting this option.

    image : pygame.surface
        The image file / pygame surface handling the visual element of the option.

    selected : bool
        Indicates whether the user has selected this option, True if option is selected.

    test : BaseTest Object
        A class for handling test properties

    coordinates : tuple[int, int]
        x, y coordinates of option on screen
    
    width : int
        The width of the box in pixels

    """

    @property
    def value(self):
        return self.test.cost()