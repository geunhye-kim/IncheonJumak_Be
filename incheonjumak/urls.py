from django.contrib import admin
from django.urls import path,include, re_path
from incheonjumak import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Incheon Jumak",
        default_version='v1',
        description="Incheon Jumak test API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="incheonjumak@gmail.com"),
        license=openapi.License(name="A2_YUNIBUS"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('review/', include("review.urls")),
    path('alchol/', include('alchol.urls')),
    path('brewery/', include('brewery.urls')),
    path('event/', include('information.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)