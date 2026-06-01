from django.shortcuts import render
from .models import Task,Comment
from .serializers import TaskSerializer,CommentSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import openpyxl

# Create your views here.


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        tasks = Task.objects.all().order_by('position')
        search = request.GET.get("search")
        status_filter = request.GET.get("status")
        priority_filter = request.GET.get("priority")
        sort = request.GET.get("sort")

        if search:
            tasks = tasks.filter(
                Q(name__icontains = search)

                |

                Q(code__icontains = search)
            )
        
        if status_filter:
            tasks = tasks.filter(
                status = status_filter
            )
        if priority_filter:
            tasks = tasks.filter(
                priority=priority_filter
            )
        if sort == 'due_date':
            tasks = tasks.order_by(
                'due_date'
            )
        page_number = request.GET.get('page',1)
        paginator = Paginator(tasks,10)
        page_obj = paginator.get_page(page_number)
        
        serializer = TaskSerializer(page_obj,many=True)
        print(serializer)
        return Response({

        "total_pages": paginator.num_pages,

        "current_page": page_obj.number,

        "total_tasks": paginator.count,

        "results": serializer.data
        })


    
    
    def post(self,request):
        if not request.user.is_staff:
            return Response(
                {"error":"Only admin can create tasks"},
                            status=status.HTTP_403_FORBIDDEN
                            )
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            print(serializer.initial_data)
            
            print(serializer.validated_data)
            serializer.save()
            print(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None
        
    def get(self,request,pk):
        task = self.get_object(pk)
        if not task:
            return  Response(
                {"error":"Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serilizer = TaskSerializer(task)
        return Response(serilizer.data)
    
    def put(self,request,pk):
        if not request.user.is_staff:
            return Response({"error":"only admin can edit task"},status=status.HTTP_403_FORBIDDEN)

        task = self.get_object(pk)

        if not task:
            return  Response(
                {"error":"Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            serializer = TaskSerializer(task,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self,request,pk):
        if not request.user.is_staff:
            return Response({"error":"only admin can delete task"},status=status.HTTP_403_FORBIDDEN)
        task = self.get_object(pk)
        if not task:
            return  Response(
                {"error":"Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            task.delete()
            return Response({"message":"Task deleted"}, status= status.HTTP_200_OK)
        
        


#creating the temporary view for testing the jwt authentication
class TestAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        return Response({

            "username":
            request.user.username

        })
    


class TaskStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        task = Task.objects.filter(pk=pk).first()

        if not task:

            return Response(
                {
                    "error":
                    "Task not found"
                },
                status=404
            )

        status_value = request.data.get('status')

        if not status_value:

            return Response(
                {
                    "error":
                    "Status required"
                },
                status=400
            )

        task.status = status_value

        task.save()

        return Response(
            {
                "message":
                "Status updated",

                "status":
                task.status
            }
        )
    

class CommentListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        if not request.user.is_staff:

            return Response(
                {
                    "error": "Admin only"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        comments = Comment.objects.select_related(
            'user',
            'task'
        )

        serializer = CommentSerializer(
            comments,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = CommentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class TaskCommentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, task_id):

        comments = Comment.objects.filter(
            task_id=task_id
        ).select_related(
            'user'
        ).order_by(
            '-created_at'
        )

        serializer = CommentSerializer(
            comments,
            many=True
        )

        return Response(
            serializer.data
        )
    

class CommentDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self, pk):

        try:

            return Comment.objects.get(
                pk=pk
            )

        except Comment.DoesNotExist:

            return None
        
    def get(self, request, pk):

        comment = self.get_object(pk)

        if not comment:

            return Response(
                {
                    "error":
                    "Comment not found"
                },
                status=404
            )

        serializer = CommentSerializer(
            comment
        )

        return Response(
            serializer.data
        )
    def delete(self, request, pk):

        if not request.user.is_staff:

            return Response(
                {
                    "error":
                    "Only admin can delete comments"
                },
                status=403
            )

        comment = self.get_object(pk)

        if not comment:

            return Response(
                {
                    "error":
                    "Comment not found"
                },
                status=404
            )

        comment.delete()

        return Response(
            {
                "message":
                "Comment deleted"
            }
        )
    
class TaskReorderAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request):
        if not request.user.is_staff:
            return Response(
                {
                    "error":
                    "Only admin can reorder tasks"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        task = request.data
        for item in task:
            task = Task.objects.filter(id=item['id']).first()
            if task:
                task.position = item['position']
                task.save()
        return Response({
                "message":
                "Order updated successfully"
            })
    

class ExportPDFAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        if not request.user.is_staff:

            return Response(
                {
                    "error":
                    "Admin only"
                },
                status=403
            )

        response = HttpResponse(
            content_type='application/pdf'
        )

        response[
            'Content-Disposition'
        ] = 'attachment; filename="tasks.pdf"'

        pdf = canvas.Canvas(
            response
        )

        pdf.setFont(
            "Helvetica-Bold",
            16
        )

        pdf.drawString(
            220,
            800,
            "Task Report"
        )

        tasks = Task.objects.order_by(
            'position'
        )

        y = 760

        for task in tasks:

            pdf.drawString(
                50,
                y,
                f"{task.code}"
            )

            pdf.drawString(
                120,
                y,
                task.name
            )

            pdf.drawString(
                300,
                y,
                task.priority
            )

            pdf.drawString(
                400,
                y,
                task.status
            )

            y -= 25

        pdf.save()

        return response
    


class ExportExcelAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        if not request.user.is_staff:

            return Response(
                {
                    "error":
                    "Admin only"
                },
                status=403
            )

        workbook = openpyxl.Workbook()

        sheet = workbook.active

        sheet.title = "Tasks"

        sheet.append([

            "Code",
            "Name",
            "Priority",
            "Status",
            "Due Date"

        ])

        tasks = Task.objects.order_by(
            'position'
        )

        for task in tasks:

            sheet.append([

                task.code,

                task.name,

                task.priority,

                task.status,

                str(task.due_date)

            ])

        response = HttpResponse(
            content_type=
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response[
            'Content-Disposition'
        ] = 'attachment; filename="tasks.xlsx"'

        workbook.save(
            response
        )

        return response