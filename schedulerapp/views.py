from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from .serializer import AvailabilitySerializer
from rest_framework.views import APIView
from rest_framework import status

from .serializer import CustomUserSerializer
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Availability
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from django.http import Http404
from datetime import timedelta


# Create your views here.

"""Below I have written three class views.
1.Register: 
    This view is used to register a new user/candidate(these terms are used interchanged in this project),interviewer,manager.
2.RegisterAvailabilityView
    This view helps users and interviewers to register their availability by providing the day and start time and end time ,when they will be available
3.InterviewTimeslotsView
    This view is used to get the available timeslots based on the recent availability information provided by them assuming the date to be same ,when the candidate and interviewer is are inputted
"""


class Register(APIView):
    def post(self, request):

        password = request.data.get("password")

        try:

            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                hashed_password = make_password(password)
                serializer.validated_data["password"] = hashed_password
                user = serializer.save()
                return Response(
                    {"message": "Account Created Successfully", "id": user.id},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAvailabilityView(APIView):

    def post(self, request):

        candidate_id = request.data.get("candidate_id")
        interviewer_id = request.data.get("interviewer_id")
        starting_time = request.data.get("start_time")
        ending_time = request.data.get("end_time")
        try:
            candidate = CustomUser.objects.filter(id=candidate_id)
            interviewer = CustomUser.objects.filter(id=interviewer_id)

            start_time = datetime.strptime(starting_time, "%I:%M %p").time()
            end_time = datetime.strptime(ending_time, "%I:%M %p").time()
            data = request.data.copy()

            data.pop("start_time", None)
            data.pop("end_time", None)
            data.pop("candidate_id", None)
            if candidate:

                data.update(
                    {
                        "start_time": start_time,
                        "end_time": end_time,
                        "user": candidate_id,
                    }
                )
            elif interviewer:
                data.update(
                    {
                        "start_time": start_time,
                        "end_time": end_time,
                        "user": interviewer_id,
                    }
                )
            else:
                return Response(
                    {"error": "No user or interviewer with that ID exists!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if candidate.exists():
                serializer = AvailabilitySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "The candidate Availability has been added"},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                    )
            elif interviewer.exists():
                serializer = AvailabilitySerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "The Interviewer Availability has been added"},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InterviewTimeSlotsView(APIView):

    def get(self, request):
        interviewer_id = request.query_params.get("interviewer_id")
        candidate_id = request.query_params.get("candidate_id")
        try:
            candidate = get_object_or_404(CustomUser, id=candidate_id)
            interviewer = get_object_or_404(CustomUser, id=interviewer_id)

            candidate_availability = (
                Availability.objects.filter(user=candidate_id)
                .order_by("-interview_date")
                .first()
            )
            interviewer_availability = (
                Availability.objects.filter(user=interviewer_id)
                .order_by("-interview_date")
                .first()
            )

            if not interviewer_availability or not candidate_availability:
                return Response(
                    {
                        "error": "Candidate and interviewer have not shared their availability"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            candidate_start_time = datetime.combine(
                datetime.today(), candidate_availability.start_time
            )
            candidate_end_time = datetime.combine(
                datetime.today(), candidate_availability.end_time
            )
            interviewer_start_time = datetime.combine(
                datetime.today(), interviewer_availability.start_time
            )
            interviewer_end_time = datetime.combine(
                datetime.today(), interviewer_availability.end_time
            )

            if (
                candidate_end_time <= interviewer_start_time
                or interviewer_end_time <= candidate_start_time
            ):
                return Response(
                    {
                        "error": "The candidates and interviewers availability is not overlapping, could not produce slots where both are available!"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            overlap_start = max(candidate_start_time, interviewer_start_time)
            overlap_end = min(candidate_end_time, interviewer_end_time)
            slot_duration = timedelta(minutes=60)
            slots = []
            current_time = overlap_start
            while current_time + slot_duration <= overlap_end:
                slot = f"{current_time.strftime('%I:%M %p')} - {(current_time + slot_duration).strftime('%I:%M %p')}"
                slots.append(slot)
                current_time += slot_duration

            return Response({"available_slots": slots}, status=status.HTTP_200_OK)

        except Http404:
            raise NotFound(
                "The Interviewer/Candidate you are looking for does not exist."
            )
