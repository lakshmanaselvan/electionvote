from django.shortcuts import render, redirect
from .models import Voter, Candidate

def home(request):
    return render(request, "home.html", {})

def login(request):
    if request.method == 'POST':
        voter_id = request.POST['voter_id']
        password = request.POST['password']
        try:
            voter = Voter.objects.get(voter_id=voter_id, password=password)
            # Successful login            
            # You can perform additional actions here, such as setting session variables
            request.session['voter_id'] = voter.voter_id
            return redirect('voting_page')  # Change this to the URL name of your dashboard
        except Voter.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'Invalid voter ID or password.'})
    return render(request, 'login.html')

def voting_page(request):
    error_message = '' 
    if request.method == 'POST':
        selected_candidate_id = request.POST.get('Candidate.cid')

        if selected_candidate_id:
            try:
                selected_candidate = Candidate.objects.get(pk=selected_candidate_id)
                voter_id = request.session.get('voter_id')  # Retrieve voter_id from the session

                if voter_id:
                    # Check if the voter has already voted
                    if not Voter.objects.filter(voter_id=voter_id).exists():
                        Voter.objects.create(voter_id=voter_id, candidate=selected_candidate)
                        return redirect('vote_count')  # Redirect to a success page after voting
                    else:
                        error_message = 'You have already voted.'
                else:
                    return redirect('login')  # Redirect to login page if voter_id is not in session

            except Candidate.DoesNotExist:
                error_message = 'Invalid candidate selection.'

    candidates = Candidate.objects.all()
    return render(request, 'voting_page.html', {'candidates': candidates, 'error_message': error_message})


def vote_count(request):
    candidate  = Candidate.objects.all()
    return render(request, "votecount.html", {'candidate':candidate})