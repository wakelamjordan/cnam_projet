# cnam_projet

1- projete
    dans le cadre du projet en bînome de 120h
    projet de plateforme pour une mairie

2- workflow (a produire)
    a- branch
        -main
            contien le code principale de l application
        -dev
            contien toutes les etapes de developpement
        -conception
            contien tout les production de document lors de la phase de conception et spéciification
    b- industrialisation continu
        .github/workflows/CICD.yml 
        step
            connexion
                test connexion à l hebergeur
            transfert-api
                transfert le contenu du repertoire api du repository
            deployement-front
                creation de la machine virtuel
                copie dans la machine virtuel le contenu du repertoire front du repository
                execution des commandes
                    npm install
                    npm run build
                envoi du contenu du fichier out genere par transfert ssh sur l hebergeur dans le repertoire front

3- utilisation du projet
    a- recuperation repository
        git clone <url repository>
    b- lancement
        (require docker)
        dans le repertoire du projet
        docker compose up