from django.shortcuts import render, redirect
from student.forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from student.models import Question, Exam, Student_Exam, Answer, Student_Answer, E_Skill
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

# Create your views here.
def index(request):
        return render(request, 'student/index.html')

@login_required
def special (request):
    return HttpResponse("You are logged in, NICE")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                if user.is_superuser:
                    return redirect('admin:index')
                return redirect('student:exams')

            else:
                return HttpResponse("Account Not Active")
        else:
            print("someone tried to login and faild")
            print("username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")

    else:
        login_form = LoginForm()
        return render(request,'student/login.html', {'login_form':LoginForm})

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            context = {'login_form': LoginForm}
            return render(request,'student/login.html', context)
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'student/registration.html', {'user_form':user_form,'registered':registered})

def exams(request):
    if request.user.is_authenticated:
        username = request.user.username
        exams = Exam.objects.all()
        return render(request,'student/exams.html', {'exams':exams, 'username':username})
    else:
        return HttpResponse("<h1> Login First </h1>")

def ready(request, exam_id):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            return redirect('student:questions', exam_id)
        else:
            exam = Exam.objects.get(id=exam_id)
            try:
                has_finish_exam = Student_Exam.objects.filter(student_name = username, exam__id = exam_id).get()
                #return HttpResponse(has_finish_exam)
                if has_finish_exam.has_finish:
                    return redirect('student:finish', exam_id)
                else:
                    new_student_exam = Student_Exam.objects.filter(student_name=username, exam=exam).update(total_mark=0)

            except Student_Exam.DoesNotExist:
                new_student_exam = Student_Exam.objects.create(student_name = username, exam = exam, total_mark = 0)

            context = { 'exam':exam }
            return render(request, 'student/get_ready.html',context)
    else:
        return HttpResponse("<h1> Login First </h1>")

def questions(request, exam_id):
    if request.user.is_authenticated:
        username = request.user.username



        questions = []
        skills = E_Skill.objects.filter(exam__id=exam_id).prefetch_related('question_set').all()
        question = ''
        for skill in skills:
            questions += Question.objects.filter(skill__pk=skill.pk)[:int(skill.ratio)]
            #questions[skill.skill.name] = question
        #return HttpResponse(questions)
        #questions = tuple(questions)

        #questions = Question.objects.filter(exam_id=exam_id)
        answers = Answer.objects.filter(question__exam_id=exam_id)
        exam_name = questions[0].exam.name
        #paginator
        paginator = Paginator(questions, 1)
        page = request.GET.get('page')
        all_questions = paginator.get_page(page)
        context = {'questions': all_questions, 'answers':answers, 'username': username, 'exam_id': exam_id, 'exam_name': exam_name}
        return render(request, 'student/questions.html', context)

    else:
        return HttpResponse("<h1> Login First </h1>")

def finish(request, exam_id):
    if request.method == 'POST':
        exam = request.POST.get('exam', None)
    elif request.method == 'GET':
        exam = exam_id
    username = request.user.username

    student_exam = Student_Exam.objects.get(student_name=username, exam__id=exam)
    student_answers = Student_Answer.objects.filter(student_exam=student_exam)
    correct_answers = []
    questions_ids = []
    for answer in student_answers:
        questions_ids.append(answer.question.id)
        if answer.student_answer.is_correct:
            correct_answers.append(answer.student_answer)

    mark = (len(correct_answers)*100)/len(student_answers)

    finish_exam = Student_Exam.objects.filter(student_name=username, exam__id=exam).update(total_mark=mark, has_finish = True)
    is_pass = mark >= student_exam.exam.success_score
    all_answers = Answer.objects.filter(question__in=questions_ids)
    #return HttpResponse(all_answers)

    context = {'username' : username , 'student_answers':student_answers, 'all_answers':all_answers,'mark': int(mark), 'is_pass':is_pass, 'exam_name':student_exam.exam.name}
    return render(request, 'student/finish.html', context)




@csrf_exempt
def save_answers(request):
    if request.method == 'POST':
        exam = request.POST.get('exam', None)
        question = request.POST.get('question', None)
        answer = request.POST.get('answer', None)
        username = request.user.username

        student_question = Question.objects.get(id = question)
        student_answer = Answer.objects.get(title = answer)
        student_exam = Student_Exam.objects.get(student_name = username, exam__id = exam)
        skill = E_Skill.objects.get(id=1)

        try:
            st_answer = Student_Answer.objects.get(question = student_question, student_exam= student_exam)
            if answer != st_answer.student_answer:
                new_answer = Student_Answer.objects.filter(question= student_question, student_exam= student_exam, skill = skill).update(student_answer = student_answer)

        except Student_Answer.DoesNotExist:
            st_answer = None
            create_student_answer = Student_Answer.objects.create(
                question = student_question, student_answer = student_answer, student_exam = student_exam,skill = skill
            )

        return HttpResponse(username)
    elif request.method == 'GET':
        exam = request.GET.get('exam', None)
        question = request.GET.get('question', None)
        username = request.user.username

        student_question = Question.objects.get(id=question)
        student_exam = Student_Exam.objects.get(student_name=username, exam__id=exam)
        skill = E_Skill.objects.get(id=1)

        get_answer = Student_Answer.objects.filter(question=student_question, student_exam__exam__id = exam, student_exam__student_name=username, skill=skill)

        #print(exam)
        #print(question)
        #print(username)
        #print(get_answer)

        #context = { 'get_answer':get_answer[0].student_answer }
        print(get_answer[0].student_answer.title)
        data = {
            'answer_id': get_answer[0].student_answer.id,
            'answer_title' : get_answer[0].student_answer.title,
        }

        #print(get_answer[0].student_answer)
        #return HttpResponse(data)

        return JsonResponse(data, safe=False ,content_type='application/json')
        # return render(request, 'student/questions.html', context)
