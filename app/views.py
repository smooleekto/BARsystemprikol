from django.shortcuts import render
from .forms import CustomThemeForm, ThemeChooseForm, TeacherRegisterForm, StudentRegisterForm, LoginForm, UpdateTeachersInfoForm, AddThemeForm
from .models import Teachers, Students, TeachersThemes, Departaments
from django.views import View
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
import re
from django.forms.utils import ErrorList


# Create your views here.
def home(request):
    teachers = Teachers.objects.all()
    students = Students.objects.all()
    teachers_update = UpdateTeachersInfoForm
    add_theme = AddThemeForm
    theme_choose = ThemeChooseForm
    themes = TeachersThemes.objects.all()
    customtheme = CustomThemeForm
    countstudents = [[item.user_id] for item in teachers]
    allthemes = [item.theme for item in students]
    for item in countstudents:
        item.append(len(students.filter(teacher=item[0])))  
    data = {'customtheme': customtheme, 'teachers': teachers, 'themes':themes, 'teachers_update': teachers_update, 'add_theme':add_theme, 'students':students, 'theme_choose':theme_choose,  'countstudents': countstudents, 'allthemes':allthemes}
    
    if request.method == 'POST' and 'btn-teachers-update' in request.POST:
        teachers_update = UpdateTeachersInfoForm(request.POST)
        if teachers_update.is_valid():
            updatefname = teachers_update.cleaned_data['first_name']
            updatelname = teachers_update.cleaned_data['last_name']
            updateptr = teachers_update.cleaned_data['patronymic']
            updatequant = teachers_update.cleaned_data['quantity']
            updatestdtheme = teachers_update.cleaned_data['student_theme']
            print(updatequant)
            if updatefname != '':
                Teachers.objects.filter(user_id=request.user.id).update(first_name=updatefname)
            if updatelname != '':
                Teachers.objects.filter(user_id=request.user.id).update(last_name=updatelname)
            if updateptr != '':
                Teachers.objects.filter(user_id=request.user.id).update(patronymic=updateptr)
            Teachers.objects.filter(user_id=request.user.id).update(quantity=updatequant)
            if updatestdtheme == True and 'Тема на вибір студента' not in [TeachersThemes.objects.filter(teacher_id=request.user.id)[i].theme for i in range(len(TeachersThemes.objects.filter(teacher_id=request.user.id)))]:
                themes_table = TeachersThemes()
                themes_table.theme = 'Тема на вибір студента'
                user = Teachers.objects.filter(user_id=request.user.id)[0]
                themes_table.teacher = user
                themes_table.save()
            elif updatestdtheme == True and 'Тема на вибір студента' in [TeachersThemes.objects.filter(teacher_id=request.user.id)[i].theme for i in range(len(TeachersThemes.objects.filter(teacher_id=request.user.id)))]:
                pass
            else:
                TeachersThemes.objects.filter(teacher_id=request.user.id, theme='Тема на вибір студента').delete()
            return redirect(to='/')
        
    if request.method == 'POST' and 'btn-add-theme' in request.POST:
        add_theme = AddThemeForm(request.POST)
        if add_theme.is_valid():
            themes = TeachersThemes()
            themes.theme = add_theme.cleaned_data['theme']
            themes.teacher_id = request.user.id
            themes.save()
    if request.method == 'POST' and 'delete-theme-teacher' in request.POST:
        student = Students.objects.filter(user_id=request.user.id)
        student.update(theme='')
        teacher = Teachers.objects.filter(user_id=199999)
        student.update(teacher=teacher[0])
        return redirect(to='/')
    if request.method == 'POST' and 'btn-choose-theme' in request.POST:
        choose_theme = ThemeChooseForm(request.POST)
        if choose_theme.is_valid():
            student = Students.objects.filter(user_id=request.user.id)
            theme = choose_theme.cleaned_data['theme'].theme
            teacher = choose_theme.cleaned_data['teacher']
            student.update(theme=theme)
            student.update(teacher=teacher)
        return redirect(to='/')
    if request.method == 'POST' and 'btn-choose-customtheme' in request.POST:
        choose_theme = CustomThemeForm(request.POST)
        if choose_theme.is_valid():
            student = Students.objects.filter(user_id=request.user.id)
            theme = choose_theme.cleaned_data['theme']
            student.update(theme=theme)
        return redirect(to='/')
    if request.method == 'POST' and 'teachers-name-sort-up' in request.POST:
        sortteachers = Teachers.objects.all()
        sortteachers = sortteachers.order_by('last_name')
        data['teachers'] = sortteachers
    if request.method == 'POST' and 'teachers-name-sort-down' in request.POST:
        sortteachers = Teachers.objects.all()
        sortteachers = sortteachers.order_by('-last_name')
        data['teachers'] = sortteachers
    if request.method == 'POST' and 'teachers-quantity-sort-up' in request.POST:
        sortteachers = Teachers.objects.all()
        sortteachers = sortteachers.order_by('quantity')
        data['teachers'] = sortteachers
    if request.method == 'POST' and 'teachers-quantity-sort-down' in request.POST:
        sortteachers = Teachers.objects.all()
        sortteachers = sortteachers.order_by('-quantity')
        data['teachers'] = sortteachers
    if request.method == 'POST' and 'students-name-sort-up' in request.POST:
        sortstudents = Students.objects.all()
        sortstudents = sortstudents.order_by('last_name', 'group')
        data['students'] = sortstudents
    if request.method == 'POST' and 'students-name-sort-down' in request.POST:
        sortstudents = Students.objects.all()
        sortstudents = sortstudents.order_by('-last_name', '-group')
        data['students'] = sortstudents
        

    return render(request, 'app/home.html', data)


class TeacherRegisterView(View):
    form_class = TeacherRegisterForm
    initial = {'key': 'value'}
    template_name = 'app/teacher_register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(TeacherRegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            teachers_table = Teachers()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            lastname = form.cleaned_data.get('last_name')
            user_id = user.id
            firstname = form.cleaned_data.get('first_name')
            patronymic = form.cleaned_data.get('patronymic')
            departament = form.cleaned_data.get('departament')
            teachers_table.departament = departament
            teachers_table.last_name = lastname
            teachers_table.first_name = firstname
            teachers_table.patronymic = patronymic
            teachers_table.user_id = user_id
            teachers_table.save()
            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class StudentRegisterView(View):
    form_class = StudentRegisterForm
    initial = {'key': 'value'}
    template_name = 'app/student_register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(StudentRegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid() and re.match('^([A-Z][A-Z]-\d\d)$', form.cleaned_data.get('group')):
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            students_table = Students()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            lastname = form.cleaned_data.get('last_name')
            group = form.cleaned_data.get('group')
            user_id = user.id
            firstname = form.cleaned_data.get('first_name')
            patronymic = form.cleaned_data.get('patronymic')
            students_table.last_name = lastname
            students_table.first_name = firstname
            students_table.patronymic = patronymic
            students_table.group = group
            students_table.user_id = user_id
            students_table.save()
            return redirect(to='login')
        elif re.match(form.cleaned_data['group'], '^([A-Z][A-Z]-\d\d)$') == None:
            form.errors['GroupError'] = 'Неправильний код групи. Приклад: КМ-03'

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


def themedelete(request, theme):
    theme = TeachersThemes.objects.get(theme=theme)
    theme.delete()
    student = Students.objects.filter(theme=theme)
    student.update(theme='')
    return redirect('/')

def teacher_profile(request, user_id):
    teacher = Teachers.objects.filter(user_id=user_id)[0]
    teachers = Teachers.objects.all()
    students = Students.objects.all()
    countstudents = [[item.user_id] for item in teachers]
    for item in countstudents:
        item.append(len(students.filter(teacher=item[0])))  
    data = {'teacher': teacher, 'teachers': teachers, 'students':students, 'countstudents': countstudents}
    return render(request, 'app/teacher_profile.html', data)


def theme_accept(request, user_id):
    student = Students.objects.filter(user_id = user_id)
    student.update(theme_status='Тему затверджено')
    teacher_id = student[0].teacher.user_id
    return redirect(f'/teacher/{teacher_id}')


def theme_decline(request, user_id):
    student = Students.objects.filter(user_id=user_id)
    teacher_id = student[0].teacher.user_id
    student.update(theme_status='Тему відхилено')
    return redirect(f'/teacher/{teacher_id}')


def load_ajax(request):
    teacher = request.GET.get('teacher')
    teacherthemes = TeachersThemes.objects.filter(teacher=teacher).order_by('theme')
    students = Students.objects.all()
    studentsthemes = [item.theme for item in students]
    return render(request, 'app/load_ajax.html', {'teacherthemes': teacherthemes, 'studentsthemes':studentsthemes})