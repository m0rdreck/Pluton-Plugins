Remove plugin
==============

In English          

  Setup:

    Add the "Remove" folder in rust_dedicated\Release\server\my_server_identity\Pluton\Plugins\Remove\Remove.py
    Then in the game console ( open with f1 ) write pluton.reload
    The plugin is now ready for use

  Commands list:

    /remove ( only admin ) admin can destroy all building
    /owner ( only admin ) for know name of builder
    /destroy to destroy one object
    /share "name" for share your building part
    /unshare "name" for unshare your building part
    /destroyConfig for see all list of plugin configuration
    /destroyConfigUpdate "config" "value" for change plugin configuration

  Configuration list:

    language=en
      fr for french language
      en for english language
    remove=1
    destroy=1
    owner=1
      1 for activate
      0 for desactivate
    remove_delay=15000
    destroy_delay=15000
    owner_delay=15000
      change this value for time of function is activate in ms

En Français

  Installation:

    Ajouter le dossier "Remove" dans rust_dedicated\Release serveur\my_server_identity\Pluton\Plugins\Remove\Remove.py
    Ensuite dans la console du jeu (ouvrir avec f1) écrire pluton.reload 
    Le plugin est maintenant prêt à fonctionner

  Liste des commandes

    /remove ( only admin ) l'admin peut détruire n'importe quelle batiment
    /owner ( only admin ) pour connaître le nom du constructeur
    /destroy pour détruire un batiment
    /share "name" pour partager vos batiments
    /unshare "name" pour enlever le partage
    /destroyConfig pour voir la liste des configurations du plugin 
    /destroyConfigUpdate "config" "valeur" pour modifier une configuration du plugin

  Liste des configurations:

    language=fr
      fr Pour la langue française
      en Pour la langue anglaise
    remove=1
    destroy=1
    owner=1
      1 activer
      0 désactiver
    remove_delay=15000
    destroy_delay=15000
    owner_delay=15000
      Permet de changer le temps d'activation de la fonction
  
