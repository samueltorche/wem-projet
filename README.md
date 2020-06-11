# Web mining - Movie Recommendation - Netchill & Flix
Ayrton Dumas, Marcro Mattei, Samuel Torche
WEM 2020


# Contexte et objectifs
## But du projet
Le but du projet Netflix & Chill est de pouvoir recommander des films à un utilisateur en se basant sur du Market Basket Analysis qui permet de pouvoir trouver des films qui sont souvent appréciés par des personnes qui ont les même goûts que l’utilisateur.

## Contexte et objectifs
Ce projet est réalisé dans le cadre du cours de Web Mining. L’objectif est que l’utilisateur fournisse le nom de 1 ou plusieurs films qu’il apprécie, et que le système ressortent des films qu’il serait susceptible d’apprécier.
Les films susceptibles d’être appréciés seront récupérés en se basant sur les personnes qui ont vu le ou les films entrés par l’utilisateur et qui ont apprécié d’autres films similaires.

# Données
### Source
La source de nos données sera le dataset MovieLens (https://grouplens.org/datasets/movielens/), plus particulièrement le MovieLens 25M Dataset. Le dataset peut être utilisé librement à des fins éducatives et de recherche.

### Description
Cet ensemble de données décrit le classement 5 étoiles de MovieLens, un service de recommandation de films. Il contient 25’000’095 classifications sur 62’423 films. Ces données ont été créées par 162’541 utilisateurs entre le 09 janvier 1995 et le 21 novembre 2019. Cet ensemble de données a été généré le 21 novembre 2019.
Une fois le ZIP extrait après téléchargement, on obtient plusieurs fichiers. Dans notre cas, on va s’intéresser au fichier movies.csv et ratings.csv


Le fichier movies.csv est composé de 3 colonnes: movieId (integer), title (string), genres (string). Il contient les données de base des 62’423 films susmentionnées.

![datamain](https://i.imgur.com/FMsNlF4.png)

Le fichier ratings.csv contient 4 colonnes: userId (integer), movieId (integer), rating (integer), timestamp. Ce fichier contient les 25’000’095 évaluations par les 162’541 utilisateurs.
![datamain](https://i.imgur.com/G21IiDJ.png)


Grâce à ces fichiers, on peut savoir quels utilisateurs ont donné quelles notes à un film et ainsi construire notre système de recommandation.

### Extraction
Pour l’extraction des données, il suffit simplement de télécharger le dataset et garder les fichiers intéressants. Ainsi, on peut facilement importer les fichiers CSV dans notre système.

# Etat de l'art
Nous avons trouvé des articles qui présentait brièvement des implémentations possible afin de construire des systèmes de recommandation:
- Movie Recommendation with Market Basket Analysis: implémentation en R utilisant également des sets de données provenant de MovieLens https://rstudio-pubs-static.s3.amazonaws.com/203264_7e572fa75b40422d90bd2fd5f3825798.html
- MBA For Breakfast — A Simple Guide to Market Basket Analysis: article démontrant l'utilisation de librairies de MBA en python sur un set de données de type supermarché (pain-beurre) comme vu en cours de Data Management au semestre précédent https://towardsdatascience.com/mba-for-breakfast-4c18164ef82b

Ceci nous a aidé à savoir comment mettre en place les données: il faut créer une matrice de transactions. 1 transaction correspond à une ligne et correspond à un utilisateur. Il y a une colonne pour chaque films, et si l'utilisateur a vu ce film, on mettra un 1 pour la colonne, sinon un 0.
![Transactions](https://i.imgur.com/WPM00G8.png)

## Librairies

Il existe plusieurs librairies en python permettant de faire du MBA. Il y a tout d'abord celle présentée dans l'article mentionné au dessus: mlxtend (http://rasbt.github.io/mlxtend/).
Mlxtend est très bien documenté, et propose des implémentations pour le minage des items sets fréquent: apriori et fpgrowth, tout en précisant des besoins minimaux tels qu'un support minimum. Il est bien sûr ensuite possible d'avoir les règles d'association sur la base de ces items sets fréquents.
Il y a d'autres librairies tels efficient-apriori (https://pypi.org/project/efficient-apriori/) ou bien encore apyori (https://pypi.org/project/apyori/), mais ces librairies sont moins documentés, ne proposent pas autant de customisation, et un simple test démontre qu'elles sont bien plus lentes à l'exécution que mlxtend, donc nous allons utiliser cette librairie.

Pour la lecture des données en format CSV et leur manipulation, l'excellente et populaire librairie pandas (https://pandas.pydata.org/), que nous avons l'habitude d'utiliser dans plusieurs cours, va nous permettre de pouvoir charger les données en mémoire sous format de dataframe facilement manipulable.

# Conception
Dans ce chapitre, nous allons présenter l'architecture globale du projet avec les technologies utilisés ainsi que les cas d'utilisation et les routes de l'API.

## Architecture
Notre architecture est constituée principalement de 3 composants : 
* Une application web en Vue.js. Notre groupe a déjà réalisé plusieurs projets ensemble et est expérimenté dans le developpement web avec le framework web [Vue.JS](https://vuejs.org/).
* Un serveur python avec le framework Flask pour constituer l’API. Python est choisi car les librairies utilisés sont disponibles en Python.
* Un fichier de données des critiques de films en CSV
![Architecture](https://i.imgur.com/abf897m.png)
L’application Web atteindra le serveur à l’aide de l’API mise en place avec Flask. Les appels seront des requêtes qui transmettent un ou des noms de films.
Le serveur Python reçoit la requête à l’aide de son API Flask et la traitera. Il accèdera aux données contenues dans ses règles qui auront été préalablement construites à l’aide du fichier de données CSV au lancement du serveur.
Une fois les films récupérés, il les transmettra à l’application Web qui les affichera à l’utilisateur.
![Flow](https://i.imgur.com/bOpKmYv.png)
Le backend consulte la base de données des films et leur ratings ce qui lui permet de construire les règles MBA, c’est la première étape et correspond aux flèches 1-3 du schéma ci-dessus. Les flèches 4-9 permettent d’illustrer les échanges qui se passent entre les différentes entités lors d’une recommandation de films, à noter que la flèche 7 est optionnelle et dépend du fait que l’utilisateur a ajouté une note.

## Use case
![Use case](https://i.imgur.com/qlXC0N6.png)
Un utilisateur “User” définit la liste des films qu’il a déjà regardés. Il peut ensuite générer les recommandations liées à cette liste.
Lorsqu’il définit la liste des films qu’il a regardés, il peut également attribuer une note aux films s’il en a envie. Ceci permettra de mettre à jour la base de données avec de nouvelles notes d’utilisateurs.


## Serveur

| Route        | Params           | Return  |
| ------------- |-------------| -----|
| GET /get_recommendations      | movie_ids[] | recommendations[] |
| POST /add_rating      | {"user_id", "movie_id", "rating":r      |  - |
| GET /get_movies | -      |   movies[] |
| GET /get_recommendations_for_ratings | user_id | recommendations[]

La différence entre la première et la quatrième est qu'on donne explicitement les id des films pour la première, et que pour la quatrième, on donne uniquement l'id de l'utilisateur, et dans ce cas, c'est le système qui ira chercher les id de films correspondants. En pratique, la quatrième n'est pas accessible depuis l'interface, car si on imagine qu'un user a fourni beacoup de ratings, le système ne trouvera pas de règles correspondantes, et cette route ne permettait pas de pouvoir customiser ces recommandations de manière satisfaisante. En effet, en pratique, on imagine mieux fournir 2-3 films qu'on apprécie et avoir le système nous fournir des recommendation basés sur ces 2-3 films plutôt que la trentaine de films pour lesquels on a soumis notre avis.

## Fonctionnement des recommendations

![activity](https://i.imgur.com/Jb9aUp0.png)
Les règles seront sauvegardées dans un fichier afin de ne pas avoir à les générer lors de chaque requête.

## Différence aves les approches existantes
La différence de notre projet avec les approches existantes réside dans le fait qu'un utilisateur peut ajouter des ratings via l'interface. En effet, cela permettra à notre dataset d'améliorer ses performances de plus en plus avec le temps. Ainsi, on pourrait imaginer recréer les règles tous les "x" jours en prenant en compte les derniers avis ajouté. On pourrait également imaginer pouvoir ajouter les derniers films sortis avec un formulaire sur l'interface, ce qui permettrait à notre système d'être pérenne.


# Fonctionnalités
La totalités des fonctionnalités sont disponibles sur l'interface web.




## Recherche de films

L'application permet aux utilisateurs de faire la recherche d'un film dans la base de donnée
![Gantt](https://i.imgur.com/T91yPsq.png =250x150)


## Détails d'un film
L'utilisateur peut voir les détails d'un film recherché et ajouter son avis.
![details](https://i.imgur.com/9FBme6E.png =200x150)

Il a également la possibilité d'ajouter le film à "ses films" pour générer des recommandations.

## Générer des recommandations

Lorsque l'utilisateur ajoute plusieurs films à sa liste, il peut générer les recommandations liées à ces films
![recommandation](https://i.imgur.com/NcmI10A.png =450x100)

Dans l'exemple précédent, l'utilisateur à ajouté deux films (Harry Potter 3 et 4), il peut ensuite générer la liste des recommandations:

* "Harry Potter and the Sorcerer's Stone (a.k.a. Harry Potter and the Philosopher's Stone)"
* "Forrest Gump"
* "Pirates of the Caribbean: The Curse of the Black Pearl"



# Techniques, algorithmes et outils utilisés 
Ce chapitre sert à détailler l'implémentation technique du projet.
## Preprocessing
Dans les données des films, l'année du films est mélangé à la colonne titre du film: "Harry Potter and the Chamber of Secrets (2002)". Une première étape de preprocessing est simplement d'enlever l'année du titre et l'ajouter dans une nouvelle colonne year, ceci dans un but purement esthétique pour l'interface.

Dans les données des avis (ratings), les avis ont des notes de 1 à 5. De manière, on peut déduire que les avis avec une note inférieure à 3 sont des avis négatifs. Nous avons pris le choix d'ignorer ces avis. Une autre possibilité aurait été de tenir compte des avis, mais de tweaker les algorithmes de MBA afin de tenir compte d'avis négatifs et trouver comment leur donner de l'importance, car un avis négatif transmet quand même de l'information. Cette possibilité aurait pris beacoup trop de temps à implémenter.

## Tuning
En ce qui concerne le "tuning" des paramètres pour le MBA, nous avons fait les choix suivants : 
* Algorithme pour miner les items sets fréquents: fpgrowth -> nous avions le choix entre apriori et fpgrowth, et nous avons choisi fpgrowth car, contrairement à apriori, fpgrowth ne génère pas de candidats explicitement, ce qui fait qu'il est bien plus adapté aux grands set de données, ce qui est notre cas.
* Min support : 0.1 -> Cette valeur a été choisie car elle permet d'avoir un nombre de règles conséquent. En montant celle-ci à 0.2, le nombre de règles trouvées est à 0.
* Métrique pour créer les règles : **Lift** -> La confidence ne permettait pas d'obtenir des règles assez "précises". C'est-à-dire qu'avec une confidence trop haute (0.9 par ex.), les règles restaient nombreuses mais leur pertinence n'était pas très bonne :  certains films recherchés ne retournaient aucune suggestion alors qu'il y avait la possibilité avec le set de données (Recherche de suggestions pour "Harry Potter 1" -> aucun résultat retourné). Avec une confidence plus basse (0.5), les règles étaient très nombreuses mais les suggestions n'étaient pas non plus très bonne car trop de films étaient retournés en tant que suggestion. Le lift a permis d'alléger le nombre de règles retournées mais celles-ci restent pertinentes.
* Min treshold: 4 -> Suivant différent tests, cette valeur a montré un bon équilibre entre nombre de règles et pertinences de celles-ci.

## Techniques
Afin de créer la matrice de transactions qui est nécessaire aux algorithmes de MBA, il faut pivoter la table sur les films afin que ceux-ci deviennent une colonne. Le dataset contenant énormément de films (62’423) et d'utilisateur, on se retrouvera avec une matrice de 162’541 lignes (1 pour chaque utilisateur), et 62’424 colonnes (1 pour chaque film et 1 pour l'id de l'utilisateur). Cette matrice doit tenir en mémoire afin de pouvoir exécuter les algorithme. Il y a une énorme perte de mémoire car un utilisateur aura fournis un avis positif pour très peu de films, hors on est obligé de stocker un 0 pour les films pour lesquels il n'a pas fourni un avis. Un moyen de palier à ce problème est l'utilisation de matrices sparses. Une matrice permet de ne pas stocker tous ces 0 inutiles afin d'économiser de l'espace mémoire. La librairie mlxtend permet d'implémenter ceci: http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/#example-3-working-with-sparse-representations

## Taille des données
À la base, nous voulions utiliser le dataset décrit dans le chapitre "Données". Cependant nous avons dû revoir ce point car bien qu'ayant tenté d'optimiser la mémoire avec une utilisation de matrice sparse et les meilleurs algorithmes existants, le temps de calcul ainsi que la mémoire posaient problème (script qui tourne pendant 4h avant de faire un memory leak).
Plusieurs possibilités étaient alors envisageables:
1. Utiliser un sous-groupe de données : 
    - Choisir les x films (par ex. 10k) ayant le plus d'avis et n'exécuter les algorithmes que sur ceux-ci.
    - Trouver un moyen de grouper les films (par ex. par genre) et ne prendre qu'un genre pour les recommendations.
2. Prendre un dataset plus petit : MovieLens propose un dataset recommendé pour le développement est donc plus petit. Il contient 100'000 avis appliqués sur 9'000 films par 600 utilisateurs. 

Nous avons alors choisi la deuxième proposition, c'est-à-dire d'utiliser un dataset plus petit. Le problème de la première option est qu'il risque d'intégrer un biais dans le système.

Notre choix peut sembler limiter étant donné qu'il n'y a que 600 utilisateurs mais celui-ci est tout de même assez conséquent pour obtenir des résulats intéressants et il n'est pas biaisé.


# Planification
Les couleurs des tâches dans le Gantt ci-dessous indiquent à quel membre la tâche est attribuée :
* Violet -> Marco Mattei
* Rouge -> Ayrton Dumas
* Vert -> Samuel Torche
* Bleu -> Toute l’équipe

![Gantt](https://i.imgur.com/ZQPhOaQ.png)

En pratique, nous avons réussi à suivre notre planning. La seule différence est que toute l'équipe a travaillé sur l'implémentation MBA en python dès le 15 mai, et non pas le 22 mai.

# Conclusion / Travail futur
Etant tous fans de films, ce projet était très intéressant pour l'ensemble du groupe.

Les tests ont cependant démontré qu'il est très difficile de créer un système de recommendation de films et que celui-ci dépend totalement des données utilisées. En effet, si le set de données contient des films qui ont été notés beaucoup plus de fois que d'autres, le système sera "biaisé", dans le sens où ces films ont beaucoup plus de probabilités d'apparaître dans les règles et impactent donc les "antécédents". C'est le cas par exemple du film "Forrest Gump".

De plus, le fait que les algorithmes prennent beaucoup de mémoire même avec les optimisations implémentées, il a été nécessaire de prendre un set de données plus petit et ceci impacte donc les performances du système car plus on a de données plus il est facile de créer des règles d'association cohérentes.

Bien que ces problèmes soient présents, notre application et système de recommendation sont fonctionnels et les différentes suggestions de recommendations sont pertinentes. Lorsque des suggestions sont trouvées, celles-ci sont effectivement correctes et ont du sens, car les différents films suggérés correspondent au goûts attendus selon les films indiqués. De plus, lorsqu'on veut des suggestions par rapport à un film d'une saga ("Harry Potter" par exemple), les films conseillés contiendront des autres films de la saga également.

Pour un travail futur, il serait intéressant d'essayer d'utiliser un set de données plus grand. Ceci pourrait être fait en parallélisant les traitements sur plusieurs machines ou alors en prenant des "bouts" du set et de les traiter un à un avant de les rassembler pour créer les règles finales. Ceci permettrait d'augmenter la performance du système.
En plus de ça, l'application web pourrait être améliorée pour qu'elle soit plus ergonomique. Effectivement, ce n'était pas l'objectif principal de ce projet, c'est pourquoi celle-ci a un aspect beaucoup plus "prototype". La création de comptes pour pouvoir enregistrer des recommendations ou modifier les notes qu'on a attribué à certains films serait également une route à explorer. Pour l'instant, les ratings ajouté via l'inteface sont sauvegardés dans un fichier à part. On peut imaginer créer un script s'occupant chaque semaine de merger ces nouveaux ratings dans le dataset existant et de réexécuter le script s'occupant de générer les règles.

# Démarage de l'application
Comme expliqué plus bas, l'architecture de MovieRecommendation est client-serveur.
* Client **Vue.JS**
* Serveur Flask **python3**

### Requirement
- python 3.6
- pip3
- Node.js 8.0+
- npm

### Installation
```bash
# install python modules
pip install -r "requirements.txt"

# install vuejs
cd web-app
npm install

# create rules
python test_small_dataset.py
```


### Démarrage

**Client**
```bash
cd web-app
npm run serve
```

**Serveur**
```bash
python api.py
```