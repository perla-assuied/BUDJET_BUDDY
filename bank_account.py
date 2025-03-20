import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Client:
    def __init__(self, id, nom, prenom, mot_de_passe, solde=0.0):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.mot_de_passe = mot_de_passe
        self.solde = solde
        self.transactions = []
        # Ajouter une transaction initiale
        self.ajouter_transaction("Ouverture de compte", 0.0)
    
    def ajouter_transaction(self, type_transaction, montant):
        self.transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": type_transaction,
            "montant": montant,
            "solde_apres": self.solde
        })
    
    def deposer(self, montant):
        if montant <= 0:
            return False
        self.solde += montant
        self.ajouter_transaction("Dépôt", montant)
        return True
    
    def retirer(self, montant):
        if montant <= 0 or montant > self.solde:
            return False
        self.solde -= montant
        self.ajouter_transaction("Retrait", -montant)
        return True
    
    def get_derniere_transactions(self, nombre=10):
        return self.transactions[-nombre:] if len(self.transactions) >= nombre else self.transactions[:]

class BanqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ma Banque")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.client_actuel = None
        
        # Créer les clients
        self.clients = self.creer_clients()
        self.prochain_id = max([int(id) for id in self.clients.keys()]) + 1 if self.clients else 1
        
        # Frame pour l'authentification
        self.frame_auth = tk.Frame(root, bg="#f0f0f0")
        self.frame_auth.pack(pady=50)
        
        # Ajouter un logo/titre
        tk.Label(self.frame_auth, text="🏦 MA BANQUE", font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#1a237e").pack(pady=20)
        
        tk.Label(self.frame_auth, text="Identifiant Client:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.entry_id = tk.Entry(self.frame_auth, font=("Arial", 12), width=30)
        self.entry_id.pack(pady=5)
        
        tk.Label(self.frame_auth, text="Mot de Passe:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.entry_password = tk.Entry(self.frame_auth, font=("Arial", 12), width=30, show="*")
        self.entry_password.pack(pady=5)
        
        # Frame pour les boutons
        auth_buttons_frame = tk.Frame(self.frame_auth, bg="#f0f0f0")
        auth_buttons_frame.pack(pady=20)
        
        login_button = tk.Button(auth_buttons_frame, text="Se Connecter", font=("Arial", 12), 
                 width=20, command=self.authentifier)
        login_button.grid(row=0, column=0, padx=10)
        login_button.configure(bg="#303f9f", fg="white", activebackground="#1a237e", activeforeground="white")
        
        signup_button = tk.Button(auth_buttons_frame, text="S'inscrire", font=("Arial", 12), 
                 width=20, command=self.afficher_inscription)
        signup_button.grid(row=0, column=1, padx=10)
        signup_button.configure(bg="#009688", fg="white", activebackground="#00796b", activeforeground="white")
        
        # Frame pour l'inscription (initialement cachée)
        self.frame_inscription = tk.Frame(root, bg="#f0f0f0")
        
        tk.Label(self.frame_inscription, text="🏦 INSCRIPTION", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#009688").pack(pady=20)
        
        # Formulaire d'inscription
        form_frame = tk.Frame(self.frame_inscription, bg="#f0f0f0")
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Nom:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.entry_nom = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.entry_nom.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Prénom:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.entry_prenom = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.entry_prenom.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Mot de Passe:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.entry_mdp_inscription = tk.Entry(form_frame, font=("Arial", 12), width=30, show="*")
        self.entry_mdp_inscription.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Confirmer Mot de Passe:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5, padx=10)
        self.entry_mdp_confirm = tk.Entry(form_frame, font=("Arial", 12), width=30, show="*")
        self.entry_mdp_confirm.grid(row=3, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Dépôt Initial (optionnel):", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5, padx=10)
        self.entry_depot_initial = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.entry_depot_initial.grid(row=4, column=1, pady=5, padx=10)
        self.entry_depot_initial.insert(0, "0.0")
        
        # Boutons d'inscription
        inscription_buttons_frame = tk.Frame(self.frame_inscription, bg="#f0f0f0")
        inscription_buttons_frame.pack(pady=20)
        
        valider_button = tk.Button(inscription_buttons_frame, text="Valider l'inscription", font=("Arial", 12), 
                     width=20, command=self.inscrire)
        valider_button.grid(row=0, column=0, padx=10)
        valider_button.configure(bg="#009688", fg="white", activebackground="#00796b", activeforeground="white")
        
        retour_button = tk.Button(inscription_buttons_frame, text="Retour", font=("Arial", 12), 
                   width=20, command=self.retour_connexion)
        retour_button.grid(row=0, column=1, padx=10)
        retour_button.configure(bg="#9e9e9e", fg="white", activebackground="#757575", activeforeground="white")
        
        # Frame pour les opérations bancaires (initialement cachée)
        self.frame_operations = tk.Frame(root, bg="#f0f0f0")
        
        # Labels pour afficher les informations du client
        self.label_bienvenue = tk.Label(self.frame_operations, text="", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#1a237e")
        self.label_bienvenue.pack(pady=10)
        
        self.label_solde = tk.Label(self.frame_operations, text="", font=("Arial", 16), bg="#f0f0f0")
        self.label_solde.pack(pady=10)
        
        # Frame pour les boutons d'opération
        button_frame = tk.Frame(self.frame_operations, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Création des boutons directement sans utiliser les dictionnaires
        deposer_btn = tk.Button(button_frame, text="Déposer", font=("Arial", 12), 
                            width=15, command=self.deposer)
        deposer_btn.configure(bg="#4caf50", fg="white", activebackground="#388e3c", activeforeground="white")
        deposer_btn.grid(row=0, column=0, padx=10, pady=10)
        
        retirer_btn = tk.Button(button_frame, text="Retirer", font=("Arial", 12), 
                            width=15, command=self.retirer)
        retirer_btn.configure(bg="#ff9800", fg="white", activebackground="#f57c00", activeforeground="white")
        retirer_btn.grid(row=0, column=1, padx=10, pady=10)
        
        rafraichir_btn = tk.Button(button_frame, text="Rafraîchir", font=("Arial", 12), 
                                width=15, command=self.rafraichir)
        rafraichir_btn.configure(bg="#2196f3", fg="white", activebackground="#1976d2", activeforeground="white")
        rafraichir_btn.grid(row=1, column=0, padx=10, pady=10)
        
        deconnexion_btn = tk.Button(button_frame, text="Se Déconnecter", font=("Arial", 12), 
                                width=15, command=self.se_deconnecter)
        deconnexion_btn.configure(bg="#f44336", fg="white", activebackground="#d32f2f", activeforeground="white")
        deconnexion_btn.grid(row=1, column=1, padx=10, pady=10)
        
        # Frame pour afficher les transactions
        self.frame_transactions = tk.Frame(self.frame_operations, bg="white", bd=2, relief=tk.GROOVE)
        self.frame_transactions.pack(pady=20, fill=tk.BOTH, expand=True, padx=50)
        
        # Titre de la section transactions
        tk.Label(self.frame_transactions, text="Historique des Transactions", 
                font=("Arial", 14, "bold"), bg="#e0e0e0", fg="#1a237e").pack(fill=tk.X)
        
        # En-tête des colonnes
        header_frame = tk.Frame(self.frame_transactions, bg="#e0e0e0")
        header_frame.pack(fill=tk.X)
        
        column_headers = ["Date", "Type", "Montant", "Solde"]
        column_widths = [25, 20, 15, 15]
        
        for idx, (header, width) in enumerate(zip(column_headers, column_widths)):
            tk.Label(header_frame, text=header, font=("Arial", 11, "bold"), 
                    bg="#e0e0e0", width=width, anchor="w").grid(row=0, column=idx, padx=5, pady=5)
        
        # Liste des transactions
        self.transactions_list = tk.Text(self.frame_transactions, font=("Arial", 10), height=10)
        self.transactions_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar pour la liste des transactions
        scrollbar = tk.Scrollbar(self.frame_transactions)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transactions_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.transactions_list.yview)
        
        # Configurer les tags pour les couleurs
        self.transactions_list.tag_configure("depot", foreground="#4caf50")
        self.transactions_list.tag_configure("retrait", foreground="#f44336")

    def creer_clients(self):
        clients = {}
        client_data = [
            (1, "Dupont", "Jean", "DupontJEAN123*", 1500.0),
            (2, "Martin", "Sophie", "MARTINSophie654*", 2200.0),
            (3, "Lefebvre", "Pierre", "LEfeBVREPierre908*", 800.0),
            (4, "Bernard", "Marie", "BERNARDMARIe456!", 3500.0),
            (5, "Thomas", "Paul", "THOMASPaul432!", 1200.0),
            (6, "Petit", "Julie", "PETITjulie34!", 950.0),
            (7, "Robert", "Michel", "ROBERTMichel987?", 2800.0),
            (8, "Richard", "Emma", "rICHARDEMMA45/", 1700.0),
            (9, "Durand", "Philippe", "DURANDPHIlippe98765+", 3200.0),
            (10, "Leroy", "Claire", "LEROYCLAIRe6789!", 600.0)
        ]
        
        for id, nom, prenom, mot_de_passe, solde in client_data:
            clients[str(id)] = Client(id, nom, prenom, mot_de_passe, solde)
        
        return clients

    def authentifier(self):
        client_id = self.entry_id.get()
        password = self.entry_password.get()
        
        if not client_id or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        if client_id in self.clients and self.clients[client_id].mot_de_passe == password:
            self.client_actuel = self.clients[client_id]
            
            # Mise à jour de l'interface
            self.label_bienvenue.config(text=f"Bienvenue, {self.client_actuel.prenom} {self.client_actuel.nom} !")
            self.mettre_a_jour_solde()
            self.rafraichir()
            
            # Cacher le frame d'authentification et afficher le frame d'opérations
            self.frame_auth.pack_forget()
            self.frame_operations.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        else:
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect")

    def afficher_inscription(self):
        # Cacher le frame d'authentification et afficher le frame d'inscription
        self.frame_auth.pack_forget()
        self.frame_inscription.pack(pady=20)
        
        # Effacer les champs existants
        self.entry_nom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_mdp_inscription.delete(0, tk.END)
        self.entry_mdp_confirm.delete(0, tk.END)
        self.entry_depot_initial.delete(0, tk.END)
        self.entry_depot_initial.insert(0, "0.0")

    def retour_connexion(self):
        # Cacher le frame d'inscription et afficher le frame d'authentification
        self.frame_inscription.pack_forget()
        self.frame_auth.pack(pady=50)

    def inscrire(self):
        # Récupérer les données du formulaire
        nom = self.entry_nom.get().strip()
        prenom = self.entry_prenom.get().strip()
        mot_de_passe = self.entry_mdp_inscription.get()
        confirmation = self.entry_mdp_confirm.get()
        
        # Vérifier si les champs obligatoires sont remplis
        if not nom or not prenom or not mot_de_passe or not confirmation:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return
        
        # Vérifier si les mots de passe correspondent
        if mot_de_passe != confirmation:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return
        
        # Vérifier le dépôt initial
        try:
            depot_initial = float(self.entry_depot_initial.get())
            if depot_initial < 0:
                messagebox.showerror("Erreur", "Le dépôt initial ne peut pas être négatif")
                return
        except ValueError:
            messagebox.showerror("Erreur", "Le dépôt initial doit être un nombre")
            return
        
        # Créer un nouveau client
        nouveau_client = Client(self.prochain_id, nom, prenom, mot_de_passe, depot_initial)
        self.clients[str(self.prochain_id)] = nouveau_client
        
        # Ajouter la transaction de dépôt initial si nécessaire
        if depot_initial > 0:
            nouveau_client.ajouter_transaction("Dépôt initial", depot_initial)
        
        # Informer l'utilisateur et retourner à l'écran de connexion avec son ID pré-rempli
        messagebox.showinfo("Succès", f"Inscription réussie !\nVotre identifiant client est: {self.prochain_id}")
        
        # Retourner à l'écran de connexion
        self.frame_inscription.pack_forget()
        self.frame_auth.pack(pady=50)
        
        # Pré-remplir l'identifiant pour faciliter la connexion
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, str(self.prochain_id))
        self.entry_password.delete(0, tk.END)
        
        # Incrémenter l'ID pour le prochain client
        self.prochain_id += 1

    def mettre_a_jour_solde(self):
        self.label_solde.config(text=f"Solde actuel: {self.client_actuel.solde:.2f} €")

    def deposer(self):
        montant = simpledialog.askfloat("Dépôt", "Entrez le montant à déposer:", minvalue=0.01)
        if montant:
            if self.client_actuel.deposer(montant):
                self.mettre_a_jour_solde()
                self.rafraichir()
                messagebox.showinfo("Succès", f"Dépôt de {montant:.2f} € effectué avec succès")
            else:
                messagebox.showerror("Erreur", "Montant invalide")

    def retirer(self):
        montant = simpledialog.askfloat("Retrait", "Entrez le montant à retirer:", minvalue=0.01)
        if montant:
            if self.client_actuel.retirer(montant):
                self.mettre_a_jour_solde()
                self.rafraichir()
                messagebox.showinfo("Succès", f"Retrait de {montant:.2f} € effectué avec succès")
            else:
                messagebox.showerror("Erreur", "Montant invalide ou solde insuffisant")

    def rafraichir(self):
        # Effacer les anciennes données
        self.transactions_list.delete(1.0, tk.END)
        
        # Obtenir les dernières transactions
        transactions = self.client_actuel.get_derniere_transactions()
        transactions.reverse()  # Afficher les plus récentes en premier
        
        # Afficher les transactions avec couleurs
        for trans in transactions:
            date = trans["date"]
            type_trans = trans["type"]
            montant = trans["montant"]
            solde = trans["solde_apres"]
            
            # Formater la ligne
            ligne = f"{date}  {type_trans.ljust(15)}  "
            self.transactions_list.insert(tk.END, ligne)
            
            # Insérer le montant avec couleur
            montant_str = f"{montant:+.2f} €".ljust(15)
            
            if type_trans == "Dépôt" or type_trans == "Dépôt initial":
                self.transactions_list.insert(tk.END, montant_str, "depot")
            elif type_trans == "Retrait":
                self.transactions_list.insert(tk.END, montant_str, "retrait")
            else:
                self.transactions_list.insert(tk.END, montant_str)
            
            # Insérer le solde
            solde_str = f"{solde:.2f} €\n"
            self.transactions_list.insert(tk.END, solde_str)

    def se_deconnecter(self):
        self.client_actuel = None
        
        # Effacer les champs de saisie
        self.entry_id.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        
        # Cacher le frame d'opérations et afficher le frame d'authentification
        self.frame_operations.pack_forget()
        self.frame_auth.pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = BanqueApp(root)
    root.mainloop()
    root = tk.Tk()
    app = BanqueApp(root)
    root.mainloop()

