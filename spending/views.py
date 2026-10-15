from django.shortcuts import render,get_object_or_404

# Create your views here.

from rest_framework.views import APIView
from spending.serializers import UserSerializer,ExpenseSerializer
from rest_framework.response import Response

from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from spending.models import Expense
from spending.permissions import IsOwner


class SignupView(APIView):

    def post(self,request):

        form_data=request.data

        serializer_instance=UserSerializer(data=form_data)

        if serializer_instance.is_valid():

             cleaned_data=serializer_instance.validated_data

             user_object=User.objects.create_user(**cleaned_data)


             serializer_instance=UserSerializer(user_object)

             return Response(data=serializer_instance.data)
        else:

            return Response(data=serializer_instance.errors)


class GetmeView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user=request.user

        instance=User.objects.get(username=auth_user)

        serializer_instance=UserSerializer(instance)

        return Response(data=serializer_instance.data)

class ExpenseListCreateView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        qs=Expense.objects.filter(owner=request.user)

        serializer_instance=ExpenseSerializer(qs,many=True)


        return Response(data=serializer_instance.data)

    def post(self,request):


        form_data=request.data

        serializer_instance=ExpenseSerializer(data=form_data)


        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)
        else:

            return Response(data=serializer_instance.errors)
class ExpenseRetirveUpdateView(APIView):
    
    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[IsOwner]

    def get(self,request,pk=None):

        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance=ExpenseSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)


        form_data=request.data

        serialiser_instance=ExpenseSerializer(data=form_data,instance=instance)

        if serialiser_instance.is_valid():

            serialiser_instance.save()

            # cleaned_data=serialiser_instance.validated_data

            # qs=Expense.objects.filter(id=pk).update(**cleaned_data)

            # serialiser_instance=ExpenseSerializer(qs,many=True)

            return Response(data=serialiser_instance.data)

        else:
            return Response(data=serialiser_instance.errors)

    def delete(self,request,pk=None):

        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        # qs=Expense.objects.filter(id=pk).delete()

        # serialiser_instance=ExpenseSerializer(qs)

        instance.delete()


        return Response({"message":"deleteed"})
    
from datetime import datetime
from django.db.models import Sum
class ExpenseSummary(APIView):
    authentication_classes=[authentication.TokenAuthentication]


    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={

            "todays_total":0
         }
        
        cur_date=datetime.now().date()
        cur_month=datetime.now().month
        cur_year=datetime.now().year
        
        #monthly transactions

        monthly_transaction=Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_transaction:

            monthly_total=monthly_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            response_data["monthly_total"]=monthly_total

        #todays transaction

        todays_transaction=Expense.objects.filter(owner=request.user,created_at__date=cur_date)

        if todays_transaction:

            todays_expense=todays_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            category_sum=todays_transaction.values("category").annotate(total=Sum("amount"))

            response_data["todays_total"]=todays_expense
            response_data["category_summary"]=category_sum
            #response_data={"todays_total":todays_expense}

        return Response(data=response_data)


from spending.ai_service import get_budget_plan
class BudegetPlanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={

            "total_expense":0

        }

        cur_month=datetime.now().month

        cur_year=datetime.now().year

        monthly_transaction=Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_transaction:

            monthly_total=monthly_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            response_data["monthly_total"]=monthly_total

            category_summary=monthly_transaction.values("category").annotate(total=Sum("amount"))

            response_data["category_summary"]=category_summary
            
            budeget_plan=get_budget_plan(response_data)
            
            response_data["plan"]=budeget_plan

        return Response(data=response_data)