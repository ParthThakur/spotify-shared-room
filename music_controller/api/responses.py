from rest_framework.response import Response
from rest_framework import status

ERROR_BAD_REQUEST = Response({'Error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
ERROR_DOES_NOT_EXIST = Response({'Error': 'Room does not exist.'}, status=status.HTTP_404_NOT_FOUND)
ERROR_NOT_IN_ROOM = Response({'Error': 'Not currently in room'}, status=status.HTTP_400_BAD_REQUEST)
ERROR_NOT_A_HOST = Response({'Error': 'User not a host'}, status=status.HTTP_403_FORBIDDEN)

SUCCESS_JOINED = Response({'Success': 'Room joined successfully'}, status=status.HTTP_200_OK)
SUCCESS_LEFT = Response({'Success': 'Left room successfully',}, status=status.HTTP_202_ACCEPTED)
SUCCESS_UPDATED = Response({'Success': 'Room settings were updated successfully'}, status=status.HTTP_202_ACCEPTED)
