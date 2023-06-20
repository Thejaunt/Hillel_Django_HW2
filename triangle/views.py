from django.shortcuts import render

from triangle.forms import TriangleForm


def find_hypotenuse(request):
    form = TriangleForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            cath1 = form.cleaned_data.get("cath1")
            cath2 = form.cleaned_data.get("cath2")
            res = round(float(cath1**2 + cath2**2) ** 0.5, 2)
            return render(request, "form.html", {"form": form, "res": res})

    return render(request, "form.html", {"form": form})
