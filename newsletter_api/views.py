from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import DEFAULT_FROM_EMAIL

class SendMail(APIView):
    def post(self, request, *args, **kwargs):
        email_address = request.data.get('email_address', None)
        message = request.data.get('message', None)
        
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

            
        if message is None:
            message = ''
        
        try:
            send_mail(
                'Test Mail',
                f'This is the message you typed: {message}',
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[email_address]
            )
            return Response({
                'message': 'email sent successfully'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                'error': 'an error occured, please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
email_view = SendMail.as_view()