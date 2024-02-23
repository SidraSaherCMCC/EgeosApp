from django.http import JsonResponse
from .models import FileData,Feature,Geometry,Properties,CRS,FeatureCollection,SheenPolygon,RequestPayloadBody
from django.views.decorators.csrf import csrf_exempt
import json
import random
from .utils.parse_date_time import ParseDateTime
from .utils.extract_request_payload_params import ParsePolygons
from .utils.truncate_polygons import TruncatePolygons
from .utils.truncate_points import TruncatePoints
import requests
from .configprop.user_specific_reader import load_simulation_config
from .configprop.simulation_reader import read_config
from .utils.wms_utils import WMSUtils
from .utils.post_process_simulation_response import PostProcessSimulationResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



@csrf_exempt
def get_file_content(request, file_id):
    try:
        file_path = f'C:\CMCC\Egeos\egeosfiles\{file_id}.json'
        with open(file_path, 'r') as file:
            # Read file content
            file_content = file.read()
            content_as_json = json.loads(file_content)

            # Create a dictionary to represent the response
            response_data = {
                "file_id": file_id,
                "content": content_as_json,
                "status": "success"
            }

            # Return the response as JSON
            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, safe=False)

    except FileNotFoundError:
        # Handle file not found error
        response_data = {
            "file_id": file_id,
            "status": "error",
            "message": "File not found"
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, safe=False)



@csrf_exempt
def load_create_features_object(request, file_id):
    try:
        print("load_create_features_object")
        file_path = f'C:\CMCC\Egeos\egeosfiles\{file_id}.json'
        with open(file_path, 'r') as file:
            # Read file content
            file_content = file.read()
            response_data = json.loads(file_content)

            # Create instances of your classes based on the loaded data
            crs = CRS(response_data["crs"]["type"], response_data["crs"]["properties"])

            features = []
            for feature_data in response_data["features"]:
                geometry_data = feature_data.get("geometry")
                geometry_instance = None
                if geometry_data:
                    geometry_instance = Geometry(geometry_data["type"], geometry_data.get("coordinates"))
                    polygons_list= ParsePolygons.map_coordinates(geometry_data.get("coordinates"))
                    map_feature= SheenPolygon(geometry_data["type"], geometry_data.get("coordinates"), polygons_list)
                    properties_data = feature_data["properties"]
                    #print("properties_data")
                    #print(properties_data)
                    # Handle the date-time attribute explicitly
                    relevant_properties = {
                        "feature_id": properties_data["id"],
                        "length_km": properties_data["length_km"],
                        "width_km": properties_data["width_km"],
                        "baric_lat": properties_data["baric_lat"],
                        "min_lat": properties_data["min_lat"],
                        "possible_s": properties_data["possible_s"],
                        "class_val": properties_data["class_val"],
                        "region_aff": properties_data["region_aff"],
                        "max_lon": properties_data["max_lon"],
                        "area_km": properties_data["area_km"],
                        "country_as": properties_data["country_as"],
                        "max_lat": properties_data["max_lat"],
                        "min_lon": properties_data["min_lon"],
                        "baric_lon": properties_data["baric_lon"],
                        "alarm_lev": properties_data["alarm_lev"],

                        # ... (other fields)
                        "date_time": properties_data["date-time"],
                    }

                    properties_instance = Properties(**relevant_properties)

                    feature_instance = Feature(feature_data["id"], geometry_instance,map_feature, feature_data["geometry_name"], properties_instance)
                    features.append(feature_instance)

            feature_collection_instance = FeatureCollection(response_data["totalFeatures"], features, crs)

            #content_as_json = json.dumps(feature_collection_instance, default=lambda o: o.__dict__)
            content_as_json = json.loads(json.dumps(feature_collection_instance, default=lambda o: o.__dict__))
            # Create a dictionary to represent the response
            response_data = {
                "file_id": file_id,
                "content": content_as_json,
                "status": "success"
            }

            # Return the response as JSON
            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, safe=False)

    except FileNotFoundError:
        # Handle file not found error
        response_data = {
            "file_id": file_id,
            "status": "error",
            "message": "File not found"
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, safe=False)



@csrf_exempt
def run_forecast_modelling(request):
    print("here")
    print(request)
    if request.method == 'POST':
        try:
            # Assuming 'file_content' is passed in the request body
            file_content = json.loads(request.body)

            # Placeholder logic: Simulate CMCC processing
            cmcc_unique_id = "99999"  # The first 6 digits

            # Generate the last four digits randomly
            random_digits = str(random.randint(10000, 99999))

            # Combine the first six digits and the random four digits
            complete_cmcc_unique_id = cmcc_unique_id + random_digits
            processing_code = 0

            # Create the response data
            response_data = {
                "processing_id": complete_cmcc_unique_id,
                "processing_code": processing_code
            }

            # Return the response as JSON
            return JsonResponse(response_data, status=200, json_dumps_params={'ensure_ascii': False}, safe=False)

        except json.JSONDecodeError:
            processing_code = 11
            # Handle the case where the request body is not a valid JSON
            response_data = {
                "error": "Invalid JSON in the request body",
                "processing_code": processing_code
            }
            return JsonResponse(response_data, status=400, json_dumps_params={'ensure_ascii': False}, safe=False)

    else:
        processing_code = 12
        # Handle unsupported HTTP methods
        response_data = {
            "error": "Unsupported HTTP method",
            "processing_code": processing_code
        }
        return JsonResponse(response_data, status=500, json_dumps_params={'ensure_ascii': False}, safe=False)


def convert_to_simulation_name(event_id):
    # Replace spaces with underscores
    simulation_name = event_id.replace(" ", "_")
    return simulation_name

def obtain_slat_slon_string(sheen_polygon):
    list_polygons = sheen_polygon.get("polygons")
    point_strings = []

    for j, polygon in enumerate(list_polygons, start=1):
        polygon_index = j
        polygon_coordinates = polygon.get("coordinates")
        print(polygon)
        for i, point in enumerate(polygon_coordinates, start=1):
            point_index = i
            print(point)
            latitude, longitude = point.get("latitude"), point.get("longitude")

            point_strings.append(
                f'"Slat_{polygon_index}_{point_index}": "{latitude}", '
                f'"Slon_{polygon_index}_{point_index}": "{longitude}"'
            )

    return ', '.join(point_strings)

@csrf_exempt  # This is added to handle POST requests without CSRF token for simplicity. Use it carefully.
def convert_event_to_request_payload(request,file_id):
    #if request.method == 'POST':
    try:
        # Load the JSON data from the request body
        #payload = json.loads(request.body)
        #feature_collection = payload.get('feature_collection', {})
        create_features_url = "http://127.0.0.1:8000/egeos-adaptor/load_create_features_object/"
        #file_id="CSKS1_DGM_B_WR_00_VV_RA_FF_20210607042748_20210607042803_2021-0"
        response = requests.get(f"{create_features_url}{file_id}/")
        robj= response.json()
        print(robj)
        feature_collection_dict=robj['content']
        #feature_collection_dict = json.loads(feature_collection)
        feature_id = feature_collection_dict.get("features", [{}])[0].get("id")
        simulation_name = convert_to_simulation_name(feature_id)
        print("simulationName", simulation_name)
        # Example usage
        date_time_features  = feature_collection_dict.get("features", [{}])[0].get("properties").get("date_time")
        #print(date_time_features)
        date_payload = ParseDateTime.parse_datetime(date_time_features)
        # Call the method and print the result
        payload_dict = date_payload
        print(payload_dict)

        sheen_polygon=feature_collection_dict.get("features", [{}])[0].get("sheenpolygon")
        #print(sheen_polygon)
        
        slatslon_str = obtain_slat_slon_string(sheen_polygon)

        print(slatslon_str)
        first_point = feature_collection_dict.get("features", [{}])[0].get("sheenpolygon").get("polygons")[0].get("coordinates")[0]
        start_lat_start_lon = ParsePolygons.extract_start_lat_start_lon(first_point)

        print(start_lat_start_lon.startLat)
        print(start_lat_start_lon.startLon)

        degree_and_minutes = ParsePolygons.extract_degrees_and_minutes(first_point)

        # Print the values
        print(f"Lat Degree: {degree_and_minutes.lat_degree}")
        print(f"Lat Minutes: {degree_and_minutes.lat_minutes}")
        print(f"Lon Degree: {degree_and_minutes.lon_degree}")
        print(f"Lon Minutes: {degree_and_minutes.lon_minutes}")

        #get area km
        area_km  = feature_collection_dict.get("features", [{}])[0].get("properties").get("area_km")

        # Example usage:
        file_path = "C:/CMCC/Egeos/EgeosCode/egeosdjango/egeosapp/configprop/user_specific.ini"
        user_specific_config = load_simulation_config(file_path)

        # Display the values
        for key, value in user_specific_config.items():
            print(f"{key}: {value}")

        # Example usage:
        file_path = 'C:/CMCC/Egeos/EgeosCode/egeosdjango/egeosapp/configprop/simulation.ini'  # Replace with the actual path to your config file
        config_values = read_config(file_path)

        # Access individual parameters
        min_volume = config_values.getint('minVolume')
        oil = config_values.get('oil')
        oil_type = config_values.get('oilType')
        max_number_of_polygons = config_values.getint('maxNumberOfPolygons')
        max_number_of_points = config_values.getint('maxNumberOfPoints')
        wind = config_values.get('wind')
        contour_slick = config_values.getboolean('contourSlick')
        oil_density_coefficient = config_values.getfloat('oilDensityCoefficient')


        # Get spill rate coefficient from the configuration
        spill_rate_coeff_str = user_specific_config.get("spillRateCoefficient", "0.0")

        min_volume = 1.0

        spill_rate = ParsePolygons.compute_spill_rate(spill_rate_coeff_str, min_volume)

        # Print the result
        print(spill_rate)

        #Compute Oil Density
        print(oil_density_coefficient)
        print(area_km)
        oil_density_computation = oil_density_coefficient*area_km
        

        # Print the values
        print(f"minVolume: {min_volume}")
        print(f"oil: {oil}")
        print(f"oilType: {oil_type}")
        print(f"maxNumberOfPolygons: {max_number_of_polygons}")
        print(f"maxNumberOfPoints: {max_number_of_points}")
        print(f"wind: {wind}")
        print(f"contourSlick: {contour_slick}")

        truncate_polygons = TruncatePolygons()
        truncated_polygons = truncate_polygons.truncate_coordinates(max_number_of_polygons, slatslon_str)

        # Print the result
        print("truncated_polygons")
        print(truncated_polygons)

        truncate_points = TruncatePoints()
        truncated_points = truncate_points.truncate_points(max_number_of_points, truncated_polygons)

        # Print the result
        print("truncated_points")
        print(truncated_points)

        ssarequest_payload = RequestPayloadBody('',simulation_name,'',str(start_lat_start_lon.startLat),str(start_lat_start_lon.startLon),
                                                user_specific_config.get("model"),wind,user_specific_config.get("simulationDuration"),
                                                date_payload.year,date_payload.month,date_payload.day,
                                                date_payload.hour,date_payload.minute,degree_and_minutes.lat_degree,degree_and_minutes.lat_minutes,
                                                degree_and_minutes.lon_degree,degree_and_minutes.lon_minutes,user_specific_config.get("spillType"),
                                                user_specific_config.get("duration"),spill_rate,oil,oil_type,oil_density_computation,
                                                user_specific_config.get("stokesDrift"),user_specific_config.get("windCorrection"),
                                                user_specific_config.get("horizontalDiffusivity"),user_specific_config.get("oilParcelNumber"),
                                                user_specific_config.get("var_19"),user_specific_config.get("var_29"),user_specific_config.get("var_39"),
                                                user_specific_config.get("plotStep"),user_specific_config.get("selector"),contour_slick,truncated_points)
        content_as_json = json.loads(json.dumps(ssarequest_payload, default=lambda o: o.__dict__))
        # Create a dictionary to represent the response
        response_data = {
            "content": content_as_json,
            "status": "success"
        }

        # Return the response as JSON
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, safe=False)
        #return JsonResponse({"message": "Request processed successfully"})
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON data in the request"}, status=400)
    #else:
    #    return JsonResponse({"message": "Unsupported method"}, status=405)


def fetch_report_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Assuming the response is JSON
    else:
        return None

def fetch_ossi_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Assuming the response is JSON
    else:
        return None

@csrf_exempt  # This is added to handle POST requests without CSRF token for simplicity. Use it carefully.
def generate_forecast_modelling_response(request):
    if request.method == 'POST':
        wms_url = "https://ov-matteo.cmcc-opa.eu/cgi-bin/mapserv?service=WMS"
        try:
            post_process_simulation_response = PostProcessSimulationResponse()
            wms_accessibility = WMSUtils.check_wms_accessibility(wms_url)
            print(wms_accessibility)

            if wms_accessibility == "WMS is accessible!":
                request_data = json.loads(request.body.decode('utf-8'))
                simulation_id = request_data.get('simulationId')
                api_url = WMSUtils.generate_wms_url("GetCapabilities", simulation_id)
                wms_url = WMSUtils.generate_layer_url(simulation_id)
                
                response_xml = requests.get(api_url).text
                print(response_xml)
                
                processed_response = post_process_simulation_response.parse_xml_string(response_xml, simulation_id, wms_url)
                print("wmss", processed_response.wmss)
                
                if not processed_response.wmss:
                    #simulation_id = request_data.get('simulationId')
                    #processed_response = post_process_simulation_response.prepare_failed_response(simulation_id)
                    #json_data = json.dumps(processed_response.to_dict(), indent=2)
                    return JsonResponse("You’re not allowed to see the event with that event_id", status=404)
                else:
                    processed_response.status="SUCCEED"
                    report_url = WMSUtils.generate_report_url(simulation_id)
                    report_data = fetch_report_from_url(report_url)
                    processed_response.report = report_data
                    print(processed_response)
                    ossi_url = WMSUtils.generate_oilspill_impact_url(simulation_id)
                    ossi_data=fetch_ossi_from_url(ossi_url)
                    processed_response.oilspill_impact = ossi_data
                    processed_response.netcdf_repository = "https://cmcc-endpoint.cmcc-opa.eu/something/cmcc-unique-id/repository.tgz"
                    json_data = json.dumps(processed_response.to_dict(), indent=2)
                    print(json_data)
                    return JsonResponse(json.loads(json_data), status=200)
            else:
                # Your logic for a failed response
                return JsonResponse({"message": "WMS is not accessible!"}, status=500)
        except Exception as e:
            #print(e)
            # Handle other exceptions if needed
            return JsonResponse({"message": "Bad Request, Date parsing error, Port not found"}, status=400)
    else:
        return JsonResponse({"message": "Unsupported method"}, status=405)
