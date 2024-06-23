# ----------------------------------------------------------------
#                     URLS DO APP - ESTOQUE
# ----------------------------------------------------------------


# urls.py
from django.urls import path
from .views import AlimentoListView, AlimentoCreateView, AlimentoUpdateView, AlimentoDeleteView, EntradasListView
from .views import SaidasListView, UtilizarAlimentoView, EntradasPDFView, SaidasPDFView

urlpatterns = [
    path('', AlimentoListView.as_view(), name='alimento_list'),
    path('alimento/create/', AlimentoCreateView.as_view(), name='alimento_create'),
    path('alimento/<int:pk>/update/', AlimentoUpdateView.as_view(), name='alimento_update'),
    path('alimento/<int:pk>/delete/', AlimentoDeleteView.as_view(), name='alimento_delete'),
    path('alimentos/utilizar/<int:pk>/', UtilizarAlimentoView.as_view(), name='utilizar_alimento'),
    path('entradas/', EntradasListView.as_view(), name='entradas_list'),  # URL para listagem de entradas
    path('saidas/', SaidasListView.as_view(), name='saidas_list'),  # URL para listagem de saídas
    path('entradas/pdf/', EntradasPDFView.as_view(), name='entradas_pdf'),
    path('saidas/pdf/', SaidasPDFView.as_view(), name='saidas_pdf'),
]
