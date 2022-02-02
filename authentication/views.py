from rest_framework import viewsets, status, generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
import authentication.models as am
import authentication.serializers as aps


class LoginTokenViewSet(TokenObtainPairView):
    serializer_class = aps.LoginTokenserializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = am.AppUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = aps.ChangePasswordSerializer

