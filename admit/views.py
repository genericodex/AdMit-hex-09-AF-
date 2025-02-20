from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from .models import School, Applicant, Application, Payment
from .serializers import SchoolSerializer, ApplicantSerializer, ApplicationSerializer, PaymentSerializer,TestimonialSerializer

@api_view(['GET'])
def home(request):
    #documentation
    return Response({
        "message":"Welcome to the admit API",
        "endpoints": {
            "GET /schools/": "Get all schools",
            "POST /create_school/": "Create a school",
            "POST /create_applicant/": "Create an applicant",
            "POST /submit_application/": "Submit an application",
            "POST /submit_payment/": "Submit a payment",
            "GET /view_application/<int:application_id>/": "View a specific application",
            "GET /view_payment/<int:payment_id>/": "View a specific payment",
            "GET /view_school/<int:school_id>/": "View a specific school",
            "GET /view_applicant/<int:applicant_id>/": "View a specific applicant",
            "PUT /edit_application/<int:application_id>": "Edit a specific application",
            "PUT /edit_applicant/<int:applicant_id>": "Edit a specific applicant",
            "POST /upload_testimonial/": "Upload a testimonial",
            "GET /applications/": "View all applications",
            "GET /my-applications/<application_id>/" : "View applications personal to the logged in user"
            }

        
        })

@api_view(['GET'])
def schools(request):
    schools = School.objects.all()
    serialized_schools = SchoolSerializer(schools, many=True)
    return Response(serialized_schools.data)

@api_view(['POST'])
def create_school(request):
    serialized_school = SchoolSerializer(data=request.data)
    if serialized_school.is_valid():
        serialized_school.save()
        return Response(serialized_school.data)
    return Response(serialized_school.errors)

#create applicant
@api_view(['POST'])
def create_applicant(request):
    serialized_applicant = ApplicantSerializer(data=request.data)
    if serialized_applicant.is_valid():
        serialized_applicant.save()
        return Response(serialized_applicant.data)
    return Response(serialized_applicant.errors)

#create a view for the applicants to submit their applications
@api_view(['POST'])
def submit_application(request):
    serialized_application = ApplicationSerializer(data=request.data)
    if serialized_application.is_valid():
        serialized_application.save()
        return Response(serialized_application.data)
    return Response(serialized_application.errors)

#create a view for the applicants to submit their payments
@api_view(['POST'])
def submit_payment(request):
    serialized_payment = PaymentSerializer(data=request.data)
    if serialized_payment.is_valid():
        serialized_payment.save()
        return Response(serialized_payment.data)
    return Response(serialized_payment.errors)

#view for someone to view a specific application
@api_view(['GET'])
def view_application(request,application_id):
    application = Application.objects.get(id=application_id)
    serialized_application = ApplicationSerializer(application)
    return Response(serialized_application.data)

#view for someone to view a specific payment
@api_view(['GET'])
def view_payment(request,payment_id):
    payment = Payment.objects.get(id=payment_id)
    serialized_payment = PaymentSerializer(payment)
    return Response(serialized_payment.data)

#view all applications
@api_view(['GET'])
def view_applications(request):
    applications = Application.objects.all()
    serialized_applications = ApplicationSerializer(applications, many=True)
    return Response(serialized_applications.data)

#view applications for logged in user
@api_view(['GET'])
def view_personal_applications(request,applicant_id):
    user = request.user
    #get count of pending applications
    pending_applications_count = Application.objects.filter(applicant=applicant_id, status='pending').count()
    #accepted applications
    accepted_applications_count = Application.objects.filter(applicant=applicant_id, status='accepted').count()
    
    applications = Application.objects.filter(applicant=applicant_id)
    serialized_applications = ApplicationSerializer(applications, many=True)
    #return serialized applications and application counts
    return Response({'applications': serialized_applications.data, 'pending_applications_count': pending_applications_count, 'accepted_applications_count': accepted_applications_count})

#view for someone to view a specific school
@api_view(['GET'])
def view_school(request,school_id):
    school = School.objects.get(id=school_id)
    serialized_school = SchoolSerializer(school)
    return Response(serialized_school.data)

#view for someone to view a specific applicant
@api_view(['GET'])
def view_applicant(request,applicant_id):
    applicant = Applicant.objects.get(id=applicant_id)
    serialized_applicant = ApplicantSerializer(applicant)
    return Response(serialized_applicant.data)

#view to edit a specific application
@api_view(['PUT'])
def edit_application(request,application_id):
    application = Application.objects.get(id=application_id)
    serialized_application = ApplicationSerializer(instance=application, data=request.data)
    if serialized_application.is_valid():
        serialized_application.save()
        return Response(serialized_application.data)
    return Response(serialized_application.errors)

#view to edit applicant information
@api_view(['PUT'])
def edit_applicant(request,applicant_id):
    applicant = Applicant.objects.get(id=applicant_id)
    serialized_applicant = ApplicantSerializer(instance=applicant, data=request.data)
    if serialized_applicant.is_valid():
        serialized_applicant.save()
        return Response(serialized_applicant.data)
    return Response(serialized_applicant.errors)

#viewset to handle testimonial uploads
class TestimonialViewSet(ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = TestimonialSerializer

    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        #applicant = Applicant.objects.get(id=self.request.user.id)
        serializer.save(
                       file=self.request.data.get('file'))
        return Response({"message":"Testimonial uploaded successfully"})