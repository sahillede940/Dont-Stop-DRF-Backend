from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from user.serializers import UserSelectorSerializer

from .models import Competition
from . import serializers
from user.models import UserSelector
from rest_framework import filters

from django.contrib.auth import get_user_model

User = get_user_model()


class OptimizedQuerySetMixin:
    def get_queryset(self):
        if self.action == 'list':
            return Competition.objects.exclude(creator=self.request.user)
        else:
            return Competition.objects.filter(pk=self.kwargs['pk'])


class CompetitionViewSet(OptimizedQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CompetitionSerializer
    lookup_field = 'pk'
    search_fields = ['name', 'description']
    filter_backends = (filters.SearchFilter,)

    def is_creator(self):
        return self.request.user == self.get_object().creator

    def create(self, request, *args, **kwargs):
        request.data['creator'] = request.user
        competition = Competition.objects.create(**request.data)
        return Response({
            "success": True,
            "message": "Competition Created Successfully",
            "competition": self.serializer_class(competition).data,
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        competition = self.get_object()
        super().retrieve(request, *args, **kwargs)
        return Response({
            "success": True,
            "competition": self.serializer_class(competition).data,
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        competition = self.get_object()
        if self.is_creator():
            competition = super().update(request, *args, **kwargs)
            return Response({
                "success": True,
                "message": "Competition Updated Successfully",
                "competition": competition.data,
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "You are not the creator of this competition."
        }, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        competition = self.get_object()
        if self.is_creator():
            competition.delete()

            return Response({
                "success": True,
                "message": "Competition Deleted Successfully",
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "You are not the creator of this competition."
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserCompetitionView(generics.ListAPIView):
    serializer_class = serializers.CompetitionSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        competitions = Competition.objects.filter(creator=user)
        return Response({
            "success": True,
            "competitions": self.serializer_class(competitions, many=True).data,
        }, status=status.HTTP_200_OK)


class ApplyCompetitionView(generics.GenericAPIView):
    serializer_class = serializers.CompetitionSerializer

    def patch(self, request, pk):
        user = request.user
        competition = Competition.objects.get(pk=pk)

        if competition.applied_users.filter(pk=user.pk).exists():
            return Response({'message': 'You have already applied.'}, status=400)
        competition.applied_users.add(user)

        userSelector = UserSelector.objects.create(
            user_applied=user,
            competition=Competition.objects.get(pk=pk),
            note=request.data.get('note'),
            status=False,
        )
        userSelector = UserSelectorSerializer(userSelector).data

        competition.save()
        return Response({
            'success': True,
            'userSelector': userSelector,
            'message': f'Applied successfully to {competition.name}'
        }, status=200)

    def delete(self, request, pk):
        user = request.user
        competition = Competition.objects.get(pk=pk)
        if not competition:
            return Response({'message': 'Competition does not exist.'}, status=400)

        if not competition.applied_users.filter(pk=user.pk).exists():
            return Response({'message': 'You have not applied.'}, status=400)
        competition.applied_users.remove(user)

        userSelector = UserSelector.objects.get(
            user_applied=user,
            competition=competition
        )
        userSelector.delete()

        competition.save()
        return Response({
            'success': True,
            'message': f'Application to {competition.name} was cancelled'
        }, status=200)


class AcceptCompetitionView(generics.GenericAPIView):

    def is_creator(self, request):
        compId = self.request.data.get('compId')
        return request.user == Competition.objects.get(pk=compId).creator

    def patch(self, request):

        if not self.is_creator(request):
            return Response({
                'success': False,
                'message': 'You are not the creator of this competition.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        userSelectorId = request.data.get('userSelectorId')
        userSelector = UserSelector.objects.get(pk=userSelectorId)
        userSelector.status = True
        userSelector.save()
        userSelector = UserSelectorSerializer(userSelector).data

        return Response({
            'success': True,
            'userSelector': userSelector,
        }, status=200)


class RemoveRequestView(generics.GenericAPIView):

    def delete(self, request, compId, userSelectorId):

        userSelector = UserSelector.objects.get(pk=userSelectorId)
        user = User.objects.get(pk=userSelector.user_applied.pk)

        Competition.objects.get(pk=compId).applied_users.remove(user)
        userSelector.delete()
        return Response({
            'success': True,
            'message': 'Request was removed'
        }, status=200)


class CompStatus(generics.GenericAPIView):
    serializer_class = UserSelectorSerializer

    def get(self, request, compId=None, *args, **kwargs):
        user = UserSelector.objects.filter(competition=compId)
        user = self.serializer_class(user, many=True).data

        return Response({
            'success': True,
            'users': user
        })


class ShowMyReq(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        userSelectors = UserSelector.objects.filter(user_applied=user)
        userSelectors = UserSelectorSerializer(userSelectors, many=True).data

        return Response({
            'status': True,
            'userSelectors': userSelectors
        })