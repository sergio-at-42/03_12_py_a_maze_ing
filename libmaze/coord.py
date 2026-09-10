from pydantic import BaseModel


class Coord(BaseModel):

    x: int
    y: int


    # def __init__(self, x: int, y: int) -> None:
    #     self.x: int = x
    #     self.y: int = y
