from django.urls import path
from .views import TaskListCreateAPIView,TaskDetailAPIView,TestAPIView,TaskStatusAPIView,CommentListCreateAPIView,CommentDetailAPIView,TaskCommentAPIView,TaskReorderAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path("tasks/",TaskListCreateAPIView.as_view(),name='task-list'),
    path("tasks/<int:pk>",TaskDetailAPIView.as_view(),name='task-detail'),
    path("login/",TokenObtainPairView.as_view(),name='login'),
    path("refresh/",TokenRefreshView.as_view(),name='token-refresh'),
    #A temp test url for test view
    path("test/",TestAPIView.as_view(),name = 'test'),

    path('tasks/<int:pk>/status/',TaskStatusAPIView.as_view(),name='task-status'),
    path('comments/',CommentListCreateAPIView.as_view(), name='comment-list'),
    path('comments/<int:pk>/',CommentDetailAPIView.as_view(),name='comment-detail'),
    path('tasks/<int:task_id>/comments/',TaskCommentAPIView.as_view(),name='task-comments'),
    path('tasks/reorder/',TaskReorderAPIView.as_view(),name='task-reorder'),
]