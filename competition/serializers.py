from rest_framework import serializers
from .models import Competition
from user.models import UserSelector


class UserCompInlineSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(view_name='competition-detail')


class CompetitionSerializer(serializers.ModelSerializer):
    already_applied = serializers.SerializerMethodField()
    is_accepted = serializers.SerializerMethodField()
    fullName = serializers.CharField(source='creator.fullName', read_only=True)

    class Meta:
        model = Competition
        fields = "__all__"

    def get_already_applied(self, obj):
        request = self.context.get('request')
        if request:
            return obj.applied_users.filter(pk=request.user.pk).exists()
        return False

    def get_is_accepted(self, obj):
        request = self.context.get('request')
        if request:
            userSelector = UserSelector.objects.filter(
                user_applied=request.user, competition=obj)
            if userSelector:
                return userSelector[0].status
        return False

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
