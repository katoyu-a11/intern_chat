from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ImageForm, LoginForm, SignUpForm,TalkForm,UsernameForm,MailForm,PasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,PasswordChangeView,LogoutView
from .models import ImageModel
from .models import TalkModel
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


def class_view_decorator(function_decorator):
    
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


@login_required
def home(request):
    return render(request, 'myapp/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        imageform = ImageForm(request.POST, request.FILES)
        if form.is_valid() and imageform.is_valid():
            user = form.save()
            imageform.instance.image_user = user
            imageform.save()
        return redirect('index')
    else:
        imageform = ImageForm()
        form = SignUpForm()
        return render(request, 'myapp/signup.html', {'form': form, 'imageform' : imageform})


def index(request):

    return render(request, "myapp/index.html")


class login_view(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"
account_login = login_view.as_view()

@login_required
def friends(request):
    login_user = request.user
    data = User.objects.exclude(id = login_user.id)
    image = ImageModel.objects.all()
    params = {'data':data,'image':image,'login_user':login_user}
    return render(request, 'myapp/friends.html', params)

@login_required
def talk_room(request,user_id,friend_id):
    user = User.objects.get(id = user_id)
    friend = User.objects.get(id = friend_id)
    talk = TalkModel.objects.filter(Q(sender = user,talkname = friend)|Q(sender = friend,talkname = user)).order_by('pub_date')
    talkform = TalkForm()
    params = {'friend':friend,'talk':talk,'form':talkform}
    
    if request.method == 'POST':
        talkform = TalkForm(request.POST)
        if talkform.is_valid:
            talkform.instance.sender = user
            talkform.instance.talkname = friend
            talkform.save()
        return redirect('talk_room',user_id,friend_id)

    return render(request,'myapp/talk_room.html',params)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def username_change(request):
    user = request.user
    obj = User.objects.get(id= user.id)
    form = UsernameForm()
    if request.method == 'POST':
        username = UsernameForm(request.POST,instance = obj)
        if username.is_valid:
            username.save()
            return render(request,'myapp/change_complete.html',{'item':'ユーザー名'})
    
    return render(request,'myapp/change.html',{'item':'ユーザー名','form':form})

@login_required
def mail_change(request):
    user = request.user
    obj = User.objects.get(id= user.id)
    form = MailForm()
    if request.method == 'POST':
        email = MailForm(request.POST,instance = obj)
        if email.is_valid:
            email.save()
            return render(request,'myapp/change_complete.html',{'item':'メールアドレス'})
    
    return render(request,'myapp/change.html',{'item':'メールアドレス','form':form})
    

@login_required
def icon_change(request):
    user = request.user
    obj = ImageModel.objects.get(image_user = user)
    if request.method == 'POST':
        imageform = ImageForm(request.POST, request.FILES,instance = obj)
        if imageform.is_valid():
            imageform.save()
        return render(request,'myapp/change_complete.html',{'item':'アイコン'})
    else:
        imageform = ImageForm()
        return render(request, 'myapp/icon_change.html', {'form': imageform})


@class_view_decorator(login_required)
class password_change(PasswordChangeView):
    form_class = PasswordForm
    template_name = 'myapp/password_change.html'
    success_url = reverse_lazy('setting')


@class_view_decorator(login_required)
class logout_view(LoginRequiredMixin,LogoutView):
    template_name = 'myapp/index.html'