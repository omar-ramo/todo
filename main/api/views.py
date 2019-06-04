from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TaskSerializer

from ..models import Task

@api_view(['GET', 'POST'])
def task_list(request):
	if(request.method == 'GET'):
		tasks = Task.objects.all()
		tasks_serializer = TaskSerializer(tasks, many=True)
		return Response(tasks_serializer.data)
	elif(request.method == 'POST'):
		print(request.data)
		task_serializer = TaskSerializer(data=request.data)
		if(task_serializer.is_valid()):
			return Response(task_serializer, status=status.HTTP_201_CREATED)
		else:
			return Response(task_serializer, status=status.HTTP_400_BAD_REQUEST)