from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from sqlalchemy import create_engine
import camelot
import pandas as pd
from time import process_time
from .models import StanAkcesoria
from inwentaryzacja.models import Raport

# Create your views here.

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



def simple_upload(request):
    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)


            # przerabiamy plik pdf
        try:
            t_start = process_time()
            print(t_start)
            tables = camelot.read_pdf(settings.MEDIA_ROOT+filename, pages='1-end')
            t_stop = process_time()
            print(t_stop)
            df = pd.DataFrame()
            print("przekonwertowano plik w ciągu ", t_stop-t_start, " sekund.")
            for i in range(tables.n):
                df_temp = tables[i].df
                df_temp.drop(df_temp.index[0], inplace=True)

                df = df.append(df_temp)

            # dodaje nazwy kolumn i resetuje index
            df.columns = ['symbol', 'nazwa', 'imei', 'ilosc']
            df.reset_index(drop=True, inplace=True)


            # zapisujemy plik i to koniec programu dla windows
            #df.to_csv('stan.csv')



            # Obróbka pliku to już na serwerze się bedzie działo

            # tworze tabele z samymi akcesoriami i wszystkie dodaje do tabeli
            df_akcesoria = pd.DataFrame()
            df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('GSM')])
            df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('Ory')])
            df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('Akc')])
            df_akcesoria = df_akcesoria.append(df[df.symbol.str.startswith('KAT')])
            print("Ilość akcesorii: ", df_akcesoria['ilosc'].astype(int).sum())

            df_akc = df_akcesoria[['symbol', 'nazwa', 'ilosc']]
            #df_akc['ilosc'] = df_akc['ilosc'].astype(str).astype(int)

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

            df_akc.reset_index(drop=True, inplace=True)
            df_akc['id'] = df_akc.index
            df_akc.set_index('id')

            df_akc['nazwa'] = df_akc['nazwa'].map(lambda x: x.replace('\n', ''))
            # usuwamy spacje i duze litery aby przygotowac string do wyszukiwania
            df_akc['searchstring'] = df_akc['nazwa'].map(lambda x: x.lower())
            df_akc['searchstring'] = df_akc['searchstring'].map(lambda x: x.replace(' ', ''))

            df_akc.to_sql(StanAkcesoria._meta.db_table, con=engine, if_exists='replace')


            # tworze tabele prepaid i dodaje wszystko do tabeli
            # usuwam startery mnp
            df_prepaid_voice = pd.DataFrame()
            df_prepaid_net = pd.DataFrame()
            df_prepaid_voice = df_prepaid_voice.append(df[df.symbol.str.startswith('ST')])
            df_prepaid_voice.drop(df_prepaid_voice[df_prepaid_voice['symbol'] == 'ST-P4-DALAS-MNP-MS'].index, inplace=True)
            df_prepaid_voice.drop(df_prepaid_voice[df_prepaid_voice.symbol.str.startswith('ST-P4-INT')].index, inplace=True)
            df_prepaid_net = df_prepaid_net.append(df[df.symbol.str.startswith('ST-P4-INT')])
            print(df_prepaid_voice)
            print(df_prepaid_net)

            #print("Ilość prepaid: ", df_prepaid['ilosc'].astype(int).sum())

            # tworze tabele z urzadzeniami i wszystkie dodaje do tabeli
            df_urzadzenia = pd.DataFrame()
            df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('TE')])
            df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('UZ')])
            df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('ZE')])
            df_urzadzenia = df_urzadzenia.append(df[df.symbol.str.startswith('GA')])
            print("Ilość urządzeń: ", df_urzadzenia['ilosc'].astype(int).sum())

            # tworze tabele ze zdrapkami
            df_zdrapki = pd.DataFrame()
            df_zdrapki = df_zdrapki.append(df[df.symbol.str.startswith('VO')])
            print("Ilość zdrapek: ",df_zdrapki['ilosc'].astype(int).sum())

            raport = Raport(
                kto = request.user,
                telefony_elza = df_urzadzenia['ilosc'].astype(int).sum(),
                voice_elza = df_prepaid_voice['ilosc'].astype(int).sum(),
                data_elza = df_prepaid_net['ilosc'].astype(int).sum(),
                zdrapki_elza = df_zdrapki['ilosc'].astype(int).sum()
            )

            raport.save()

            return redirect("inwentaryzacja:inwentaryzacja-update", pk=raport.id)

        except:
            print("Coś poszło nie tak")
            return render(request, 'magazyn/simple_upload.html', {
                'error': "Coś poszło nie tak"
            })
        # return render(request, 'magazyn/simple_upload.html', {
        #     'zdrapki': df_zdrapki['ilosc'].astype(int).sum(),
        #     'urzadzenia': df_urzadzenia['ilosc'].astype(int).sum(),
        #     'prepaid_net': df_prepaid_net['ilosc'].astype(int).sum(),
        #     'prepaid_voice': df_prepaid_voice['ilosc'].astype(int).sum()
        # })
    #return reverse("inwentaryzacja:inwentaryzacja-lista")
    return render(request, 'magazyn/simple_upload.html')
