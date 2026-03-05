import json
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from .models import ChatSession, Message

OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"


def chat_view(request, session_id=None):
    """Render the main chat interface."""
    if session_id:
        session = get_object_or_404(ChatSession, session_id=session_id)
    else:
        # Get the most recent session or create one
        session = ChatSession.objects.first()
        if not session:
            session = ChatSession.objects.create()

    messages = session.messages.all()
    sessions = ChatSession.objects.all()[:20]

    return render(request, 'chatbot/chat.html', {
        'session': session,
        'messages': messages,
        'sessions': sessions,
    })


@require_POST
def send_message(request):
    """Handle sending a message and getting a response from Ollama."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

        session = get_object_or_404(ChatSession, session_id=session_id)

        # Save user message
        Message.objects.create(
            session=session,
            role='user',
            content=user_message,
        )

        # Update session title from first message
        if session.messages.count() == 1:
            title = user_message[:50] + ('...' if len(user_message) > 50 else '')
            session.title = title
            session.save()

        # Build conversation history for Ollama
        conversation = [
            {"role": msg.role, "content": msg.content}
            for msg in session.messages.all()
        ]

        # Call Ollama API
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "messages": conversation,
                    "stream": False,
                },
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            assistant_content = result.get('message', {}).get('content', 'No response received.')
        except requests.exceptions.ConnectionError:
            assistant_content = (
                "⚠️ **Cannot connect to Ollama.**\n\n"
                "Please make sure Ollama is running:\n"
                "```\nollama serve\n```\n"
                "And that you have pulled the model:\n"
                "```\nollama pull llama3.2\n```"
            )
        except requests.exceptions.Timeout:
            assistant_content = "⏱️ **Request timed out.** The model took too long to respond. Please try again."
        except requests.exceptions.RequestException as e:
            assistant_content = f"❌ **Error communicating with Ollama:** {str(e)}"

        # Save assistant message
        assistant_msg = Message.objects.create(
            session=session,
            role='assistant',
            content=assistant_content,
        )

        return JsonResponse({
            'response': assistant_content,
            'message_id': assistant_msg.id,
            'session_title': session.title,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def new_chat(request):
    """Create a new chat session."""
    session = ChatSession.objects.create()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'session_id': str(session.session_id),
            'title': session.title,
        })
    return redirect('chatbot:chat_session', session_id=session.session_id)


@require_GET
def get_history(request):
    """Return message history for a session."""
    session_id = request.GET.get('session_id')
    if not session_id:
        return JsonResponse({'error': 'session_id is required'}, status=400)

    session = get_object_or_404(ChatSession, session_id=session_id)
    messages = [
        {
            'role': msg.role,
            'content': msg.content,
            'created_at': msg.created_at.isoformat(),
        }
        for msg in session.messages.all()
    ]
    return JsonResponse({'messages': messages, 'title': session.title})


@require_GET
def get_sessions(request):
    """Return list of all chat sessions."""
    sessions = ChatSession.objects.all()[:20]
    return JsonResponse({
        'sessions': [
            {
                'session_id': str(s.session_id),
                'title': s.title,
                'updated_at': s.updated_at.isoformat(),
            }
            for s in sessions
        ]
    })


@require_POST
def delete_session(request, session_id):
    """Delete a chat session."""
    session = get_object_or_404(ChatSession, session_id=session_id)
    session.delete()
    return JsonResponse({'status': 'deleted'})
