# -*- coding: utf-8 -*-

'''
Module avec l'ensemble des fonctions utilisées :
-scrap_twitter
-construction_network
-construction_liens
...
...
'''


#IMPORTS
import pdb
import tweepy
import pickle
import sys
import networkx as nx
import time
import matplotlib.pyplot as plt
import math
import os
import csv
import folium


'''Fonction scrap_twitter : permet de récupérer la base de données globales des informations
du compte twitter voulu, en fonction des identifiants pour l'API twitter
permet de construire les liens de la BDD globale.

-consumer_key, consumer_secret, access_token, access_token_secret, compte_twitter = str

exemple :
Datas = scrap_twitter("V4oZsoDlApl4jM5ykvZ4HCv4Q","0Pa1P4WU00j944BYK41K1p8pWjFbEnzeYHZoWIAunQl6FMDjq3",
        "1311020670-BRnEdRVcpxZy2ObVz4nfAl4w6CIncXlFE0WnRhm","ungu6tVmt4jbxFC2TLSXPsL7zWmQDo41KtWNUOJwnZmW1","@MonZippo")
        
Conseils : laisser la base de donnée qui n'a pas été finie de scrappée avec le même nom et dans le même dossier (pour pouvoir recommencer la collecte)

LIMITE : scrapping des informations des followers du compte étudié !
'''

def scrap_twitter(consumer_key, consumer_secret, access_token, access_token_secret, compte_twitter):

        #Authentification API
        auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret) 
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        
        
        try:
                with open(compte_twitter+'/Datas_globales_'+compte_twitter,'rb') as fichier:
                        Base=pickle.load(fichier)

                print('on recommence la collecte')
                
                List_Followers_Compte=Base[compte_twitter]['Datas']['List_Followers']

        except:
                print('on commence la collecte pour la première fois')
                # Trouver le nombre de followers de compte_twitter
                user_information=api.get_user(screen_name=compte_twitter)
                nbre_followers_compte=user_information.followers_count

                # Trouver les identifiants des followers de compte_twitter
                List_Followers_Compte=[]
                for iden in tweepy.Cursor(api.followers_ids,screen_name=compte_twitter).items(nbre_followers_compte):
                        List_Followers_Compte.append(iden)


                Base={}
                Base[compte_twitter]={}
                Base[compte_twitter]['Datas']={}
                Base[compte_twitter]['Datas']['List_Followers']=List_Followers_Compte
        i=0
        for iden in List_Followers_Compte:
                if iden in Base[compte_twitter]['Datas'].keys():
                        i=i+1

                else:
                        try:    
                                A={}

                                user_information=api.get_user(id=iden)
                                A['name']=user_information.name
                                A['screen_name']=user_information.screen_name
                                A['created_at']=user_information.created_at

                                A['nb_followers']=user_information.followers_count
                                A['nb_friends']=user_information.friends_count
                                A['nb_tweets']=user_information.statuses_count


                                sn=A['screen_name']
                                fol=A['nb_followers']
                                fr=A['nb_friends']
                                tw=A['nb_tweets']

                                List_Followers=[]
                                for iden_fol in tweepy.Cursor(api.followers_ids,screen_name=sn).items(fol):
                                        List_Followers.append(iden_fol)
                        
                                A['List_Followers']=List_Followers
                        

                                List_Friends=[]
                                for iden_fr in tweepy.Cursor(api.friends_ids,screen_name=sn).items(fr):
                                        List_Friends.append(iden_fr)

                                A['List_Friends']=List_Friends
                                

                                
                                Base[compte_twitter]['Datas'][iden]=A
                                Base[compte_twitter]['Datas'][iden]['Problem']='non'


                        except Exception as exc:
                                print(iden,repr(exc))
                                Base[compte_twitter]['Datas'][iden]={}
                                Base[compte_twitter]['Datas'][iden]['Problem']='oui'
                                


                        i=i+1
                        
                        directory=compte_twitter
                        if not os.path.exists(directory):
                                os.makedirs(directory)
                                
                        with open(compte_twitter+'/Datas_globales_'+compte_twitter,'wb') as fichier:
                                pickle.dump(Base,fichier)
                
                        print(i, " comptes twitter récupérés, sur ",len(List_Followers_Compte))
                        print(api.rate_limit_status()['resources']['followers']['/followers/ids'])
                        print(api.rate_limit_status()['resources']['friends']['/friends/ids'])


        
        with open(compte_twitter+'/Datas_globales_'+compte_twitter,'rb') as fichier:
            
            Base=pickle.load(fichier)

        construction_liens(compte_twitter+'/Datas_globales_'+compte_twitter)
        

        
          



'''
Fonction construction_liens : permet de construire le dictionnaire de liens, entre les individus d'une
base de donnée filtrée. 
-path : chemin d'accès de la base de donnée filtrée (car liens d'une BDD classique déjà créés)

->Il faut les ajouter à la base de donnée filtrée... Ou le créer dès le filtrage !! (comme pour BDD classique)

exemple :
construction_liens('/BDD/MonZippo')
'''

def construction_liens(path):
    #Ca marche
    #path = '@MonZippo/Datas_globales_@MonZippo'
    with open (path,'rb') as fichier:
        Base=pickle.load(fichier)
    for k in Base.keys():
        
        Base[k]['Liens']={}
        for iden1 in Base[k]['Datas'].keys():
            if iden1 != "List_Followers":
                Base[k]['Liens'][iden1]={}
                for iden2 in Base[k]['Datas'].keys():
                    if iden2 != "List_Followers":
                        if iden2 != iden1:
                            try:
                                if iden2 in Base[k]['Datas'][iden1]['List_Followers']:
                                
                            
                                
                                    Base[k]['Liens'][iden1][iden2]=1
                                else :
                                    Base[k]['Liens'][iden1][iden2]=0
                            except:
                                continue
                        else :
                            pass
    
    with open(path, 'wb') as fichier:
        pickle.dump(Base, fichier)                      
                
        

        
    

        



'''
Fonction construction_network : représente le network en image d'un base de donnée. 
Paramètres :
#Paths + format sortie
path_entree='Datas_Test_filtrees7'
path_sortie='ReseauTest'
format_sortie = "png"

#Général
kv=0.7 -> Ecart entre les noeuds
nb_reptition = 2 -> Plusieurs représentations (permet de choisir le reseau le plus lisible)
titre="Reseau essai2" -> Titre affiché au dessus du graphe.
zoom=(40 ,40) #=figsize -> "Zoom" sur le reseau
axes = 0 -> 1 pour faire apparaitre les axes

#liens
taille_liens =5 -> largeur des liens
#noeuds
couleur_noeuds='yellow'
taille_noeuds = 4000
#labels
bin_labels = 1
couleur_labels='black'
taille_labels=4
type_labels = 'name' #name, screen_name, iden.

Exemple :
construction_network('Datas_Test_filtrees7','ReseauTest',"png",0.7,2, "Reseau essai2", (40 ,40), 0, 5, 'yellow', 4000, 1, black, 4, 'screen_name')
'''

def construction_network(path_entree, path_sortie, format_sortie, kv, nb_repetition, titre, zoom, axes, color_bg, couleur_liens, taille_liens,
 couleur_noeuds, taille_noeuds, bin_labels, couleur_labels, taille_labels, type_labels):
     
     #Ouverture BDD
     with open (path_entree,'rb') as fichier:
         
         Base=pickle.load(fichier)
     i=0
     while i<nb_repetition :
         for compte_twitter in Base.keys():
             #Creation du graphe
             g=nx.Graph()
             #Creation des noeuds
             for elem in Base[compte_twitter]['Datas'].keys():
                 if elem !="List_Followers":
                     g.add_node(elem)
             print("Nombre de noeuds :", len(g.nodes()))
                 
                 
                 
             #Ajout liens
             for iden1 in Base[compte_twitter]['Liens'].keys():
                 
                             
                            
                 for iden2 in Base[compte_twitter]['Liens'][iden1].keys():
                             
                     if Base[compte_twitter]['Liens'][iden1][iden2]==1 and g.has_edge(iden1,iden2)==False and iden1!=iden2:
                                 
                                    
                         g.add_edge(iden1, iden2)
                     else:
                                     
                         pass
                
             print('Nombre de liens :', len(g.edges()))




             #REPRESENTATION GRAPHIQUE

             # len(g.node.keys()) = nombre de noeuds = N = 97
             # on prend une valeur = 4*valeur par défaut
             N=len(g.node.keys())


             #Position
             #kv=(1/math.sqrt(N))*4 #sqrt = square root = racine carré --> kv = optimal distance entre les nodes. Si on augmente kv, il y aura + de distance entre nodes en moyenne = plus lisible. Ici, valeur pas défaut (1/sqrt(N)) fois 4

             p =nx.spring_layout(g,k=kv) #ecart entre les noeuds

             #Taille graphe
             plt.figure(figsize=zoom) #taille du graph, plus c'est petit, plus on "zoom"

             #Nodes Labels : Name / Screen_name / ID
             if bin_labels == 1 :
                 Node_Label={}
                 if type_labels=='name' or 'screen_name':
                     for noeud in g.node.keys():
                         
                         try:
                             Node_Label[noeud]=Base[compte_twitter]['Datas'][noeud][type_labels]
                         except:
                             print('pb de recuperation de key')
                             pdb.set_trace()
                             pass
                         try:
                             print(Base[compte_twitter]['Datas'][noeud]['name'],Base[compte_twitter]['Datas'][noeud]['screen_name'] )
                         except:
                             print('Pas réussi à récup le name de', noeud)
                 else:
                     for noeud in g.node.keys():
                         Node_Label[noeud]=noeud
            


             #DRAW
            
             #Draw noeuds
             nx.draw_networkx_nodes(g, pos=p,alpha=1, node_size=taille_noeuds, node_color=couleur_noeuds )


             #Draw Liens
             nx.draw_networkx_edges(g, pos=p, width=taille_liens, edge_color=couleur_liens)

             #Draw Labels
             if bin_labels==1 :
                 nx.draw_networkx_labels(g, pos=p, labels=Node_Label, font_size=45,font_color=couleur_labels, alpha=taille_labels)




             #Titre
             plt.title(titre, size=75)

             #Axes
             if axes == 1:
                 plt.axis('on')
             else :
                 plt.axis('off')
             
             #Color background
             #plt.figure().set_facecolor(color_bg)

             #Enregistrement du fichier (si une répétition)
             if nb_repetition<2:                 
                 plt.savefig(path_sortie+'.'+format_sortie, format=format_sortie)
             else :
                 i=i+1
                 plt.savefig(path_sortie+str(i)+'.'+format_sortie, format=format_sortie)
                 
  
         


        



'''
Fonction filtrage :
1-Utilisateur renseigne le chemin de la BDD voulue (paramètre de la fonction) -> Import
2-Applique un/des filtrs à une BDD en fonction de différents critères :
nb de friends, nb de followers, mesures, probleme de recup datas...
3-Construit le dictionnaire de liens associés à la base de donnée filtrée.
4-Sauvergarde la BDD filtrée dans un chemin décidé par l'utilisateur

exemple : filtrage('@MonZippo/Datas_globales_@MonZippo', 0, 0, 0, 0, 1, 50, 0, 0, 0, 0, 0, 0, 0, 1, '@MonZippo/Datas_filtrees1_MonZippo')

LIMITE : pour le moment, on peut supprimer que des comtpes "inferieurs" à un paramètre
'''




def filtrage(path_entree, tweets_bin, nb_tweets, friends_bin, nb_friends, followers_bin, nb_followers, mesure_bin, degree_centrality_bin,
             closeness_bin, eigen_vector_bin, pourcentage, csv_bin, path_sortie):
                 
                 
                
                 
                 #Variables locales
                 liste_del=[]
                 Dict_mesure = {}
                 Nli = []
                 compte_pb=0
        
                 #Toutes les variables choisies par l'utilisateur seront récupérées via l'interface
        
                 #------- importation de la base --------
                 try:
                     
                     with open(path_entree,'rb') as fichier:
                         
                         Base=pickle.load(fichier)
                 except:
                     
                     print('Probleme, base de donnée indiquée introuvable')
                     pass
                 #------ création du dossier de sortie, si il n'existe pas déjà --------
                 '''Fait par l'utilisateur avec l'outil Browse'''
    
                
                 #Comparatif 1:
                 for elem in Base.keys():
                     comparatif = len(Base[elem]['Datas'].keys())- 1
                     print('Nb de compte de la base AVANT filtre : ', comparatif)
        
                 #Filtre del utilisateurs avec un pb de recupération de données:
                 for compte_twitter in Base.keys():
                     for iden in Base[compte_twitter]['Datas'].keys():
                         if iden != 'List_Followers':
                             if Base[compte_twitter]['Datas'][iden]['Problem']=='oui':
                                 liste_del.append(iden)
                #Suppression dans la foulée pour pouvoir appliquer les autres filtres:
                     for iden in liste_del :
                         del Base[compte_twitter]['Datas'][iden]
                         compte_pb=compte_pb+1
                 print('Nombre de compte twitter supprimés car problème de récupération de données : ', compte_pb)
                 liste_del=[]
                 
                 
                 #---- Filtre followers ----------
                 if followers_bin == 1:
                     
                        
                                 
                     for compte_twitter in Base.keys():
                         
                        
                        
                             
                         for iden in Base[compte_twitter]['Datas'].keys():
                             if iden != "List_Followers":
                                 if Base[compte_twitter]['Datas'][iden]['nb_followers'] < nb_followers :
                                     liste_del.append(iden)
                                     print('Suppression de ', Base[compte_twitter]['Datas'][iden]['name'], 'car il a ', Base[compte_twitter]['Datas'][iden]['nb_followers'], 'followers (abonnés)')
                                 else:
                                     pass
                            


                 #----- Filtre friends ---------
                 if friends_bin == 1:
                     
                     for compte_twitter in Base.keys():
                         for iden in Base[compte_twitter]['Datas'].keys():
                             
                              if iden != "List_Followers":
                                  

                                  if Base[compte_twitter]['Datas'][iden]['nb_friends'] < nb_friends:
                                      print('Suppression de ', Base[compte_twitter]['Datas'][iden]['name'], 'car il a ', Base[compte_twitter]['Datas'][iden]['nb_tweets'], 'friends')
                                      liste_del.append(iden)
                                  else:
                                      pass
                              else:
                                  pass
                 

                         
                 else:
                     pass
                         
                 #----- Filtre tweets ----------- 
        
                 if tweets_bin == 1:
                     for compte_twitter in Base.keys():
                         for iden in Base[compte_twitter]['Datas'].keys():
                             if iden != "List_Followers":
                                 if Base[compte_twitter]['Datas'][iden]['nb_tweets'] < nb_tweets :
                                     print('Supression de ', Base[compte_twitter]['Datas'][iden]['name'], 'car il a ', Base[compte_twitter]['Datas'][iden]['nb_tweets'], 'Tweets')
                                     liste_del.append(iden)
                                 else:
                                     pass
                                 
        
                 #------- MESURE ---------- #
                 #Attention, puisqu'il y a une liste del : on parle bien de la mesure en fonction de l'ensemble de la BDD d'origine.
                 
                 
                 if mesure_bin == 1:
                     print('Filtre par MESURE')    
            
                     #Pour la mesure, il y a besoin de construire le network (noeuds + liens)
                     g=nx.Graph()
                     
                     for compte_twitter in Base.keys():
                         
                         #Ajout noeuds
                         
                         for elem in Base[compte_twitter]['Datas'].keys():
                             
                             if elem != "List_Followers":
                                 
                                 g.add_node(elem)
                
                             
                         #Ajout liens
                        
                         
                         
                         for iden1 in g.node.keys():
                             #print('Iden 1 = ', iden1)
                         
                        
                             for iden2 in g.node.keys():
                                 #print('Iden 2 = ', iden2)
                                 if iden1!=iden2:
                                     if Base[compte_twitter]['Liens'][iden1][iden2]==1 and g.has_edge(iden1,iden2)==False:
                                         g.add_edge(iden1, iden2)
                                     else : 
                                         #print('Pas de lien entre', iden1, 'et', iden2)
                                         pass
                                 else :
                                     #print('Ce sont els mêmes iden : ', iden1, '==', iden2)
                                     pass
                                         
                                     
          
                         #------- degree centrality -------

                         if degree_centrality_bin == 1:
                             Dict_mesure = nx.degree_centrality(g)
                         if closeness_bin == 1:
                             print('Choix de la mesure Closeness')
                             Dict_mesure = nx.closeness_centrality(g)
                         if eigen_vector_bin == 1:
                            Dict_mesure = nx.eigenvector_centrality(g)


                         for noeud in g.node.keys():
                             Nli.append(Dict_mesure[noeud])
                         Nli.sort()
                         seuil = round(len(Nli)*pourcentage)
                         seuil_mesure=(Nli[seuil])
                         print('Seuil pour la mesure : ', seuil_mesure)

                         for n in g.node.keys():
                                
                                       
                             if Dict_mesure[n] < seuil_mesure:
                                 
                                 try:
                                     
                                     
                        
                        
                                     print('Suppression de', Base[compte_twitter]['Datas'][n]['name'], 'car son degré est de', Dict_mesure[n])
                                     liste_del.append(n)
                                 except:
                                     pass
                                     #print('Probleme de key sur ', n)
                                     
                                 
                                     
                                
                             else:
                        
                                 pass
                                
                            
                 #SUPRESSION REELLE DES IDEN DU DICT A PARTIR DE LISTE_DEL
                 
                 for ele in liste_del:
                     try:
                         
                         #print('Supression de ', Base[compte_twitter]['Datas'][ele]['name'])
                         del Base[compte_twitter]['Datas'][ele]
                     except:
                         ('Pas réussi à supprimer ', ele)
                         pass
                         
                         
                 #Comparatif 2:
                 for elem in Base.keys():
                     
                     comparatif = len(Base[elem]['Datas'].keys())- 1
                     print('Nb de compte de la base APRES filtre : ', comparatif)
        
                 #------ CSV ------------#
                 if csv_bin==1:
                     with open(path_sortie+'.csv', 'w') as output:
                            print('ECRITURE CSV')
                         
                         
                            data = csv.writer(output, delimiter=";", lineterminator="\n")
                            row = ['Screen name','ID','nb followers', 'nb friends', 'nb tweets','probleme']
                            data.writerow(row)
                            for compte_twitter in Base.keys():
                                
                                         
                                for iden in Base[compte_twitter]['Datas'].keys():
                                    
                                 
                                    try:
                                        
                                     
                                     #PB : screen name avec emoticones -> passe dans le except
                                        row = [Base[compte_twitter]['Datas'][iden]['screen_name'], iden, Base[compte_twitter]['Datas'][iden]['nb_followers'], Base[compte_twitter]['Datas'][iden]['nb_friends'],Base[compte_twitter]['Datas'][iden]['nb_tweets'], Base[compte_twitter]['Datas'][iden]['Problem']]
                                        data.writerow(row)
                                    except :
                                        
                                        print('Probleme car key = List_Followers au lieu d un ID---> key =', iden)
                                        continue
                 else:
                     
                     
                     pass
        
        
                    
                 #----- Enregistrement ---------
        
                 with open(path_sortie,'wb') as fichier:
                         pickle.dump(Base,fichier)
                 
                 construction_liens(path_sortie)

        
        
                 

                 
                 




'''Fonction scrap_tweets : permet de récupérer les tweets au sens large, d'un ou plusieurs comptes tweeter'''

def scrap_tweets(screen_name, consumer_key, consumer_secret, access_token, access_token_secret, path_sortie) :
    #Variables
    alltweets=[]
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret) 
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    #Scrap tweets
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print("getting tweets before %s"% (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))

    with open(path_sortie,'wb') as fichier:
        
        pickle.dump(alltweets,fichier)
        
        
'''Fonction analyse_tweets qui permet une analyse des tweets en fonction de kw 
(combien de tweets contiennent ce, ou ces kw, au total et par keyword) + par date (au total et par keyword)'''  
def analyse_tweets(path_entree, kw):
    with open(path_entree,'rb') as fichier1:
        Base=pickle.load(fichier1)
        
        for tweet in Base:
            if kw in tweet.text:
                
                print(tweet.text)
                
'''Fonction filtre_tweets permet de filtrer la liste de tweets en fonciton de certains critères : date, retweets, "aime", mot-clés
filtre_tweets("Tweets@Charleseasy", 1, 0, 0, 0, 0, 1, 1, 0, 0, "Tweets@CharleseasyFiltrés")
filtre_tweets("Tweets@Charleseasy", 0, 0, 0, 0, 0, 0, 0, 1, [2018,12,28], "Tweets@CharleseasyFiltrés")
filtre_tweets("Tweets@Charleseasy", 0, 0, 0, 1, ['Australia','basket'], 0, 0, 0, 0, "Tweets@CharleseasyFiltrés")'''
def filtre_tweets(path_entree,bin_del_rt, bin_rt, nb_rt, bin_kw, kw, bin_like, nb_like, bin_date, date, path_sortie):
    with open(path_entree,'rb') as fichier1:
        Base=pickle.load(fichier1)
    
    #Supprimer les retweets
    i=0
    Base_Clean=[]
    if bin_del_rt==1:
        print('\n \n FILTRE SUPRESSION DES RETWEETS')
        for tweet in Base:
            if tweet.text[:2] != "RT":
                print (tweet.text)
                Base_Clean.append(tweet)            
            i=i+1
        Base=Base_Clean
    
            
    #Supprimer les tweets qui ont été retweeté moins de fois que nb_rt
    i=0
    Base_Clean=[]
    if bin_rt==1:
        print('\n \n FILTRE SNOMBRE DE RETWEETS')
        for tweet in Base:
            if tweet.retweet_count > nb_rt:
                print(tweet.text)
                Base_Clean.append(tweet)
            i=i+1
        Base=Base_Clean
    #Supprimer les tweets qui ont été ajouté en tant que favori moins de fois que nb_like
    #!!! Attention, favorite_count toujours = à 0 pour les RT. !!!
    i=0
    Base_Clean=[]
    if bin_like==1:
        print('\n \n FILTRE NOMBRE DE LIKES')
        for tweet in Base:
            if tweet.favorite_count >= nb_like :
                print(tweet.text)
                Base_Clean.append(tweet)
            i=i+1
        Base=Base_Clean
    
    #Supprimer les tweets qui ont été tweeté avant la date indiqué (date)
    i=0
    Base_Clean=[]
    if bin_date == 1:
        print('\n \n FILTRE PAR DATE')
        for tweet in Base:
            if tweet.created_at.year > int(date[0:4]) :
                Base_Clean.append(tweet)
        
                print ("On garde :  ", tweet.text, "car créé le", tweet.created_at)
        
            elif tweet.created_at.year== int(date[0:4]) and tweet.created_at.month > int(date[5:7]) :
                Base_Clean.append(tweet)
                print ("On garde : ", tweet.text, "car créé le", tweet.created_at)
        
            elif tweet.created_at.year== int(date[0:4]) and tweet.created_at.month == int(date[5:7]) and tweet.created_at.day > int(date[8:10]):     
                Base_Clean.append(tweet)
                print ("On garde :  ", tweet.text, "car créé le", tweet.created_at)
            else :
                continue
        Base=Base_Clean
         
    #Garder les tweets qui contiennent un des mots clés
    i=0
    Base_Clean=[]     
    if bin_kw==1:
        liste_kw=[]
        virgule=","
        for k in kw.split(virgule):
            liste_kw.append(k)
            print("ajout du kw", k)
        print('\n \n FILTRE PAR KW')
        for tweet in Base:
            for k in liste_kw :
                if k in tweet.text:
                    Base_Clean.append(tweet)
                    print(tweet.text)
                else:
                    continue
        Base=Base_Clean
        
        #IL FAUT SUPPRIMER LES DOUBLONS (si plusieurs kw présents dans un seul et meme tweet)
        
        print('NOMBRE DE TWEETS AVEC AU MOINS UN DES MOTS CLES :', len(Base))


    
            
        
        
    #ENREGISTREMENT
    with open(path_sortie,'wb') as fichier:
        
        pickle.dump(Base,fichier)             
    
    
    
    
  
        

        
    
        

'''Fonction fusion_bdd : permet de fusionner deux BDD construites avec les fonctions précédentes,
la BDD de sortie est construire de la même façon que celles récoltées "brutes"'''
def fusion_bdd(path1, path2, path_sortie) :
    
    #Variables
    i=0
    Base1_Clean={}
    Base2_Clean={}
    Base_Fusion={}
    
    #Ouverture des bases
    try:
        with open(path1,'rb') as fichier1:
            Base1=pickle.load(fichier1)
    except:
        print('Base1 introuvable ou illisible')
    
    try:
        with open(path2,'rb') as fichier2:
            Base2=pickle.load(fichier2)
    except:
        print('Base2 introuvable ou illisible')
        


    
    #Fusion des DATAS
    for k in Base1.keys():
        Base1_Clean = Base1[k]['Datas'] 
        
    for k in Base2.keys():
        Base2_Clean = Base2[k]['Datas']
    Base_Fusion['Fusion']={}
    Base_Fusion['Fusion']['Datas']={}
    Base1_Clean.update(Base2_Clean)
    Base_Fusion['Fusion']['Datas']=Base1_Clean
    
    
    
    
    #return Base_Fusion
    
    with open(path_sortie,'wb') as fichier:
        
        pickle.dump(Base_Fusion,fichier)
    #Creation des Liens
    construction_liens(path_sortie)
    
    
def representation_tweets(path_entree, bin_csv,  bin_geo, sortie_csv="", sortie_geo=""):
        with open(path_entree,'rb') as fichier1:
            Base=pickle.load(fichier1)
            
        if bin_csv==1:
            
            with open(sortie_csv+'.csv', 'w') as output:
                         
                         
                data = csv.writer(output, delimiter=";", lineterminator="\n")
                row = ['Screen name','tweeté le :', 'Nombre de likes (ajotu aux favoris)', 'Nombre de retweets','Texte', 'Géolocalisation']
                data.writerow(row)
                for tweet in Base:
                    
                    row = [tweet.user.screen_name, tweet.created_at,tweet.favorite_count, tweet.retweet_count, tweet.text.encode('utf8'), tweet.coordinates]
                    data.writerow(row)
                    
        if bin_geo ==1:
            print("Représentation des tweets de manière géographique")
            i=True
            
            #Zoom initial = dernier tweet avec coordonnées
            for tweet in Base :
                if i == True :
                    try:
                        zoom_lat = (tweet.coordinates['coordinates'][0])
                        zoom_long = (tweet.coordinates['coordinates'][1])
                        i=False
                    except:
                        pass
                else :
                    pass
                    

            macarte = folium.Map(location=[zoom_long,zoom_lat], zoom_start=10)
            folium.TileLayer("stamenterrain").add_to(macarte)
            
            #Ajout des "markers"
            for tweet in Base:
                try:
                    
                    date = str(tweet.created_at.day)+ '/'+str(tweet.created_at.month)+'/' +str(tweet.created_at.year)
                    popup_text = tweet.text+ '\n'+ date
                    folium.Marker([tweet.coordinates['coordinates'][1], tweet.coordinates['coordinates'][0]], popup=popup_text).add_to(macarte)
                    print('ajout dun marker')
                except :
                    pass
                
            
            macarte.save(sortie_geo+'.html')
            
            
                
            
    
    
                         
                     

    
    

        
