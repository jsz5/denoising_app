from django.urls import path

from images import views

urlpatterns = [
    path(
        "add-noise",
        views.AddNoiseView.as_view(),
        name="add-noise",
    ),
    path(
        "remove-noise",
        views.RemoveNoise.as_view(),
        name="remove-noise",
    ),

]
