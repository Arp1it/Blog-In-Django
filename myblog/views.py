from django.shortcuts import render, HttpResponse, redirect
from myblog.models import Post, Blogcomment
from django.contrib import messages
from myblog.templatetags import extratem

# Create your views here.
def bloghome(request):
    allPosts = Post.objects.all()
    context = {"allPosts":allPosts}
    return render(request, "myblog/blogHome.html", context)

def blogpost(request, slugg):
    post = Post.objects.filter(slug=slugg).first()
    post.views = post.views + 1
    post.save()

    comments = Blogcomment.objects.filter(post=post, parent=None)
    replies = Blogcomment.objects.filter(post=post).exclude(parent=None)

    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict:
            replyDict[reply.parent.sno] = [reply]
            # print(reply.parent.sno)
            # print(reply.sno)
        else:
            replyDict[reply.parent.sno].append(reply)
            # print(reply.parent.sno)

    # print(replies)
    # print(replyDict)
    # print(request.user)
    content = {"post":post, "comments":comments, "user":request.user, "replyDict":replyDict}
    return render(request, "myblog/blogPost.html", content)
    # return HttpResponse(f"this is blogpost {slugg}")

# Creating Postcomment API
def postcomment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentsno")

        if parentSno == "":
            comment = Blogcomment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")

        else:
            parrentt = Blogcomment.objects.get(sno=parentSno)
            comment = Blogcomment(comment=comment, user=user, post=post, parent=parrentt)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")

    return redirect(f'/blog/{post.slug}')