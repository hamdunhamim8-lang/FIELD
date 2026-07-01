from django.contrib import admin
from .models import (
    JobPosting, Applicant, ApplicationStatus, Application,
    Interview, Document, Skill, JobPostingSkill, ApplicantSkill
)

# Register your models here.

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'employment_type', 'status', 'location', 'posted_date', 'deadline']
    list_filter = ['status', 'employment_type', 'posted_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'posted_date'


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'city', 'country', 'created_at']
    list_filter = ['city', 'country', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'created_at'


@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job_posting', 'status', 'applied_date', 'updated_at']
    list_filter = ['status', 'applied_date']
    search_fields = ['applicant__first_name', 'applicant__last_name', 'job_posting__title']
    date_hierarchy = 'applied_date'
    raw_id_fields = ['applicant', 'job_posting', 'status']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'interview_type', 'scheduled_date', 'status', 'interviewer_name']
    list_filter = ['interview_type', 'status', 'scheduled_date']
    search_fields = ['application__applicant__first_name', 'application__job_posting__title', 'interviewer_name']
    date_hierarchy = 'scheduled_date'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'document_type', 'application', 'file_size', 'upload_date']
    list_filter = ['document_type', 'upload_date']
    search_fields = ['file_name', 'application__applicant__first_name', 'application__job_posting__title']
    date_hierarchy = 'upload_date'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name']


@admin.register(JobPostingSkill)
class JobPostingSkillAdmin(admin.ModelAdmin):
    list_display = ['job_posting', 'skill', 'proficiency_level']
    list_filter = ['proficiency_level', 'skill__category']
    search_fields = ['job_posting__title', 'skill__name']


@admin.register(ApplicantSkill)
class ApplicantSkillAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'skill', 'proficiency_level', 'years_experience']
    list_filter = ['proficiency_level', 'skill__category']
    search_fields = ['applicant__first_name', 'applicant__last_name', 'skill__name']
