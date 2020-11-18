from django.urls import path
from . import views
#New import for media files
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newreport",views.new_report, name="newreport"),
    path("inactive", views.inactive, name="inactive"),
    path("report/<int:report_id>", views.report, name="report"),
    path("plot",views.plot,name="plot"),
    path("solved/<int:report_id>",views.solved, name="solved"),
    path("pending/<int:report_id>", views.pending, name = "pending"),
    path("pending", views.pending_report, name = "pending_report"),
    path("pendingitem/<int:pending_item_id>",views.pending_item,name = "pending_item"),
    path("unattended", views.unattended, name="unattended")

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)