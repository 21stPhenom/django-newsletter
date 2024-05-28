from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import DEFAULT_FROM_EMAIL
from newsletter_api.tasks import send_email_task

class SendMail(APIView):
    def post(self, request, *args, **kwargs):
        email_address = request.data.get('email_address', None)
        message = request.data.get('message', None)
        
        if type(email_address) != str:
            return Response({
                'error': 'email address must be a string'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # handle empty email address parameter
        if email_address is None:
            return Response({
                'error': 'email parameter must not be empty'
            }, status=status.HTTP_400_BAD_REQUEST)

        # validate email address before sending mail
        try:
            validate_email(email_address)
        except ValidationError:
            print(email_address)
            return Response({
                'error': 'invalid email received'
            }, status=status.HTTP_400_BAD_REQUEST)

        # replace `None` with an empty string
        if message is None:
            message = ''
            
        try:
            send_email_task.delay(email_address, message)
            return Response({
                'message': 'email sent successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured, please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
email_view = SendMail.as_view()