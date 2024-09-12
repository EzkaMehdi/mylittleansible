# MyLittleAnsible Project 🚀

## Description 📝
MyLittleAnsible est un outil d'automatisation écrit en Python qui permet de gérer des configurations et des services sur des serveurs distants via SSH. Cet outil supporte diverses actions comme copier des fichiers, gérer des services système, et appliquer des templates de configuration.

## Prérequis 🛠️
- Python 3.8+
- pip (Python package manager)
- Docker (pour la simulation de serveurs locaux)

## Installation 📦

### 1. Clonage du Répertoire 📂
Clonez le dépôt sur votre machine locale en utilisant Git (installez Git si ce n'est pas déjà fait) :
```bash
git clone https://yourrepository.com/mylittleansible.git
cd mylittleansible
```

### 2. Configuration de l'Environnement Virtuel 🌐
Il est recommandé d'utiliser un environnement virtuel pour gérer les dépendances.

```bash
python -m venv venv
source venv/bin/activate  # Pour Unix/Linux
venv\Scripts\activate     # Pour Windows
```
### 3. Installation des Dépendances 🔽
Installez toutes les dépendances nécessaires en utilisant pip :

```bash
pip install -r requirements.txt
```

## Configuration des Machines Docker 🐳
### Installation de Docker 🐳
Assurez-vous que Docker est installé sur votre machine. Vous pouvez télécharger Docker Desktop à partir de Docker Hub.

### Création d'une Machine Docker 🖥️
Pour simuler un environnement de serveur, vous pouvez utiliser Docker pour créer un conteneur avec SSH accessible. Utilisez la commande suivante pour créer un conteneur Ubuntu avec un service SSH :

```bash
docker run -d -p 2222:22 --name my-ssh-server rastasheep/ubuntu-sshd:18.04
```
Répétez cette commande en changeant le nom du conteneur et le port exposé pour simuler plusieurs serveurs.

### Configuration SSH 🔑
Par défaut, le conteneur utilise l'utilisateur root avec le mot de passe root. Assurez-vous de changer ces informations ou de configurer correctement les règles de sécurité si vous utilisez cet environnement en production.

### Utilisation 🚀
Configuration du fichier inventory.yml 📄
Configurez inventory.yml avec les adresses IP, les ports SSH, et les informations d'authentification pour chaque serveur que vous souhaitez gérer.

### Configuration du fichier todos.yml 📝
Définissez les tâches à exécuter sur les serveurs dans le fichier todos.yml. Chaque tâche peut spécifier un module (par exemple, copy, service) et les paramètres nécessaires.

### Exécution de l'Outil 🖥️
Exécutez l'outil avec les fichiers de configuration appropriés :

```bash
python -m mylittleansible -f todos.yml -i inventory.yml
```
## Conclusion 🎉
MyLittleAnsible est un outil flexible pour l'automatisation de la gestion des configurations et des services sur plusieurs serveurs. Pour toute question ou problème, veuillez consulter la documentation ou me contacter ezka.mehdi@gmail.com.