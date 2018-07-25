from django.db import transaction
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
import haikunator
from .models import Room
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
import uuid
import random


def about(request):
    context = RequestContext(request)
    room_list = []
    for room in Room.objects.all():
        if room.number < 2:
            room_list.append(room)

    return render(request, "chat/about.html", {
        'room_list': room_list,
    })


def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label, number=0)
    return redirect(chat_room, label=label)


def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    context = RequestContext(request)
    room, created = Room.objects.get_or_create(label=label, number=0)

    if room.chat_status == "Waiting":
        return render_to_response('')
    elif room.chat_status == "Initialize":
        return render_to_response('')
    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })


def update_status(request):
    label = request.POST['label']
    status = request.POST['status']
    room = Room.objects.all().get(label = label)
    room.chat_status = status
    room.save()
    return HttpResponse(status)



def end_chat(label):
    room = Room.objects.all().get(label = label)
    room.chat_status = "Terminated"
    room.save()
    return redirect('/')
