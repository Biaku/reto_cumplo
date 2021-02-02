import requests
from decouple import config
from django.contrib import messages
from django.shortcuts import render, redirect


def index(request):
    context = {}
    bmx_token = config('BMX_TOKEN')
    headers = {'Bmx-Token': bmx_token}

    if request.GET.get('type', None):
        id_serie = request.GET['type']
        initial_date = request.GET.get('initial_date', None)
        final_date = request.GET.get('final_date', None)
        url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{id_serie}/datos/{initial_date}/{final_date}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            data = data['bmx']['series'][0]['datos']
            total = 0
            list_imports = []
            list_dates = []
            for d in data:
                total += float(d['dato'])
                list_dates.append(d['fecha'])
                list_imports.append(d['dato'])

            context.update({
                'data': data,
                'promedio': total / len(data),
                'max_value': max(list_imports),
                'min_value': min(list_imports),
                'labels_chart': list_dates,
                'data_chart': list_imports,
            })
        else:
            messages.error(request, 'No se pudo cargar la informacion')
            return redirect('home:index')

    return render(request, 'home/index.html', context)
