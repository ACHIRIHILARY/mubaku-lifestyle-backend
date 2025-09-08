/admin/ django.contrib.admin.sites.index        admin:index
/admin/<app_label>/     django.contrib.admin.sites.app_index    admin:app_list
/admin/<url>    django.contrib.admin.sites.catch_all_view
/admin/account/emailaddress/    django.contrib.admin.options.changelist_view    admin:account_emailaddress_changelist
/admin/account/emailaddress/<path:object_id>/   django.views.generic.base.RedirectView
/admin/account/emailaddress/<path:object_id>/change/    django.contrib.admin.options.change_view        admin:account_emailaddress_change
/admin/account/emailaddress/<path:object_id>/delete/    django.contrib.admin.options.delete_view        admin:account_emailaddress_delete
/admin/account/emailaddress/<path:object_id>/history/   django.contrib.admin.options.history_view       admin:account_emailaddress_history
/admin/account/emailaddress/add/        django.contrib.admin.options.add_view   admin:account_emailaddress_add
/admin/appointments/appointment/        django.contrib.admin.options.changelist_view    admin:appointments_appointment_changelist
/admin/appointments/appointment/<path:object_id>/       django.views.generic.base.RedirectView
/admin/appointments/appointment/<path:object_id>/change/        django.contrib.admin.options.change_view        admin:appointments_appointment_change
/admin/appointments/appointment/<path:object_id>/delete/        django.contrib.admin.options.delete_view        admin:appointments_appointment_delete
/admin/appointments/appointment/<path:object_id>/history/       django.contrib.admin.options.history_view       admin:appointments_appointment_history
/admin/appointments/appointment/add/    django.contrib.admin.options.add_view   admin:appointments_appointment_add
/admin/appointments/appointmentslot/    django.contrib.admin.options.changelist_view    admin:appointments_appointmentslot_changelist
/admin/appointments/appointmentslot/<path:object_id>/   django.views.generic.base.RedirectView
/admin/appointments/appointmentslot/<path:object_id>/change/    django.contrib.admin.options.change_view        admin:appointments_appointmentslot_change
/admin/appointments/appointmentslot/<path:object_id>/delete/    django.contrib.admin.options.delete_view        admin:appointments_appointmentslot_delete
/admin/appointments/appointmentslot/<path:object_id>/history/   django.contrib.admin.options.history_view       admin:appointments_appointmentslot_history
/admin/appointments/appointmentslot/add/        django.contrib.admin.options.add_view   admin:appointments_appointmentslot_add
/admin/appointments/provideravailability/       django.contrib.admin.options.changelist_view    admin:appointments_provideravailability_changelist
/admin/appointments/provideravailability/<path:object_id>/      django.views.generic.base.RedirectView
/admin/appointments/provideravailability/<path:object_id>/change/       django.contrib.admin.options.change_view        admin:appointments_provideravailability_change
/admin/appointments/provideravailability/<path:object_id>/delete/       django.contrib.admin.options.delete_view        admin:appointments_provideravailability_delete
/admin/appointments/provideravailability/<path:object_id>/history/      django.contrib.admin.options.history_view       admin:appointments_provideravailability_history
/admin/appointments/provideravailability/add/   django.contrib.admin.options.add_view   admin:appointments_provideravailability_add
/admin/appointments/provideravailabilityexception/      django.contrib.admin.options.changelist_view    admin:appointments_provideravailabilityexception_changelist
/admin/appointments/provideravailabilityexception/<path:object_id>/     django.views.generic.base.RedirectView
/admin/appointments/provideravailabilityexception/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:appointments_provideravailabilityexception_change
/admin/appointments/provideravailabilityexception/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:appointments_provideravailabilityexception_delete
/admin/appointments/provideravailabilityexception/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:appointments_provideravailabilityexception_history
/admin/appointments/provideravailabilityexception/add/  django.contrib.admin.options.add_view   admin:appointments_provideravailabilityexception_add
/admin/auth/group/      django.contrib.admin.options.changelist_view    admin:auth_group_changelist
/admin/auth/group/<path:object_id>/     django.views.generic.base.RedirectView
/admin/auth/group/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:auth_group_change
/admin/auth/group/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:auth_group_delete
/admin/auth/group/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:auth_group_history
/admin/auth/group/add/  django.contrib.admin.options.add_view   admin:auth_group_add
/admin/autocomplete/    django.contrib.admin.sites.autocomplete_view    admin:autocomplete
/admin/jsi18n/  django.contrib.admin.sites.i18n_javascript      admin:jsi18n
/admin/login/   django.contrib.admin.sites.login        admin:login
/admin/logout/  django.contrib.admin.sites.logout       admin:logout
/admin/notifications/loyaltyprogram/    django.contrib.admin.options.changelist_view    admin:notifications_loyaltyprogram_changelist
/admin/notifications/loyaltyprogram/<path:object_id>/   django.views.generic.base.RedirectView
/admin/notifications/loyaltyprogram/<path:object_id>/change/    django.contrib.admin.options.change_view        admin:notifications_loyaltyprogram_change
/admin/notifications/loyaltyprogram/<path:object_id>/delete/    django.contrib.admin.options.delete_view        admin:notifications_loyaltyprogram_delete
/admin/notifications/loyaltyprogram/<path:object_id>/history/   django.contrib.admin.options.history_view       admin:notifications_loyaltyprogram_history
/admin/notifications/loyaltyprogram/add/        django.contrib.admin.options.add_view   admin:notifications_loyaltyprogram_add
/admin/notifications/notification/      django.contrib.admin.options.changelist_view    admin:notifications_notification_changelist
/admin/notifications/notification/<path:object_id>/     django.views.generic.base.RedirectView
/admin/notifications/notification/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:notifications_notification_change
/admin/notifications/notification/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:notifications_notification_delete
/admin/notifications/notification/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:notifications_notification_history
/admin/notifications/notification/add/  django.contrib.admin.options.add_view   admin:notifications_notification_add
/admin/password_change/ django.contrib.admin.sites.password_change      admin:password_change
/admin/password_change/done/    django.contrib.admin.sites.password_change_done admin:password_change_done
/admin/payments/escrowreleaseschedule/  django.contrib.admin.options.changelist_view    admin:payments_escrowreleaseschedule_changelist
/admin/payments/escrowreleaseschedule/<path:object_id>/ django.views.generic.base.RedirectView
/admin/payments/escrowreleaseschedule/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:payments_escrowreleaseschedule_change
/admin/payments/escrowreleaseschedule/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:payments_escrowreleaseschedule_delete
/admin/payments/escrowreleaseschedule/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:payments_escrowreleaseschedule_history
/admin/payments/escrowreleaseschedule/add/      django.contrib.admin.options.add_view   admin:payments_escrowreleaseschedule_add
/admin/payments/payment/        django.contrib.admin.options.changelist_view    admin:payments_payment_changelist
/admin/payments/payment/<path:object_id>/       django.views.generic.base.RedirectView
/admin/payments/payment/<path:object_id>/change/        django.contrib.admin.options.change_view        admin:payments_payment_change
/admin/payments/payment/<path:object_id>/delete/        django.contrib.admin.options.delete_view        admin:payments_payment_delete
/admin/payments/payment/<path:object_id>/history/       django.contrib.admin.options.history_view       admin:payments_payment_history
/admin/payments/payment/add/    django.contrib.admin.options.add_view   admin:payments_payment_add
/admin/r/<path:content_type_id>/<path:object_id>/       django.contrib.contenttypes.views.shortcut      admin:view_on_site
/admin/reviews/dispute/ django.contrib.admin.options.changelist_view    admin:reviews_dispute_changelist
/admin/reviews/dispute/<path:object_id>/        django.views.generic.base.RedirectView
/admin/reviews/dispute/<path:object_id>/change/ django.contrib.admin.options.change_view        admin:reviews_dispute_change
/admin/reviews/dispute/<path:object_id>/delete/ django.contrib.admin.options.delete_view        admin:reviews_dispute_delete
/admin/reviews/dispute/<path:object_id>/history/        django.contrib.admin.options.history_view       admin:reviews_dispute_history
/admin/reviews/dispute/add/     django.contrib.admin.options.add_view   admin:reviews_dispute_add
/admin/reviews/review/  django.contrib.admin.options.changelist_view    admin:reviews_review_changelist
/admin/reviews/review/<path:object_id>/ django.views.generic.base.RedirectView
/admin/reviews/review/<path:object_id>/change/  django.contrib.admin.options.change_view        admin:reviews_review_change
/admin/reviews/review/<path:object_id>/delete/  django.contrib.admin.options.delete_view        admin:reviews_review_delete
/admin/reviews/review/<path:object_id>/history/ django.contrib.admin.options.history_view       admin:reviews_review_history
/admin/reviews/review/add/      django.contrib.admin.options.add_view   admin:reviews_review_add
/admin/services/service/        django.contrib.admin.options.changelist_view    admin:services_service_changelist
/admin/services/service/<path:object_id>/       django.views.generic.base.RedirectView
/admin/services/service/<path:object_id>/change/        django.contrib.admin.options.change_view        admin:services_service_change
/admin/services/service/<path:object_id>/delete/        django.contrib.admin.options.delete_view        admin:services_service_delete
/admin/services/service/<path:object_id>/history/       django.contrib.admin.options.history_view       admin:services_service_history
/admin/services/service/add/    django.contrib.admin.options.add_view   admin:services_service_add
/admin/services/servicecategory/        django.contrib.admin.options.changelist_view    admin:services_servicecategory_changelist
/admin/services/servicecategory/<path:object_id>/       django.views.generic.base.RedirectView
/admin/services/servicecategory/<path:object_id>/change/        django.contrib.admin.options.change_view        admin:services_servicecategory_change
/admin/services/servicecategory/<path:object_id>/delete/        django.contrib.admin.options.delete_view        admin:services_servicecategory_delete
/admin/services/servicecategory/<path:object_id>/history/       django.contrib.admin.options.history_view       admin:services_servicecategory_history
/admin/services/servicecategory/add/    django.contrib.admin.options.add_view   admin:services_servicecategory_add
/admin/socialaccount/socialaccount/     django.contrib.admin.options.changelist_view    admin:socialaccount_socialaccount_changelist
/admin/socialaccount/socialaccount/<path:object_id>/    django.views.generic.base.RedirectView
/admin/socialaccount/socialaccount/<path:object_id>/change/     django.contrib.admin.options.change_view        admin:socialaccount_socialaccount_change
/admin/socialaccount/socialaccount/<path:object_id>/delete/     django.contrib.admin.options.delete_view        admin:socialaccount_socialaccount_delete
/admin/socialaccount/socialaccount/<path:object_id>/history/    django.contrib.admin.options.history_view       admin:socialaccount_socialaccount_history
/admin/socialaccount/socialaccount/add/ django.contrib.admin.options.add_view   admin:socialaccount_socialaccount_add
/admin/socialaccount/socialapp/ django.contrib.admin.options.changelist_view    admin:socialaccount_socialapp_changelist
/admin/socialaccount/socialapp/<path:object_id>/        django.views.generic.base.RedirectView
/admin/socialaccount/socialapp/<path:object_id>/change/ django.contrib.admin.options.change_view        admin:socialaccount_socialapp_change
/admin/socialaccount/socialapp/<path:object_id>/delete/ django.contrib.admin.options.delete_view        admin:socialaccount_socialapp_delete
/admin/socialaccount/socialapp/<path:object_id>/history/        django.contrib.admin.options.history_view       admin:socialaccount_socialapp_history
/admin/socialaccount/socialapp/add/     django.contrib.admin.options.add_view   admin:socialaccount_socialapp_add
/admin/socialaccount/socialtoken/       django.contrib.admin.options.changelist_view    admin:socialaccount_socialtoken_changelist
/admin/socialaccount/socialtoken/<path:object_id>/      django.views.generic.base.RedirectView
/admin/socialaccount/socialtoken/<path:object_id>/change/       django.contrib.admin.options.change_view        admin:socialaccount_socialtoken_change
/admin/socialaccount/socialtoken/<path:object_id>/delete/       django.contrib.admin.options.delete_view        admin:socialaccount_socialtoken_delete
/admin/socialaccount/socialtoken/<path:object_id>/history/      django.contrib.admin.options.history_view       admin:socialaccount_socialtoken_history
/admin/socialaccount/socialtoken/add/   django.contrib.admin.options.add_view   admin:socialaccount_socialtoken_add
/admin/users/profile/   django.contrib.admin.options.changelist_view    admin:users_profile_changelist
/admin/users/profile/<path:object_id>/  django.views.generic.base.RedirectView
/admin/users/profile/<path:object_id>/change/   django.contrib.admin.options.change_view        admin:users_profile_change
/admin/users/profile/<path:object_id>/delete/   django.contrib.admin.options.delete_view        admin:users_profile_delete
/admin/users/profile/<path:object_id>/history/  django.contrib.admin.options.history_view       admin:users_profile_history
/admin/users/profile/add/       django.contrib.admin.options.add_view   admin:users_profile_add
/admin/users/user/      django.contrib.admin.options.changelist_view    admin:users_user_changelist
/admin/users/user/<id>/password/        django.contrib.auth.admin.user_change_password  admin:auth_user_password_change
/admin/users/user/<path:object_id>/     django.views.generic.base.RedirectView
/admin/users/user/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:users_user_change
/admin/users/user/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:users_user_delete
/admin/users/user/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:users_user_history
/admin/users/user/add/  django.contrib.auth.admin.add_view      admin:users_user_add
/api/schema/    drf_spectacular.views.SpectacularAPIView        schema
/api/schema/redoc/      drf_spectacular.views.SpectacularRedocView      redoc
/api/schema/swagger-ui/ drf_spectacular.views.SpectacularSwaggerView    swagger-ui
/api/v1/auth/   rest_framework.routers.APIRootView      api-root
/api/v1/auth/\.<format>/        rest_framework.routers.APIRootView      api-root
/api/v1/auth/jwt/create/        rest_framework_simplejwt.views.TokenObtainPairView      jwt-create
/api/v1/auth/jwt/refresh/       rest_framework_simplejwt.views.TokenRefreshView jwt-refresh
/api/v1/auth/jwt/verify/        rest_framework_simplejwt.views.TokenVerifyView  jwt-verify
/api/v1/auth/users/     djoser.views.UserViewSet        user-list
/api/v1/auth/users/<pkid>/      djoser.views.UserViewSet        user-detail
/api/v1/auth/users/<pkid>\.<format>/    djoser.views.UserViewSet        user-detail
/api/v1/auth/users/activation/  djoser.views.UserViewSet        user-activation
/api/v1/auth/users/activation\.<format>/        djoser.views.UserViewSet        user-activation
/api/v1/auth/users/me/  djoser.views.UserViewSet        user-me
/api/v1/auth/users/me\.<format>/        djoser.views.UserViewSet        user-me
/api/v1/auth/users/resend_activation/   djoser.views.UserViewSet        user-resend-activation
/api/v1/auth/users/resend_activation\.<format>/ djoser.views.UserViewSet        user-resend-activation
/api/v1/auth/users/reset_email/ djoser.views.UserViewSet        user-reset-username
/api/v1/auth/users/reset_email\.<format>/       djoser.views.UserViewSet        user-reset-username
/api/v1/auth/users/reset_email_confirm/ djoser.views.UserViewSet        user-reset-username-confirm
/api/v1/auth/users/reset_email_confirm\.<format>/       djoser.views.UserViewSet        user-reset-username-confirm
/api/v1/auth/users/reset_password/      djoser.views.UserViewSet        user-reset-password
/api/v1/auth/users/reset_password\.<format>/    djoser.views.UserViewSet        user-reset-password
/api/v1/auth/users/reset_password_confirm/      djoser.views.UserViewSet        user-reset-password-confirm
/api/v1/auth/users/reset_password_confirm\.<format>/    djoser.views.UserViewSet        user-reset-password-confirm
/api/v1/auth/users/set_email/   djoser.views.UserViewSet        user-set-username
/api/v1/auth/users/set_email\.<format>/ djoser.views.UserViewSet        user-set-username
/api/v1/auth/users/set_password/        djoser.views.UserViewSet        user-set-password
/api/v1/auth/users/set_password\.<format>/      djoser.views.UserViewSet        user-set-password
/api/v1/auth/users\.<format>/   djoser.views.UserViewSet        user-list
/api/v1/users/<str:username>/   apps.users.controllers.get_profile_by_username  users_api:get_profile_by_username
/api/v1/users/<str:username>/update/    apps.users.controllers.update_profile   users_api:update_profile
/api/v1/users/<str:username>/verify-provider/   apps.users.controllers.verify_provider  users_api:verify_provider
/api/v1/users/me/       apps.users.controllers.get_current_user_profile users_api:my_profile
/api/v1/users/me/data/  apps.users.controllers.get_current_user_data    users_api:current_user_data
/api/v1/users/me/unified/       apps.users.controllers.unified_profile_view     users_api:unified_profile
/api/v1/users/users/<uuid:user_id>/update-role/ apps.users.controllers.update_user_role users_api:update_user_role
/staticfiles/<path>     django.views.static.serve