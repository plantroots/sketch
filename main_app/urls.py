from django.urls import path
from . import views

# TEMPLATE TAGGING
app_name = 'main_app'

urlpatterns = [
    path('<int:id>',views.video_focus,name="video_focus"),
    path('delete/<int:id>',views.delete_video,name='delete_video')
]