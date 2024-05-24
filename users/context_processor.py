from users.models import Profile

def get_user(request):
    user = request.user

    context = {
        'user': user,
    }

    return context