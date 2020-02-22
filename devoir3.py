# coding : utf-8

# Bonjour Jean-Hugues! Voici mon troisième devoir qui a été bien agréable à réaliser, surtout grâce à votre aide précieuse. J'ai décidé de moissonner les données de LaPresse.ca en faisant ressortir tous les URLS, titres, auteurs, dates de publication et contenus des articles de janvier 2020.
# Vous trouverez ma démarche justifiée en #commentaires. Bonne lecture! Amélie :-) 

import requests, csv
from bs4 import BeautifulSoup
# Importation des fichiers nécessaires à la création du .csv

url = "https://www.lapresse.ca/archives/2020/1/"
# Travail de moissonnage fait à partir de cette URL choisie

fichier = "moissonnage.csv"
# Création du futur fichier.csv

entetes = {
    "User-Agent": "Amélie Brissette - 5147780087 : requête envoyée dans le cadre du cours de journalisme EDM4466 à l'UQAM", 
    "From": "amelie-brissette@hotmail.com"
} 
# Création d'une carte de visite informatique (pas obligatoire à la réussite du devoir mais c'est éthique)
#print(entetes) Petit test print pour confirmer que l'entêtes s'affiche correctement [réussi] 

n = 0
#Création d'un compteur

date = list(range(1,32))
# Création de la fin de l'URL qui contient toutes les dates

for janvier in date:
    urlJanvier = url + str(janvier) + ".php"
    urlJanvier.strip() # Permet d'avoir un URL complet et sans espace. 
    print(urlJanvier)
    # Création de la boucle qui permet d'imprimer toutes les URLS dans les archives du mois de janvier sur LaPresse.ca. 
    
    site = requests.get(urlJanvier, headers=entetes)
    print(site.status_code)

    page = BeautifulSoup(site.text, "html.parser")
    # print(page) Petit test pour vérifier que tout le script contenu dans l'url s'imprime correctement [réussi].

    articles = page.find("ul", class_="square square-spread").find_all("li")
    # Création de la variable [articles] qui va me permettre de sélectionner le script désiré contenu dans l'URL.
    #print(articles) Petit test pour voir si le scipt s'imprime au complet [réussi].

    for article in articles:
        lapresse = []
        n += 1
        urlArticle = article.find("a")["href"]
        # Retirer la liste des URLS voulues de la page Web.
        print(n, urlArticle) # Ça fonctionne! Les URLS s'impriment.

        siteArticle = requests.get(urlArticle, headers=entetes)
        pageArticle = BeautifulSoup(siteArticle.text, "html.parser")

        date1 = page.find("h3", class_="archives-date").text
        print(date1)
        # Création de l'élément [date1] qui correspond à la journée d'archives du mois de janvier.

        try:
            titre = pageArticle.find("span", class_="title titleModule__main").text.strip()
        except:
            try:
                titre = pageArticle.find("div", class_="article-header").text.strip()
            except:
                titre = "Sans titre"
        print(titre)
        # Création de l'élément [titre] avec l'ajout d'une exception lorsque le titre est inconnu.

        try:
            date2 = pageArticle.find("span", class_="publicationsDate--type-publication").text.strip()
        except:
            date2 = "Sans date"
        print(date2)
        # Création de l'élément [date2] qui correspond à la date de publication de l'article avec l'ajout d'une exception lorsque la date est inconnue.

        try:
            auteur = pageArticle.find("span", class_="name authorModule__name").text.strip()  
        except:
            auteur = "Inconnu"
        print("Par", auteur)
        # Création de l'élément [auteur] avec l'ajout d'une exception lorsque l'auteur est inconnu et ajout du "Par" afin de rendre la lecture du fichier plus limpide.

        pars = pageArticle.find_all("p")
        texte = ""
        for par in pars:
            print(par.text.strip())
            texte = texte + par.text.strip()
        # Impression du script des paragraphes des URLS sélectionnées.

        texte = texte.replace("\u2009", "")
        texte = texte.replace("\u2981", "")
        texte = texte.replace("\u2028", "")
        texte = texte.replace("\u202f", "")
        texte = texte.replace("\u0301", "")
        texte = texte.replace("\u0302", "")
        texte = texte.replace("\u011f", "")
        texte = texte.replace("\u0100", "")
        # Remplacement des variables nuisant à l'impression du code; problème qui se glissait sans cesse dans l'impression de mon code, mais qui semble être lié aux ordinateurs Windows car tout fonctionne sur un Mac. 
        # Comme ce code-erreur répétitif se produit à l'article du 7 janvier #448, mon fichier CSV s'arrête également à cet article. 
        
        print("."*20)
        # Création d'un séparateur qui vient effectuer une distinction entre les groupes de données. 

        lapresse.append(n)
        lapresse.append(date1)
        lapresse.append(urlArticle)
        lapresse.append(titre)
        lapresse.append(date2)
        lapresse.append(auteur)
        lapresse.append(texte)
        #print(lapresse) Petit test  pour voir si le contenu s'imprime correctement [réussi].

        presse = open(fichier,"a")
        moissonnage_lapresse = csv.writer(presse)
        moissonnage_lapresse.writerow(lapresse) 
        # Ouverture du fichier csv contenant toutes les données sélectionnées.

        # Fin du moissonnage de données. 
