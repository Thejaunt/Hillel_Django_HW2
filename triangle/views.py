from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from triangle.forms import PersonForm, TriangleForm

from .models import Person


def find_hypotenuse(request):
    form = TriangleForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            cath1 = form.cleaned_data.get("cath1")
            cath2 = form.cleaned_data.get("cath2")
            res = round(float(cath1**2 + cath2**2) ** 0.5, 2)
            return render(request, "form.html", {"form": form, "res": res})

    return render(request, "form.html", {"form": form})


def create_person(request):
    form = PersonForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save()
            return redirect(reverse("update_person", args=[obj.pk]))
    return render(request, "create_person.html", {"form": form})


def update_person(request, pk):
    obj = get_object_or_404(Person, pk=pk)
    form = PersonForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            if form.has_changed():
                obj = form.save()
        return redirect(reverse("update_person", args=[obj.pk]))
    return render(request, "update_person.html", {"form": form})
