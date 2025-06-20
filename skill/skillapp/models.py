from django.db import models
# Lookup Tables
class Year(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    
class CollegeType(models.Model):
    type_name = models.CharField(max_length=100)
    def __str__(self):
        return self.type_name


class College(models.Model):
    college_name = models.CharField(max_length=255)
    def __str__(self):
        return self.college_name

class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    def __str__(self):
        return self.dept_name

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    def __str__(self):
        return self.course_name

class TrainingProvider(models.Model):
    tp_name = models.CharField(max_length=200)
    def __str__(self):
        return self.tp_name

class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Main Candidate Profile Table

class CandidateProfile(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    register_number = models.CharField(max_length=100)
    profile_link = models.URLField(blank=True)

    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    college_type = models.ForeignKey(CollegeType, on_delete=models.SET_NULL, null=True)
    college_name = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    tp = models.ForeignKey(TrainingProvider, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"{self.name} ({self.register_number})"


