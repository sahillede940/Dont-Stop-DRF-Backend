from rest_framework import serializers
from .models import Competition
from user.models import UserSelector


class UserCompInlineSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(view_name='competition-detail')


class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competition
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get('request')
        if attrs.get('teamsize') and attrs.get('teamsize') < 1:
            raise serializers.ValidationError(
                {"teamsize": "Team size must be greater than 0."})

        if attrs.get('creator') and attrs.get('creator') != request.user:
            raise serializers.ValidationError(
                {"creator": "You are not the creator of this competition."})

        return attrs
    

class ApplyCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSelector
        fields = "__all__"
