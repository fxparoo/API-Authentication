from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import authentication.models as am
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_registration.api.serializers import DefaultRegisterUserSerializer


class RegisterUserSerializer(DefaultRegisterUserSerializer):
    class Meta:
        model = am.AppUser

    def create(self, validated_data, *args):
        student = validated_data.get('student')
        data = validated_data.copy()
        return self.register_user(student, data)

    def register_user(self, student, data):
        if student:
            request = self.context.get('request')
            student_data = request.data.get('student_data')
            user = am.AppUser.objects.create_user(**data)
            user.role = 'Student'
            user.is_student = student_data.get('student_name')
            user.save()
            am.student.objects.create(first_name=student_data.get('first_name'),
                                      last_name=student_data.get('last_name'),
                                      email=student_data.get('email'))
            return user
        else:
            user = am.AppUser.objects.create_user(**data)
            user.role = 'Teacher'
            user.save()
            return user


class LoginTokenSerializer(TokenObtainPairSerializer):
    """Custom Serializer for jwt access and refresh token"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_active'] = user.is_active
        token['role'] = user.role
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['is_student'] = user.is_student
        token['is_teacher'] = user.is_teacher
        token['is_librarian'] = user.is_librarian

        return token


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = am.AppUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"message": "Password fields don't match"})
        return attrs

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError({"message": "incorrect old password"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            "message": "password updated successfully"
        }



