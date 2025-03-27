from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .utils import fetch_houses

class HouseListView(APIView):
    """Fetch houses from an external API and return data"""

    def get(self, request):
        response = fetch_houses()

        if response['status_code'] == 200:
            return Response({'data':response['data'], 'status':status.HTTP_200_OK, 'success': True}, status=status.HTTP_200_OK)
        
        return Response(
            {"error": response['error'], 'status':response['status_code'], 'success': False},
            status=response['status_code'],
        )