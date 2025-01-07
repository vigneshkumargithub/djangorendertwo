# from .models import AcademicSession, AcademicTerm


# class SiteWideConfigs:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         current_session = AcademicSession.objects.get(current=True)
#         current_term = AcademicTerm.objects.get(current=True)

#         request.current_session = current_session
#         request.current_term = current_term

#         response = self.get_response(request)

#         return response


##### updated for render deployment

# from django.core.exceptions import ObjectDoesNotExist
# from .models import AcademicSession, AcademicTerm


# class SiteWideConfigs:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             # Attempt to fetch the current academic session
#             current_session = AcademicSession.objects.get(current=True)
#         except ObjectDoesNotExist:
#             # If no current session exists, set it to None
#             current_session = None

#         try:
#             # Attempt to fetch the current academic term
#             current_term = AcademicTerm.objects.get(current=True)
#         except ObjectDoesNotExist:
#             # If no current term exists, set it to None
#             current_term = None

#         # Add the session and term to the request object
#         request.current_session = current_session
#         request.current_term = current_term

#         # Process the request
#         response = self.get_response(request)
#         return response



### 2nd

from .models import AcademicSession, AcademicTerm

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_session = AcademicSession.objects.get(current=True)
        except AcademicSession.DoesNotExist:
            current_session = None  # or some default handling

        try:
            current_term = AcademicTerm.objects.get(current=True)
        except AcademicTerm.DoesNotExist:
            current_term = None  # or some default handling

        # Attach to the request object for use in views/templates
        request.current_session = current_session
        request.current_term = current_term

        response = self.get_response(request)
        return response
