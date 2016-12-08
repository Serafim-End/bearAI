# coding: utf-8

from django.conf.urls import url

from rest_framework import routers

import views


router = routers.DefaultRouter()


urlpatterns = [
    url(r'^receive/', views.TelegramBotView.as_view(), name='receive'),

]
