from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from .serializers import RegisterSerializer, TaskSerializer
from .models import Task

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user)

        # по статусу
        status_val = self.request.query_params.get("status")
        if status_val:
            qs = qs.filter(status=status_val)

        # по created_at
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        # по due_date
        due_on = self.request.query_params.get("due_on")
        due_from = self.request.query_params.get("due_from")
        due_to = self.request.query_params.get("due_to")
        if due_on:
            qs = qs.filter(due_date=due_on)
        if due_from:
            qs = qs.filter(due_date__gte=due_from)
        if due_to:
            qs = qs.filter(due_date__lte=due_to)

        return qs.order_by("-created_at")