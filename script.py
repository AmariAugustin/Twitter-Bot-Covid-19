import tweepy
from tweepy import api
import requests
import json
import time
import os
from GrabzIt import GrabzItImageOptions
from GrabzIt import GrabzItClient
import os
from PIL import Image
import webbrowser

sourceFileDir=os.path.dirname(os.path.abspath(__file__))
os.chdir(sourceFileDir)

class Data:
    def __init__(self):
        """
        Peux etre associé au fonction date, nouveau_cas_positif, nombre_mort_debut, nombre_mort aujourd'hui, rea, nombre_rea_24h, hosp, hosp_24h\n
        Ne prend aucun argument \n
        Ne renvoie rien quand la fonction est appelée toute seule
        """
        self.data_Covid= requests.get("https://coronavirusapifr.herokuapp.com/data/live/france")
        self.data_Covid_Json= self.data_Covid.json()
    def date(self):
        """
        Permet de récupèrer la date des donnees recuperer\n
        Ne prend aucun argument\n
        Renvoie la date de prélevement des informations sour la forme jj/mm/aaaa
        """
        listeDate = self.data_Covid_Json[0]['date']
        liste = [i for i in listeDate]
        return liste[8]+liste[9]+"/"+liste[5]+liste[6]+"/"+liste[0]+liste[1]+liste[2]+liste[3]
    def nouveau_cas_positif(self):
        """
        Permet de récupèrer le nombre de nombre de nouveau cas positif au covid grace a l'api\n
        Ne prend aucun argument\n
        Renvoie une valeur de type int 
        """
        return self.data_Covid_Json[0]['conf_j1']
    def nombre_mort_debut(self):
        """
        Permet de récupèrer le nombre de mort du au covid depuis le debut de l'épidémie grace a l'api\n
        Ne prend aucun argument\n
        Renvoie une valeur de type int  
        """
        return self.data_Covid_Json[0]['dc_tot']
    def nombre_mort_aujourdhui(self):
        """
        Permet de récupèrer le nombre de nombre de mort les dérnières 24h causée par le covid grace a l'api\n
        Ne prend aucun argument \n
        Renvoie une valeur de type int 
        """
        return self.data_Covid_Json[0]['date']
    def rea(self):
        return self.data_Covid_Json[0]['rea']
    def nombre_rea_24h(self):
        """
        Permet de récupèrer le nombbre de nombre de personne entrée en réa les dèrenieres 24h causée par le covid grace a l'api\n
        Ne prend aucun argument \n
        Renvoie une valeur de type int 
        """
        return self.data_Covid_Json[0]['incid_rea']
    def hosp(self):
        """
        Permet de récupèrer le nombbre de nombre de personne actuellement en hospitalisation causée par le covid grace a l'api\n
        Ne prend aucun argument \n
        Renvoie une valeur de type int 
        """
        return self.data_Covid_Json[0]['hosp']
    def hosp_24h(self):
        """
        Permet de récupèrer le nombbre de nombre de personne entrée en hospitalisation les dèrenieres 24h causée par le covid grace a l'api\n
        Ne prend aucun argument \n
        Renvoie une valeur de type int 
        """
        return self.data_Covid_Json[0]['incid_hosp']

class Graphique:
    def __init__(self):
        """
        Peux etre associé au fonctions screen, et screnn2\n
        Ne prend aucun argument\n
        Ne renvoie rien quand la fonction est appelée toute seule 
        """
        self.auth = GrabzItClient.GrabzItClient("ODI0NjUzYzE2OGU2NGIxZGIzZjE5OTIxYWZmZDE0ZTA=", "Fjg/Pz9bPz8/PzV0FD05PxI/dj9XPz98Fj9Scj8/Fz8=")
        self.option = GrabzItImageOptions.GrabzItImageOptions()
        self.option.format = "png"
    def screen(self):
        """
        Permet de récupèrer un graphique montrant l'évolution du covid en france sur le site du gouvernement\n
        Ne prend aucun argument \n
        Renvoie une image en png se situant dans le fichier "data"
        """
        self.auth.URLToImage("https://www.gouvernement.fr/info-coronavirus/carte-et-donnees#situation_epidemiologique_-_tests_positifs_chez_les_personnes_vaccinees_et_non_vaccinees", self.option)
        self.auth.SaveTo("data/result.png")
    def screen2(self):
        """
        Permet de récupèrer un graphique montrant l'évolution du covid en france sur le site du gouvernement\n
        Ne prend aucun argument \n
        Renvoie une image en png se situant dans le fichier "data"
        """
        self.auth.URLToImage("https://www.gouvernement.fr/info-coronavirus/carte-et-donnees#situation_epidemiologique_-_nombre_moyen_de_nouveaux_cas_confirmes_quotidiens",self.option)
        self.auth.SaveTo("data/result2.png")


auth = tweepy.OAuthHandler("KEY", "KEY")
auth.set_access_token("KEY", "KEY")
api_tw= tweepy.API(auth)

class Tweet:
    def __init__(self):
        """
        Peux etre associé au fonction tweet_du_jours, et thread1\n
        Ne prend aucun argument\n
        Ne renvoie rien quand la fonction est appelée toute seule 
        """
        self.data= Data()
        #self.graph=Graphique()
        self.tweet1=None
        #self.graph.screen()
        #self.graph.screen2()
    def tweet_du_jour(self):
        """
        Permet de tweeter le tweet du jour avec les bonnes information, avec une présentation correcte \n
        Ne prend aucun argument\n
        Renvoie un tweet sur le compte twitter associée au token précédemment renseigner\n
        Ne renvoie rien dans la console
        """
        self.tweet1=api_tw.update_status(status= 
        "🔴 Le " +  str(self.data.date()) + " en France  🇫🇷  : " + "\n" + "\n" + 
        "📈 Nombre de nouveau cas  : "+ str(self.data.nouveau_cas_positif()) + "\n" +  
        "​👨‍⚕️️​ Patients actuellement dans les services de réanimation : " + str(self.data.rea()) + " ( Nouvelle admition en 24h : " + str(self.data.nombre_rea_24h())+" )"+ "\n" + 
        "🏥 Patients actuellement hospitalisés : " + str(self.data.hosp()) + " ( Nouvelle admition en 24h : " + str(self.data.hosp_24h())+" )"
        )
        self.tweet1
    def thread1(self):
        """
        Permet de tweeter sous la forme de réponse au tweet du jour un graphique \n
        Ne prend aucun argument\n
        Renvoie un tweet sur le compte twitter associée au token précédemment renseigner\n
        Ne renvoie rien dans la console
        """
        api_tw.update_status("@CovId19_InfoBot Voici un lien qui mène vers le site du gouvernement afin d'avoir plus d'indo sur le covid 19 en France : https://www.gouvernement.fr/...." ,in_reply_to_status_id=self.tweet1.id_str) 



tweet= Tweet()
try:
    tweet.tweet_du_jour()
    print("#########  Tweet du jour postée a l'instant  #########") 
    tweet.thread1()
    print("#########  Réponse Ajouté  #########")
    webbrowser.open("https://twitter.com/CovId19_InfoBot")
except:
    print("#########  Tweet du jour déja postée  #########")
    webbrowser.open("https://twitter.com/CovId19_InfoBot")

