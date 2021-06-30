from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('group', GroupViewSet, basename='group')
router.register(r'posts/(?P<post_id>[\da-z]+)/comments',
                CommentViewSet, basename='comment')
router.register('follow', FollowViewSet, basename='follow')

jwt = [
    path(
        '',
        views.TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
    path(
        'refresh/',
        views.TokenRefreshView.as_view(),
        name="jwt-refresh"
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', include(jwt)),
]
