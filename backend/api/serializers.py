from .models import User, Organization, Workshop, UserOrganization,LoginWorkshop
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email","password", "bio", "role"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email","password", "bio", "role"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}
    

class OrganizationSerializer(serializers.ModelSerializer):
    numb_of_users = serializers.IntegerField(read_only=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "info", "numb_of_users"]

    def get_numb_of_users(self, obj):
        return UserOrganization.objects.filter(organization_id=obj.id).count()
    

class WorkshopSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)
    numb_of_users = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = '__all__'

    def get_numb_of_users(self, obj):
        return LoginWorkshop.objects.filter(workshop_id=obj.id).count()

class ProfessorWorkshopSerializer(serializers.ModelSerializer):
    numb_of_users = serializers.IntegerField(read_only=True)
    class Meta:
        model = Workshop
        fields = '__all__'
        extra_kwargs = {'user_id': {'write_only':True}}


class UserOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrganization
        fields = "__all__"
        extra_kwargs = {'user_id': {'read_only':True}}


class LoginWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginWorkshop
        fields = "__all__"
        extra_kwargs = {'workshop_id': {'read_only':True}}


class StudentWorkshopSerializer(serializers.ModelSerializer):
    workshop = WorkshopSerializer(source='workshop_id', read_only=True)

    class Meta:
        model = LoginWorkshop
        fields = "__all__"
        extra_kwargs = {'workshop_id': {'read_only':True}, 'user_id': {'write_only': True}}

class StudentProfessorSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email","password", "bio", "organizations"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def get_organizations(self,obj):
        user_organizations = UserOrganization.objects.filter(user_id=obj.id)
        organization_id = user_organizations.values_list('organization_id', flat=True)
        organizations = Organization.objects.filter(id__in=organization_id)
        return OrganizationSerializer(organizations, many=True).data