from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("fictions", views.Fictions.as_view(), name="fictions"),
    path("add_fiction", views.AddFiction.as_view(), name="add_fiction"),
    path("quotes/<int:fiction>", views.Quotes.as_view(), name="quotes"),
    path("add_quote/<int:fiction>", views.AddQuote.as_view(), name="add_quote"),
    path("pokemon_api_how_to", views.APIGuide.as_view(), name="apiGuide"),
    path("pokemon_api", views.PokemonApiView.as_view(), name="pokemon_api"),
    path("pokemon_api/<int:pokemon_id>", views.PokemonApiDetailView.as_view(), name="pokemon_api_unique"),
    path("data_analysis", views.DataAnalysis.as_view(), name="dataAnalysis")
]