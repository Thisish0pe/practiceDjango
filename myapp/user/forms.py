from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# settings.py 내부에 AUTH_USER_MODEL 선언해주었기 때문에 User model 사용할 경우, get_user_model 로 모델을 불러오는 것.
User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email']


