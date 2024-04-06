from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from .permission import AdminOrStaffPermission
from .models import *
from .serializer import *
from .filters import TeacherFilter

# Create your views here.


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin", "staff"]:
            subjects = Subject.objects.all()
            subject_count = Subject.objects.count()

            serializer = SubjectListSerializer({
                'subject_count': subject_count,
                'subjects': subjects
            })
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view subjects.")
        
    def retrieve(self, request, *args, **kwargs):
        subject = self.get_object()
        if request.user.role in ["admin", "staff"]:
            serializer = SubjectSerializer(subject)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You are not allowed to view this object.")

    def create(self, request, *args, **kwargs):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        subject = self.get_object()

        try:
            # Trigger pre_delete signal to check association with teachers
            # protect_subject_delete(sender=Subject, instance=subject)

            if request.user.role == "admin":
                subject.delete()
                return Response({'response': 'Subject deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        subjetct = self.get_object()
        serializer = SubjectSerializer(subjetct, data=request.data)
        if serializer.is_valid():
            if request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin", "staff"]:
            queryset = Grade.objects.all()
            serializer = GradeSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view subjects.")
        
    def retrieve(self, request, *args, **kwargs):
        grade = self.get_object()
        if request.user.role in ["admin", "staff"]:
            serializer = GradeSerializer(grade)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You are not allowed to view this object.")

    def create(self, request, *args, **kwargs):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        grade = self.get_object()

        if request.user.role == "admin":
            try:
                grade.delete()
                return Response({'response': 'Grade deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            except ValidationError as e:
                return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You are not allowed to delete this object.")
        
    def update(self, request, *args, **kwargs):
        grade = self.get_object()
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            if request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemunerationListCreateView(generics.ListCreateAPIView):
    queryset = Remuneration.objects.all()
    serializer_class = RemunerationSerializer
    permission_classes = [permissions.IsAuthenticated, AdminOrStaffPermission]

class RemunerationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Remuneration.objects.all()
    serializer_class = RemunerationSerializer
    permission_classes = [permissions.IsAuthenticated, AdminOrStaffPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Remuneration successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50  # Set the desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100


class TeacherViewSet(ModelViewSet):
    queryset = Teachers.objects.prefetch_related('subject').all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['subject', 'experience', 'english_fluency']
    filterset_class = TeacherFilter
    search_fields = ["teacher_name","roll_no"]

    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin", "staff"]:
            queryset = Teachers.objects.all()
        else:
            raise PermissionDenied("You are not allowed to view teacher.")

        queryset = self.filter_queryset(queryset)
        total_count = queryset.count()

        # Serialize the queryset
        serializer = SimpleTeacherSerializer(queryset, many=True)

        # Sort results based on total_rating after serialization
        sorted_data = sorted(serializer.data, key=lambda x: x['total_rating'], reverse=True)

        # Get the requested page number from the query parameter
        page_number = request.query_params.get('page', 1)

        # Create a Paginator instance with the page size
        paginator = Paginator(sorted_data, self.pagination_class.page_size)

        try:
            # Try to get the requested page, or return an empty list if invalid
            page = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            return Response({
                'total_count': total_count,
                'total_pages': paginator.num_pages,
                'page_size': self.pagination_class.page_size,
                'current_page': 0,  # Indicate that it's an empty page
                'results': [],
            })

        # Include pagination information in the response
        response_data = {
            'total_count': total_count,
            'total_pages': paginator.num_pages,
            'page_size': self.pagination_class.page_size,
            'current_page': page.number,
            'results': page.object_list,  # Use the paginated results
        }

        return Response(response_data)
    # def list(self, request, *args, **kwargs):
    #     if request.user.role in ["admin", "staff"]:
    #         queryset = Teachers.objects.all()
    #         queryset = self.filter_queryset(queryset)
            
            
    #         ordering_param = self.request.query_params.get('ordering', 'total_rating')
    #         total_count = queryset.count()
    #         if ordering_param == 'total_rating':
    #             serializer = SimpleTeacherSerializer(queryset, many=True)

    #             sorted_data = sorted(serializer.data, key=lambda x: x['total_rating'], reverse=True)
    #             response_data = {
    #             'total_count': total_count,
    #             'teachers': sorted_data
    #         }
    #             return Response(response_data)
            
    #         serializer = SimpleTeacherSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     else:
    #         raise PermissionDenied("You are not allowed to view subjects.")


        
    def create(self, request, *args, **kwargs):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, *args, **kwargs):
        teacher = self.get_object()
        if request.user.role == "admin":
            teacher.delete()
            return Response({'response': 'teacher deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You are not allowed to delete this object.")
        
    def update(self, request, *args, **kwargs):
        teacher = self.get_object()
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        
        if serializer.is_valid():
            if request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, *args, **kwargs):
        teacher = self.get_object()
        if request.user.role in ["admin", "staff"]:
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You are not allowed to view this object.")
