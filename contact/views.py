from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from zoneinfo import ZoneInfo

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            msg = serializer.save()
            # Convert UTC to India/Kolkata timezone
            india_time = timezone.localtime(
                msg.created_at,
                ZoneInfo("Asia/Kolkata")
            )
            # Send email notification to YOU
            send_mail(
                subject=f"[Portfolio] New message from {msg.name}: {msg.subject or 'No subject'}",
                message=(
                    f"From: {msg.name} <{msg.email}>\n"
                    f"Received: {india_time:%Y-%m-%d %H:%M:%S IST}\n\n"
                    f"{msg.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )
            # Send confirmation to the sender
            send_mail(
                subject="Got your message! I'll be in touch soon.",
                message=(
                    f"Hi {msg.name},\n\n"
                    f"Thanks for reaching out! I received your message and will get back to you within 24 hours.\n\n"
                    f"— Your Saqlain Ahamed Baig"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[msg.email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)