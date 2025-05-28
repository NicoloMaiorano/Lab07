import copy
from copy import deepcopy

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self.n_soluzioni = 0
        self.soluzione_ottima = []
        self.costo_ottimo = -1

    def umiditaMedia(self, mese):

        situazioni = MeteoDao.get_all_situazioni()
        somma = 0
        i = 0

        for s in situazioni:
            if str(s.data.month) == str(mese):
                somma = somma + s.umidita
                i = i+1

        media = somma/i

        return media

    def ammissibile(self, candidato, parziale):
        #vincolo 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidato.localita:
                counter = counter+1
        if counter >= 6:
            return False
        #vincolo permanenza
        if len(parziale) == 0:
            return True

        if len(parziale)<3:
            if candidato.localita != parziale[0].localita:
                return False
        else:
            if parziale[-1].localita != parziale[-2].localita or parziale[-1].localita != parziale[-3].localita or parziale[-2].localita != parziale[-3].localita:
                if parziale[-1].localita != candidato.localita:
                    return False

        return True


    def sequenza(self, mese):
        self.n_soluzioni = 0
        self.soluzione_ottima = []
        self.costo_ottimo = -1
        situazioni = MeteoDao.get_situazioni_meta_mese(mese)
        self.ricorsione([], situazioni)
        #print(self.n_soluzioni)
        return self.soluzione_ottima, self.costo_ottimo

    def trova_candidati(self, parziale, situazioni):

        giorno = len(parziale)+1 #perchè se la lista è lunga 2 vuol dire che mi serve il terzo giorno, quindi +1
        candidati = []
        for situazione in situazioni:
            if situazione.data.day == giorno:   #se il giorno corrisponde allora lo posso considerare uno dei candidati possibili
                candidati.append(situazione)
        return candidati

    def calcola_costo(self, parziale):

        costo = 0
        citta_precedente = ""

        for situazione in parziale:
            if citta_precedente != situazione.localita:
                costo = costo + 100
            else:
                costo = costo + situazione.umidita

            citta_precedente = situazione.localita

        return costo


    def ricorsione(self, parziale, situazioni):

        if len(parziale) == 15:  #condizione terminale
            self.n_soluzioni += 1
            costo = self.calcola_costo(parziale)
            #print(parziale)

            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)
        else: #condizione ricorsiva
            candidati = self.trova_candidati(parziale, situazioni)
            for candidato in candidati:
                if self.ammissibile(candidato, parziale) == True:
                    parziale.append(candidato)
                    self.ricorsione(parziale, situazioni)
                    parziale.pop()


if __name__ == '__main__':
        my_model= Model()
        my_model.sequenza()
