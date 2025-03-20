CREATE DATABASE banque;
USE banque;
CREATE TABLE utilisateurs ( 
id INT PRIMARY KEY AUTO_INCREMENT,
nom VARCHAR (100) NOT NULL, 
email VARCHAR (100) UNIQUE NOT NULL, 
mot_de_passe VARCHAR (255) NOT NULL, 
date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE transactions (
id INT PRIMARY KEY AUTO_INCREMENT, 
utilisateur_id INT NOT NULL,
reference VARCHAR(50) NOT NULL, 
description TEXT  NOT NULL,
montant DECIMAL (10,2) NOT NULL, 
date_transaction DATE NOT NULL, 
type_transaction ENUM ("retrait","depot","transfert") NOT NULL, 
categorie VARCHAR(100),
FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);
CREATE TABLE comptes (
id INT PRIMARY KEY AUTO_INCREMENT,
utilisateurs_id INT NOT NULL, 
solde DECIMAL (10,2) NOT NULL DEFAULT 0.00,
date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (utilisateurs_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);
CREATE TABLE connexions (
id INT PRIMARY KEY AUTO_INCREMENT,
utilisateurs_id INT NOT NULL, 
date_connexion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
adresse_ip VARCHAR (45),
FOREIGN KEY (utilisateurs_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);
INSERT INTO utilisateurs (nom, email, mot_de_passe)
VALUES 
            (1, "Dupont", "Jean", "DupontJEAN123*", 1500.0),
            (2, "Martin", "Sophie", "MARTINSophie654*", 2200.0),
            (3, "Lefebvre", "Pierre", "LEfeBVREPierre908*", 800.0),
            (4, "Bernard", "Marie", "BERNARDMARIe456!", 3500.0),
            (5, "Thomas", "Paul", "THOMASPaul432!", 1200.0),
            (6, "Petit", "Julie", "PETITjulie34!", 950.0),
            (7, "Robert", "Michel", "ROBERTMichel987?", 2800.0),
            (8, "Richard", "Emma", "rICHARDEMMA45/", 1700.0),
            (9, "Durand", "Philippe", "DURANDPHIlippe98765+", 3200.0),
            (10, "Leroy", "Claire", "LEROYCLAIRe6789!", 600.0);
            
SELECT * FROM utilisateurs WHERE email = "marie.martin@example.com";