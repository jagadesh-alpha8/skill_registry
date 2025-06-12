from django.core.management.base import BaseCommand
import pandas as pd
from skillapp.models import Year, CollegeType, College, Department, Course, TrainingProvider, CandidateProfile

class Command(BaseCommand):
    help = 'Import candidate data from an Excel file'

    def handle(self, *args, **kwargs):
        # Update this path to your actual file path if needed
        file_path = 'candidates.xlsx'

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error reading file: {e}"))
            return

        count = 0

        for _, row in df.iterrows():
            year, _ = Year.objects.get_or_create(name=row['Year'])
            college_type, _ = CollegeType.objects.get_or_create(type_name=row['College Type'])
            college, _ = College.objects.get_or_create(college_name=row['College Name'])
            department, _ = Department.objects.get_or_create(dept_name=row['Department'])
            course, _ = Course.objects.get_or_create(course_name=row['Course'])
            tp, _ = TrainingProvider.objects.get_or_create(tp_name=row['Training Provider'])

            CandidateProfile.objects.create(
                name=row['Name'],
                mobile_number=str(row['Mobile Number']),
                email=row['Email'],
                register_number=row['Register Number'],
                profile_link=row.get('Profile Link', ''),
                year=year,
                college_type=college_type,
                college_name=college,
                department=department,
                course=course,
                tp=tp
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} candidate profiles successfully."))
