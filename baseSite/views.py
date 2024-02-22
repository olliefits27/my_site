from django.views import generic
from .models import Fiction, Quote, Pokemon, Type
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import PokemonSerializer


class Index(generic.TemplateView):
    template_name = "index.html"


class APIGuide(generic.TemplateView):
    template_name = "apiGuide.html"


class DataAnalysis(generic.TemplateView):
    template_name = "dataAnalysis.html"


class Fictions(generic.ListView):
    model = Fiction
    queryset = Fiction.objects.order_by("name")
    context_object_name = "fictions"
    template_name = "fictions.html"


class AddFiction(generic.CreateView):
    model = Fiction
    fields = ["name", "category", "image"]
    success_url = "/fictions"
    template_name = "add_fiction.html"


class Quotes(generic.ListView):
    model = Quote
    context_object_name = "quotes"
    template_name = "quotes.html"

    def get_queryset(self):
        return Quote.objects.filter(fiction=self.kwargs['fiction'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fiction"] = self.kwargs['fiction']
        fiction = Fiction.objects.get(pk=self.kwargs['fiction'])
        context["name"] = fiction.name
        return context


class AddQuote(generic.CreateView):
    model = Quote
    fields = ["quote", "character", "image"]
    template_name = "add_quote.html"
    success_url = "/fictions"

    def form_valid(self, form, **kwargs):
        fiction = Fiction.objects.get(pk=self.kwargs['fiction'])
        form.instance.fiction = fiction
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        fiction = self.kwargs['fiction']
        return f"/quotes/{fiction}"


class PokemonApiView(APIView):
    def get(self, request, *args, **kwargs):
        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'number': request.data.get('number'),
            'name': request.data.get('name'),
        }
        serializer = PokemonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PokemonApiDetailView(APIView):
    def get_object(self, pokemon_id):
        try:
            return Pokemon.objects.get(number=pokemon_id)
        except Pokemon.DoesNotExist:
            return None

    def get(self, request, pokemon_id, *args, **kwargs):
        pokemon = self.get_object(pokemon_id)
        if not pokemon:
            return Response(
                {"error": "Object with Pokemon ID does not exist"}
            )
        serializer = PokemonSerializer(pokemon, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pokemon_id, *args, **kwargs):
        pokemon = self.get_object(pokemon_id)
        if not pokemon:
            return Response(
                {"error": "Object with Pokemon ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'number': request.data.get('number'),
            'name': request.data.get('name'),
        }
        serializer = PokemonSerializer(instance=pokemon, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)