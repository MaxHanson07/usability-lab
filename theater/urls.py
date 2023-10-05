from django.urls import path
from rest_framework_nested import routers
from .views import NoteCreateView, NoteUpdateView, NoteDeleteView, TestView, VideoCreateView, VideoDeleteView
from . import views

urlpatterns = [
    path('', views.home, name='theater'),
    path('test/<int:pk>/', TestView.as_view(), name="theater-detail"),
    path('test/<int:pk>/note/new/', NoteCreateView.as_view(), name='note-create'),
    path('test/<int:pk_alt>/note/edit/<int:pk>/', NoteUpdateView.as_view(), name='note-update'),
    path('test/<int:pk_alt>/note/delete/<int:pk>/', NoteDeleteView.as_view(), name='note-delete'),
    path('test/<int:pk>/video/new/', VideoCreateView.as_view(), name='video-create'),
    path('test/<int:pk_alt>/video/delete/<int:pk>/', VideoDeleteView.as_view(), name='video-delete'),
    path('test/<int:pk>/transcript/new/', views.TranscriptCreate, name='transcript-create'),
    # path('testjson/<int:pk>/', TestJsonDetailView.as_view(), name="test-json"),

]
# router = routers.DefaultRouter()
# router.register('tests', views.TestView, basename='tests')

# tests_router = routers.NestedDefaultRouter(router, 'tests', lookup='test')
# tests_router.register('notes', views.NotesUpdateForm, basename='product-notes')

# tests_router = routers.NestedDefaultRouter(router, 'tests', lookup='usabilitytest')
# tests_router.register('notes, views.ReviewViewSet, basename='test-notes')
# tests_router.register('videos, views.ReviewViewSet, basename='test-videos')

# products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

# urlpatterns = router.urls + tests_router