#post-list-view with paginator-codes...
from taggit.models import Tag
from BlogApp.forms import *
# Create your views here.

# Create your views here.
from BlogApp.forms import postform
from django.http import HttpResponseRedirect
from BlogApp.forms import signupform
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
def home_page(request):
     return render(request,'BlogApp/home.html')

def postview(request):
    form = postform()

    print('welcome')
    if request.method=='POST':
          form = postform(request.POST,request.FILES)
          if form.is_valid():
              user =form.save(commit=True)
              return HttpResponseRedirect('/thank')
    return render(request,'BlogApp/postmain.html',{'form':form})


def logout_view(request):
      request.session.clear()
      return render(request,'Blogapp/logout.html')

def signupview(request):
    sent= False
    form = signupform()
    if request.method=='POST':
        form = signupform(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.set_password)
            user.save()
            sent=True
            return HttpResponseRedirect('/account/login/',{'sent':sent})
    else:
        form= signupform()
    return render(request,'BlogApp/signup.html',{'form':form,'sent':sent})








def post_list_view(request,tag_slug=None):
    print("post_list_view with paginator")
    post_list=Post.objects.all();
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 2)  # no.of.pages(20/2-rec=>10-pages)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'BlogApp/post_list.html', {"post_list": post_list, 'tag': tag})

def post_detail_view(request, year,month,day,post):
    post=get_object_or_404(Post,slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day);
    return render(request, "BlogApp/post_detail.html",{'post':post})


#post-list-view with paginator-codes...
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from BlogApp.models import Post
# Create your views here.
def post_list_view(request):
    post_list=Post.objects.all()
    paginator=Paginator(post_list,2)		#no.of.pages(20/2-rec=>10-pages)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'BlogApp/post_list.html',{"post_list":post_list})



#Listview with pagination
from django.views.generic import ListView
class PostListView(ListView):
    model=Post
    paginate_by=1

'''
from django.core.mail import send_mail
send_mail('Hello', 'Very imp msg....','renukapatangay1@gmail.com',['devipatangay@gmail.com','patangay7@gmail.com'])
'''

#views for email
from django.core.mail import send_mail
from BlogApp.forms import EmailSendForm
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id, status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],	post.title)
            message="Read Post At: \n{}\n\n{} 'Comments:\n{}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject, message, 'renukapatangay1@gmail.com', [cd['to']]) #use[]
            sent=True;
    else:
        form=EmailSendForm()
        return render(request,'BlogApp/sharebymail.html', {'post':post,'form':form,'sent':sent})




#bootstarp-sample.html-view
def bs_smaple_view(request):
    return render(request,"BlogApp/Sample.html")


#comment form-view
from BlogApp.models import Comment
from BlogApp.forms import CommentForm
from django.db.models import Count


def post_detail_view(request, year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                status='published',
                publish__year=year,
                publish__month=month,
                publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]

    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'BlogApp/post_detail.html',{"post":post, 'form':form, 'comments':comments,'csubmit':csubmit,'similar_posts':similar_posts})

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,UpdateView
from django.core.files.storage import FileSystemStorage


class commentview(CreateView):
    model = Comment
    fields= ['name','email','body']
    templates_name = 'BlogApp/comment.html'

class commentdelete(DetailView):
    model = Comment
    success_url= reverse_lazy('succ')

def commentdeletesucc(request):
    return render(request,'BlogApp/delete.html')

class postupdateview(UpdateView):
    model = Post
    fields= ('title','slug','author','body','images')

def profileupdate(request,pk):
    user = User.objects.get(id=pk)
    print('hi')
    if request.method=='POST':
        print('hello')
        form= signupform(request.POST,isinstance=user)
        print('welcome')
        if form.is_valid():
            ser=user.username()
            print('good')
            user.save(commit=True)
            return redirect('/update/')
    print('ok')
    return render(request,'BlogApp/user_form.html',{'user':user,})

class Postdeleteview(DetailView):
    model = Post
    success_url= reverse_lazy('succ1')

def postsuccview(request):
     return render(request,'BlogApp/delete.html')

def contactview(request):
    return render(request,'BlogApp/contact.html')



