from django.urls import path, include
from rest_framework.routers import DefaultRouter
from msn_app.views import PostView, LikeView, UserView

router = DefaultRouter()
router.register(r'users', UserView)
router.register(r'posts', PostView)
router.register(r'likes', LikeView)

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('', include(router.urls)),
]
