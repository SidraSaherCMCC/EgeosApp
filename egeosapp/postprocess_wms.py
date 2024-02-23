from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class ReceiveSimulationRequest(APIView):
    wms_url = "https://ov-matteo.cmcc-opa.eu/cgi-bin/mapserv?service=WMS"

    def post(self, request):
        try:
            post_process_simulation_response = PostProcessSimulationResponse()
            wms_accessibility = self.check_wms_accessibility(self.wms_url)
            print(wms_accessibility)

            if wms_accessibility == "WMS is accessible!":
                # Your logic for a successful response
                return Response({"message": "Success!"}, status=status.HTTP_200_OK)
            else:
                # Your logic for a failed response
                return Response({"message": "WMS is not accessible!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(e)
            # Handle other exceptions if needed
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def check_wms_accessibility(self, wms_url):
        is_accessible = self.is_wms_accessible(wms_url)

        if is_accessible:
            return "WMS is accessible!"
        else:
            return "WMS is not accessible!"

    def is_wms_accessible(self, wms_url):
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
