from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        # db에 UTC 기준으로 시간을 저장하는 것이 아닌 한국시간으로 저장하기
        # now = timezone.now() -> UTC 시간으로 저장
        now = timezone.localtime()
        # email address를 표준으로 자동 교정해주는 django 기능
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            # 이 계정이 활성인가.
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # create_user
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    # create_superuser
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
    

class User(AbstractUser):
    username = None # 본 프로젝트에서는 username대신 email을 사용하기 때문에 오류 방지차원에서 username = None 사용
    email = models.EmailField(unique=True, max_length=225)
    name = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager() #User 모델에서 UserManager 클래스 사용