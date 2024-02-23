from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    latitude: float
    longitude: float

@dataclass
class Polygon:
    coordinates: List[Point]

@dataclass
class SheenPolygon:
    type: str
    coordinates: List[List[List[List[float]]]]
    polygons: List[Polygon]

def obtain_slat_slon_string(sheen_polygon):
    list_polygons = sheen_polygon.polygons
    point_strings = []

    for j, polygon in enumerate(list_polygons, start=1):
        polygon_index = j
        for i, point in enumerate(polygon.coordinates, start=1):
            point_index = i
            point_strings.append(
                f'"Slat_{polygon_index}_{point_index}": "{point[0]}", '
                f'"Slon_{polygon_index}_{point_index}": "{point[1]}"'
            )

    return ', '.join(point_strings)

# Example usage:
sheen_polygon = SheenPolygon(
    type="some_type",
    coordinates=[[[[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]]]],
    polygons=[Polygon(coordinates=[[10.0, 20.0], [30.0, 40.0], [50.0, 60.0]])]
)

result = obtain_slat_slon_string(sheen_polygon)
print(result)
