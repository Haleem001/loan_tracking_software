from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username' , 'email' , 'first_name' , 'last_name' , 'password' , 'password2', 'Status']
    
    def validated_status(self, validated_data):
        if validated_data['Status'] == 'Admin':
            user = CustomUser.objects.create_superuser(validated_data['Status'],
                                                 validated_data['username'],  validated_data['email'],
                                                 validated_data['password'], validated_data['first_name'], validated_data['last_name'] )
        elif validated_data['Status'] == 'Staff':
            user = CustomUser.objects.create_staffuser(
                validated_data['Status'], validated_data['username'], validated_data[
                    'email'],
                validated_data['password'], validated_data['first_name'], validated_data['last_name'])
        elif validated_data['Status'] == 'User':
            user = CustomUser.objects.create_user(validated_data['Status'], validated_data['username'], validated_data[
                'email'],
                validated_data['password'], validated_data['first_name'], validated_data['last_name'])
        return user
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs


    def create(self, validated_data):
        user = self.validated_status(validated_data)
        user.save()
        return user
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('old_password', 'password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."})
#         return attrs

#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError(
#                 {"old_password": "Old password is not correct"})
#         return value

#     def update(self, instance, validated_data):
#         instance.set_password(validated_data['password'])
#         instance.save()
#         return instance
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        if not user.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError({"old_password": "Wrong password."})
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'Status',  'username',  'email', 'first_name', 'last_name']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {'email': {'read_only': True}}

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance