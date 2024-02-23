import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List
from egeosapp.models import PostProcessedWMS,WMS


class PostProcessSimulationResponse:
    
    def parse_xml_string(self, xml_response, simulation_id, wms_url):
        post_processed_wms = PostProcessedWMS()

        try:
            root = ET.fromstring(xml_response)

            for wms_capabilities in root.findall(".//{http://www.opengis.net/wms}WMS_Capabilities"):
                name = wms_capabilities.findtext(".//{http://www.opengis.net/wms}Name")
                print("Name:", name)

            wms_list = []
            for layer in root.findall(".//{http://www.opengis.net/wms}Layer"):
                layer_name = layer.findtext(".//{http://www.opengis.net/wms}Name")
                dimension = layer.findtext(".//{http://www.opengis.net/wms}Dimension")
                print("Name:", layer_name)
                print("Dimension:", dimension)

                #date_range_list = self.generate_datetime_list(dimension)
                date_range_list = dimension

                if layer_name == "Witoil-Total-Oil":
                    wms_object = WMS()
                    wms_object.layer = layer_name
                    wms_object.time_range = date_range_list
                    wms_object.wms_description = "Modeled concentration of oil found at the sea surface in tons/km2"
                    wms_object.wms_url = wms_url
                    wms_list.append(wms_object)
                if layer_name == "Witoil-Beached":
                    wms_object = WMS()
                    wms_object.layer = layer_name
                    wms_object.time_range = date_range_list
                    wms_object.wms_description = "Modeled concentration of oil found permanently or temporarily attached to the coast in tons of oil per km of impacted coastline"
                    wms_object.wms_url = wms_url
                    wms_list.append(wms_object)

            #record = RecordCreateService.get_record(simulation_id)
            post_processed_wms.wmss = wms_list

            #if record is not None:
            #    post_processed_wms.acquisition_id = record.get("correlationId")
            #    if record.get("status") == "C":
            #        post_processed_wms.status = "SUCCEED"

        except Exception as ex:
            print(ex)

        return post_processed_wms

    def generate_datetime_list(self, date_range):
        datetime_list = []

        parts = date_range.split("/")
        start_str = parts[0]
        end_str = parts[1]
        interval_str = parts[2]

        iso_format = "%Y-%m-%dT%H:%M:%SZ"
        output_format = "%d-%m-%Y %H:%M"

        print("Start Date:", start_str)
        print("End Date:", end_str)

        start_date = datetime.strptime(start_str, iso_format)
        end_date = datetime.strptime(end_str, iso_format)
        interval_millis = self.parse_interval(interval_str)

        current_date_time = start_date

        while current_date_time <= end_date:
            datetime_list.append(current_date_time.strftime(output_format))
            current_date_time += timedelta(milliseconds=interval_millis)

        return datetime_list

    def parse_interval(self, interval_str):
        # Parse interval like "PT1H" to milliseconds
        interval_millis = 0

        if interval_str.startswith("PT") and interval_str.endswith("H"):
            hours_str = interval_str[2:-1]
            hours = int(hours_str)
            interval_millis = hours * 60 * 60 * 1000

        return interval_millis

    def set_wms_status(self, simulation_id):
        post_processed_wms = PostProcessedWMS()
        #record = RecordCreateService.get_record(simulation_id)
        #post_processed_wms.acquisition_id = record.get("correlationId")
        post_processed_wms.status = "FAILED"

        return post_processed_wms

    def prepare_failed_response(self, simulation_id):
        WMS_list = []
        post_processed_wms = PostProcessedWMS()
        wms_object = WMS()
        wms_object.layer = " "
        wms_object.wms_dates = []
        wms_object.wms_description = "mdslk totaloil description"
        wms_object.wms_url = ""
        WMS_list.append(wms_object)

        post_processed_wms.wmss = WMS_list

        #record = RecordCreateService.get_record(simulation_id)
        #post_processed_wms.acquisition_id = record.get("correlationId")
        post_processed_wms.status = "FAILED/OOD"

        return post_processed_wms
