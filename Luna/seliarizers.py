from rest_framework import serializers

from Luna.models import HydroponicSystem, Reading


class HydroponicSystemSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = HydroponicSystem
        fields = ["id", "owner", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "owner"]


class ReadingSerializer(serializers.ModelSerializer):
    hydroponic_system = serializers.PrimaryKeyRelatedField(
        queryset=HydroponicSystem.objects.none()
    )

    class Meta:
        model = Reading
        fields = ["id", "hydroponic_system", "temperature", "ph", "tds", "timestamp"]
        read_only_fields = ["timestamp"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "request" in self.context:
            self.fields["hydroponic_system"].queryset = HydroponicSystem.objects.filter(
                owner=self.context["request"].user
            )
