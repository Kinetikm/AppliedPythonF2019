from django.conf.urls import url
from .views import PostList, PostDetail

urlpatterns = [
    url(r'flights/all/', PostList.as_view()),
    url(r'flights/create/', PostDetail.as_view()),
    # url(r'flights/all', FlightListAPIView.as_view()),
    # url(r'flights/<int:pk>', FlightDetailAPIView.as_view()),
    # url(r'flights/dep_sort', FlightDepListView.as_view()),
    # url(r'flights/air_sort', FlightArrListView.as_view()),
]