import numpy as np
import pytvmaze
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# from sklearn.metrics.pairwise import linear_kernel
# from django.shortcuts import HttpResponse
# from matplotlib import pyplot as plt
from Collab_Filter import data2, indices, cosine_sim, movies_list
from mysite import settings
from .forms import RegisterForm, LogInForm, ReviewsForm
from .models import UserList, ReviewsList
# from .models import Youtube
from youtube_search import YoutubeSearch

tvm = pytvmaze.TVMaze()
from tvmaze.api import Api

api = Api()


def mainpage(response):
    return render(response, "main/login_init.html", {})


def synopsis(request):
    # Receives synopsis title from search engine
    res = request.POST['title']
    # Database scraping
    # video_db = Youtube.objects.all()
    # Converts dataframe to json object
    video_out = YoutubeSearch(res, max_results=10).to_json()
    # Truncates the json to the link of 11 characters
    video_out = video_out[20:31]

    return render(request, "main/Synopsis.html", {'video': video_out})


# Authenticate here
def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST or None)
        if form.is_valid():
            username = User.objects.get(email=form.cleaned_data['username'])
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect(request.GET.get('next',
                                                                settings.LOGIN_REDIRECT_URL))
            else:
                error = 'Invalid username or password.'
            return render(request, "main/login.html")

    #             # templates/registration/login.html
    # return render(request, "main/home.html")


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "main/register.html", {"form": form})


def home(response):

    # Return 2 Values, Movie List, TV List
    # pop = data2.sort_values('popularity', ascending=False)
    pop = movies_list[['title_x']]
    val = pop.reset_index()
    val = val[['title_x']].to_dict()
    movies = sorted(val.items())

    # Reduces list to 10
    out = api.show.list()
    out = out[0:10]

    # Initialize temporary list
    temp = []
    row_vec = []

    # Insert typecast and truncate
    for i in range(len(out)):
        # Typecasts the API output into a string
        temp = str(out[i])
        # Parses the string for HTML output
        row_vec.append(temp[14:len(temp) - 3])
    # Uses the set function to prevent duplicates
    row_vec = list(set(row_vec))
    col_vec = np.array(row_vec, ndmin=2)

    return render(response, "main/home.html", {'Table1': movies, 'Table2': col_vec, 'form': user_list})


def logout(request, redirect=None, auth=None):
    auth.logout(request)
    return redirect('home_url')


def display(request):
    def rec(title, cosine_sim=cosine_sim):
        # Find index of the movie that matches the title
        if title in indices:

            idx = indices[title]
            # Get pairwise similarity scores of all movies with that movie
            sim_scores = list(enumerate(cosine_sim[idx]))

            # Sort the movies based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get scores of 10 most similar movies
            sim_scores = sim_scores[1:11]

            # Get movie indices
            movie_indices = [i[0] for i in sim_scores]

            # Return top 10 most similar movies
            return data2['title_x'].iloc[movie_indices]
        else:
            return []

    # Redirects in the display.html page and Outputs the user's recommendations
    # Display IMDB and TVMaze recommendations
    z = []
    temp = 0
    res = request.POST['title']
    # Only displays TVMaze Table if not found in IMBD Database
    if len(rec(res)) == 0:
        # Finds shows using TVMaze API
        x = api.search.shows(res)

        # Initialize temporary list
        temp = []
        row_vec = []

        # Insert typecast and truncate
        for i in range(len(x)):
            # Typecasts the API output into a string
            temp = str(x[i])
            # Parses the string for HTML output
            row_vec.append(temp[14:len(temp) - 3])
        # Uses the set function to prevent duplicates
        row_vec = list(set(row_vec))
        col_vec = np.array(row_vec, ndmin=2)

        return render(request, 'main/display.html', {'result2': col_vec, 'form': user_list}) 
    # If the input works for both algorithms, display 2 tables
    else:
        val = rec(res)
        val = val.reset_index()
        val = val[['title_x']].to_dict()
        movies = sorted(val.items())

        # Finds shows using TVMaze API
        x = api.search.shows(res)
        for i in range(len(x)):
            # Typecasts the API output into a string
            y = str(x[i])
            # Truncates the string for HTML output
            z.append(y[14:len(y) - 3])
        # Uses the set function to prevent duplicates
        z = list(set(z))
        # 1D vector is transposed into a column vector
        col_vec = np.array(z, ndmin=2)

        return render(request, 'main/display.html', {'result': movies, 'result2': col_vec, 'form': user_list}) 


def review(request):
    if request.method == "POST":
        form = ReviewsForm(request.POST)
        # Receive user input and post to DB
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = ReviewsForm()

    return render(request, "main/reviews.html", {'reviewForm': form})


# # Display User List
# def profile_list(list):
#     user_list = []
#     for i in range(len(list)):
#         user_list.append(list[i])
#     return user_list


from random import randint as r

user_list = []


def profile(request):
    x = []
    y = []
    z = []
    new_list = []

    # Submit added shows to database
    # Modify list if show is deleted
    # if request.method == "POST":
    #     form2 = UserForm(request.POST)
    #     if form2.is_valid():
    #         form2.save()
    # else:
    #     form2 = UserForm()

    # if request.method == 'POST':
    #
    #   if myform.is_valid():
    #       for i in range(len(col_vec)):
    #           title = myform.cleaned_data[col_vec[i]]
    #           query = UserList(name=title)
    #           query.save()

    # Return a table with the user's list based on html button (dropdown?)
    col_vec = np.array(user_list, ndmin=2)

    # Recommends Shows based on User's List
    temp = 0
    if len(user_list) != 0:
        temp = r(0, len(user_list) - 1)
        # Finds shows using TVMaze API
        x = api.search.shows(user_list[temp])
        for i in range(len(x)):
            # Typecasts the API output into a string
            y = str(x[i])
            # Truncates the string for HTML output
            z.append(y[14:len(y) - 3])
        # Uses the set function to prevent duplicates
        new_list = list(z)
    # 1D vector is transposed into a column vector
    col_vec2 = np.array(new_list, ndmin=2)

    # # Calls user form for profile
    # form2 = UserForm(request.POST)

    return render(request, 'main/user_profile.html', {'form': col_vec, 'rec': col_vec2})


def operation1(request):
    if request.POST['addTitle']:
        res = request.POST['addTitle']
        if res not in user_list:
            # saved = UserForm(request.POST)
            # # Receive user input and post to DB
            # if saved.is_valid():
            #     saved.save()
            user_list.append(res)
    col_vec = np.array(user_list, ndmin=2)
    return render(request, 'main/user_profile.html', {'form': col_vec})


def operation2(request):
    if request.POST['delTitle']:
        res2 = request.POST['delTitle']
        if res2 in user_list:
            idx = user_list.index(res2)
            del user_list[idx]
    col_vec = np.array(user_list, ndmin=2)
    return render(request, 'main/user_profile.html', {'form': col_vec})

    # if request.method == "POST":
    #     form = ReviewsForm(request.POST)
    #     # Receive user input and post to DB
    #     if form.is_valid():
    #         form.save()
    #         return redirect("/home")
    # else:
    #     form = ReviewsForm()

# GOALS: Concatenate YT search api
# Connect DBs

# def display_video(request):
#     videos = Youtube.objects.all()
#     context = {'videos': videos}
#     return render(request, 'main/display.html', context)
# if user clicks to add title, the title info is added to User List Home
# That same title is used to update the UI database and update the recommendations
# if user clicks to delete title, the title will be erased from the user's and UI's list
# Allow the user to navigate the list by clicking or scrolling
# Redirect the user to view more recommendations

# if form2.is_valid():
#     title = form2.cleaned_data['title']
#     genre = form2.cleaned_data['']
#     if form2:
#         if form2.is_active:
#             auth_login(request, form2)
#             return HttpResponseRedirect(request.GET.get('next',
#                                                         settings.LOGIN_REDIRECT_URL))

# Required installments
# pip install python-tvmaze
# pip install numpy scipy scikit-learn
# pip install django-star-ratings
# pip install django-cms
