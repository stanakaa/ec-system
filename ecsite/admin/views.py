from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import LoginForm
from .models import Admin


class adminLogin(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()

        context = {
            "form": form,
        }
        return render(request, "adminLogin.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "adminLogin.html", context)

        admin_id = form.cleaned_data["admin_id"]
        password = form.cleaned_data["password"]

        admin = Admin.objects.filter(
            admin_id=admin_id,
            password=password
        ).first()

        if admin is None:
            context = {
                "form": form,
                "error": "管理者ID、またはパスワードが間違っています。",
            }
            return render(request, "adminLogin.html", context)

        request.session["admin_id"] = admin.admin_id

        return redirect("admin_main")


class adminMain(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        context = {
            "admin_id": request.session["admin_id"],
        }
        return render(request, "adminMain.html", context)
    

class adminLogout(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" in request.session:
            del request.session["admin_id"]

        return redirect("admin_login")
