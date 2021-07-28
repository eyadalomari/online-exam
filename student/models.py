from django.db import models

# Create your models here.

class Exam(models.Model):
    class Meta():
        verbose_name_plural = 'Exams'
    name = models.CharField(blank = False, max_length = 1000)
    status = models.BooleanField(default=True)
    number_of_questions = models.IntegerField(blank = False)
    success_score = models.IntegerField()

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(blank=False, max_length=1000)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class E_Skill(models.Model):
    class Meta():
        verbose_name_plural = 'Exam_Skills'
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    ratio = models.PositiveIntegerField()

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.skill.name



class Question_Type(models.Model):
    name = models.CharField(blank=False, max_length=1000)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.TextField(blank = False, max_length = 2000)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    skill = models.ForeignKey(E_Skill, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    media = models.ImageField(blank=True, upload_to="question/")
    type = models.ForeignKey(Question_Type, on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.TextField(blank = False, max_length = 2000)
    is_correct = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " - " + str(self.is_correct)


class Student_Exam(models.Model):
    #must set on login to exam
    student_name = models.CharField(max_length=200)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    #total mark must set on finish button
    total_mark = models.IntegerField()
    has_finish = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "name: "+self.student_name + ", Exam: " + str(self.exam) + ", mark: " + str(self.total_mark)


class Student_Answer(models.Model):
    #these fileds must set on click on any radio button
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    student_exam = models.ForeignKey(Student_Exam, on_delete=models.CASCADE)
    skill = models.ForeignKey(E_Skill, on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  str(self.student_exam) + ",   answer mark = " + str(self.student_answer)

