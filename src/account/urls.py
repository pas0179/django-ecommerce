from django.urls import path
# Utilisation ddes vues personnalisé pour login et logout
from .views import login_user, logout_user, dashboard, register, edit, activate

# Vue auto de django.auth
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)


urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/<int:orders_id>/", dashboard, name="order_list_by_order"),
    path("register/", register, name="register"),
    path("edit/", edit, name="edit"),
    # url redirige si authentification sur login
    path('activate/<uidb64>/<token>', activate, name='activate'),

    

    # integration des vues django.auth pour modifié et reset du mot de passe
    # change password urls
    path('password-change/',
        PasswordChangeView.as_view(
            # Modification du chemin du fichier html qui par defaut doit
            # être dans un dossier registration
            template_name="account/password_change.html",
            ),
        name='password_change',
    ),

    path('password-change/done/',
        PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html",
            ),
        name="password_change_done",
    ),

    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="account/password_reset.html",
            ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html",
            ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),

]