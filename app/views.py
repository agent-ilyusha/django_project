import datetime

import app.constant as constant

from typing import Any

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from django.views.generic import ListView, FormView

from rest_framework.response import Response

from app.forms import RegistrationForm
from app.models import Car, Owner, Address, ServiceRecord, CarToServiceRecord, CarToOwner


def home_page(request: WSGIRequest):
    return render(
        request,
        'index.html',
        {
            'cars': Car.objects.count(),
            'owners': Owner.objects.count(),
            'addresses': Address.objects.count(),
            'services': ServiceRecord.objects.count(),
        }
    )


def register(request: WSGIRequest):
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Owner.objects.create(
                user=user,
                name=form.cleaned_data['first_name'],
                surname=form.cleaned_data['last_name'],
            )
            return redirect('profile')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form, 'errors': errors},
    )


@login_required
def login_view(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect("profile")
    else:
        form = AuthenticationForm()
        return render(
            request,
            'registration/login.html'
        )


def logout_view(request: WSGIRequest):
    logout(request)
    return redirect("login")


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required
def profile(request: WSGIRequest):
    owner = Owner.objects.get(user=request.user)
    data = {'owner': owner}
    return render(
        request,
        'pages/profile.html',
        data
    )


def create_listview(model_class, plural_name, template):
    class CustomListView(ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = Paginator(instances, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context

    return CustomListView


def settings_view(request: WSGIRequest):
    if request.method.lower() == 'get':
        owner = Owner.objects.get(user=request.user)
    elif request.method.lower() == 'post':
        owner = Owner.objects.get(user=request.user)
        owner.name = request.POST.get('name')
        owner.number = request.POST.get('number')
        owner.surname = request.POST.get('surname')
        owner.patronymic = request.POST.get('patronymic')
        owner.save()

    data = {'owner': owner}
    return render(
        request,
        'pages/settings.html',
        data
    )


def validate_car(request: WSGIRequest):
    errors = []
    car_data = {
        'mark': request.POST.get('mark'),
        'model': request.POST.get('model'),
        'date_of_issue': request.POST.get('date_of_issue'),
        'price': request.POST.get('price'),
        'description': request.POST.get('description'),
        'for_sale': True if request.POST.get('for_sale') else False,
    }

    if not request.POST.get('mark'):
        errors.append('Пожалуйста, заполните поле "mark"!')
    if not request.POST.get('model'):
        car_data['model'] = request.POST.get('model')
        errors.append('Пожалуйста, заполните поле "model"!')
    if len(request.POST['mark']) > constant.MAX_LENGTH_CAR_FIELDS:
        car_data['mark'] = request.POST.get('mark')
        errors.append(f'Длина поля "Марка" слишком большая! Уменьшите ее до {constant.MAX_LENGTH_CAR_FIELDS}')
    if len(request.POST['model']) > constant.MAX_LENGTH_OWNER_FIELDS:
        car_data['mark'] = request.POST.get('model')
        errors.append(f'Длина пол "Модель" слишком болшая! Уменьшите ее до {constant.MAX_LENGTH_OWNER_FIELDS}')
    try:
        if datetime.datetime.fromisoformat(request.POST.get('date_of_issue')) > datetime.datetime.today():
            car_data['date_of_issue'] = request.POST.get('date_of_issue')
            errors.append(f'Дата создания должна быть меньше сегодняшний даты!')
    except ValueError:
        car_data['date_of_issue'] = request.POST.get('date_of_issue')
        errors.append(f'Дата создания либо пустая, либо указана неверно!')
    try:
        if float(request.POST.get('price')) < 0:
            car_data['price'] = request.POST.get('price')
            errors.append(f'Цена должна быть больше 0!')

        if float(request.POST.get('price')) > constant.MAX_PRICE_CAR:
            car_data['price'] = request.POST.get('price')
            errors.append(f'Цена должна быть меньше {constant.MAX_PRICE_CAR}!')
    except ValueError:
        car_data['price'] = request.POST.get('price')
        errors.append(f'Вы указали не число, либо не заполнили поле!')
        if len(request.POST.get('description')) > constant.MAX_LENGTH_DESCRIPTION_FIELD:
            car_data['description'] = request.POST.get('description')
            errors.append(f'Длина поля "Описание" слишком большая! Уменьшите ее до {constant.MAX_LENGTH_DESCRIPTION_FIELD}')
    return errors, car_data


def validate_sr(data: dict):
    sr_data = {
        'type_work': data.get('type_work'),
        'the_date_of_the': data.get('the_date_of_the'),
        'price': data.get('price'),
    }
    errors = []
    if len(*data.get('type_work')) > constant.MAX_LENGTH_TYPE_WORK:
        errors.append(f'Уменьшите длину поля "Тип работы"!')
    if not data.get('type_work'):
        errors.append(f'Заполните поле "Тип работы"!')
    try:
        if datetime.datetime.fromisoformat(*data.get('the_date_of_the')) > datetime.datetime.today():
            errors.append('Дата должна быть меньше сегодняшний даты!')
    except ValueError:
        errors.append('Вы указали дату не в корректной форме!')
    except TypeError:
        errors.append('Вы указали дату не в корректной форме!')

    try:
        if float(*data.get('price')) < 0:
            errors.append('Цена услуг должна быть больше 0!')
        if float(*data.get('price')) > constant.MAX_PRICE_SERVICE_RECORD:
            errors.append(f'Цена услуг должна быть меньше {constant.MAX_PRICE_SERVICE_RECORD}!')
    except ValueError:
        errors.append('Вы указали не число!')
    except TypeError:
        errors.append('Вы указали не число!')

    return errors, sr_data


def create_car(request: WSGIRequest):
    if request.method.lower() == 'get':
        car = Car
        data = {'car': car}
        return render(
            request,
            'car/create.html',
            data
        )
    elif request.method.lower() == 'post':
        errors, car_data = validate_car(request)
        if not errors:
            for_sale = request.POST.get('for_sale')
            car = Car.objects.create(
                mark=request.POST.get('mark'),
                model=request.POST.get('model'),
                date_of_issue=request.POST.get('date_of_issue'),
                price=request.POST.get('price'),
                description=request.POST.get('description'),
                for_sale=True if for_sale == 'on' else False,
            )

            user = Owner.objects.get(user=request.user)
            c2o = CarToOwner.objects.create(
                car_id=car,
                owner_id=user,
            )

        service_records = list()
        service_record = dict()
        list_service_records = list()
        errors_sr, sr_data = list(), list()
        data = dict(request.POST)

        if data.get('type_work0'):
            index = int(list(data.keys())[-1][-1])
            for name, value in data.items().__reversed__():
                if name[-1] != str(index):
                    service_records.append(service_record)
                    index -= 1
                    service_record = dict()
                if index < 0:
                    break
                elif name[-1] == str(index):
                    service_record[name[:-1]] = value
            for service_record in service_records:
                valid_sr = validate_sr(service_record)
                errors_sr.append(valid_sr[0])
                list_service_records.append(valid_sr[1])

        if errors_sr[0] or errors:
            print(errors, errors_sr)
            return render(
                request,
                'car/create.html',
                {
                    'car_data': car_data,
                    'errors': errors,
                    'list_service_records': list_service_records,
                    'errors_sr': errors_sr,
                },
            )

        for val in list_service_records:
            sr = ServiceRecord.objects.create(
                type_work=val.get('type_work')[0],
                the_date_of_the=val.get('the_date_of_the')[0],
                price=val.get('price')[0],
            )
            sr.save()
            CarToServiceRecord.objects.create(car_id=car, service_id=sr)

        cars = Car.objects.all()
        car.save()
        c2o.save()
        return redirect(
            '/car/views/',
            cars=cars
        )
    return Response('Bad Request', 400)


def view_cars(request: WSGIRequest):
    cars = Car.objects.all()
    data = {'cars': cars}
    return render(
        request,
        'car/views_all_cars.html',
        data,
    )


def get_car(request: WSGIRequest):
    car_id = request.POST.get('car_id')
    car = Car.objects.get(id=car_id)
    owner = Owner.objects.get(user=request.user)
    try:
        flag = CarToOwner.objects.get(car_id=car, owner_id=owner)
    except CarToOwner.DoesNotExist:
        flag = False
    return flag, car, car_id


def view_car(request: WSGIRequest):
    if request.method != 'POST':
        return redirect('view_cars')
    data = get_car(request)
    return render(
        request,
        'car/car_view.html',
        {'car': data[1].__repr__(), 'flag': data[0], 'id': data[2], 'for_sale': data[1].for_sale}
    )


def settings_vehicle(request: WSGIRequest):
    if request.method.lower() == 'post':
        data = get_car(request)
        for name, value in request.POST.items():
            if name == 'for_sale':
                setattr(data[1], name, True if value == 'True' else False)
            try:
                setattr(data[1], name, float(value.replace(',', '.')))
            except ValueError:
                setattr(data[1], name, value)
        data[1].save()
        sr = [val.get_dict() for val in ServiceRecord.objects.filter(car_id=data[1])]

        return render(
            request,
            'car/settings.html',
            {
                'car': data[1],
                'flag': data[0],
                'sr': sr,
                'date_of_issue': str(data[1].__repr__()['date_of_issue']),
            }
        )
    return render(
        request,
        'extensions/bad_request.html'
    )


def buy_car(request: WSGIRequest):
    if request.method.lower() == 'post':
        car = Car.objects.get(id=request.POST.get('car_id'))
        owner = Owner.objects.get(user=request.user)
        if float(owner.money) >= float(car.price):
            owner.money = float(owner.money) - float(car.price)
            CarToOwner.objects.get(car_id=car).delete()
            CarToOwner.objects.create(car_id=car, owner_id=owner)
            flag = True
            msg = 'Сделка прошла успешно!'
            owner.save()
        else:
            flag = False
            msg = 'У вас не хватило денег, попробуйте в иной раз!'
        return render(
            request,
            'car/buy.html',
            {'flag': flag, 'msg': msg, 'car': car}
        )
    return render(
        request,
        'extensions/bad_request.html'
    )


def replenishment(request: WSGIRequest):
    msg = ''
    owner = Owner.objects.get(user=request.user)
    try:
        money = float(request.POST.get('sum'))
        if money > 0:
            owner.money = owner.money + money if owner.money else money
            owner.save()
        else:
            msg = 'Нужно ввести положительное число!'
    except TypeError:
        msg = "Введите положительное число!"
    except ValueError:
        msg = "Введите число!"

    if msg != '':
        return render(
            request,
            'pages/replenishment.html',
            {'msg': msg, 'owner': owner}
        )
    return redirect(
        "/profile/",
        owner=owner,
    )


def delete_car(request: WSGIRequest):
    if request.POST.get('delete'):
        car = Car.objects.get(id=request.POST.get('delete'))
        car.delete()
        msg = 'Машина удалена!'
    else:
        msg = 'Вы не указали машину!'
    return render(
        request,
        'car/delete.html',
        {'msg': msg}
    )


CarListView = create_listview(Car, 'cars', 'catalog/cars.html')
OwnerListView = create_listview(Owner, 'owners', 'catalog/owners.html')
AddressListView = create_listview(Address, 'addresses', 'catalog/addresses.html')
ServiceRecordListView = create_listview(ServiceRecord, 'services', 'catalog/services.html')
