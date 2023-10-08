from rest_framework import generics, permissions, status
from . import serializers
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from .models import Competition
from user.models import UserSelector


class OptimizedQuerySetMixin:
    def get_queryset(self):
        if self.action == 'list':
            return Competition.objects.all()
        else:
            return Competition.objects.filter(pk=self.kwargs['pk'])


class CompetitionViewSet(OptimizedQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CompetitionSerializer
    lookup_field = 'pk'

    def is_creator(self):
        return self.request.user == self.get_object().creator

    def create(self, request, *args, **kwargs):
        request.data['creator'] = request.user
        competition = Competition.objects.create(**request.data)
        print(request.data)
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


class ApplyCompetition(generics.GenericAPIView):
    serializer_class = serializers.ApplyCompetitionSerializer

    def post(self, request, pk=None, *args, **kwargs):
        userComp = UserSelector.objects.create(
            user=request.user,
            Competition=Competition.objects.get(pk=pk),
            note=request.data['note']
        )

        competition = Competition.objects.get(pk=request.data['competition'])
        competition.applied_users.add(userComp)

        return Response({
            "success": True,
            "message": f"Applied Successfully for comp {request.data['competition']}",
            "userComp": self.serializer_class(userComp).data,
        }, status=status.HTTP_201_CREATED)
