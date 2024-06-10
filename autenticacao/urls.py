# ----------------------------------------------------------------
#                     URLS DO APP - ESTOQUE
# ----------------------------------------------------------------

# urls.py

from django.urls import path
# from .views import AlimentoListView, AlimentoCreateView, AlimentoUpdateView, AlimentoDeleteView


from autenticacao.views import HomeView, SigupView, SiginView, ExitView
urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),  # Substitua 'login_view' pela sua função de visualização de login
    # path('menu/', MenuView.as_view(), name='menu'),
    path('', HomeView.as_view(), name='home'),
    path('sigup/', SigupView.as_view(), name='sigup'),
    path('sigin/', SiginView.as_view(), name='sigin'),
    path('exit/', ExitView.as_view(), name='exit'),
    # Outras rotas do aplicativo de autenticação
]
