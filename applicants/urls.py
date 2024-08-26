from django.urls import path
from .views import CreateApplicantView, SearchApplicantsView, ShortlistApplicantView, RejectApplicantView, \
    NameBasedSearchView

urlpatterns = [
    path('create/', CreateApplicantView.as_view(), name='create-applicant'),
    path('search/', SearchApplicantsView.as_view(), name='search-applicants'),
    path('shortlist/<int:pk>/', ShortlistApplicantView.as_view(), name='shortlist-applicant'),
    path('reject/<int:pk>/', RejectApplicantView.as_view(), name='reject-applicant'),
    path('search-by-name/', NameBasedSearchView.as_view(), name='search-by-name'),
]
