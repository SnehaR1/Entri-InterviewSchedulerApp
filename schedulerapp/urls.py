from django.urls import path
from .views import (
    Register,
    RegisterAvailabilityView,
    InterviewTimeSlotsView,
)


urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path(
        "register_availability/",
        RegisterAvailabilityView.as_view(),
        name="register_availability",
    ),
    path("generate_slots/", InterviewTimeSlotsView.as_view(), name="generate_slots"),
]
