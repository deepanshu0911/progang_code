from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from operations.models import ProgangUser, Consultation, Quotation, Proposal, Feedback
from django.db.models import Q
from operations.serializers import UserSerializer, ConsultSerializer, QuotationSerializer, ProposalSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views import View
from django.contrib.auth.hashers import make_password, check_password


@csrf_exempt
def userSignup(request):
  if request.method == "POST":
    data = JSONParser().parse(request)
    if not ProgangUser.objects.filter(email=data['email']).exists():
     user = ProgangUser.objects.create(firstName=data['firstName'], lastName=data['lastName'],
     email=data['email'])
     user.is_active = False
     mail_subject = 'Activate your account.'
     current_site = get_current_site(request)
     uid = urlsafe_base64_encode(force_bytes(user.pk))
     token = account_activation_token.make_token(user)
     user.signupToken = token
     user.save()
     activation_link = "{0}/api/activate/{1}/{2}".format(current_site, uid, token)
     message = "Welcome to Progang {0},\n {1}".format(user.firstName+' '+user.lastName, activation_link)
     email = EmailMessage(mail_subject, message, to=[data['email']])
     email.send()
     return JsonResponse("E-mail Sent", safe=False)
    else:
      return JsonResponse("User exists", safe=False) 

def activate(request, uidb64, token):
    # try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = ProgangUser.objects.get(pk=uid, is_active=False, password=None, signupToken=token)
    # except(TypeError, ValueError, OverflowError):
      #  user = None 
      #  print("User None")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        redirect_link = 'http://localhost:4200/set-password/' + user.email + '/' + token
        return redirect(redirect_link)
    else:
      redirect_link = 'http://localhost:4200/signup'
      return redirect(redirect_link)
    
def checkActive(request, email, token):
  if request.method == "GET":
    user = ProgangUser.objects.get(email=email, is_active=False, signupToken=token)
    if user.is_active:
      return JsonResponse('Active', safe=False)

@csrf_exempt
def setPassword(request):
  if request.method == "POST":
    data = JSONParser().parse(request)
    try:
     user = ProgangUser.objects.get(email=data['email'])
     user.password = make_password(data['password'])
     user.save()
     return JsonResponse('Done', safe=False)
    except:
      return JsonResponse("Error", safe=False)  


# Google user signup
@csrf_exempt
def user(request):
    if request.method == "POST":
        data =  JSONParser().parse(request)
        if not ProgangUser.objects.filter(email=data['email']).exists():
          user = ProgangUser.objects.create(google_id=data['id'], photoUrl=data['photoUrl'],
          email= data['email'], firstName= data['firstName'], lastName=data['lastName'])
          user.save()
          userData = UserSerializer(user, many=True)
          return JsonResponse({'status': 'mobile', 'user': userData.data}, safe=False)
        elif ProgangUser.objects.filter(email=data['email']).exists():
            user = ProgangUser.objects.get(email=data['email'])
            fetchUser = ProgangUser.objects.filter(email=data['email'])
            userData = UserSerializer(fetchUser, many=True)
            if user.mobile is None:
              return JsonResponse({'status':"mobile", 'user': userData.data}, safe=False)    
            else:
             return JsonResponse({'status':"allset", 'user': userData.data}, safe=False)    
        else:
            return JsonResponse("error", safe=False)
    return HttpResponse("Hello")

@csrf_exempt
def userLogin(request):
   if request.method == "POST":
     data = JSONParser().parse(request)
     if ProgangUser.objects.filter(email=data['email'], is_active=True).exists():
       user = ProgangUser.objects.get(email=data['email'])
       loginPassword = data['password']
       check = check_password(loginPassword, user.password)
       if check:
        userFilter = ProgangUser.objects.filter(email=data['email'], is_active=True)
        userData = UserSerializer(userFilter, many=True)
        return JsonResponse({'user': userData.data,'status':"Done"}, safe=False)
       else:
        return JsonResponse({'status' : "Wrong"}, safe=False)
     else:
       return JsonResponse({"status": "No account"}, safe=False)    

@csrf_exempt
def requestConsult(request):
  if request.method == "POST":
    data = JSONParser().parse(request)
    if data['id']!=0:
      Consultation.objects.create(user_id=data['id'], name=data['name'],
      email=data['email'], mobile=data['mobile'], consultType=data['consultType'],
      slot=data['slot'])
      return JsonResponse("Done", safe=False)
    elif not ProgangUser.objects.filter(id=data['id']).exists():
      Consultation.objects.create(user_id=-1,name=data['name'],
      email=data['email'], mobile=data['mobile'], consultType=data['consultType'],
      slot=data['slot'])
      return JsonResponse("Done", safe=False) 
    else:
      return JsonResponse("Error", safe=False)  

@csrf_exempt
def requestQuote(request):
  if request.method == "POST":
    data = JSONParser().parse(request)
    if data['id']!=0:
      Quotation.objects.create(user_id=data['id'], name=data['name'],
      emailOrMobile=data['emailOrMobile'], platform=data['platform'],
      requirements=data['requirements'])
      return JsonResponse("Done", safe=False)
    elif not ProgangUser.objects.filter(id=data['id']).exists():
      Quotation.objects.create(user_id=-1,name=data['name'],
      emailOrMobile=data['emailOrMobile'], platform=data['platform'],
      requirements=data['requirements'])
      return JsonResponse("Done", safe=False) 
    else:
      return JsonResponse("Error", safe=False)  

@csrf_exempt
def requestProposal(request, *args, **kwargs):
  if request.method == "POST":
    # data = JSONParser().parse(request)
    userId = request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    mobile = request.POST['mobile']
    platform = request.POST.get('platform')
    requirements = request.POST['requirements']
    theFile = request.FILES.get('file')
    if userId!= '0':
      Proposal.objects.create(user_id=userId, name=name,
      email=email, mobile=mobile, platform=platform,
      requirements=requirements,pdfFile=theFile)
      return JsonResponse("Done", safe=False)
    elif not ProgangUser.objects.filter(id=userId).exists():
      Proposal.objects.create(user_id=userId, name=name,
      email=email, mobile=mobile, platform=platform,
      requirements=requirements,pdfFile=theFile)
      return JsonResponse("Done", safe=False) 
    else:
      return JsonResponse("Error", safe=False)


@csrf_exempt
def getQuote(request):
  if request.method == "POST":
    data = JSONParser().parse(request)
    data = Quotation.objects.filter(user_id=data['id'])
    quotations = QuotationSerializer(data, many=True)
    return JsonResponse(quotations.data, safe=False)
    # return JsonResponse("Error", safe=False)  

@csrf_exempt
def getProposal(request):
  if request.method == "POST":
    data = JSONParser().parse(request)
    data = Proposal.objects.filter(user_id=data['id'])
    proposals = ProposalSerializer(data, many=True)
    return JsonResponse(proposals.data, safe=False)
    # return JsonResponse("Error", safe=False)  

@csrf_exempt
def uploadImage(request):
  if request.method == "POST":
    info = JSONParser().parse(request)
    data = request.FILES.get(info['file'], False)
    print(data)
    # print(data['file'])
    ProgangUser.objects.filter(id=1).update(photoUrl=data)
    return HttpResponse("Done")

@csrf_exempt
def feedback(request):
   if request.method == "POST":
     data = JSONParser().parse(request)
     if data['name'] is not None:
       Feedback.objects.create(name=data['name'], email=data['email'],
       msg=data['msg'])
       return JsonResponse("Done", safe=False)

@csrf_exempt
def profileUpdate(request):
  if request.method == "POST":
    userId = request.POST['id']
    organisation = request.POST.get('organisation')
    mobile = request.POST.get('mobile')
    country = request.POST.get('country')
    state = request.POST.get('state')
    city = request.POST.get('city')
    theFile = request.FILES.get('file')
    if ProgangUser.objects.filter(id=userId).exists():
      user = ProgangUser.objects.get(id=userId)
      user.organisation = organisation
      user.mobile = mobile
      user.country = country
      user.state = state
      user.city = city
      if theFile is not None:
        user.profileImg = theFile
      user.save()
      user = ProgangUser.objects.filter(id=userId)
      userData = UserSerializer(user, many=True)        
      return JsonResponse({'user': userData.data, 'status': "Done"}, safe=False)    
