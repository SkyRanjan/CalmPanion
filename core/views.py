# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm
import google.generativeai as genai
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key="AIzaSyBkXzfRGtwglDc7hydSOPRBpAuweDcdIHc")

# Define keywords for identifying the type of input
MENTAL_SUPPORT_KEYWORDS = ['stress', 'anxious', 'overwhelmed', 'help', 'mental', 'sad', 'depressed']

@csrf_exempt
def chatbot_interaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '').lower()

        if user_input:
            # Short response for greetings
            if any(greeting in user_input for greeting in ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good afternoon']):
                return JsonResponse({"response": "Hi there! I'm CalmPanion. How can I assist you today?"})

            # Detailed response for mental support queries
            elif any(keyword in user_input for keyword in MENTAL_SUPPORT_KEYWORDS):
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction="""You are an empathetic AI stress management assistant focused on helping users reduce stress through practical task management techniques. 
                    Assess the user's current stress levels, identify key stressors, and provide personalized strategies using methods like Pomodoro Technique, Eisenhower Matrix, and mindfulness exercises. 
                    Offer step-by-step, actionable advice that breaks down overwhelming tasks into manageable steps. 
                    Maintain a supportive tone, validate the user's feelings, and gently guide them towards more effective stress reduction and productivity.
                    Don't ask questions, just provide the tips and tasks. The tasks should be detailed and structured."""
                )
                response = model.generate_content(user_input)
                return JsonResponse({"response": response.text})

            # Default response for unrecognized inputs
            else:
                return JsonResponse({"response": "I'm here to help with stress management and productivity tips. Could you tell me more about how you're feeling?"})
        else:
            return JsonResponse({"response": "Please share more about how you're feeling or what you'd like help with."})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

def index(request):
    return render(request, 'core/index.html')

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def interaction(request):
    return render(request, 'core/interaction.html')

from django.shortcuts import render

@login_required
def task_tracker(request):
    return render(request, 'core/task-tracker.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('core:home')
    else:
        form = SignInForm()
    return render(request, 'core/signin.html', {'form': form})

@login_required
def home(request):
    return render(request, 'core/home.html', {'user': request.user})