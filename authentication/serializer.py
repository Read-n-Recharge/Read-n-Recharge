from .models import User,StudyPrefernce
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ('id',  'first_name', 'last_name', 'email')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['verified'] = user.profile.verified

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id 
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name','password','confirm_password')

    def validatePassword(self,attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']

        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class StudyPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPrefernce
        fields = ('chronotype','concentration','studying_style','procrastination','physical_activity')

    
                
             

        


