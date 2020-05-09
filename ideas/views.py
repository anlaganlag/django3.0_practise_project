from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import IdeaForm
from .models import Idea


class IdeaList(ListView):
    model = Idea


class IdeaDetail(DetailView):
    model = Idea
    context_object_name = "idea"


@login_required
def add_or_change_idea(request, pk=None):
    idea = None
    if pk:
        idea = get_object_or_404(Idea, pk=pk)

    if request.method == "POST":
        form = IdeaForm( request,data=request.POST, files=request.FILES, instance=idea)

        if form.is_valid():
            idea = form.save()
            return redirect("ideas:idea_detail", pk=idea.pk)
    else:
        form = IdeaForm(request, instance=idea)

    context = {"idea": idea, "form": form}
    return render(request, "ideas/idea_form.html", context)


@login_required
def delete_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        idea.delete()
        return redirect("ideas:idea_list")
    context = {"idea": idea}
    return render(request, "ideas/idea_deleting_confirmation.html", context)

def idea_handout_pdf(request, pk):
    from django.template.loader import render_to_string
    from django.utils.timezone import now as timezone_now
    from django.utils.text import slugify
    from django.http import HttpResponse
    from weasyprint import HTML
    from weasyprint.fonts import FontConfiguration
    idea = get_object_or_404(Idea, pk=pk)
    context = {"idea": idea}
    html = render_to_string(
    "ideas/idea_handout_pdf.html", context
    )
    response = HttpResponse(content_type="application/pdf")
    response[
    "Content-Disposition"
    ] = "inline; filename={date}-{name}-handout.pdf".format(
    date=timezone_now().strftime("%Y-%m-%d"),
    name=slugify(idea.translated_title),
    )
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(
    response, font_config=font_config)
    return response