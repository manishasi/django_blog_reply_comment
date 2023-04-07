from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  ProfileForm,PostForm,UserForm,CommentForm,ReplyForm
from .models import Profile, Post,Comment,Reply
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Count, Q
from datetime import datetime
#.............home page.................
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    # print(form,'pppppppppppppppppppppppppppppppp')
    if request.user.id is not None:
        user_id=request.user.id
        # print(user_id)
        liked_list=[]
        like_post=Post.objects.filter(likes=user_id)
        for i in like_post:
            liked_list.append(i.title)
        # print(like_post)
        # print("lnkjanjknjknkjsbahjbjkbsakj-----------------")
        comment_form = CommentForm()
        form = ReplyForm()
        context = {'posts': posts,'user_id':user_id,'liked_list':liked_list,'comment_form':comment_form ,'form':form}
    else:

        comment_form = CommentForm()
        context = {'posts': posts}
    # print("bhjasbhjbkjsha",posts)
    return render(request, 'home.html', context)

# ..........registration form............
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'registration.html', {'user_form': user_form,'profile_form': profile_form})

#.............user login.............
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            # if user.is_staff and not user.is_superuser:
            #     messages.error(request, 'Admin login not allowed')
            # else:   
                login(request, user)
                return redirect('profile')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')


#..........update profile................
@login_required
def update(request):
    profile = get_object_or_404(Profile, user=request.user)
    user_name=request.user
    # user=get_object_or_404(User)
    # print(user,"slknldslknskllkdn")
    if request.method == 'POST':
        # print(request.POST,"-----------------------------------")
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        # user_form = UserForm(instance=user)
        form = ProfileForm(instance=profile)
        # messages.success(request, 'Username and password is incorrect')
    context = {'form': form,'name':user_name}
    return render(request, 'update.html', context)


#.................profile................
# @user_passes_test(user_login)
@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    profile_details=Profile.objects.filter(user=request.user)
    user = User.objects.filter(username=request.user)
    print(profile)
    context = {'details':profile_details,'user_details':user}
    return render(request,'profile.html',context)

#..........post create...........
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.created_at=datetime.now()
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form}
   

    return render(request, 'create_post.html', context)



#...........like on post........
@login_required
def like_post(request, id):
    # print(id,"idddddddddddddddd")
    post = get_object_or_404(Post, id=id)
    # print('pooooooooooossstttttttt',post)
    if request.method == 'POST':
        # print(request.method,"----------------------")
        if request.user in post.likes.all():
            # user has already liked the post, remove their like
            post.likes.remove(request.user)
        else:
            # user has not liked the post yet, add their like and remove dislike
            post.likes.add(request.user)
            # post.dislikes.remove(request.user)
    # print("loginnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    return redirect('home')


#............delete on post............
@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')

    context = {'post': post}
    return render(request, 'delete_post.html', context)


#...............logout.................   
def user_logout(request):
    logout(request)
    return redirect('login')


#..................comment on post................
@login_required
def comment_view(request, id):
    print("xsh xs xshgsxnhzsxgnhzamsxnzhAM")
    post=get_object_or_404(Post,id=id)
    print(post,'pppppppppppppppppppppppppppppppppppp')
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    print(comments,'cccccccccccccccccccccccccccccccccccc')
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            print(new_comment,'newwwwwwwwwwwwwwwwwwwwwww')
            # redirect to same page and focus on that comment
            return redirect('home')
  
    else:
            comment_form = CommentForm()
    return redirect('home')


#................comment on reply....................
@login_required
def reply(request,id):
    print("thisssssssssssss")
    comment=get_object_or_404(Comment,id=id)
    print(comment,'commmmmmmmmmmmmmmmmmmmmeeennnttttttttt')
    reply= Comment.objects.all()
    print(reply,'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
    if request.method == "POST":
        form = ReplyForm(request.POST)
        print(form,'ffffffffffffffffffffffffffffffffffffff')
        if form.is_valid():
            reply = form.save(commit=False)
            print(reply,'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            reply.author = request.user
            # reply.post = Post(id=post_id)
            reply.comment = Comment(id=id)
            reply.save()
            return redirect('home')
    else:
            form = ReplyForm()
    return redirect('home')


def reply_thread(request, id=None):
    print("kjbkjb",id
    )
    if id:
        parent_comment = Reply.objects.get(id=id)
        print("vjhvjhvjhv",parent_comment)
    else:
        parent_comment = None

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            print("yes its going to vailid")
            comment = form.save(commit=False)
            comment.author = request.user
            # comment.parent = parent_comment
            comment.save()
            print("naskjnsajkn save hogya")
            return redirect('comment_thread', comment_id=parent.id if parent else None)
    else:
        form = ReplyForm()

    reply_comment = Reply.objects.filter(parent=parent_comment)
    print("jksnkjndjndsjkn is the best",reply_comment)
    return render(request, 'comment_thread.html', {'comments': reply_comment, 'parent_comment': parent_comment, 'form': form})



# def reply(request, id):
   
#     comments = get_object_or_404(Comment, id=id)
#     reply = comments.replies.filter(replay__isnull=True)
#     if request.method == 'POST':
#         # comment has been added
#         form = ReplyForm(request.POST)
#         if form.is_valid():
#             replay_obj = None
#             # get parent comment id from hidden input
#             try:
#                 # id integer e.g. 15
#                  replay_id = int(request.POST.get('replay_id'))
#             except:
#                  replay_id = None
#             # if parent_id has been submitted get parent_obj id
#             if  replay_id:
#                 replay_obj = Reply.objects.get(id= replay_id)
#                 # if parent object exist
#                 if  replay_obj:
#                     # create replay comment object
#                     replay_comment = form.save(commit=False)
#                     replay_comment.author = request.user
#                     # assign parent_obj to replay comment
#                     replay_comment. replay = replay_obj
            
#             # create comment object but do not save to database
#             new_comment = form.save(commit=False)
#             # assign ship to the comment
#             new_comment.comments = comments
#             # save
#             new_comment.save()
#             return redirect('home')
#     else:
#         form =ReplyForm()
#     return render(request,'home.html')



#...............comment on like....................
@login_required
def like_comment(request, id):
    comment = Comment.objects.get(pk=id)
    user = request.user
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    return redirect('home')


#.................reply on like.................
@login_required
def like_reply(request, id):
    reply = Reply.objects.get(pk=id)
    user = request.user
    if user in reply.likes.all():
        reply.likes.remove(user)
    else:
       reply.likes.add(user)
    return redirect('home')


#.............comment deleted.................
@login_required
def delete_comment(request, id):
    comment= get_object_or_404(Comment, id=id)

    if request.method == 'POST':
        comment.delete()
        # messages.success(request, 'comment deleted successfully')
        return redirect('home')

    context = {'post': comment}
    return render(request, 'delete_post.html', context)


#.................reply deleted..................
@login_required
def delete_reply(request, id):
    reply= get_object_or_404(Reply, id=id)

    if request.method == 'POST':
        reply.delete()
        # messages.success(request,'reply deleted successfully')
        return redirect('home')

    context = {'post': reply}
    return render(request, 'delete_post.html', context)

@login_required
def post_view(request, id):
    post = get_object_or_404(Post, id=id)
    print(post,"&&&&&&&&&&&&&&&&&&&&&&")
    post.views += 1
    post.save()
    comment_form = CommentForm()
    form = ReplyForm()
    return render(request, 'post_view.html', {'post': post,'comment_form':comment_form ,'form':form})

# @login_required
# def post_view(request, id):
#     post = get_object_or_404(Post, id=id)

#      # Update the view count on each visit to this post.
#     if post:
#            post.views = post.views + 1
#            post.save()
#     context = {'post': post}

#     return render(request, "home.html", context)


# @login_required
# def post_view(request, id):
#     post = get_object_or_404(Post, id=id)
#     if not post.viewers.filter(id=request.user.id).exists():
#         post.viewers.add(request.user)
#     return render(request, 'home.html', {'post': post})


# @login_required
# def update_post(request):
#     profile = get_object_or_404(Profile, user=request.user)
#     user_name=request.user
#     # user=get_object_or_404(User)
#     # print(user,"slknldslknskllkdn")
#     if request.method == 'POST':
#         # print(request.POST,"-----------------------------------")
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully')
#             return redirect('profile')
#     else:
#         # user_form = UserForm(instance=user)
#         form = ProfileForm(instance=profile)
#         # messages.success(request, 'Username and password is incorrect')
#     context = {'form': form,'name':user_name}
#     return render(request, 'update.html', context)






# @login_required
# def comment_view(request,id):
#     print(id,"*************")
#     # parent_comment = get_object_or_404(Comment, id=id)
#     if request.method=="POST":
#         # print(POST,"------------------------------")
#         comment_form = CommentForm(request.POST)
#         print(comment_form,"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
#         if comment_form.is_valid():
            
#             cd=comment_form.cleaned_data
#             print(cd,"..........................")
#             new_comment =  comment_form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.post = Post.objects.get(id=id)
#             new_comment.save()
#             return redirect('home')
#     else:
#         comment_form = CommentForm()
#     return render(request,'add_comment.html',{'comment_form':comment_form})

# def comment_view(request, id):
#     # get post object
#     post = get_object_or_404(Post,id=id)
#     # list of active parent comments
#     comments=post.comments.filter(active=True, parent_comment__isnull=True)
#     # print("manishaaa",comments[0].replies.all)
#     print(comments,"**********************88")
#     if request.method == 'POST':
#         # comment has been added
#         comment_form = CommentForm(data=request.POST)
#         print( comment_form,"&&&&&&&&&&&&&&&&&&&&&&")
#         if comment_form.is_valid():
#             parent_obj = None
#             # get parent comment id from hidden input
#             try:
#                 # id integer e.g. 15
#                 parent_id = int(request.POST.get('parent_comment_id'))
#             except:
#                 parent_id = None
#             # if parent_id has been submitted get parent_obj id
#             if parent_id:
#                 parent_obj = Comment.objects.get(id=parent_id)
#                 # author = form.cleaned_data['author']
#                 # comment = form.cleaned_data['comment']
#                 # if parent object exist
#                 if parent_obj:
#                     # create replay comment object
#                     reply_comment = comment_form.save(commit=False)
#                     # assign parent_obj to replay comment
                   
#                     reply_comment.parent_comment = parent_obj
#             # normal comment
#             # create comment object but do not save to database
#             new_comment = comment_form.save(commit=False)
#             new_comment.author = request.user
#             # assign ship to the comment
#             new_comment.post = post
#             # save    
#             new_comment.save()
#             return redirect("home")
#             # return HttpResponseRedirect(post.get_absolute_url())
#     else:
#         comment_form = CommentForm()
#     return render(request,
#                   'home.html',
#                   {'post': post,
#                    'comments': comments,
#                    'comment_form': comment_form})

