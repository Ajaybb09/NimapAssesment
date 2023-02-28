from datetime import date, datetime
from django.shortcuts import render
from rest_framework.response import Response    
from .models import Employee , EmployeeToken , Client , Project
from .serializers import EmployeeSerializer , ClientSerilaizer,ProjectSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import authentication_classes
from .jwt import customerJWTAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


#Add user

@api_view(['POST'])
@authentication_classes([customerJWTAuthentication,])
@permission_classes([IsAuthenticated,])
def Adduser(request):
    detail=[]
    data={}
    user = request.user.id
    print("userid",user)
    data['Name'] = request.POST.get('Name')
    data['email'] = request.POST.get('email')
    data['Createdby'] = str(user)
    data['password'] = make_password(request.POST.get('password'))
    serializer = EmployeeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        for s in [serializer.data]:
            if s['Createdby'] is not None:
                    userobj = Employee.objects.filter(id =  s['Createdby']).first()
                    print(userobj)
                    print(userobj.Name)
                    s['Createdby'] = userobj.Name
                    detail.append(s)
        Response_= {
                        "data":detail[0],
                        "response":{ 
                            "n":1,
                            "msg":"User has been Added successfully",
                            "Status":"Success"

                        }
                    }

        return Response(Response_)
    else:
        Response_= {
                        "data":serializer.errors,
                        "response":{
                            "n":0,
                            "msg":"User Cannot be added",
                            "Status":"Fail"

                        }
                    }

        return Response(Response_)       


@api_view(['GET'])
def getalluser(request):
     item = Employee.objects.all()
     serializer = EmployeeSerializer(item , many= True)
     for i in serializer.data:
            if i['Createdby'] is not None:
                userobj = Employee.objects.filter(id =  i['Createdby']).first()
                i['Createdby'] = userobj.Name
     return Response(serializer.data)


@api_view(['POST'])
def Login(request):
    email = request.POST.get('email')
    password = request.POST.get("password")
    EmailObj = Employee.objects.filter(email=email).first()
    print(EmailObj)
    serializer = EmployeeSerializer(EmailObj)
    if email is not None:    
            check = check_password(password,EmailObj.password)    
            if check == True:
                checkbj = EmployeeToken.objects.filter(Employee=EmailObj.id,isactive=True).first()
                if checkbj is not None:
                    EmployeeToken.objects.filter(Employee=EmailObj.id,isactive=True).update(isactive=False)
                Token = EmployeeToken.objects.create(Employee = EmailObj.id , authToken = EmailObj.token)
                return Response({
                                "n":1,
                                "msg":"Login Succes ",
                                "Status":"Success",
                                "token":Token.authToken,
                                "ser":serializer.data,
                            })
            else:
                Response_ = {
                                
                                "n":0,
                                "msg":"Login Failed ",
                                "Status":"Login Failed"

                                }
                            
                return Response(Response_) 
    else:
        Response_ = {
                                
                                "n":0,
                                "msg":"Employee With this Email Does not Exists ",
                                "Status":"Login Failed"

                                }
                            
        return Response(Response_)    
    

#CREATING CLIENT

@api_view(['POST'])
@authentication_classes([customerJWTAuthentication,])
@permission_classes([IsAuthenticated,])
def addclient(request):
    detail=[]
    user = request.user.id
    data={}
    data['client_name'] = request.POST.get('client_name')
    data['Createdby'] = str(user)
    serializer = ClientSerilaizer(data=data)
    if serializer.is_valid():
        serializer.save()
        for s in [serializer.data]:
            if s['Createdby'] is not None:
                    userobj = Employee.objects.filter(id =  s['Createdby']).first()
                    print(userobj)
                    print(userobj.Name)
                    s['Createdby'] = userobj.Name
                    detail.append(s)
        Response_= {
                        "data":detail[0],
                         
                    }

        return Response(Response_)
    else:
        Response_= {
                        "data":serializer.errors,
                        "response":{
                            "n":0,
                            "msg":"client data Cannot be added",
                            "Status":"Fail"

                        }
                    }

        return Response(Response_)   


@api_view(['GET'])
def getallclients(request):
    item = Client.objects.all()
    serializer = ClientSerilaizer(item , many= True)
    for i in serializer.data:
        if i['Createdby'] is not None:
            userobj = Employee.objects.filter(id = i['Createdby']).first()
            print(userobj)
            i['Createdby'] = userobj.Name
    return Response(serializer.data)


@api_view(['GET'])
def getclients(request, id):
    item = Client.objects.filter(id=id).first()
    print(item)
    serializer = ClientSerilaizer(item)
    
    if serializer.data['Createdby'] is not None:
            userobj = Employee.objects.filter(id = serializer.data['Createdby']).first()
            print(userobj)
            serializer.data['Createdby'] = userobj.Name   
    proobj = Project.objects.filter(client_id = id)
    ser = ProjectSerializer(proobj, many = True)
    plist=[]
    for k in ser.data:
        prolist ={
            'id': k['id'],
            'name' : k['project_name']
        }
        plist.append(prolist)
    print(plist)
    maindata={
        'id':serializer.data['id'],
        'client_name' : serializer.data['client_name'],
        'projects':plist,
        'created_at':serializer.data['created_at'],
        'created_by':userobj.Name,
        'updated_at':serializer.data['updated_at']
    }

    return Response(maindata,status=200)




@api_view(['PUT'])
def updateclient(request, id):
    detail=[]
    item = Client.objects.filter(id = id).first()
    dates = datetime.now()
    data = {}
    data['client_name'] = request.POST.get('client_name')
    data['updated_at'] = dates
    serializer = ClientSerilaizer(item , data=data, partial = True)
    if serializer.is_valid():
        serializer.save()
        for s in [serializer.data]:
            if s['Createdby'] is not None:
                    userobj = Employee.objects.filter(id =  s['Createdby']).first()
                    print(userobj)
                    print(userobj.Name)
                    s['Createdby'] = userobj.Name
                    detail.append(s)
        Response_= {
                        "data":detail[0],
                        "response":{ 
                            "n":1,
                            "msg":"client  data has been Updated successfully",
                            "Status":"Success"

                        }
                    }

        return Response(Response_)
    else:
        Response_= {
                        "data":serializer.errors,
                        "response":{
                            "n":0,
                            "msg":"client data Cannot be Updated",
                            "Status":"Fail"

                        }
                    }

        return Response(Response_)   


@api_view(['DELETE'])
def deleteclient(request, id):
    item = Client.objects.filter(id=id).first()
    item.delete()
    return Response(status=204)


@api_view(['POST'])
@authentication_classes([customerJWTAuthentication,])
@permission_classes([IsAuthenticated,])
def CreateProject(request,id):
    detail=[]
    data={}
    data['client_id'] = id
    data['Createdby'] = str(request.user.id)
    data['user_id'] = request.POST.getlist('user_id')
    data['project_name'] = request.POST.get('project_name')
    serializer = ProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        userlist=[]
        for s in [serializer.data]:
            userobj = Employee.objects.filter(id =  s['Createdby']).first()

            s['Createdby'] = userobj.Name            
            clietobj = Client.objects.filter(id=s['client_id']).first()
            s['client_id'] = clietobj.client_name
            for k in s['user_id']:    
                    useridobj = Employee.objects.filter(id= k ).first()
                    user_data={
                         'id':useridobj.id,
                         'name':useridobj.Name
                    }
                    userlist.append(user_data)
            s['users']=userlist
            maindata={
                 'id':serializer.data['id'],
                 'project_name':serializer.data['project_name'],
                 'users':s['users'],
                 'created_at':serializer.data['created_at'],
                 'created_by':userobj.Name
            }
            detail.append(maindata)
        print("detail",detail)
        Response_= {
                        "data":detail[0],
                        "response":{ 
                            "n":1,
                            "msg":"client  data has been Added successfully",
                            "Status":"Success"

                        }
                    }

        return Response(Response_)
    else:
         print("error",serializer.errors)


#list of all projects assigned to the logged-in User

@api_view(['GET'])
@authentication_classes([customerJWTAuthentication,])
@permission_classes([IsAuthenticated,])
def getprojects(request):
    detail=[]
    item = Project.objects.filter(user_id = request.user.id)
    serializer = ProjectSerializer(item , many=True)
    for i in serializer.data:
        userobj = Employee.objects.filter(id=i['Createdby']).first()
        maindata={
                'id' : i['id'],
                'project_name' : i['project_name'],
                'created_at' : i['created_at'], 
                'Createdby':userobj.Name

        }
        detail.append(maindata)
    print(detail)
    Response_={
          "data":detail,
    }   
    return Response(Response_)


