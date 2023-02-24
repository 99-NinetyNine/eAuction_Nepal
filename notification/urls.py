from django.urls import path

from . import views
urlpatterns = [
    #notification alerts
    path('alerts/',views.ListAlertsView.as_view(),name='notification_list'),
    path('alerts/handle',views.ListHandleView.as_view(),name='handle_notification'),
]