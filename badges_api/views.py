from django.forms import ValidationError
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Badge, Achievement
from .serializers import BadgeSerializer, AchievementSerializer
from users.models import User

class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AchievementsListCreateView(generics.ListCreateAPIView):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id:
            return Achievement.objects.filter(user__id=user_id)
        return Achievement.objects.none()

    def create(self, request):
        user_id = request.data.get('user')
        badge_id = request.data.get('badge')

        if not user_id or not badge_id:
            return Response({'detail': 'User and Badge are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
    
            user = User.objects.get(id=user_id)
            badge = Badge.objects.get(id=badge_id)

            achievement_data = {
                'user': user.id,
                'badge': badge.id
            }

            serializer = self.get_serializer(data=achievement_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'detail': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)
        except Badge.DoesNotExist:
            return Response({'detail': 'Invalid badge ID.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            # Handle unique constraint violation or validation errors
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
