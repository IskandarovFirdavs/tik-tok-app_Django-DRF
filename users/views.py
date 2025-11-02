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

from posts.models import PostModel
from posts.serializers import PostModelSerializer
from .models import Follow
from .serializers import UserSerializer, LoginSerializer, FollowSerializer, UserModelSerializer

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
        posts = PostModel.objects.filter(user=request.user)
        post_serializer = PostModelSerializer(posts, many=True)

        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "first_name": getattr(request.user, "first_name", ""),
            "last_name": getattr(request.user, "last_name", ""),
            "avatar": request.build_absolute_uri(request.user.avatar.url) if request.user.avatar else None,
            "bio": getattr(request.user, "bio", ""),
            "follower_count": request.user.followers_count,
            "following_count": request.user.following_count,
            "posts": post_serializer.data,
        })

    def put(self, request):
        serializer = UserModelSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {'message': 'User deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


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



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)