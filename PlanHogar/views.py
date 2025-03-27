import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import random
import os

from dotenv import load_dotenv

load_dotenv()


PROPERTIES_API = os.getenv("PROPERTIES_API")

class HouseListView(APIView):
    """Fetch houses from an external API and return data"""

    def get(self, request):
        try:
            response = requests.get(PROPERTIES_API)

            if response.status_code == 200:
                data = response.json()

                data["bedrooms"] = random.randint(1, 5)  # Between 1 and 5 bedrooms
                data["bathrooms"] = random.randint(1, 3)  # Between 1 and 3 bathrooms
                data["living_rooms"] = random.randint(1, 2)  # 1 or 2 living rooms
                data["garage"] = random.choice([True, False])  # Garage availability
                data["square_meters"] = random.randint(50, 400)  # Random house size
                
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Failed to fetch data from external API"},
                    status=response.status_code,
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )