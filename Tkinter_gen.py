from tkinter import *
import tweepy
import pdb
import pickle
import networkx as nx 
import pandas as pd
from module import *
from tkinter import filedialog
import tkinter.tix


#-----------------INDEX---------------------#
class Index(Frame):
    
    def __init__(self, fenetre, **kwargs):  #Une classe Index qui découle de la classe Frame (classe Frame modifiée)
    
        Frame.__init__(self, fenetre, **kwargs) #Fenetre = parent ?
        self.pack(fill=BOTH) #Afficher la frame sur toute la fenetre
        
        #Titre
        self.titre = Label(self, text="Choix du module")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        #Bouton Scrap Twitter
        self.bouton_scrap_twitter = Button(self, text="Récupération de données Twitter", command=self.clique_scrap_twitter)
        self.bouton_scrap_twitter.grid(row=1, column=0)
        
        #Bouton Fusion
        self.bouton_fusion = Button(self, text="Fusionner des bases de données Twitter", command=self.clique_fusion) #Renvoie à la fonction cliquer
        self.bouton_fusion.grid(row=1, column=1)
        
        #Bouton Filtre
        self.bouton_fusion = Button(self, text="Filtrer des bases de données Twitter", command=self.clique_filtre)
        self.bouton_fusion.grid(row=2, column=0)
        
        #Bouton Network
        self.bouton_fusion = Button(self, text="Représentation graphique des réseaux", command=self.clique_network)
        self.bouton_fusion.grid(row=2, column=1)
        
        #Bouton Scrap Tweets
        self.bouton_fusion = Button(self, text="Récupération de tweets", command=self.clique_scrap_tweets)
        self.bouton_fusion.grid(row=3, column=0)
        
        #Bouton Filtres Tweets
        self.bouton_filtre_tweets = Button(self, text="Filtres de tweets", command=self.clique_filtre_tweets)
        self.bouton_filtre_tweets.grid(row=3, column=1)
        
        #Bouton Representation Tweets
        self.bouton_filtre_tweets = Button(self, text="Représentation de tweets", command=self.clique_recup_tweets)
        self.bouton_filtre_tweets.grid(row=4, column=0)
        
        
        Representation_Tweets
    
    def clique_scrap_twitter(self):
        self.forget()
        interface = Scrap_Twitter(fenetre)
        interface.mainloop()
    def clique_fusion(self):
        self.forget()
        interface = Fusion(fenetre)
        interface.mainloop()
    def clique_filtre(self):
        self.forget()
        interface = Filtre(fenetre)
        interface.mainloop()
    def clique_network(self):
        self.forget()
        interface=Network(fenetre)
        interface.mainloop()
    def clique_scrap_tweets(self):
        self.forget()
        interface=Scrap_Tweets(fenetre)
        interface.mainloop()
    def clique_filtre_tweets(self):
        self.forget()
        interface=Filtre_Tweets(fenetre)
        interface.mainloop()
    def clique_recup_tweets(self):
        self.forget()
        interface=Representation_Tweets(fenetre)
        interface.mainloop()



#-----------------SCRAP TWITTER---------------------#
class Scrap_Twitter(Frame):
     def __init__(self, fenetre, **kwargs):
         
         
         Frame.__init__(self, fenetre, **kwargs)
         self.pack(fill=BOTH)
        
         #Titre
         self.titre = Label(self, text="Récupération de données Twitter")
         self.titre.grid(row=0, column=0, columnspan=2)
         
         #Consumer Key
         self.question1 = Label(self, text="Consumer Key")
         self.question1.grid(row=1, column=0)
         var_consumer_key=IntVar()
         self.reponse1 = Entry(self,textvariable=var_consumer_key) 
         self.reponse1.grid(row=1, column=1)
         
         #Consumer Secret
         self.question2 = Label(self, text="Consumer Secret")
         self.question2.grid(row=2, column=0)
         var_consumer_secret=IntVar()
         self.reponse2 = Entry(self,textvariable=var_consumer_secret) 
         self.reponse2.grid(row=2, column=1)

         #Access Token
         self.question3 = Label(self, text="Acess Token")
         self.question3.grid(row=3, column=0)
         var_access_token = IntVar()
         self.reponse3 = Entry(self,textvariable=var_access_token) 
         self.reponse3.grid(row=3, column=1)
        
         #Access Token Secret
         self.question4 = Label(self, text="Acess Token Secret")
         self.question4.grid(row=4, column=0)
         var_access_token_secret=IntVar()
         self.reponse4 = Entry(self,textvariable=var_access_token_secret)
         self.reponse4.grid(row=4, column=1)
         
         #Compte dont on va récupérer les données
         self.question5 = Label(self, text="Compte Twitter :")
         self.question5.grid(row=5, column=0)
         compte_twitter=StringVar()
         self.reponse5 = Entry(self,textvariable=compte_twitter) 
         self.reponse5.grid(row=5, column=1)
         
         #Bouton Retour
         self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
         self.bouton_retour.grid(row=7, column=0)
         
         #Bouton Valider
         self.bouton_valider = Button(self, text="Valider", command=self.clique_valider)
         self.bouton_valider.grid(row=7, column=1)
         
         self.texte = Label(self, text="Attention, en cliquant sur Valider, vous lancez le processus de récupération des données. \n Ce processus peut prendre un certain temps en focntion de la taille de la base de donnée. \n Vous pouvez suivre l'avancée de cette récupération via la console. \n Une fenêtre vous indiquera quand le processus sera terminé.")
         self.texte.grid(row=8, column=0, columnspan=2)
        
         
     def clique_retour(self): 
         self.forget()
         interface = Index(fenetre)
         interface.mainloop()
         
     def clique_valider(self):
         
         global g_consumer_key
         g_consumer_key=self.reponse1.get()
         global g_consumer_secret
         g_consumer_secret=self.reponse2.get()
         global g_access_token
         g_access_token=self.reponse3.get()
         global g_access_token_secret
         g_access_token_secret=self.reponse4.get()
         global g_nom_twitter
         g_nom_twitter = self.reponse5.get()
         self.forget()
         interface = Scrap_Twitter2(fenetre)
         interface.mainloop()
         #scrap_twitter(self.reponse1.get(),self.reponse2.get(),self.reponse3.get(),self.reponse4.get(),self.reponse5.get())
         
         

     
         
         
class Scrap_Twitter2(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        
        #Titre
        self.titre = Label(self, text="Récupération de données Twitter : REUSSIE")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        
        self.texte = Label(self, text="La récupération des données Twitter a réussie. La base de donnée a été automatiquement enregistrée à l'adresse : \n /[compte twitter]/Datas_globales_[comtpe twitter]")
        self.texte.grid(row=1, column=0)
        
        #Scrapping Twitter
        scrap_twitter(g_consumer_key, g_consumer_secret, g_access_token, g_access_token_secret, g_nom_twitter)
        
        
        
        
    
         

         
         
#-----------------FUSION---------------------#
class Fusion(Frame):
     def __init__(self, fenetre, **kwargs):
         Frame.__init__(self, fenetre, **kwargs)
         self.pack(fill=BOTH)
        
         self.titre = Label(self, text="Fusion de bases de données Twitter")
         self.titre.grid(row=0, column=0, columnspan=2)
         
         self.browseButton1 = Button(self, text="BDD numéro 1", command=self.fileSelect1)
         self.browseButton1.grid(row=1, column=0)
         
         self.browseButton2 = Button(self, text="BDD numéro 2", command=self.fileSelect2)
         self.browseButton2.grid(row=1, column=1)
         
         self.bouton_sortie = Button(self, text="Chemin de sortie", command=self.fileSelect3)
         self.bouton_sortie.grid(row=2, column=0)
         
         #Bouton Retour
         self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
         self.bouton_retour.grid(row=3, column=0)
         
         self.bouton_valider = Button(self, text = 'Valider', command=self.clique_valider)
         self.bouton_valider.grid(row=3, column=1)

         
       
     def fileSelect1(self):
         global original1   
         original1 = filedialog.askopenfilename(filetypes = [("Files","*")])
         
     def fileSelect2(self):
         global original2   
         original2 = filedialog.askopenfilename(filetypes = [("Files","*")])
     
     def fileSelect3(self):
         global path_sortie
         path_sortie = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",title = "Select file", filetypes = [("All files","*.*")])
         print('Path sortie :', path_sortie) 
     
     def clique_valider(self):
         fusion_bdd(original1, original2, path_sortie)
         self.forget()
         interface=Fusion2(fenetre)
         interface.mainloop()
     
     def clique_retour(self): 
         self.forget()
         interface = Index(fenetre)
         interface.mainloop()



class Fusion2(Frame):
    def __init__(self, fenetre, **kwargs):
         Frame.__init__(self, fenetre, **kwargs)
         self.pack(fill=BOTH)
         
         self.titre = Label(self, text="Fusion de bases de données Twitter : REUSSIE")
         self.titre.grid(row=0, column=0, columnspan=2)
         
         #Bouton Retour à l'index
         self.bouton_retour = Button(self, text="Retour à l'index des modules", command=self.clique_retour)
         self.bouton_retour.grid(row=1, column=0)
         
         
    def clique_retour(self): 
         self.forget()
         interface = Index(fenetre)
         interface.mainloop()
         


     
         
     
          
     
     
         
     
     
     


     
#-----------------FILTRE---------------------#
class Filtre(Frame):
    
    def __init__(self, fenetre, **kwargs):
        
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        
        #Titre
        self.titre = Label(self, text="Filtre de bases de données Twitter")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        #Base de donnée à filtrer : input (browse)
        self.browseButton1 = Button(self, text="Base de donnée à filtrer", command=self.fileSelect1)
        self.browseButton1.grid(row=1, column=0, columnspan=2)
        
        #Tweets
        self.texte1 = Label(self, text="Filtrage par nombre de Tweets :")
        self.texte1.grid(row=2, column=0)
        self.tweets_bin = IntVar()
        self.tweets_bin2 = Checkbutton(self, text="", variable=self.tweets_bin)
        self.tweets_bin2.grid(row=2, column=1)
        


        
        self.texte2 = Label(self, text="Nombre de Tweets :")
        self.texte2.grid(row=3, column=0)
        self.nb_tweets=IntVar()
        self.bouton_nb_tweets = Entry(self,textvariable=self.nb_tweets) 
        self.bouton_nb_tweets.grid(row=3, column=1)
        
        
        #Friends
        self.texte3 = Label(self, text="Filtrage par nombre de Friends :")
        self.texte3.grid(row=4, column=0)
        self.friends_bin = IntVar()
        self.bouton_friends_bin = Checkbutton(self, text="", variable=self.friends_bin)
        self.bouton_friends_bin.grid(row=4, column=1)
        
        self.texte4 = Label(self, text="Nombre de Friends :")
        self.texte4.grid(row=5, column=0)
        self.nb_friends=IntVar()
        self.bouton_nb_friends = Entry(self,textvariable=self.nb_friends) 
        self.bouton_nb_friends.grid(row=5, column=1)
        
        #Followers
        self.texte5 = Label(self, text="Filtrage par nombre de Followers :")
        self.texte5.grid(row=6, column=0)
        self.followers_bin = IntVar()
        self.bouton_followers_bin = Checkbutton(self, text="", variable=self.followers_bin)
        self.bouton_followers_bin.grid(row=6, column=1)
        
        self.texte6 = Label(self, text="Nombre de Followers :")
        self.texte6.grid(row=7, column=0)
        self.nb_followers=IntVar()
        self.bouton_nb_followers = Entry(self,textvariable=self.nb_followers) 
        self.bouton_nb_followers.grid(row=7, column=1)
        
        #Mesures
        self.texte7 = Label(self, text="Filtrage par importance du compte (en terme de mesure)")
        self.texte7.grid(row=8, column=0)
        self.mesure_bin = IntVar()
        self.bouton_mesure_bin = Checkbutton(self, text="", variable=self.mesure_bin)
        self.bouton_mesure_bin.grid(row=8, column=1)
        
        self.select = StringVar()
        self.liste = Listbox(self, height=3)
        self.liste.configure(exportselection=False)
        self.liste.insert(1, "Degré de centralité")
        self.liste.insert(2, "Closeness")
        self.liste.insert(3, "Eigen Vector")

        self.texte8 = Label(self, text="Choix de la mesure : ")
        self.texte8.grid(row=9, column=0)
        self.liste.grid(row=9, column=1)
        
        self.texte9 = Label(self, text="Pourcentage des comptes les moins importants supprimés : ")
        self.texte9.grid(row=10, column=0)
        
        
        self.bouton_pourcentage = Spinbox(self, from_=0, to=1,increment=0.01)
        self.bouton_pourcentage.grid(row=10, column=1)
        
        #CSV
        self.texte10 = Label(self, text="Ecriture de la base en fichier CSV :")
        self.texte10.grid(row=11, column=0)
        self.csv_bin = IntVar()
        self.bouton_csv_bin = Checkbutton(self, text="", variable=self.csv_bin)
        self.bouton_csv_bin.grid(row=11, column=1)
        
        #Base de donnée sortie (output : path)
        self.bouton_sortie = Button(self, text="Chemin de sortie", command=self.fileSelect3)
        self.bouton_sortie.grid(row=12, column=0, columnspan=2 )
        
        #Bouton Retour
        self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
        self.bouton_retour.grid(row=13, column=0)
        
        #Bouton Valider
        self.bouton_valider = Button(self, text = 'Valider', command=self.clique_valider)
        self.bouton_valider.grid(row=13, column=1)
     
     
    def fileSelect1(self):
        global original1   
        original1 = filedialog.askopenfilename(filetypes = [("Files","*")])
    def fileSelect3(self):
        global path_sortie
        path_sortie = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",title = "Select file", filetypes = [("All files","*.*")])
        print('Path sortie :', path_sortie)
    
    def clique_valider(self):
        #ENREGISTREEMENT DE TOUS LES PARAMETRES
        print("Base de donnée à filtrer : " , original1)
        print("Binary Tweets : ", self.tweets_bin.get())
        print("Nb de Tweets :" ,self.nb_tweets.get())
        print("Binary Friends: ", self.friends_bin.get())
        print("Nb Friends : ", self.nb_friends.get())
        print("Binary Followers: ", self.followers_bin.get())
        print("Nb Followers : ", self.nb_followers.get())
        print("Binary Mesure :", self.mesure_bin.get())
        if self.mesure_bin.get() == 1 :
            print("Mesure choisie :", self.liste.get(self.liste.curselection()))
            print("Pourcentage : ", self.bouton_pourcentage.get())
        else :
            pass
        print("Binary CSV : ", self.csv_bin.get())
        print("Path sortie :", path_sortie)
        
        if self.mesure_bin.get()==1:
            if self.liste.get(self.liste.curselection()) == "Degré de centralité":
                degree_centrality_bin=1
                closeness_bin=0
                eigen_vector_bin=0
                
            elif self.liste.get(self.liste.curselection()) == "Closeness":
                closeness_bin=1
                degree_centrality_bin=0
                eigen_vector_bin=0
            elif self.liste.get(self.liste.curselection()) == "Eigen Vector":
                eigen_vector_bin=1
                degree_centrality_bin=0
                closeness_bin=0
                
            else:
                print('Problème car vous avez cochez la case filtre par mesure, mais vous n avez pas choisi la mesure.')
        else :
            degree_centrality_bin=0
            closeness_bin=0
            eigen_vector_bin=0 
            
                
            
                
        #filtrage(original1, self.tweets_bin.get(), self.nb_tweets.get(), self.friends_bin.get(), self.nb_friends.get(), self.followers_bin.get(), self.nb_followers.get(), self.mesure_bin.get(), self.liste.get(self.liste.curselection()), self.bouton_pourcentage.get(), self.csv_bin.get(), path_sortie)
        
        filtrage(original1, self.tweets_bin.get(), self.nb_tweets.get(), self.friends_bin.get(), self.nb_friends.get(), self.followers_bin.get(), self.nb_followers.get(), self.mesure_bin.get(),
        degree_centrality_bin,closeness_bin, eigen_vector_bin, float(self.bouton_pourcentage.get()), self.csv_bin.get(), path_sortie)
                 
        self.forget()
        interface=Filtre2(fenetre)
        interface.mainloop()
     
    def clique_retour(self): 
        self.forget()
        interface = Index(fenetre)
        interface.mainloop()
    
        
        

class Filtre2(Frame):
    
    def __init__(self, fenetre, **kwargs):
        
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        
        #Titre
        self.titre = Label(self, text="Filtrage de la base de donnée réussie !")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        #Bouton Retour
        self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
        self.bouton_retour.grid(row=1, column=0)
        

        

        
        
    def clique_retour(self): 
        self.forget()
        interface = Index(fenetre)
        interface.mainloop()
    
        
        


#-----------------NETWORK---------------------#
class Network(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        self.titre = Label(self, text="Représentation graphique de réseaux Twitter")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        
        #Base de donnée pour construire le réseau : input (browse)
        self.browseButton1 = Button(self, text="Base de donnée pour construire le réseau", command=self.fileSelect1)
        self.browseButton1.grid(row=1, column=0, columnspan=2)
        
        #Nb_repetition
        self.texte1 = Label(self, text="Nombre de graphe créés : ")
        self.texte1.grid(row=2, column=0)
        self.nb_repetitions=IntVar()
        self.nb_repetitions.set(1)
        self.bouton_nb_repetitions = Entry(self,textvariable=self.nb_repetitions) 
        self.bouton_nb_repetitions.grid(row=2, column=1)
        
        #Titre du graphe
        self.texte2 = Label(self, text="Titre du graphe : ")
        self.texte2.grid(row=3, column=0)
        self.titre=StringVar()
        self.titre.set("Titre")
        self.bouton_titre = Entry(self,textvariable=self.titre) 
        self.bouton_titre.grid(row=3, column=1)
        
        #Zoom
        self.texte3 = Label(self, text="Zoom sur le graphe :")
        self.texte3.grid(row=4, column=0)
        self.zoom=IntVar()
        self.zoom.set(40)
        self.bouton_zoom = Entry(self,textvariable=self.zoom) 
        self.bouton_zoom.grid(row=4, column=1)
        
        #Axes
        self.texte4 = Label(self, text="Activer les axes :")
        self.texte4.grid(row=5, column=0)
        self.axes_bin = IntVar()
        self.bouton_axes_bin = Checkbutton(self, text="", variable=self.axes_bin)
        self.bouton_axes_bin.grid(row=5, column=1)
        
        #Color background
        color_bg="white"
        
        #LIENS
        #Couleur liens
        self.texte5 = Label(self, text="Couleur des liens :")
        self.texte5.grid(row=6, column=0)
        self.couleur_liens = StringVar()
        self.couleur_liens.set("black")
        self.bouton_couleur_liens = OptionMenu(self, self.couleur_liens, "black", "white", "yellow", "red", "green")
        self.bouton_couleur_liens.grid(row=6, column=1)
        
        #Taille liens
        self.texte6 = Label(self, text="Taille des liens : ")
        self.texte6.grid(row=7, column=0)
        self.taille_liens=IntVar()
        self.taille_liens.set(5)
        self.bouton_taille_liens = Entry(self,textvariable=self.taille_liens) 
        self.bouton_taille_liens.grid(row=7, column=1)
        
        #NOEUDS
        #Couleur noeuds
        self.texte7 = Label(self, text="Couleur des noeuds :")
        self.texte7.grid(row=8, column=0)
        self.couleur_noeuds = StringVar()
        self.couleur_noeuds.set("black")
        self.bouton_couleur_noeuds = OptionMenu(self, self.couleur_noeuds, "black", "white", "yellow", "red", "green")
        self.bouton_couleur_noeuds.grid(row=8, column=1)
        
        #Taille noeuds
        self.texte8 = Label(self, text="Taille des noeuds : ")
        self.texte8.grid(row=9, column=0)
        self.taille_noeuds=IntVar()
        self.taille_noeuds.set(4000)
        self.bouton_taille_noeuds = Entry(self,textvariable=self.taille_noeuds) 
        self.bouton_taille_noeuds.grid(row=9, column=1)
        
        #LABELS
        #Binary labels
        self.texte9 = Label(self, text="Afficher des labels : ")
        self.texte9.grid(row=10, column=0)
        self.bin_labels = IntVar()
        self.bouton_bin_labels = Checkbutton(self, text="", variable=self.bin_labels)
        self.bouton_bin_labels.grid(row=10, column=1)
        
        #Type labels
        self.texte9 = Label(self, text="Type de labels :")
        self.texte9.grid(row=11, column=0)
        self.type_labels = StringVar()
        self.type_labels.set("screen_name")
        self.bouton_type_labels = OptionMenu(self, self.type_labels, "name", "screen_name", "iden")
        self.bouton_type_labels.grid(row=11, column=1)
        
        #Taille labels
        self.texte10 = Label(self, text="Tailles des labels : ")
        self.texte10.grid(row=12, column=0)
        self.taille_labels = IntVar()
        self.taille_labels.set(4)
        self.bouton_type_labels = Entry(self,textvariable=self.taille_labels) 
        self.bouton_type_labels.grid(row=12, column=1)
        
        #Couleur labels
        self.texte11 = Label(self, text="Couleur des labels :")
        self.texte11.grid(row=13, column=0)
        self.couleur_labels = StringVar()
        self.couleur_labels.set("black")
        self.bouton_couleur_labels = OptionMenu(self, self.couleur_labels, "black", "white", "yellow", "red", "green")
        self.bouton_couleur_labels.grid(row=13, column=1)
        
        #Kv
        self.texte12 = Label(self, text="Dispersion des noeuds* :")
        self.texte12.grid(row=14, column=0)
        self.kv=DoubleVar()
        self.kv.set(0.7)
        self.bouton_kv = Entry(self,textvariable=self.kv) 
        self.bouton_kv.grid(row=14, column=1)
        
        #Path sortie
        self.bouton_sortie = Button(self, text="Chemin de sortie : Browse", command=self.fileSelect3)
        self.bouton_sortie.grid(row=15, column=0, columnspan=2)
        
        #Format sortie
        self.texte13 = Label(self, text="Format de sortie")
        self.texte13.grid(row=16, column=0)
        self.format_sortie = StringVar()
        self.format_sortie.set("png")
        self.bouton_format_sortie = OptionMenu(self, self.format_sortie, "png", "pdf")
        self.bouton_format_sortie.grid(row=16, column=1)
        
        #Bouton Retour
        self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
        self.bouton_retour.grid(row=17, column=0)
        
        #Bouton Valider
        self.bouton_valider = Button(self, text = 'Valider', command=self.clique_valider)
        self.bouton_valider.grid(row=17, column=1)
        
        
        
    
        
    def clique_valider(self):
        
        
        zoom_clean = (self.zoom.get(), self.zoom.get())
        
        '''print(original1, path_sortie, self.format_sortie.get(), self.kv.get(), self.nb_repetitions.get(), 
        self.titre.get(), zoom_clean, self.axes_bin.get(), 'black', self.couleur_liens.get(), self.taille_liens.get(),
        self.couleur_noeuds.get(), self.taille_noeuds.get(), self.bin_labels.get(), self.couleur_labels.get(), self.taille_labels.get(), 
        self.type_labels.get())'''
        
        
        construction_network(str(original1), str(path_sortie), str(self.format_sortie.get()), float(self.kv.get()), int(self.nb_repetitions.get()), 
        str(self.titre.get()), zoom_clean, int(self.axes_bin.get()), 'black', str(self.couleur_liens.get()), int(self.taille_liens.get()),
        str(self.couleur_noeuds.get()), int(self.taille_noeuds.get()), int(self.bin_labels.get()), str(self.couleur_labels.get()), int(self.taille_labels.get()), 
        str(self.type_labels.get()))
        
        self.forget()
        interface=Network2(fenetre)
        interface.mainloop()
        
     
    def clique_retour(self): 
        self.forget()
        interface = Index(fenetre)
        interface.mainloop()
        
        
    def fileSelect1(self):
        global original1   
        original1 = filedialog.askopenfilename(filetypes = [("Files","*")])
        
    def fileSelect3(self):
        global path_sortie
        path_sortie = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",title = "Select file", filetypes = [("All files","*.*")])
        print('Path sortie :', path_sortie)
        
        
        

class Network2(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        self.titre = Label(self, text="Représentation graphique de réseaux Twitter : TERMINE")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        #Bouton Retour
        self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
        self.bouton_retour.grid(row=1, column=0)
        
        #Bouton Index
        self.bouton_valider = Button(self, text = 'Index des modules', command=self.clique_index)
        self.bouton_valider.grid(row=1, column=1)
        
    def clique_index(self): 
        self.forget()
        interface = Index(fenetre)
        interface.mainloop()
        
    def clique_retour(self): 
        self.forget()
        interface = Network(fenetre)
        interface.mainloop()


#-----------------SCRAP TWEETS---------------------#
'''def scrap_tweets(screen_name, consumer_key, consumer_secret, access_token, access_token_secret, path_sortie) :'''
class Scrap_Tweets(Frame):
     def __init__(self, fenetre, **kwargs):
         
         Frame.__init__(self, fenetre, **kwargs)
         self.pack(fill=BOTH)
        
         #Titre
         self.titre = Label(self, text="Récupération de Tweets")
         self.titre.grid(row=0, column=0, columnspan=2)
         
         #Consumer Key
         self.question1 = Label(self, text="Consumer Key")
         self.question1.grid(row=1, column=0)
         var_consumer_key=IntVar()
         self.reponse1 = Entry(self,textvariable=var_consumer_key) 
         self.reponse1.grid(row=1, column=1)
         
         #Consumer Secret
         self.question2 = Label(self, text="Consumer Secret")
         self.question2.grid(row=2, column=0)
         var_consumer_secret=IntVar()
         self.reponse2 = Entry(self,textvariable=var_consumer_secret) 
         self.reponse2.grid(row=2, column=1)

         #Access Token
         self.question3 = Label(self, text="Acess Token")
         self.question3.grid(row=3, column=0)
         var_access_token = IntVar()
         self.reponse3 = Entry(self,textvariable=var_access_token) 
         self.reponse3.grid(row=3, column=1)
        
         #Access Token Secret
         self.question4 = Label(self, text="Acess Token Secret")
         self.question4.grid(row=4, column=0)
         var_access_token_secret=IntVar()
         self.reponse4 = Entry(self,textvariable=var_access_token_secret)
         self.reponse4.grid(row=4, column=1)
         
         #Compte dont on va récupérer les données
         self.question5 = Label(self, text="Compte Twitter :")
         self.question5.grid(row=5, column=0)
         compte_twitter=StringVar()
         self.reponse5 = Entry(self,textvariable=compte_twitter) 
         self.reponse5.grid(row=5, column=1)
         
         self.bouton_sortie = Button(self, text="Chemin de sortie", command=self.fileSelect3)
         self.bouton_sortie.grid(row=6, column=0, columnspan=2)
         
         #Bouton Retour
         self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
         self.bouton_retour.grid(row=7, column=0)
         
         #Bouton Valider
         self.bouton_valider = Button(self, text="Valider", command=self.clique_valider)
         self.bouton_valider.grid(row=7, column=1)
         
         self.texte = Label(self, text="Attention, en cliquant sur Valider, vous lancez le processus de récupération des Tweets. \n Ce processus peut prendre un certain temps en focntion de la taille de la base de donnée. \n Vous pouvez suivre l'avancée de cette récupération via la console. \n Une fenêtre vous indiquera quand le processus sera terminé.")
         self.texte.grid(row=8, column=0, columnspan=2)
         
     def fileSelect3(self): 
         global path_sortie
         path_sortie = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",title = "Select file", filetypes = [("All files","*.*")])
         print('Path sortie :', path_sortie) 
         
     def clique_retour(self):
         self.forget()
         interface = Index(fenetre)
         interface.mainloop()
         
     def clique_valider(self):

         global g_consumer_key
         g_consumer_key=self.reponse1.get()
         global g_consumer_secret
         g_consumer_secret=self.reponse2.get()
         global g_access_token
         g_access_token=self.reponse3.get()
         global g_access_token_secret
         g_access_token_secret=self.reponse4.get()
         global g_nom_twitter
         g_nom_twitter = self.reponse5.get()
         self.forget()
         interface = Scrap_Tweets2(fenetre)
         interface.mainloop()


         
class Scrap_Tweets2(Frame):
     def __init__(self, fenetre, **kwargs):
                 
         
         
         Frame.__init__(self, fenetre, **kwargs)
         self.pack(fill=BOTH)
        
         #Titre
         self.titre = Label(self, text="Récupération de Tweets : TERMINE")
         self.titre.grid(row=0, column=0, columnspan=2)
         
         self.texte = Label(self, text="Le fichier contenant les Tweets qui viennent d'être récupéré est disponible à l'adresse indiquée à l'étape précédente")
         self.texte.grid(row=1, column=0, columnspan=2)
         
         #Scrapping Tweets
         scrap_tweets(g_nom_twitter, g_consumer_key, g_consumer_secret, g_access_token, g_access_token_secret, path_sortie) 
         
         #Bouton Retour
         self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
         self.bouton_retour.grid(row=2, column=0, columnspan=2)
         
     def clique_retour(self):
         self.forget()
         interface = Index(fenetre)
         interface.mainloop()
           
         
         '''def scrap_tweets(screen_name, consumer_key, consumer_secret, access_token, access_token_secret, path_sortie) :'''
         

         
         
class Filtre_Tweets(Frame):
    
    def __init__(self, fenetre, **kwargs):
        
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        
        #Titre
        self.titre = Label(self, text="Filtres de Tweets")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        #Base de donnée à filtrer : input (browse)
        self.browseButton1 = Button(self, text="Tweets à filtrer", command=self.fileSelect1)
        self.browseButton1.grid(row=1, column=0, columnspan=2)
        
        
        #Likes
        self.texte1 = Label(self, text="Filtrage par nombre de likes, ajout aux favoris :")
        self.texte1.grid(row=2, column=0)
        self.bin_likes = IntVar()
        self.bouton_bin_likes = Checkbutton(self, text="", variable=self.bin_likes)
        self.bouton_bin_likes.grid(row=2, column=1)
        
        self.texte2 = Label(self, text="Nombre de likes :")
        self.texte2.grid(row=3, column=0)
        self.nb_likes=IntVar()
        self.nb_likes.set(0)
        self.bouton_nb_likes = Entry(self,textvariable=self.nb_likes) 
        self.bouton_nb_likes.grid(row=3, column=1)
        
        
        #nombre de Retweets
        self.texte3 = Label(self, text="Filtrage par nombre de retweets :")
        self.texte3.grid(row=4, column=0)
        self.bin_rt = IntVar()
        
        self.bouton_bin_rt = Checkbutton(self, text="", variable=self.bin_rt)
        self.bouton_bin_rt.grid(row=4, column=1)
        
        self.texte4 = Label(self, text="Nombre de retweets :")
        self.texte4.grid(row=5, column=0)
        self.nb_rt=IntVar()
        self.nb_rt.set(0)
        self.bouton_nb_rt = Entry(self,textvariable=self.nb_rt) 
        self.bouton_nb_rt.grid(row=5, column=1)
        
        #Date
        self.texte5 = Label(self, text="Filtrage par date")
        self.texte5.grid(row=6, column=0)
        self.bin_date = IntVar()
        self.bouton_bin_date = Checkbutton(self, text="", variable=self.bin_date)
        self.bouton_bin_date.grid(row=6, column=1)
        
        self.texte6 = Label(self, text="Date (ex : 2019/1/22):")
        self.texte6.grid(row=7, column=0)
        self.date=StringVar()
        self.bouton_date = Entry(self,textvariable=self.date) 
        self.bouton_date.grid(row=7, column=1)
        
        #Mots-clés
        self.texte7 = Label(self, text="Filtrage par mots-clés")
        self.texte7.grid(row=8, column=0)
        self.bin_kw = IntVar()
        self.bouton_bin_kw = Checkbutton(self, text="", variable=self.bin_kw)
        self.bouton_bin_kw.grid(row=8, column=1)
        
        self.texte8 = Label(self, text="Mots-clés : ")
        self.texte8.grid(row=9, column=0)
        self.kw=StringVar()
        self.bouton_kw = Entry(self,textvariable=self.kw) 
        self.bouton_kw.grid(row=9, column=1)
        
        #Retweets
        self.texte9 = Label(self, text="Supprimer les Retweets : ")
        self.texte9.grid(row=10, column=0)
        self.bin_del_rt = IntVar()
        self.bouton_bin_del_rt = Checkbutton(self, text="", variable=self.bin_del_rt)
        self.bouton_bin_del_rt.grid(row=10, column=1)

        
        
        
        
        #Base de donnée sortie (output : path)
        self.bouton_sortie = Button(self, text="Chemin de sortie", command=self.fileSelect3)
        self.bouton_sortie.grid(row=12, column=0, columnspan=2 )
        
        #Bouton Retour
        self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
        self.bouton_retour.grid(row=13, column=0)
        
        #Bouton Valider
        self.bouton_valider = Button(self, text = 'Valider', command=self.clique_valider)
        self.bouton_valider.grid(row=13, column=1)
    
    
    
    
    def clique_valider(self):
        

        filtre_tweets(original1,self.bin_del_rt.get(), self.bin_rt.get(), self.nb_rt.get(), self.bin_kw.get(), self.kw.get(), self.bin_likes.get(), self.nb_likes.get(), self.bin_date.get(), self.date.get(), path_sortie)

        self.forget()
        interface=Filtre_Tweets2(fenetre)
        interface.mainloop()
     
    def clique_retour(self): 
        self.forget()
        interface = Index(fenetre)
        interface.mainloop()
    def fileSelect1(self):
        global original1   
        original1 = filedialog.askopenfilename(filetypes = [("Files","*")])
    def fileSelect3(self):
        global path_sortie
        path_sortie = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",title = "Select file", filetypes = [("All files","*.*")])
        print('Path sortie :', path_sortie)
        

class Filtre_Tweets2(Frame):
      
    def __init__(self, fenetre, **kwargs):
        
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        
        #Titre
        self.titre = Label(self, text="Filtres de Tweets : TERMINE")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        
class Representation_Tweets(Frame):
    
    def __init__(self, fenetre, **kwargs):
        
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        
        #Titre
        self.titre = Label(self, text="Representation Tweets")
        self.titre.grid(row=0, column=0, columnspan=2)
        
        #Tweets à représenter : input (browse)
        self.browseButton1 = Button(self, text="Tweets à représenter", command=self.fileSelect1)
        self.browseButton1.grid(row=1, column=0, columnspan=2)
        
        #bin CSV
        self.texte1 = Label(self, text="Représentation en fichier CSV (tableur) ?")
        self.texte1.grid(row=2, column=0)
        self.bin_csv = IntVar()
        self.bouton_bin_csv = Checkbutton(self, text="", variable=self.bin_csv)
        self.bouton_bin_csv.grid(row=2, column=1)
        
        #Sortie CSV (output : path)
        self.bouton_sortie_csv = Button(self, text="Chemin de sortie CSV", command=self.fileSelect3)
        self.bouton_sortie_csv.grid(row=3, column=0, columnspan=2 )
        
        #bin geo
        self.texte2 = Label(self, text="Représentation de la géolocalisation des Tweets?")
        self.texte2.grid(row=4, column=0)
        self.bin_geo = IntVar()
        self.bouton_bin_geo = Checkbutton(self, text="", variable=self.bin_geo)
        self.bouton_bin_geo.grid(row=4, column=1)
        
        #Sortie geo
        self.bouton_sortie_geo = Button(self, text="Chemin de sortie carte géographique des Tweets", command=self.fileSelect2)
        self.bouton_sortie_geo.grid(row=5, column=0, columnspan=2)
        
        #Bouton Retour
        self.bouton_retour = Button(self, text="Retour", command=self.clique_retour)
        self.bouton_retour.grid(row=6, column=0)
        
        #Bouton Valider
        self.bouton_valider = Button(self, text = 'Valider', command=self.clique_valider)
        self.bouton_valider.grid(row=6, column=1)
        
    
    
    def clique_valider(self):
        if self.bin_csv.get() == 1 and self.bin_geo.get()==1:
            print(original1, self.bin_csv.get(), self.bin_geo.get(),csv_sortie, geo_sortie)
            representation_tweets(original1, self.bin_csv.get(), self.bin_geo.get(),sortie_csv=csv_sortie, sortie_geo=geo_sortie)
        elif self.bin_csv.get() == 1 and self.bin_geo.get()==0:
            print(original1, self.bin_csv.get(), self.bin_geo.get(),csv_sortie)
            representation_tweets(original1, self.bin_csv.get(), self.bin_geo.get(),sortie_csv=csv_sortie)
        elif self.bin_csv.get() == 0 and self.bin_geo.get()==1:
            print(original1, self.bin_csv.get(), self.bin_geo.get(),geo_sortie)
            representation_tweets(original1, self.bin_csv.get(), self.bin_geo.get(),sortie_geo=geo_sortie)
        else :
            print('Aucune action')
            
        
            
            
        self.forget()
        interface=Representation_Tweets2(fenetre)
        interface.mainloop()
     
    def clique_retour(self): 
        self.forget()
        interface = Index(fenetre)
        interface.mainloop()
        
        
        
        
        
    
        
    def fileSelect1(self):
        global original1   
        original1 = filedialog.askopenfilename(filetypes = [("Files","*")])
        
    def fileSelect3(self):
        global csv_sortie
        csv_sortie = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",title = "Select file", filetypes = [("All files","*.*")])
        print('Path sortie csv:', csv_sortie)
    
    def fileSelect2(self):
        global geo_sortie
        geo_sortie = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",title = "Select file", filetypes = [("All files","*.*")])
        print('Path sortie géo:', geo_sortie)
        
        
        
    
class Representation_Tweets2(Frame):
    
    def __init__(self, fenetre, **kwargs):
        
        Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill=BOTH)
        
        #Titre
        self.titre = Label(self, text="Representation Tweets : TERMINE")
        self.titre.grid(row=0, column=0, columnspan=2)
    


#-------------------------------------------------------------------------------#
fenetre = Tk()#Création fenetre principale
interface = Index(fenetre) #Creation de la frame 1 de la classe Index, qui a comme parent la fenetre principale
interface.mainloop() #Loop principale
interface.destroy()
#-------------------------------------------------------------------------------#
