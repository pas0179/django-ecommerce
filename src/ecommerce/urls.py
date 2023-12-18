
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# Pour mettre une page de démarrage en place
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("store/", include("store.urls")),
    path("", RedirectView.as_view(url="/store/", permanent=True)),
    path("product/", include("product.urls")),
    path("account/", include("account.urls")),
    path("contact/", include("contact.urls")),
    path('cart/', include("cart.urls")),
    path("order/", include("order.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

