class TruncatePoints:
    def truncate_points(self, max_points_per_polygon, combined_coordinates):
        polygon_point_count = {}
        truncated_coordinates = []

        coordinate_pairs = combined_coordinates.split(",")

        for coordinate_pair in coordinate_pairs:
            slon_slat, slon_value = map(str.strip, coordinate_pair.split(":"))
            slon_parts = slon_slat.split("_")
            polygon = slon_parts[1]
            point_index = slon_parts[2]

            polygon_point_count.setdefault(polygon, 0)
            current_point_count = polygon_point_count[polygon]

            if current_point_count < max_points_per_polygon * 2:
                # Remove the surrounding quotes before converting to float
                slon_value = slon_value.strip('"')
                five_digit_value = format(float(slon_value), '.5f')
                truncated_coordinates.append(f'{slon_slat}: "{five_digit_value}"')
                polygon_point_count[polygon] = current_point_count + 1

        # Join the truncated coordinates and remove the trailing ", " if any
        result = ', '.join(truncated_coordinates).rstrip(', ')
        return result
