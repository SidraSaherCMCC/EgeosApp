from django.db import models
from dataclasses import dataclass
from typing import List
from typing import List, Dict


class FileData(models.Model):
    file_id = models.CharField(max_length=100)
    content = models.TextField()

class Feature:
    def __init__(self, feature_id, geometry, sheenpolygon, geometry_name, properties):
        self.type = "Feature"
        self.id = feature_id
        self.geometry = geometry
        self.sheenpolygon = sheenpolygon
        self.geometry_name = geometry_name
        self.properties = properties


class Geometry:
    def __init__(self, geometry_type, coordinates=None):
        self.type = geometry_type
        self.coordinates = coordinates


class Properties:
    def __init__(self, feature_id, length_km, width_km, baric_lat, min_lat, possible_s,
                 class_val, region_aff, max_lon, area_km, country_as, max_lat,
                 min_lon, baric_lon, alarm_lev, date_time):
        self.id = feature_id
        self.length_km = length_km
        self.width_km = width_km
        self.baric_lat = baric_lat
        self.min_lat = min_lat
        self.possible_s = possible_s
        self.class_val = class_val
        self.region_aff = region_aff
        self.max_lon = max_lon
        self.area_km = area_km
        self.country_as = country_as
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.baric_lon = baric_lon
        self.alarm_lev = alarm_lev
        self.date_time = date_time


class CRS:
    def __init__(self, crs_type, properties):
        self.type = crs_type
        self.properties = properties


class FeatureCollection:
    def __init__(self, total_features, features, crs):
        self.type = "FeatureCollection"
        self.total_features = total_features
        self.features = features
        self.crs = crs

class RequestPayloadBody(models.Model):
    sim_name = models.CharField(max_length=255)
    notes = models.TextField()
    start_lat = models.CharField(max_length=50)
    start_lon = models.CharField(max_length=50)
    model = models.CharField(max_length=255)
    wind = models.CharField(max_length=255)
    sim_length = models.CharField(max_length=50)
    day = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    hour = models.CharField(max_length=2)
    minutes = models.CharField(max_length=2)
    lat_degree = models.CharField(max_length=3)
    lat_minutes = models.CharField(max_length=10)
    lon_degree = models.CharField(max_length=4)
    lon_minutes = models.CharField(max_length=10)
    spill_type = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    spill_rate = models.CharField(max_length=255)
    oil = models.CharField(max_length=255)
    oil_type = models.CharField(max_length=255)
    oil_density_computation = models.CharField(max_length=255)
    var_02 = models.CharField(max_length=255)
    var_03 = models.CharField(max_length=255)
    var_10 = models.CharField(max_length=255)
    var_14 = models.CharField(max_length=255)
    var_19 = models.CharField(max_length=255)
    var_29 = models.CharField(max_length=255)
    var_39 = models.CharField(max_length=255)
    plot_step = models.CharField(max_length=255)
    selector = models.CharField(max_length=255)
    contour_slick = models.CharField(max_length=255)
    s_lats_lon_string = models.CharField(max_length=255)

    def __str__(self):
        return self.sim_name 
    
class DateRequestPayload:
    def __init__(self, year, month, day, hour, minute):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute


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


class Point:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

class Polygon:
    def __init__(self, coordinates: List[Point]):
        self.coordinates = coordinates

class SheenPolygon:
    def __init__(self, type: str, coordinates: List[List[List[float]]], polygons: List[Polygon]):
        self.type = type
        self.coordinates = coordinates
        self.polygons = polygons

class StartLatStartLon:
    def __init__(self, startLat, startLon):
        self.startLat = startLat
        self.startLon = startLon

class DegreeAndMinutes:
    def __init__(self, lat_degree, lat_minutes, lon_degree, lon_minutes):
        self.lat_degree = lat_degree
        self.lat_minutes = lat_minutes
        self.lon_degree = lon_degree
        self.lon_minutes = lon_minutes

class WMS:
    def __init__(self, layer="", time_range=None, wms_description="", wms_url=""):
        self.wms_description = wms_description
        self.wms_url = wms_url
        self.layer = layer
        self.time_range = time_range
        
    def to_dict(self):
        return {
            "wms_description": self.wms_description,
            "wms_url": self.wms_url,
            "layer": self.layer,
            "time_range": self.time_range
        }

@dataclass
class ReportPostProcessor:
    wind_drag_coefficient: str
    first_contact_time: str
    wind_fields_used: str
    legend: str
    oil_type: str
    first_contact_img: str
    beached_oil_concentration_36h: str
    beached_oil_concentration_48h: str
    beached_oil_concentration_12h: str
    mass_balance: str
    beached_oil_concentration_24h: str
    simulation_length: str
    start_time: str
    surface_oil_concentration_12h: str
    surface_oil_concentration_36h: str
    surface_oil_concentration_24h: str
    first_contact_location: str
    ocean_fields_used: str
    surface_oil_concentration_48h: str
    spill_volume: str

class PostProcessedWMS:
    def __init__(self, wmss=None, report=None, status=None , processing_code=None, netcdf_repository=None, oilspill_impact=None):
        self.wmss = wmss if wmss is not None else []
        #self.report = report
        self.status = status
        self.processing_code = processing_code
        self.netcdf_repository=netcdf_repository
        self.report = report
        self.oilspill_impact = oilspill_impact

    def to_dict(self):
        return {
            "wmss": [wms.__dict__ for wms in self.wmss],
            #"report": report.__dict__ if self.report else None,
            "status": self.status,
            "processing_code": self.processing_code,
            "netcdf_repository": self.netcdf_repository,
            "report": self.report,
            "oilspill_impact": self.oilspill_impact
        }


@dataclass
class SimulationRequest:
    status: str
    simulationId: str
    serviceId: str
    correlationId: str
    dss: str