from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('group', GroupViewSet)
router.register(r'posts/(?P<post_id>[\d]+)/comments',
                CommentViewSet, basename='comment')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/token/',
        views.TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
    path(
        'v1/token/refresh/',
        views.TokenRefreshView.as_view(),
        name="jwt-refresh"
    ),
]
