from rest_framework import serializers

from Luna.models import HydroponicSystem, Reading


class HydroponicSystemSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = HydroponicSystem
        fields = ["id", "owner", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "owner"]


class HydroponicSystemDetailSerializer(HydroponicSystemSerializer):
    latest_readings = serializers.SerializerMethodField()

    class Meta(HydroponicSystemSerializer.Meta):
        fields = HydroponicSystemSerializer.Meta.fields + ["latest_readings"]

    def get_latest_readings(self, obj):
        readings = obj.readings.all().order_by("-timestamp")[:10]
        return ReadingSerializer(readings, many=True).data


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
