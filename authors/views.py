import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe
from utils.pagination import make_pagination

from .forms import LoginForm, RegisterForm

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html',
                  {
                      'form': form,
                      'form_action': reverse('authors:register_create'),
                  })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    if form.is_valid():
        user_created = form.save(commit=False)
        user_created.set_password(user_created.password)
        user_created.save()
        messages.success(
            request,
            'Sua conta foi foi criada! Agora pode logar nessa plataforma.')

        del(request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html',
                  {
                      'form': form,
                      'form_action': reverse('authors:login_create')
                  })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(
                request,
                f'Tudo certo, você está online. Seja bem-vindo, '
                f'{form["username"].value()} 🧡'
            )
            login(request, authenticated_user)
        else:
            messages.error(request,
                           ('Credenciais inválidas, tente mais tarde ou '
                            'verifique com o administrador '
                            'para maiores informações.'
                            )
                           )

    else:
        messages.error(request,
                       ('Login inválido! Verifique seu e-email ou '
                        'a senha, tente novamente.')
                       )

    return redirect('authors:dashboard')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request,
                       ('Ops! A solicitação de deslogar é inválida. '
                        'Tente novamente ou entre em contato com suporte.')
                       )
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request,
                       ('Ops! Usuário não foi deslogado corretamente.')
                       )

        return redirect(reverse('authors:login'))

    messages.success(request,
                     ('Sua conta foi deslogada com sucesso!')
                     )
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user,
    )

    page_obg, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request,
                  'authors/pages/dashboard.html',
                  context={'recipes': page_obg,
                           'pagination_range': pagination_range,
                           }

                  )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    if not recipe:
        raise Http404()

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form
        }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe: Recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(
            request, (
                'A receita foi criada e salva com sucesso! '
                'Pode continuar editando aqui ou voltar à página anterior. 🧡'
            )
        )
        return redirect(
            reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
        )

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form,
            'form_action': reverse('authors:dashboard_recipe_new')
        }
    )


@ login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):

    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    recipe.delete()

    messages.success(request, 'Foi deletada com sucesso!')
    return redirect(reverse('authors:dashboard'))
