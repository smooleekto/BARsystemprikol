from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Teachers, TeachersThemes, Students, Departaments


class TeacherRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=15,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Ім\'я',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=15,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Прізвище',
                                                              'class': 'form-control',
                                                              }))
    patronymic = forms.CharField(max_length=15,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'По батькові',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=15,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Юзернейм',
                                                             'class': 'form-control',
                                                             }))
    password1 = forms.CharField(max_length=20,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=20,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Підтвердження паролю',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    departament = forms.ModelChoiceField(queryset=Departaments.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'username', 'password1', 'password2']


class StudentRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=15,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Ім\'я',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=15,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Прізвище',
                                                              'class': 'form-control',
                                                              }))
    patronymic = forms.CharField(max_length=15,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'По батькові',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=15,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Юзернейм',
                                                             'class': 'form-control',
                                                             }))
    group = forms.CharField(max_length=5, 
                            required=True, 
                            widget=forms.TextInput(attrs={'placeholder': 'Група',
                                                             'class': 'form-control',
                                                             }))
    password1 = forms.CharField(max_length=20,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=20,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Підтвердження паролю',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name','patronymic', 'group', 'username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=15,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Юзернейм',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=20,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateTeachersInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}))
    last_name = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}))
    patronymic = forms.CharField(max_length=15, required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'По батькові'}))
    quantity = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кількість студентів'}))
    student_theme = forms.BooleanField(required=False)
    class Meta:
        model = Teachers
        fields = ['first_name', 'last_name', 'patronymic', 'quantity', 'student_theme']


class AddThemeForm(forms.ModelForm):
    theme = forms.CharField(max_length=60, required=False, widget=forms.TextInput(attrs={'class': 'form-control__add-theme', 'placeholder': 'Напишіть тему'}))
    class Meta:
        model = TeachersThemes
        fields = ['theme']


class ThemeChooseForm(forms.ModelForm):
    class Meta:
        model = TeachersThemes
        fields = ('teacher', 'theme')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_teachers = Teachers.objects.all().exclude(user_id=199999)
        students = Students.objects.all()
        countstudents = [[item.user_id] for item in all_teachers]
        for item in countstudents:
            item.append(len(students.filter(teacher=item[0])))
        for item in countstudents: 
            if all_teachers.filter(user_id=item[0])[0].quantity == item[1]:
                all_teachers = all_teachers.exclude(user_id=item[0])
        self.fields['teacher'].queryset = all_teachers
        self.fields['teacher'].initial = 'QWE'
        self.fields['theme'] = forms.ModelChoiceField(queryset = TeachersThemes.objects.none())
        if 'teacher' in self.data:
            try:
                teacher = int(self.data.get('teacher'))
                self.fields['theme'].queryset = TeachersThemes.objects.filter(teacher=teacher).order_by('theme')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['theme'].queryset = self.instance.teacher.theme_set.order_by('theme')


class CustomThemeForm(forms.ModelForm):
    theme = forms.CharField(max_length=60, required=True)
    
    class Meta:
        model = Students
        fields = ['theme']