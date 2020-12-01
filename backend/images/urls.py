from django.urls import path

from images import views

urlpatterns = [
    path(
        "upload",
        views.UploadImage.as_view(),
        name="upload",
    ),
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
