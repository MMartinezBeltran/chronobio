import math

import arcade

from chronobio.game.location import Location

location_to_position: dict[Location, tuple[float, float]] = {
    Location.FARM: (100, 100),
    Location.FIELD1: (200, 200),
}


class MovingEntity:
    def __init__(self) -> None:
        self.target_location: Location = Location.FARM
        self.sprite: arcade.Sprite = arcade.Sprite(
            ":resources:images/tiles/boxCrate_double.png", scale=1.0
        )
        self.sprite.width = 100
        self.sprite.height = 100
        self.sprite.angle = 0

        self.x, self.y = location_to_position[self.target_location]

    def update_position(self, farm: "Farm"):
        self.sprite.center_x, self.sprite.center_y = farm.rotate(self.x, self.y)


class Farm:
    def __init__(self, x, y, angle=0):
        self.angle = angle
        self.x = x
        self.y = y
        self.employees: dict[int, MovingEntity] = {}

    def rotate(self, x, y):
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        return cos * x - sin * y + self.x, sin * x + cos * y + self.y

    def update(self, data):
        seen = set()
        for employee in data["employees"]:
            seen.add(employee["id"])
            employee_entity = self.employees.get(employee["id"], MovingEntity())
            employee_entity.target_location = Location[employee["location"]]
            self.employees[employee["id"]] = employee_entity
        for employee_id in list(self.employees):
            if employee_id not in seen:
                del self.employees[employee_id]

    def draw(self):
        sprite_list = arcade.SpriteList()

        for employee in self.employees.values():
            employee.update_position(self)
            sprite_list.append(employee.sprite)

        sprite_list.draw()