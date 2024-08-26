from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Applicant
from .serializers import ApplicantSerializer

# Create your views here.

class CreateApplicantView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer


class SearchApplicantsView(generics.ListAPIView):
    serializer_class = ApplicantSerializer

    def get_queryset(self):
        queryset = Applicant.objects.all()
        query_params = self.request.query_params

        # Search for applicants whose expected salary is between given range.
        min_salary = query_params.get('min_salary', None)
        max_salary = query_params.get('max_salary', None)
        if min_salary and max_salary:
            queryset = queryset.filter(expected_salary__gte=min_salary, expected_salary__lte=max_salary)

        # Search for applicants whose age is between given age range.
        min_age = query_params.get('min_age', None)
        max_age = query_params.get('max_age', None)
        if min_age and max_age:
            queryset = queryset.filter(age__gte=min_age, age__lte=max_age)

        # Search for applicants whose years of experience is more than specified age.
        min_exp = query_params.get('min_exp', None)
        if min_exp:
            queryset = queryset.filter(years_of_exp__gt=min_exp)

        # Search for applicant by name, phone number, email or status.
        name = query_params.get('name', None)
        email = query_params.get('email', None)
        phone_number = query_params.get('phone_number', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if phone_number:
            queryset = queryset.filter(phone_number__icontains=phone_number)

        # Search for applicant by status
        status = query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


# TODO: remove id use code
class ShortlistApplicantView(generics.UpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def patch(self, request, *args, **kwargs):
        applicant = self.get_object()
        applicant.status = 'Shortlisted'
        applicant.save()
        return Response(ApplicantSerializer(applicant).data)


class RejectApplicantView(generics.UpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def patch(self, request, *args, **kwargs):
        applicant = self.get_object()
        applicant.status = 'Rejected'
        applicant.save()
        return Response(ApplicantSerializer(applicant).data)


class NameBasedSearchView(APIView):
    def get(self, request):
        queryset = Applicant.objects.all()
        query = request.query_params.get('query', '').strip()

        if not query:
            return Response([])

        query_words = query.lower().split()

        # Find exact match
        exact_matches = queryset.filter(name__iexact=query)

        # Find partial matches
        partial_matches = queryset.none()
        for word in query_words:
            word_matches = queryset.filter(name__icontains=word)
            partial_matches = partial_matches.union(word_matches)

        # Sort matches by the number of matching words
        partial_matches = list(partial_matches)
        partial_matches.sort(key=lambda applicant: sum(word in applicant.name.lower() for word in query_words), reverse=True)

        # Combine exact matches with partial matches
        combined_results = list(exact_matches) + [candidate for candidate in partial_matches if candidate not in exact_matches]

        # Serialize and return the results
        serializer = ApplicantSerializer(combined_results, many=True)

        return Response(serializer.data)
