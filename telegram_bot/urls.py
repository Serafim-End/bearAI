# coding: utf-8

from django.conf.urls import url

from rest_framework import routers

import views
import views_new


router = routers.DefaultRouter()


urlpatterns = [
    url(r'^receive/', views.TelegramBotView.as_view(),
        name='receive'),

    url(r'^receive_new/', views_new.TelegramBotView.as_view(),
        name='receive_new'),
]
