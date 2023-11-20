import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from chat.models import GroupChat, Member


@login_required
def index(request):
    current_user = request.user
    return render(request, 'chat/index.html', {'members': current_user.member_set.all()})


@login_required
def create_chat(request):
    current_user = request.user
    title = request.POST['group_name']
    chat = GroupChat.objects.create(creator_id=current_user.id, title=title)
    Member.objects.create(chat_id=chat.id, user_id=current_user.id)
    return redirect(reverse('chat:chat', args=[chat.unique_code]))


@login_required
def chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(unique_code=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, 'chat/404.html')
    if request.method == "GET":
        if Member.objects.filter(chat_id=chat.id, user_id=current_user.id).count() == 0:
            return render(request, 'chat/join_chat.html', {'chatObject': chat})

        return render(request, 'chat/chat.html', {'chatObject': chat, 'chat_id_json': mark_safe(json.dumps(chat.unique_code))})
    elif request.method == "POST":
        Member.objects.create(chat_id=chat.id, user_id=current_user.id)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "join", 'username': current_user.username})
            }
        )

        return render(request, 'chat/chat.html', {'chatObject': chat, 'chat_id_json': mark_safe(json.dumps(chat.unique_code))})
        

@login_required
def leave_chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(unique_code=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, 'chat/404.html')
    
    if chat.creator_id == current_user.id:
        chat.delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "delete"})
            }
        )

    else:
        Member.objects.filter(chat_id=chat.id, user_id=current_user.id).delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "leave", 'username': current_user.username})
            }
        )

    return redirect('chat:index')