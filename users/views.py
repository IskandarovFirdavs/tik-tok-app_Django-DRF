from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import Follow
from .serializers import UserSerializer, LoginSerializer, FollowSerializer

User = get_user_model()

class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']
    filter_fields = ['username', 'first_name']




class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access_token': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = (AllowAny,)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        following = get_object_or_404(User, id=user_id)

        follow_obj = Follow.objects.filter(
            follower=request.user,
            following=following
        ).first()

        if follow_obj:
            follow_obj.delete()
            return Response(
                {"detail": f"{request.user.username} unfollowed {following.username}"},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            Follow.objects.create(
                follower=request.user,
                following=following
            )
            return Response(
                {"detail": f"{request.user.username} now following {following.username}"},
                status=status.HTTP_201_CREATED
            )

