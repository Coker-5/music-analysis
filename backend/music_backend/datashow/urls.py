# datashow/urls.py

from django.urls import path
from datashow.views import (
    head, center_data,
    centerLeft1, centerLeft2,
    centerRight1, centerRight2,
    bottomLeft, bottomRight,
)

urlpatterns = [
    path("head/",         head,         name="head"),
    path("centerData/",   center_data,  name="centerData"),
    path("centerLeft1/",  centerLeft1,  name="centerLeft1"),
    path("centerLeft2/",  centerLeft2,  name="centerLeft2"),
    path("centerRight1/", centerRight1, name="centerRight1"),
    path("centerRight2/", centerRight2, name="centerRight2"),
    path("bottomLeft/",   bottomLeft,   name="bottomLeft"),
    path("bottomRight/",  bottomRight,  name="bottomRight"),
]
