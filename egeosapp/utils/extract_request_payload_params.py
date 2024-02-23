from egeosapp.models import Polygon,Point,StartLatStartLon,DegreeAndMinutes
from decimal import Decimal, ROUND_DOWN


class ParsePolygons():
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
            points = [Point(point[1], point[0]) for point in polygon_coordinates]
            polygon = Polygon(coordinates=points)
            polygons.append(polygon)

        print(polygons)
        return polygons

    def extract_start_lat_start_lon(point):
        start_lat = Decimal(str(point.get("latitude"))).quantize(Decimal('0.00000'), rounding=ROUND_DOWN)
        start_lon = Decimal(str(point.get("longitude"))).quantize(Decimal('0.00000'), rounding=ROUND_DOWN)

        return StartLatStartLon(start_lat, start_lon)
    
    def extract_degrees_and_minutes(point):
        latitude = point.get("latitude")
        longitude = point.get("longitude")

        lat_degree = int(latitude)
        lon_degree = int(longitude)
        lat_minute = (latitude - lat_degree) * 60
        lon_minute = (longitude - lon_degree) * 60

        degree_and_minutes = DegreeAndMinutes(
            lat_degree=str(lat_degree),
            lat_minutes=format(lat_minute, '.5f'),
            lon_degree=str(lon_degree),
            lon_minutes=format(lon_minute, '.5f')
        )

        return degree_and_minutes
    
    def compute_spill_rate(spill_rate_coeff_str, min_volume):
        # Convert to float and perform the computation
        spill_rate_coeff = float(spill_rate_coeff_str)
        spill_rate_value = spill_rate_coeff * min_volume

        # Format the result using f-string
        formatted_spill_rate = f'{spill_rate_value:.5f}'

        return formatted_spill_rate