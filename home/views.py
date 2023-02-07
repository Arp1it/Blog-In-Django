from django.shortcuts import render, HttpResponse, redirect
from . models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from myblog.models import Post
from django.db.models import Q

# Create your views here.
def home(request):
    post = Post.objects.all().values()
    a = []
    for value in post:
        b = value.get('views')
        a.append(b)
    m = max(a)
    m1 = m-1
    m2 = m-2
    popularpost = Post.objects.filter(Q(views=m) | Q(views=m1) | Q(views=m2))
    contex ={"pposts":popularpost}
    
    return render(request, "home/home.html", contex)

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        msg = request.POST['content']

        if len(name)<3 or len(email)<5 or len(phone)<10 or len(msg)<5:
            messages.error(request, "Please fill details correctly!")

        else:
            contac = Contact(name=name, email=email, phone=phone, content=msg)
            contac.save()
            messages.success(request, "Message successfully send!")

    return render(request, "home/contact.html")

def about(request):
    return render(request, "home/about.html")

def search(request):
    query = request.GET['query']

    if len(query) > 51:
        posts = Post.objects.none()
        maxquery = "we limit queries to 50 words."

    else:
        postsblog = Post.objects.filter(title__icontains=query)
        postscontent = Post.objects.filter(content__icontains=query)
        postsauthor = Post.objects.filter(author__icontains=query)
        posts = postsblog.union(postscontent, postsauthor)
        maxquery = ""

    if posts.count() == 0:
        messages.warning(request, "No search result found")

    params = {"allPosts":posts, "query":query, "maxquery":maxquery}
    return render(request, "home/search.html", params)

def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        Email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 15 or len(username) < 4:
            messages.error(request, "Username must be under 10 character and must be greater than 4 character")
            return redirect("home")

        if not username.isalnum():
            messages.error(request, "Username should only contains letters and numbers")
            return redirect("home")

        if pass1 != pass2:
            messages.error(request, "Password is not matched")
            return redirect("home")

        # Create the user
        myuser = User.objects.create_user(username, Email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account have been successfully created.")
        return redirect("home")

    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginemail = request.POST['loginemail']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, email=loginemail, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")

        else:
            messages.error(request, "Invalid Logged In")
            return redirect("home")

    return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")

    return redirect("home")