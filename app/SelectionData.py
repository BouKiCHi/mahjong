from dataclasses import dataclass


@dataclass
class SelectionData:
    visible: bool
    x: int
    y: int
    ch: int
    plane_no: int

    def set_value(self, visible: bool, x: int, y:int , ch: int, plane_no: int):
        self.visible = visible
        self.x = x
        self.y = y
        self.ch = ch
        self.plane_no = plane_no