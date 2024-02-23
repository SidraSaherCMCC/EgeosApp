import requests


class WMSUtils:
    def is_wms_accessible(wms_url):
        try:
            response = requests.get(wms_url)

            # Check if the response code is in the 2xx range, which indicates success.
            if 200 <= response.status_code < 300:
                return True
            else:
                return False

        except Exception as e:
            # An exception occurred, indicating that the WMS service is not accessible.
            return False
    def check_wms_accessibility(wms_url):
        is_accessible = WMSUtils.is_wms_accessible(wms_url)

        if is_accessible:
            return "WMS is accessible!"
        else:
            return "WMS is not accessible!"
        

    def generate_wms_url(request, simulation_id):
        wms_url = f"https://ov-matteo.cmcc-opa.eu/cgi-bin/mapserv?service=WMS&request={request}&map=/srv/ov/backend/support/witoil/simulations/mapfiles/{simulation_id}/witoil_{simulation_id}.map"
        return wms_url

    def generate_layer_url(simulation_id):
        layer_url = f"https://ov-matteo.cmcc-opa.eu/cgi-bin/mapserv?map=witoil_{simulation_id}&REQUEST=GetMap&service=WMS"
        return layer_url

    def generate_report_url(simulation_id):
        report_url = f"https://ov-matteo.cmcc-opa.eu/backend/support/witoil/simulations/mapfiles/{simulation_id}/report/report.json"
        return report_url

    def generate_oilspill_impact_url(simulation_id):
        oilspill_impact_url = f"https://ov-prod.cmcc-opa.eu/backend/support/witoil/simulations/mapfiles/{simulation_id}/ossi.json"
        return oilspill_impact_url


    
    
