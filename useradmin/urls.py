from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.dashboard_products, name="dashboard-products"),
    path("add-products/", views.dashboard_add_product, name="dashboard-add-products"),
    path("edit-products/<pid>/", views.dashboard_edit_product, name="dashboard-edit-products"),
    path("delete-products/<pid>/", views.dashboard_delete_product, name="dashboard-delete-products"),
    path("orders/", views.dashboard_orders, name="dashboard-orders"),
    path("order-detail/<int:id>/", views.dashboard_order_detail, name="dashboard-order-detail"),
    path("change-order-status/<int:id>/", views.dashboard_change_order_status, name="dashboard-change-order-status"),
    path("settings/", views.dashboard_settings, name="dashboard-settings"),
]
