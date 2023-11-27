from django.urls import path

from main.apps import MainConfig
from main.views import HomeView, RightsContentView, AppointmentCreateView, AppointmentUserListView,\
    AppointmentListView, AppointmentDoctorListView, UserProfileView, AppointmentDeleteView, FeedbackCreateView,\
    FeedbackUserListView, FeedbackListView, FeedbackDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rights_content/', RightsContentView.as_view(), name='rights_content'),
    path('appointment/create/', AppointmentCreateView.as_view(), name='create_appointment'),

    # Список записей принадлежащих авторизованному пользователю
    path('appointments/user/', AppointmentUserListView.as_view(), name='appointments_user'),

    # Список все записей
    path('appointments/', AppointmentListView.as_view(), name='appointments'),

    # Список записей врача
    path('appointments/doctor/', AppointmentDoctorListView.as_view(), name='appointments_doctor'),

    path('patient/profile/<int:pk>', UserProfileView.as_view(), name='user_profile'),
    path('appointment/delete/<int:pk>', AppointmentDeleteView.as_view(), name='delete_appointment'),

    path('feedback/create/', FeedbackCreateView.as_view(), name='create_feedback'),
    path('feedback/user/', FeedbackUserListView.as_view(), name='user_list_feedback'),
    path('feedback/all/', FeedbackListView.as_view(), name='list_feedback'),
    path('feedback/delete/<int:pk>', FeedbackDeleteView.as_view(), name='delete_feedback'),
]
