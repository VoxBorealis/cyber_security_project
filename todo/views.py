from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, SearchForm, TaskForm
from .models import User, Task
from django.db import connection

@csrf_exempt
def index(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'attempting login - username: {username}, password: {password}')
        try:
            user = User.objects.get(username = username, password = password)
            request.session['user'] = {'id': user.id, 'username': user.username}
            
            print(f'logged in as: {user.username}')
            redirect("/")
        except:
            #show error message
            print("log in failed")
            pass
    
    context = {}
    context['login_form'] = RegisterForm
    context['task_form'] = TaskForm
    context['search_form'] = SearchForm
    if is_logged_in(request):
        tasks = Task.objects.all().filter(owner = request.session['user']['id'])
        context['tasks'] = tasks
    return render(request, 'todo/index.html', context)

def task(request, id):
    task = Task.objects.get(pk = id)
    return render(request, 'todo/task.html', {'task': task})

def is_logged_in(request):
    try:
        if request.session['user']:
            return True
    except: return False

def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/")

def count_tasks(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        query = (form['query'].value())
        with connection.cursor() as cursor:
            response = cursor.execute("SELECT id FROM todo_task WHERE task_text LIKE '%%%s%%'" % (query)).fetchall()
            print("Found entries:")
            for r in response:
                print(r[0])
            request.session['search'] = response
    return redirect("/")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/")

    context = {}
    context['register_form'] = RegisterForm
    return render(request, "todo/register.html", context)

def logout(request):
    request.session['user'] = None
    return redirect("/")
