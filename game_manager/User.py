import pydantic

# my guess as to what's in the database
class User_Args(pydantic.BaseModel):
    # do not allow creation of unspecified variables in the class, and do not perform
    # type-conversion
    model_config = pydantic.ConfigDict(extra='forbid', strict=True)

    # "xXtriviaslayerXx", "mia thermopolis", "player3", etc
    name: str
    # 0x1234, 0xFFAA88, green, etc
    color: int
    # "science", "mathematics", "biology", etc
    chips: set
    # [ x , y ]
    coords: list

class User():
    def __init__(self, username, color):
        self.username = username
        self.color = color
        self.chips = set()
        self.coords = [0,0]

    def __repr__(self):
        return f"{self.username} : {self.color} : {self.chips} : {self.coords}"

    def get_username(self) -> str:
        return self.username

    def get_color(self) -> str:
        return self.color

    def get_chips(self) -> str:
        return self.chips

    def set_chips(self, new_chip) -> None:
        self.chip.add(new_chip)

    def get_coords(self) -> list:
        return self.coords

    def set_coords(self, direction, quantity) -> None:
        self.coords[0] = direction
        self.coords[1] = quantity
