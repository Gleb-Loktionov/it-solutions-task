from django.urls import path

from money_flow import views

urlpatterns = [
   path('create', views.NoteCreateView.as_view(), name='note_create'),
   path('update/<int:id>', views.NoteUpdateView.as_view(), name='note_update'),
   path('delete/<int:id>', views.NoteDeleteView.as_view(), name='note_delete'),
   
   path('settings-data/', views.settings_data_view, name='settings_data'),
   
   path('status/create/', views.StatusCreateView.as_view(), name='status_create'),
   path('status/update/<int:id>', views.StatusUpdateView.as_view(), name='status_update'),
   path('status/delete/<int:id>', views.StatusDeleteView.as_view(), name='status_delete'),
   
   path('type/create/', views.TypeCreateView.as_view(), name='type_create'),
   path('type/update/<int:id>', views.TypeUpdateView.as_view(), name='type_update'),
   path('type/delete/<int:id>', views.TypeDeleteView.as_view(), name='type_delete'),
   
   path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
   path('category/update/<int:id>', views.CategoryUpdateView.as_view(), name='category_update'),
   path('category/delete/<int:id>', views.CategoryDeleteView.as_view(), name='category_delete'),
   path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
]