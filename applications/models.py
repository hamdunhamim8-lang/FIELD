from django.db import models
from django.utils import timezone

# Create your models here.

class JobPosting(models.Model):
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('on_hold', 'On Hold'),
    ]
    
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    requirements = models.TextField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-posted_date']
    
    def __str__(self):
        return self.title


class Applicant(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True)
    portfolio_url = models.URLField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ApplicationStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Application(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applications')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    status = models.ForeignKey(ApplicationStatus, on_delete=models.SET_NULL, null=True, related_name='applications')
    cover_letter = models.TextField(blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ['applicant', 'job_posting']
    
    def __str__(self):
        return f"{self.applicant} - {self.job_posting.title}"


class Interview(models.Model):
    INTERVIEW_TYPES = [
        ('phone', 'Phone'),
        ('video', 'Video'),
        ('in_person', 'In-person'),
        ('technical', 'Technical'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interview_type = models.CharField(max_length=50, choices=INTERVIEW_TYPES)
    scheduled_date = models.DateTimeField(null=False)
    duration = models.IntegerField(blank=True, null=True, help_text='Duration in minutes')
    interviewer_name = models.CharField(max_length=100, blank=True)
    interviewer_email = models.EmailField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.application} - {self.interview_type} on {self.scheduled_date}"


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('resume', 'Resume'),
        ('cover_letter', 'Cover Letter'),
        ('portfolio', 'Portfolio'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file_name = models.CharField(max_length=255, null=False)
    file_path = models.CharField(max_length=500, null=False)
    file_size = models.IntegerField(blank=True, null=True, help_text='File size in bytes')
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.file_name} ({self.document_type})"


class Skill(models.Model):
    CATEGORIES = [
        ('technical', 'Technical'),
        ('soft_skill', 'Soft Skill'),
        ('language', 'Language'),
        ('tool', 'Tool'),
    ]
    
    name = models.CharField(max_length=100, unique=True, null=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class JobPostingSkill(models.Model):
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='job_posting_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='job_posting_skills')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, blank=True)
    
    class Meta:
        unique_together = ['job_posting', 'skill']
    
    def __str__(self):
        return f"{self.job_posting.title} - {self.skill.name} ({self.proficiency_level})"


class ApplicantSkill(models.Model):
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applicant_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='applicant_skills')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, blank=True)
    years_experience = models.IntegerField(blank=True, null=True)
    
    class Meta:
        unique_together = ['applicant', 'skill']
    
    def __str__(self):
        return f"{self.applicant} - {self.skill.name} ({self.proficiency_level})"
