from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.response import Response
from django.db.models import Count

from .models import User,Organization,Workshop, UserOrganization,LoginWorkshop
from .serializers import UserSerializer, OrganizationSerializer,WorkshopSerializer,UserOrganizationSerializer, LoginWorkshopSerializer,ProfileSerializer,ProfessorWorkshopSerializer,StudentWorkshopSerializer,StudentProfessorSerializer

class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        curr_user = self.request.user

        return User.objects.exclude(id=curr_user.id)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Korisnik uspješno kreiran"},
            )
        else:
            return Response(
                {"message": "Greška prilikom kreiranja korisnika"}
            )
        
class UserByRoleView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        curr_user = self.request.user
        curr_role = self.kwargs["user_role"]

        return User.objects.filter(role=curr_role).exclude(id=curr_user.id)
    
class UserByProfessorView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(role='prof')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"message": "Korisnik ne postoji"},
            )


    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"message": "Korisnik je uspješno uređen"},
            )
        else:
            return Response(
                {"message": "Greška prilikom uređivanja", "errors": serializer.errors},
            )

    
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Korisnik uspješno izbrisan"}
            )
        except Exception as e:
            return Response(
                {"message": "Greška prilikom brisanja korisnika"}
            )       


class UserOrganizationView(generics.ListCreateAPIView):
    serializer_class = UserOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_pk']
        user = User.objects.get(pk=user_id)
        return UserOrganization.objects.filter(user_id=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            user_id = self.kwargs['user_pk']
            user = User.objects.get(pk=user_id)
            serializer.save(user_id=user)
        else:
            print(serializer.errors)

class UserOrganizationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_pk']
        return UserOrganization.objects.filter(user_id=user_id)
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Organizacija uspješno izbrisan"}
            )
        except Exception as e:
            return Response(
                {"message": "Greška prilikom brisanja organizacije"}
            )
        

class OrganizationView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.annotate(numb_of_users=Count('userorganization'))

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Organizacija je uspješno kreirana"},
            )
        else:
            return Response(
                {"message": "Greška prilikom kreiranja organizacije"}
            )
        
class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"message": "Organizacija ne postoji"},
            )


    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"message": "Organizacija je uspješno uređen"},
            )
        else:
            return Response(
                {"message": "Greška prilikom uređivanja organizacije"},
            )

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Organizacija uspješno izbrisan"}
            )
        except Exception as e:
            return Response(
                {"message": "Greška prilikom brisanja organizacije"}
            )  


class OrganizationUserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_id = self.kwargs['org_id']
        user_by_organization = UserOrganization.objects.filter(organization_id=organization_id)

        user_ids = user_by_organization.values_list('user_id', flat=True)

        users = User.objects.filter(id__in=user_ids)
        return users
        

class WorkshopView(generics.ListCreateAPIView):
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workshop.objects.annotate(numb_of_users=Count('loginworkshop')).select_related('user_id')

class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"message": "Radionica ne postoji"},
            )
        
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"message": "Radionica je uspješno uređen"},
            )
        else:
            return Response(
                {"message": "Greška prilikom uređivanja radionice"},
            )

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Radionica uspješno izbrisan"}
            )
        except Exception as e:
            return Response(
                {"message": "Greška prilikom brisanja radionice"}
            )


class LoginWorkshopView(generics.ListCreateAPIView):
    serializer_class = LoginWorkshopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workshop_id = self.kwargs['workshop_pk']
        workshop = Workshop.objects.get(pk=workshop_id)
        return LoginWorkshop.objects.filter(workshop_id=workshop)
    

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            workshop_id = self.kwargs['workshop_pk']
            workshop = Workshop.objects.get(pk=workshop_id)
            is_in = LoginWorkshop.objects.filter(user_id=user, workshop_id=workshop)
            if not is_in:
                serializer.save(workshop_id=workshop,user_id=user)
        else:
            print(serializer.errors)

class LoginWorkshopDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = LoginWorkshopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workshop_id = self.kwargs['workshop_pk']
        return LoginWorkshop.objects.filter(workshop_id=workshop_id)
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Korisnik uspješno izbrisan iz radionice"}
            )
        except Exception as e:
            return Response(
                {"message": "Greška prilikom brisanja korisnika iz radionice"}
            )


class ProfessorWorkshopView(generics.ListCreateAPIView):
    serializer_class = ProfessorWorkshopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Workshop.objects.filter(user_id=user).annotate(numb_of_users=Count('loginworkshop'))
    

class StudentWorkShopView(generics.ListAPIView):
    serializer_class = StudentWorkshopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return LoginWorkshop.objects.filter(user_id=user).select_related('workshop_id')
    
class StudentNotInWorkshopView(generics.ListAPIView):
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        student_workshop = LoginWorkshop.objects.filter(user_id=user).values_list('workshop_id', flat=True)
        return Workshop.objects.exclude(id__in=student_workshop).annotate(numb_of_users=Count('loginworkshop'))
    
class StudentProfessorView(generics.ListAPIView):
    serializer_class = StudentProfessorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(role='prof').prefetch_related('userorganization_set')
    

class ProfileUserView(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return User.objects.filter(id=user.id)