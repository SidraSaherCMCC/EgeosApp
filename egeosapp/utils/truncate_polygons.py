class TruncatePolygons:
    def truncate_coordinates(self, number_of_polygons, combined_coordinates):
        truncated_coordinates = []

        coordinate_pairs = combined_coordinates.split(", ")

        for coordinate_pair in coordinate_pairs:
            slat_lon, _ = coordinate_pair.split(":")
            
            # Extract the first index from slat_lon, e.g., "Slat_1_2" -> 1
            first_index = int(slat_lon.split("_")[1])
            print(first_index)
            print(number_of_polygons)
            if first_index <= number_of_polygons:
                truncated_coordinates.append(coordinate_pair)
        print(", ".join(truncated_coordinates))
        return ", ".join(truncated_coordinates)