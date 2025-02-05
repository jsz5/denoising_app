from django.urls import path

from images import views

urlpatterns = [
    path(
        "upload/",
        views.UploadImage.as_view(),
        name="upload",
    ),
    path(
        "image-processing/",
        views.ImageProcessingView.as_view(),
        name="image-processing",
    ),
    path(
        "remove-noise/",
        views.RemoveNoise.as_view(),
        name="remove-noise",
    ),
    path(
        "remove-image/",
        views.RemoveImage.as_view(),
        name="remove-image",
    )
]
