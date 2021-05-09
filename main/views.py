from django.shortcuts import render, redirect

from mysite import settings
from .models import UserList, ReviewsList
from .forms import UserForm
from .forms import RegisterForm, LogInForm, ReviewsForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
# from django.shortcuts import HttpResponse
import pandas as pd
from matplotlib import pyplot as plt
from Collab_Filter import data2, indices, cosine_sim, movies_list
import pytvmaze
import numpy as np

tvm = pytvmaze.TVMaze()
from tvmaze.api import Api

api = Api()


def mainpage(response):
    return render(response, "main/login_init.html", {})

def synopsis(request):
    res = request.POST['title']
    x = api.search.single_show(res)
    name = x.name
    summary = x.summary
    id = x.id
    show = tvm.get_show(id, embed='episodes')
    for episode in show.episodes:
        if (episode.season_number == 1):
            season = episode.season_number
        if (episode.episode_number == 1):
            ep_num = episode.episode_number
            ep_title = episode.title
            ep_sum = episode.summary
    return render(request, "main/Synopsis.html", {'Name': name, 'Sum': summary, 'season': season,
                                                  'episode': ep_num, 'title': ep_title, 'ep_sum': ep_sum})

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
    # Initialize list to display TV List
    y2 = []
    z = []
    # Return 2 Values, Movie List, TV List
    # pop = data2.sort_values('popularity', ascending=False)
    pop = movies_list[['title_x']]
    val = pop.reset_index()
    val = val[['title_x']].to_dict()
    movies = sorted(val.items())

    y = api.show.list()
    y = y[0:10]

    for i in range(len(y)):
        # Typecasts the API output into a string
        y2 = str(y[i])
        # Truncates the string for HTML output
        z.append(y2[14:len(y2) - 3])
    # Uses the set function to prevent duplicates
    z = list(set(z))
    col_vec = np.array(z, ndmin=2)

    return render(response, "main/home.html", {'Table1': movies, 'Table2': col_vec, 'form':user_list})


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

        for i in range(len(x)):
            # Typecasts the API output into a string
            y = str(x[i])
            # Truncates the string for HTML output
            z.append(y[14:len(y) - 3])
        # Uses the set function to prevent duplicates
        z = list(set(z))

        # Sprint 4 Goal: Sentimental Analysis Algorithm
        # Recommend Title based on mood of the movie

        # Fills in gaps left behind from removed duplicates
        # Condition 1
        # if len(z) != 10:
        #     temp = 10 - len(z)
        # for i in range(temp):
        #     val.append(val[i])

        # 1D vector is transposed into a column vector
        col_vec = np.array(z, ndmin=2)
        # empty_table = len(col_vec) {'check': empty_table}

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

    # # Link this data to Database
    # if request.method == "POST":
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # else:
    #     form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            title = User.objects.get(title=form.cleaned_data[''])
            genre = form.cleaned_data['password']
            # rating =
            if user:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect(request.GET.get('next',
                                                                settings.LOGIN_REDIRECT_URL))

    # Return a table with the user's list based on html button (dropdown?)
    col_vec = np.array(user_list, ndmin=2)

    # Recommends Shows based on User's List
    temp = 0
    if len(user_list) != 0:
        temp = r(0, len(user_list)-1)
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

    return render(request, 'main/user_profile.html', {'form': col_vec, 'rec': col_vec2})


def operation1(request):
    if request.POST['addTitle']:
        res = request.POST['addTitle']
        if res not in user_list:
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

# if user clicks to add title, the title info is added to User List Home
# That same title is used to update the UI database and update the recommendations
# if user clicks to delete title, the title will be erased from the user's and UI's list
# Allow the user to navigate the list by clicking or scrolling
# Redirect the user to view more recommendations


def review(request):
    if request.GET.get('title'): 
        res = request.GET.get('title')
    if request.method == "POST":
        form = ReviewsForm(request.POST)
        # Receive user input and post to DB
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = ReviewsForm()

    reviews_list = []
    reviews_list = ReviewsList.objects.filter(
        title = res
    )

    return render(request, "main/reviews.html", {'reviewForm': form, 'title': res, 'reviews_list': reviews_list})

