from django.urls import path
from .views import CreateAdminAPIView, TaskListCreateAPIView,TaskDetailAPIView,TestAPIView,TaskStatusAPIView,CommentListCreateAPIView,CommentDetailAPIView,TaskCommentAPIView,TaskReorderAPIView,ExportExcelAPIView,ExportPDFAPIView,UserProfileAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path("tasks/",TaskListCreateAPIView.as_view(),name='task-list'),
    path("tasks/<int:pk>/",TaskDetailAPIView.as_view(),name='task-detail'),
    path("login/",TokenObtainPairView.as_view(),name='login'),
    path("refresh/",TokenRefreshView.as_view(),name='token-refresh'),
    #A temp test url for test view
    path("test/",TestAPIView.as_view(),name = 'test'),

    path('tasks/<int:pk>/status/',TaskStatusAPIView.as_view(),name='task-status'),
    path('comments/',CommentListCreateAPIView.as_view(), name='comment-list'),
    path('comments/<int:pk>/',CommentDetailAPIView.as_view(),name='comment-detail'),
    path('tasks/<int:task_id>/comments/',TaskCommentAPIView.as_view(),name='task-comments'),
    path('tasks/reorder/',TaskReorderAPIView.as_view(),name='task-reorder'),
    path('export/pdf/',ExportPDFAPIView.as_view(),name='export-pdf'),

    path('export/excel/',ExportExcelAPIView.as_view(),name='export-excel'),
    path("profile/",UserProfileAPIView.as_view(),name="profile"),

    # create the url temp
    path(
    "create-admin/",
    CreateAdminAPIView.as_view(),
    name="create-admin"
)
]