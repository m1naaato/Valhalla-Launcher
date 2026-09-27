# Valhalla Launcher — DD&SS

Valhalla utilise Prism Launcher pour démarrer **Dungeons, Dragons and Space Shuttles**, Minecraft 1.12.2 avec Forge.

1. Installe une fois DD&SS dans Prism Launcher (CurseForge). Les fichiers nécessaires au client ne sont pas tous présents sur un serveur dédié.
2. Lance Valhalla et clique sur **Installer / mettre à jour DD&SS**. Le launcher cherche ton instance Prism DD&SS, télécharge les fichiers du serveur Valhalla publiés dans ce dépôt et vérifie leurs empreintes SHA-256.
3. Clique sur **Jouer** pour rejoindre le serveur.

La synchronisation GitHub copie uniquement les fichiers `mods/*.jar`, `scripts/*.zs` et `config/betterquesting/*.json|*.cfg` du serveur NitroServ. Elle ne copie ni propriétés du serveur ni secrets. Le pack ne sera pas proposé si la version, le loader ou le nombre de mods ne correspondent pas à DD&SS.

Le pack est publié dans `ddss-pack-files/` avec l'index `ddss-server-pack.json`. Les anciens fichiers NeoForge restent distincts.
