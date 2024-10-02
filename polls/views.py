from django.utils import timezone
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import Question, Choice

# Vista genérica para la página de índice
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Retorna las últimas cinco preguntas publicadas,
        excluyendo aquellas que están programadas para el futuro.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# Vista genérica para la página de detalles
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excluye cualquier pregunta que aún no ha sido publicada.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# Vista genérica para la página de resultados
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# Vista personalizada para procesar la votación
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Si no se selecciona una opción, muestra un mensaje de error.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Usa F() para incrementar los votos sin riesgo de condiciones de carrera.
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Redirige a la página de resultados después de votar correctamente.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
