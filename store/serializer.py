from rest_framework import serializers
from .models import Subject,Teachers,Grade,Remuneration

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]

class SubjectListSerializer(serializers.Serializer):
    subject_count = serializers.IntegerField()
    subjects = SubjectSerializer(many=True)


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "name"]

class RemunerationSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    grade_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Remuneration
        fields = ['id','teacher', 'grade','grade_name','min_remuneration', 'max_remuneration']

    def get_teacher(self, obj):
        teacher = obj.teacher
        return {
            "id": teacher.id,
            "teacher_name": teacher.teacher_name,
            
        }
    def get_grade_name(self, obj):
        grade = obj.grade
        return grade.name if grade else None
    
class TeacherSerializer(serializers.ModelSerializer):
    total_rating = serializers.SerializerMethodField()
    subject_name = serializers.StringRelatedField(source="subject", many=True, read_only=True)
    total_point = serializers.SerializerMethodField()
    remunerations = RemunerationSerializer(many=True)
    # remunerations_details = serializers.SerializerMethodField()

    class Meta:
        model = Teachers
        fields = [
            "id",
            "teacher_name",
            "roll_no",
            "subject",
            "subject_name",
            "whatsapp_no",
            "contact_no",
            "email",
            "experience",
            "date",
            "video_link",
            "bank_acc_holder_name",
            "bank_name",
            "account_no",
            "branch",
            "ifsc_code",
            "google_pay",
            "phone_pay",
            "about",
            "remark",
            "qualification",
            "success_demo",
            "failed_demo",
            "teacher_change",
            "total_point",
            "black_list",
            "active",
            "english_fluency",
            "interview_rating",
            "total_rating",
            "remunerations",
            # "remunerations_details"
        ]

    def create(self, validated_data):
        remuneration_data = validated_data.pop('remunerations', None)
        subject_data = validated_data.pop('subject', None)

        teacher = Teachers.objects.create(**validated_data)

        if subject_data:
            teacher.subject.set(subject_data)

        if remuneration_data:
            for remuneration_item in remuneration_data:
                grade_instance = remuneration_item.pop('grade', None)
                Remuneration.objects.create(teacher=teacher, grade=grade_instance, **remuneration_item)

        return teacher
    

    def update(self, instance, validated_data):
        remunerations_data = validated_data.pop('remunerations', None)
        validated_data.pop('date', None)
        # Update Teacher fields
        instance = super().update(instance, validated_data)

        # Update or create associated Remuneration objects
        if remunerations_data is not None:
            # If remunerations_data is provided, clear existing remunerations
            instance.remunerations.all().delete()

            for remuneration_data in remunerations_data:
                grade_instance = remuneration_data.pop('grade', None)

                # Retrieve or create grade_instance
                grade_instance_obj, _ = Grade.objects.get_or_create(name=grade_instance)

                # Create a new Remuneration instance
                Remuneration.objects.create(teacher=instance, grade=grade_instance_obj, **remuneration_data)

        return instance

    def get_total_rating(self, obj):

        experience_rating = obj.experience
        english_fluency_rating = obj.english_fluency
        interview_rating = obj.interview_rating

        if experience_rating >= 5:
            experience_rating_value = 5
        elif 4 <= experience_rating < 5:
            experience_rating_value = 4.5
        elif 3 <= experience_rating < 4:
            experience_rating_value = 4
        elif experience_rating < 3:
            experience_rating_value = 3
        else:
            experience_rating_value = 0

        rating_mapping = {
            '5+ Year': 5,
            '3+ Year': 4.5,
            '1+ Year': 4,
            '<1 Year': 3,
            '100%': 5,
            '90%': 4.5,
            '80%': 4,
            'Below 80%': 3,
        }

        total_rating = (
            experience_rating_value +
            rating_mapping.get(english_fluency_rating, 0) +
            rating_mapping.get(interview_rating, 0)
        ) / 3
        total_rating = round(total_rating, 1)
        return total_rating
    
    def get_total_point(self, obj):

        success_demo_point = obj.success_demo
        failed_demo_point = obj.failed_demo
        teacher_change_point = obj.teacher_change

 
        total_point = success_demo_point-failed_demo_point-teacher_change_point

        return total_point
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subject_name'] = [subject.name for subject in instance.subject.all()]
        return ret


class SimpleTeacherSerializer(serializers.ModelSerializer):
    total_rating = serializers.SerializerMethodField()

    class Meta:
        model = Teachers
        fields = [
            "id",
            "teacher_name",
            "roll_no",
            "black_list",
            "total_rating",
            "date",
            "about",
            
        ]

    def get_total_rating(self, obj):

        experience_rating = obj.experience
        english_fluency_rating = obj.english_fluency
        interview_rating = obj.interview_rating

        if experience_rating >= 5:
            experience_rating_value = 5
        elif 4 <= experience_rating < 5:
            experience_rating_value = 4.5
        elif 3 <= experience_rating < 4:
            experience_rating_value = 4
        elif experience_rating < 3:
            experience_rating_value = 3
        else:
            experience_rating_value = 0

        rating_mapping = {
            '5+ Year': 5,
            '3+ Year': 4.5,
            '1+ Year': 4,
            '<1 Year': 3,
            '100%': 5,
            '90%': 4.5,
            '80%': 4,
            'Below 80%': 3,
        }

        total_rating = (
            experience_rating_value +
            rating_mapping.get(english_fluency_rating, 0) +
            rating_mapping.get(interview_rating, 0)
        ) / 3
        total_rating = round(total_rating, 1)
        return total_rating
    
class SimpleTeacherListSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    teachers = SimpleTeacherSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data