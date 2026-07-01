from django.core.management.base import BaseCommand
from applications.models import ApplicationStatus, Skill


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Create Application Statuses
        statuses = [
            {'name': 'Applied', 'description': 'Application has been submitted'},
            {'name': 'Under Review', 'description': 'Application is being reviewed by HR'},
            {'name': 'Screening', 'description': 'Initial screening process'},
            {'name': 'Interview', 'description': 'Interview stage'},
            {'name': 'Technical Test', 'description': 'Technical assessment stage'},
            {'name': 'Offer', 'description': 'Job offer extended'},
            {'name': 'Rejected', 'description': 'Application rejected'},
            {'name': 'Withdrawn', 'description': 'Application withdrawn by applicant'},
        ]

        for status_data in statuses:
            status, created = ApplicationStatus.objects.get_or_create(
                name=status_data['name'],
                defaults={'description': status_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created status: {status.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Status already exists: {status.name}'))

        # Create Skills
        skills = [
            {'name': 'Python', 'category': 'technical', 'description': 'Python programming language'},
            {'name': 'Django', 'category': 'technical', 'description': 'Django web framework'},
            {'name': 'JavaScript', 'category': 'technical', 'description': 'JavaScript programming language'},
            {'name': 'React', 'category': 'technical', 'description': 'React JavaScript library'},
            {'name': 'SQL', 'category': 'technical', 'description': 'SQL database querying'},
            {'name': 'Communication', 'category': 'soft_skill', 'description': 'Effective communication skills'},
            {'name': 'Teamwork', 'category': 'soft_skill', 'description': 'Collaboration and teamwork'},
            {'name': 'Problem Solving', 'category': 'soft_skill', 'description': 'Analytical problem solving'},
            {'name': 'English', 'category': 'language', 'description': 'English language proficiency'},
            {'name': 'Git', 'category': 'tool', 'description': 'Version control with Git'},
            {'name': 'Docker', 'category': 'tool', 'description': 'Containerization with Docker'},
            {'name': 'AWS', 'category': 'tool', 'description': 'Amazon Web Services'},
        ]

        for skill_data in skills:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults={
                    'category': skill_data['category'],
                    'description': skill_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created skill: {skill.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skill already exists: {skill.name}'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
