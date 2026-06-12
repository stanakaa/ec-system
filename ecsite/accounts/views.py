from django.shortcuts import render, redirect
from django.views.generic import View
from .models import User
from .forms import LoginForm, RegisterForm, UpdateUserForm


class RegisterUser(View):
    def get(self, request, *args, **kwargs):

        form = RegisterForm()

        context = {
            "form": form,
        }
        return render(request, "registerUser.html", context)


class RegisterUserConfirm(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "registerUser.html", context)

        user_id = form.cleaned_data["user_id"]

        if User.objects.filter(user_id=user_id).exists():
            context = {
                "form": form,
                "error": "この会員IDはすでに使用されています。",
            }
            return render(request, "registerUser.html", context)

        context = {
            "form": form,
        }
        return render(request, "registerUserConfirm.html", context)


class RegisterUserCommit(View):
    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "registerUser.html", context)

        new_user = User()
        new_user.user_id = form.cleaned_data["user_id"]
        new_user.password = form.cleaned_data["password"]
        new_user.name = form.cleaned_data["name"]
        new_user.address = form.cleaned_data["address"]
        new_user.save()

        context = {
            "name": new_user.name,
        }
        return render(request, "registerUserCommit.html", context)



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
        

class Logout(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect("login")


class UserInfo(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        context = {
            "user": user,
        }
        return render(request, "userInfo.html", context)


class UpdateUser(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        form = UpdateUserForm(initial={
            "user_id": user.user_id,
            "name": user.name,
            "address": user.address,
        })

        context = {
            "form": form,
        }
        return render(request, "updateUser.html", context)


class RegisterUserConfirm(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "registerUser.html", context)

        user_id = form.cleaned_data["user_id"]

        if User.objects.filter(user_id=user_id).exists():
            context = {
                "form": form,
                "error": "この会員IDはすでに使用されています。",
            }
            return render(request, "registerUser.html", context)

        context = {
            "form": form,
        }
        return render(request, "registerUserConfirm.html", context)


class RegisterUserCommit(View):
    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "registerUser.html", context)

        new_user = User()
        new_user.user_id = form.cleaned_data["user_id"]
        new_user.password = form.cleaned_data["password"]
        new_user.name = form.cleaned_data["name"]
        new_user.address = form.cleaned_data["address"]
        new_user.save()

        context = {
            "name": new_user.name,
        }
        return render(request, "registerUserCommit.html", context)



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


class UserInfo(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        context = {
            "user": user,
        }
        return render(request, "userInfo.html", context)
    

class UpdateUser(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        form = UpdateUserForm(initial={
            "user_id": user.user_id,
            "name": user.name,
            "address": user.address,
        })

        context = {
            "form": form,
        }
        return render(request, "updateUser.html", context)


class UpdateUserConfirm(View):
    def post(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        form = UpdateUserForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "updateUser.html", context)

        old_user_id = request.session["user_id"]
        new_user_id = form.cleaned_data["user_id"]

        if old_user_id != new_user_id:
            if User.objects.filter(user_id=new_user_id).exists():
                context = {
                    "form": form,
                    "error": "この会員IDはすでに使用されています。",
                }
                return render(request, "updateUser.html", context)

        user = User.objects.get(user_id=old_user_id)

        if form.cleaned_data["password"]:
            password_display = form.cleaned_data["password"]
        else:
            password_display = user.password

        context = {
            "form": form,
            "password_display": password_display,
        }
        return render(request, "updateUserConfirm.html", context)


class UpdateUserCommit(View):
    def post(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        form = UpdateUserForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "updateUser.html", context)

        old_user_id = request.session["user_id"]
        new_user_id = form.cleaned_data["user_id"]

        if old_user_id != new_user_id:
            if User.objects.filter(user_id=new_user_id).exists():
                context = {
                    "form": form,
                    "error": "この会員IDはすでに使用されています。",
                }
                return render(request, "updateUser.html", context)

        old_user = User.objects.get(user_id=old_user_id)

        if form.cleaned_data["password"]:
            password = form.cleaned_data["password"]
        else:
            password = old_user.password

        if old_user_id == new_user_id:
            old_user.password = password
            old_user.name = form.cleaned_data["name"]
            old_user.address = form.cleaned_data["address"]
            old_user.save()

            user = old_user

        else:
            new_user = User()
            new_user.user_id = form.cleaned_data["user_id"]
            new_user.password = password
            new_user.name = form.cleaned_data["name"]
            new_user.address = form.cleaned_data["address"]
            new_user.save()

            # ShoppingCart.objects.filter(user=old_user).update(user=new_user)
            # Purchase.objects.filter(user=old_user).update(user=new_user)

            old_user.delete()

            user = new_user

        request.session["user_id"] = user.user_id
        request.session["name"] = user.name

        context = {
            "user": user,
        }
        return render(request, "updateUserCommit.html", context)


class WithdrawConfirm(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        context = {
            "user": user,
        }
        return render(request, "withdrawConfirm.html", context)


class WithdrawCommit(View):
    def post(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        name = user.name

        user.delete()
        request.session.flush()

        context = {
            "name": name,
        }
        return render(request, "withdrawCommit.html", context)
        
