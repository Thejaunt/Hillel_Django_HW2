from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
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
            messages.success(request, "Person Has Been Created")
            return redirect(reverse("person-detail", args=[obj.pk]))
    return render(request, "create_person.html", {"form": form})


def update_person(request, pk):
    obj = get_object_or_404(Person, pk=pk)
    form = PersonForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            if form.has_changed():
                obj = form.save()
                messages.success(request, "Person Has Been Updated")
            else:
                messages.success(request, "Person Is Up To Date")
        return redirect(reverse("person-detail", args=[obj.pk]))
    return render(request, "update_person.html", {"form": form})


def list_persons_view(request):
    obj_list = Person.objects.all()
    paginator = Paginator(obj_list, 5)
    page_number = request.GET.get("page")
    obj = paginator.get_page(page_number)
    return render(request, "person_list.html", {"obj": obj})


def person_detail_view(request, pk):
    obj = get_object_or_404(Person, pk=pk)
    return render(request, "person_detail.html", {"obj": obj})


def delete_person(request, pk):
    if request.method == "POST":
        obj = get_object_or_404(Person, pk=pk)
        obj.delete()
        messages.success(request, "Person Has Been Deleted")
        return redirect(reverse("list_persons"))
    else:
        raise Http404
