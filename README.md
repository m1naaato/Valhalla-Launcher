# Valhalla Launcher — DD&SS

Le launcher Valhalla installe et lance **Dungeons, Dragons and Space Shuttles** directement, sans Prism. Il utilise Minecraft 1.12.2, Forge et un dossier de jeu indépendant dans `%LOCALAPPDATA%\\Valhalla\\DDSS`.

1. Installe Valhalla et connecte ton compte Microsoft possédant Minecraft Java.
2. Clique sur **Installer / mettre à jour DD&SS**. Au premier lancement, Minecraft, Java et Forge sont téléchargés, ainsi que les mods, scripts et quêtes depuis le pack du serveur.
3. Clique sur **Jouer** pour lancer Minecraft et rejoindre le serveur Valhalla.

Les fichiers du serveur sont contrôlés par SHA-256 avant d'être placés dans le dossier de jeu. La synchronisation publique du dépôt limite les fichiers à `mods/*.jar`, `scripts/*.zs` et `config/betterquesting/*.json|*.cfg`. La version précédente utilisant Prism peut être remplacée par l'installateur de cette version.
