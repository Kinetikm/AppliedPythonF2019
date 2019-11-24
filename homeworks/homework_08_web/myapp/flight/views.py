from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from flight.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@api_view(["POST"])
def create_flight(request):
    if request.user.is_authenticated:
        AirFlight.user_create = request.user
        request.data['user_create'] = request.user.username
        serializer = AirFlightFieldsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return render(request, 'login.html', {})


@api_view(["GET"])
def flight_details(request, pk):
    flight = AirFlight.objects.get(id=pk)
    serializer = AirFlightAllSerializer(flight)
    return Response(serializer.data)


@api_view(["GET", "PUT"])
def flight_update(request, pk):
    if request.user.is_authenticated:
        flight = AirFlight.objects.get(id=pk)
        if flight.user_create == request.user.username:
            if request.method == "PUT":
                request.data['user_create'] = request.user.username
                serializer = AirFlightFieldsSerializer(flight, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({"error": serializer.errors})
            serializer = AirFlightAllSerializer(flight)
            return Response(serializer.data)
        else:
            return HttpResponse("Not you record!")
    else:
        return render(request, 'login.html', {})


@api_view(["GET"])
def flights_list(request):
    fligths = AirFlight.objects.all()
    serializer = AirFlightAllSerializer(fligths, many=True)
    return Response({"flights": serializer.data})


def delete_flight(request, pk):
    if request.user.is_authenticated:
        flight = get_object_or_404(AirFlight, id=pk)
        if flight.user_create == request.user.username:
            flight = get_object_or_404(AirFlight, id=pk)
            flight.delete()
            return HttpResponse("DELETED!")
        else:
            return HttpResponse("Not you record!")
    else:
        return render(request, 'login.html', {})


def index(request):
    return render(request, 'index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'registration.html',
                  {'user_form': user_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})
