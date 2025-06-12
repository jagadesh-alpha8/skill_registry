from django.contrib import admin
from .models import Year, CollegeType, Department, Course, TrainingProvider, CandidateProfile

admin.site.register(Year)
admin.site.register(CollegeType)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(TrainingProvider)
admin.site.register(CandidateProfile)


