from django.urls import path

from money_flow import views

urlpatterns = [
   path('create', views.NoteCreate.as_view(), name='note_create'),
   path('note/<int:id>', views.NoteDetail.as_view(), name='note_detail'),
   path('settings-data/', views.settings_data_view, name='settings_data'),
   path('status/create/', views.StatusCreateView.as_view(), name='status_create'),
   path('type/create/', views.TypeCreateView.as_view(), name='type_create'),
   path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
]