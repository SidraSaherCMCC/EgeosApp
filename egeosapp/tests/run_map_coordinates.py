from typing import List, Dict

class Point:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

class Polygon:
    def __init__(self, coordinates: List[Dict[str, float]]):
        self.coordinates = [Point(point["latitude"], point["longitude"]) for point in coordinates]

def map_coordinates(coordinates):
    print("Mapping coordinates")
    num_polygons = len(coordinates)
    polygons = []

    print("Polygons List")
    print(num_polygons)

    for i in range(num_polygons):
        num_points = len(coordinates[i][0])
        print(num_points)

        polygon_coordinates = coordinates[i][0]
        points = [{"latitude": point[1], "longitude": point[0]} for point in polygon_coordinates]
        polygon = Polygon(coordinates=points)
        polygons.append(polygon)

    print(polygons)
    return polygons

# Example usage:
coordinates_data = [[[[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]]]]
polygons = map_coordinates(coordinates_data)
