from django.urls import path
from . import views

app_name = 'MoneyManager'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:account_id>/', views.detail, name = 'detail'),
	path('add_change', views.add_change, name = 'add_change'),
	path('<int:category_id>/detail_categories', views.detail_categories, name = 'detail_categories'),
	path('<int:category_id>/remove_category', views.remove_category, name = 'remove_category'),
	path('create_account', views.create_account, name = 'create_account'),
	path('create_category', views.create_category, name = 'create_category'),
	path('<int:account_id>/remove_account', views.remove_account, name = 'remove_account'),
	path('accounts_categories_changes', views.accounts_categories_changes, name = 'accounts_categories_changes'),
	path('transfer', views.transfer, name = 'transfer')
]