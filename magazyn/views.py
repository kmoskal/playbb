from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from sqlalchemy import create_engine
import camelot
import pandas as pd
from .models import StanAkcesoria
from inwentaryzacja.models import Raport

class ListaAkcesoriView(LoginRequiredMixin, ListView):
    login_url = 'accounts:account-login'
    queryset = StanAkcesoria.objects.all()
    template_name = "magazyn/lista-akcesorii.html"
    model = StanAkcesoria
    context_object_name = 'akcesoria'

class WyszukaneAkcesoriaView(LoginRequiredMixin, ListView):
    login_url = 'accounts:account-login'
    template_name = "magazyn/lista-akcesorii.html"
    model = StanAkcesoria
    context_object_name = 'akcesoria'

    def get_queryset(self):
        query = self.request.GET.get('q').lower().replace(' ', '')
        object_list = StanAkcesoria.objects.filter(searchstring__icontains=query)

        return object_list


# file processing
def file_processing(filename):
    try:
        tables = camelot.read_pdf(settings.MEDIA_ROOT+filename, pages='1-end')
        df = pd.DataFrame()
        for i in range(tables.n):
            df_temp = tables[i].df
            df_temp.drop(df_temp.index[0], inplace=True)
            df = df.append(df_temp)

        # dodaje nazwy kolumn i resetuje index
        df.dropna(inplace=True)
        df.columns = ['symbol', 'nazwa', 'cena', 'ilosc']
        df.reset_index(drop=True, inplace=True)

        # tworze tabele z samymi akcesoriami i wszystkie dodaje do tabeli
        df_akcesoria = pd.DataFrame()
        df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('GSM')])
        df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('Ory')])
        df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('Akc')])
        df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('KAT')])
        df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('OEM')])
        df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('AKK')])
        df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('T00')])

        # tworze tabele prepaid i dodaje wszystko do tabeli
        # usuwam startery mnp
        df_prepaid_voice = pd.DataFrame()
        df_prepaid_net = pd.DataFrame()
        df_prepaid_voice = df_prepaid_voice.append(df[df.symbol.str.startswith('ST')])
        df_prepaid_voice.drop(df_prepaid_voice[df_prepaid_voice['symbol'] == 'ST-P4-DALAS-MNP-MS'].index, inplace=True)
        df_prepaid_voice.drop(df_prepaid_voice[df_prepaid_voice.symbol.str.startswith('ST-P4-INT')].index, inplace=True)
        df_prepaid_net = df_prepaid_net.append(df[df.symbol.str.startswith('ST-P4-INT')])

        # tworze tabele z urzadzeniami i wszystkie dodaje do tabeli
        df_urzadzenia = pd.DataFrame()
        df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('TE')])
        df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('UZ')])
        df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('ZE')])
        df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('GA')])
        # na koniec usuwam wszystkie telefony DEMO
        df_urzadzenia.drop(df_urzadzenia[df_urzadzenia.nazwa.str.contains('DEMO')].index, inplace=True)

        # tworze tabele ze zdrapkami
        df_zdrapki = pd.DataFrame()
        df_zdrapki = df_zdrapki.append(df[df.symbol.str.startswith('VO')])

        # tworze tabele ze sprzetem na uzyczenie i foliami clearplex
        df_uzyczenie = pd.DataFrame()
        df_uzyczenie = df[df.symbol.str.startswith('UZ')]
        df_folie = pd.DataFrame()
        df_folie = df[df.nazwa.str.contains('Clearplex', case=False)]

        # przygotowuje do zapisu do bazy
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        db_name = settings.DATABASES['default']['NAME']

        db_url = 'postgresql://{user}:{password}@localhost:5432/{db_name}'.format(
            user=user,
            password=password,
            db_name=db_name,
        )

        engine = create_engine(db_url, echo=False)


        #print('przygotowuje dane statu magazynowego')
        df_to_sql = pd.DataFrame()
        df_to_sql = df_to_sql.append(df_akcesoria)
        df_to_sql = df_to_sql.append(df_urzadzenia)
        df_to_sql.dropna(inplace=True)
        df_to_sql['ilosc'] = df_to_sql['ilosc'].astype(str).astype(int)
        df_to_sql.loc[:, ('nazwa')].map(lambda x: x.replace('\n', ''))
        df_to_sql['searchstring'] = df_to_sql['nazwa'].map(lambda x: x.lower())
        df_to_sql['searchstring'] = df_to_sql['searchstring'].map(lambda x: x.replace(' ', ''))
        df_to_sql.reset_index(drop=True, inplace=True)
        df_to_sql.index.rename('id', inplace=True)


        #zapisuje do bazy danych
        df_to_sql.to_sql(StanAkcesoria._meta.db_table, con=engine, if_exists='replace')

        raport = {
            "telefony_elza": df_urzadzenia['ilosc'].astype(int).sum(),
            "voice_elza": df_prepaid_voice['ilosc'].astype(int).sum(),
            "data_elza": df_prepaid_net['ilosc'].astype(int).sum(),
            "zdrapki_elza": df_zdrapki['ilosc'].astype(int).sum(),
            "uzyczenie_elza": df_uzyczenie['ilosc'].astype(int).sum(),
            "folia_elza": df_folie['ilosc'].astype(int).sum()
        }

        return raport

    except:
        return None

@login_required
def upload_file_to_raport(request):
    template_name = 'upload_file.html'

    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        processed_file = file_processing(filename)
        if processed_file:
            raport = Raport(
                kto = request.user,
                telefony_elza = processed_file['telefony_elza'],
                voice_elza = processed_file['voice_elza'],
                data_elza = processed_file['data_elza'],
                zdrapki_elza = processed_file['zdrapki_elza'],
                uzyczenie_elza = processed_file['uzyczenie_elza'],
                folia_elza = processed_file['folia_elza']
            )
            raport.save()
            return redirect("inwentaryzacja:inwentaryzacja-update", pk=raport.id)
        return render(request, 'magazyn/upload_file.html', {
            'error': "Coś poszło nie tak"
        })


    return render(request, 'magazyn/upload_file.html')

@login_required
def upload_file_to_magazyn(request):
    template_name = 'upload_file.html'

    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        processed_file = file_processing(filename)
        if processed_file:
            return redirect("magazyn:lista-akcesorii")
        return render(request, 'magazyn/upload_file.html', {
            'error': "Coś poszło nie tak"
        })


    return render(request, 'magazyn/upload_file.html')
