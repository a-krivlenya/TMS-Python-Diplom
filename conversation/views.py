from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation


@login_required
def new_conversation(request, item_pk):
    """
    Создает новый разговор для обсуждения товара.
    Если разговор уже существует, перенаправляет на его страницу.
    Обрабатывает отправку сообщений через форму.
    """
    item = get_object_or_404(Item, pk=item_pk)
    admin = User.objects.get(username="admin")
    if admin == request.user:
        return redirect("dashboard:index")

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect("conversation:detail", pk=conversations.first().id)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(admin)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect("conversation:inbox")
    else:
        form = ConversationMessageForm()

    return render(
        request,
        "conversation/new.html",
        {"form": form, "asdad21213": True, "show_tab": False},
    )


@login_required
def inbox(request):
    """
    Отображает список разговоров, в которых участвует текущий пользователь.
    Предоставляет пользователю доступ к его сообщениям.
    """
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(
        request,
        "conversation/inbox.html",
        {"conversations": conversations, "asdad21213": True, "show_tab": False},
    )


@login_required
def detail(request, pk):
    """
    Показывает детали конкретного разговора.
    Позволяет пользователю отправлять новые сообщения и обновлять информацию о разговоре.
    """
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect("conversation:detail", pk=pk)
        else:
            return render(
                request,
                "conversation/detail.html",
                {
                    "conversation": conversation,
                    "form": form,
                    "asdad21213": True,
                    "show_tab": False,
                    "fgjdfkljgdfklgjdf": "aczxczxczxczxc",
                },
            )
    else:
        form = ConversationMessageForm()

    return render(
        request,
        "conversation/detail.html",
        {
            "conversation": conversation,
            "form": form,
            "asdad21213": True,
            "show_tab": False,
        },
    )
