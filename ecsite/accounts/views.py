from django.shortcuts import render, redirect
from django.views.generic import View
from .models import User
from .forms import LoginForm, RegisterForm


class RegisterUser(View):
    def get(self, request, *args, **kwargs):

        form = RegisterForm()

        context = {
            "form": form,
        }
        return render(request, "register_user.html", context)


class RegisterUserConfirm(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "register_user.html", context)

        user_id = form.cleaned_data["user_id"]

        if User.objects.filter(user_id=user_id).exists():
            context = {
                "form": form,
                "error": "この会員IDはすでに使用されています。",
            }
            return render(request, "register_user.html", context)

        context = {
            "form": form,
        }
        return render(request, "register_user_confirm.html", context)


class RegisterUserCommit(View):
    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "register_user.html", context)

        new_user = User()
        new_user.user_id = form.cleaned_data["user_id"]
        new_user.password = form.cleaned_data["password"]
        new_user.name = form.cleaned_data["name"]
        new_user.address = form.cleaned_data["address"]
        new_user.save()

        context = {
            "name": new_user.name,
        }
        return render(request, "register_user_commit.html", context)



class Login(View):
        def get(self, request, *args, **kwargs):
            form = LoginForm()

            context = {
                "form": form,
            }
            return render(request, "login.html", context)
        
        def post(self, request, *args, **kwargs):
            form = LoginForm(request.POST)

            if not form.is_valid():
                context = {
                    "form": form,
                }
                return render(request, "login.html", context)
            
            user_id = form.cleaned_data.get("user_id")
            password = form.cleaned_data.get("password")

            user = User.objects.filter(user_id=user_id, password=password).first()

            if user is None:
                context = {
                    "form": form,
                    "error": "会員ID、またはパスワードが間違っています。"
                }
                return render(request, "login.html", context)
            
            request.session["user_id"] = user.user_id
            request.session["name"] = user.name

            return redirect("top")
        
