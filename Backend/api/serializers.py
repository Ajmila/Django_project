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
    class_name = serializers.CharField()
    period = serializers.CharField()
    video = serializers.FileField()
    email = serializers.CharField()



class ViewClassSerializer(serializers.Serializer):
    _id = serializers.CharField()  # Assuming '_id' is a string field
    KTU_ID = serializers.CharField()  # Assuming 'id' is an integer field
    Roll_No = serializers.IntegerField()
    Name = serializers.CharField()
    Class = serializers.CharField()
    Email = serializers.CharField()
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['Email'] = str(instance['Email'])  # Convert email to string
        return ret