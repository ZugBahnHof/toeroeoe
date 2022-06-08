from dataclasses import dataclass
from math import sqrt

from PIL import Image

from .generator import generate


@dataclass
class Vector2:
    x: float
    y: float

    def as_tuple(self):
        return self.x, self.y

    def to_integer(self):
        return Vector2(
            int(self.x),
            int(self.y)
        )

    def correct_offset(self, offset):
        return Vector2(
            self.x + offset.x,
            self.y + offset.y,
        )

    def times(self, factor: float | int):
        return Vector2(
            self.x * factor,
            self.y * factor
        )


@dataclass
class Matrix2x2:
    a: float
    b: float
    c: float
    d: float


# These are the four numbers that define the transform, i hat and j hat
i_x = 1
i_y = 0.5
j_x = -1
j_y = 0.5

# Sprite size
w = 32
h = 32


def to_screen_coordinate(tile: Vector2):
    # Without accounting for sprite size
    return Vector2(
        tile.x * i_x + tile.y * j_x,
        tile.x * i_y + tile.y * j_y,
    )


def to_screen_coordinate_sprite_size(tile: Vector2):
    # Accounting for sprite size
    return Vector2(
        tile.x * i_x * 0.5 * w + tile.y * j_x * 0.5 * w,
        tile.x * i_y * 0.5 * h + tile.y * j_y * 0.5 * h,
    )


def invert_matrix(a, b, c, d):
    # Determinant
    det = (1 / (a * d - b * c))

    return Matrix2x2(
        det * d,
        det * -b,
        det * -c,
        det * a,
    )


def to_grid_coordinate(screen: Vector2):
    a = i_x * 0.5 * w
    b = j_x * 0.5 * w
    c = i_y * 0.5 * h
    d = j_y * 0.5 * h

    inv = invert_matrix(a, b, c, d)

    return Vector2(
        screen.x * inv.a + screen.y * inv.b,
        screen.x * inv.c + screen.y * inv.d,
    )


def draw(
        size: int = 10,
        scale: float = 1,
        seed: int | str | None = None
):
    height, colors = generate(
        size,
        size,
        seed,
        scale=scale,
        return_image=False,
        return_height_and_color=True,
    )
    img_size = int((size + 1) * h), int(size * w * 3 / 4)
    offset = Vector2(*img_size).times(.5)
    offset.y = img_size[1] / 2 - size / 2 * h / sqrt(3)
    offset = offset.correct_offset(Vector2(-w/2, h/2))

    image = Image.new("RGBA", img_size)
    tile_img = Image.open("cube.png")

    for coord_y, row in enumerate(colors):
        for coord_x, color in enumerate(row):
            img_coord = (
                to_screen_coordinate_sprite_size(
                    Vector2(
                        coord_x, coord_y
                    )
                ).correct_offset(
                    offset
                )
            )

            img_coord.y += (height[coord_y, coord_x] - 128)

            color = (
                int(color[0]),
                int(color[1]),
                int(color[2]),
            )

            image.paste(
                Image.new("RGBA", (w, h), color=tuple(color)),
                (
                    img_coord.to_integer().as_tuple()
                ),
                tile_img
            )

    image.show()
