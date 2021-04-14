from rest_framework.response import Response
from rest_framework import status

ERROR_BAD_REQUEST = Response({'Error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
ERROR_DOES_NOT_ESIST = Response({'Error': 'Room does not exist.'}, status=status.HTTP_404_NOT_FOUND)
ERROR_NOT_IN_ROOM = Response({'Error': 'Not currently in room'}, status=status.HTTP_400_BAD_REQUEST)

SUCCESS_JOINED = Response({'Success': 'Room joined successfully'}, status=status.HTTP_200_OK)
SUCCESS_LEFT = Response({'Success': 'Left room successfully',}, status=status.HTTP_202_ACCEPTED)
