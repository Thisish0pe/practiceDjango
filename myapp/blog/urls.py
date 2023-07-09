from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 글 목록
    path("", views.List.as_view(), name = 'list'),
    # 상세 글 페이지
    path("detail/<int:pk>/", views.DetailView.as_view(), name = 'detail'), 
    # 글 작성 페이지
    path("write/", views.Write.as_view(), name = 'write'),
    # 글 수정 페이지
    path("detail/<int:pk>/edit/", views.Update.as_view(), name = 'edit'),
    # 글 삭제
    path("detail/<int:pk>/delete/", views.Delete.as_view(), name='delete'),
    # 코멘트 작성
    path("detail/<int:pk>/comment/write/", views.CommentWrite.as_view(), name='cm-write'),
    # 코멘트 수정
    path("detail/<int:pk>/comment/edit/", views.CommentEdit.as_view(), name='cm-edit'),
    # 코멘트 삭제
    path("detail/<int:pk>/comment/delete/", views.CommentDelete.as_view(), name='cm-delete'),
    # 해쉬태그 작성
    path("detail/<int:pk>/hashtag/write/", views.HashTagWrite.as_view(), name='tag-write'),
    # 해쉬태그 삭제
    path("detail/<int:pk>/hashtag/delete/", views.HashTagWrite.as_view(), name='tag-delete'),
]