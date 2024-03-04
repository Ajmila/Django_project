from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

class PasswordChangeSerializer(serializers.Serializer):
    username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        # Check if new password and confirm new password match
        if new_password != confirm_new_password:
            raise serializers.ValidationError("New password and confirm new password must match.")

        return data

class VideoUploadSerializer(serializers.Serializer):
    video = serializers.FileField()

# class ProcessDataSerializer(serializers.Serializer):
#     class_name = serializers.CharField()
#     branch_name = serializers.CharField()