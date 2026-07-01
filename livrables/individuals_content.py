# -*- coding: utf-8 -*-
"""Contenu détaillé des rendus individuels — Zaafir & Elyess (~10-13 pages)."""
from content_docs import individual, CODE, wrap_table  # noqa
from generate_docs import (flow_vertical, flow_horizontal, layered_stack,  # noqa
                           network_topology, fan_out, screenshot, Spacer, BLUE,  # noqa
                           CONTENT_W, cm)  # noqa

CICD_STEPS = ["Connexion Azure (identifiants sécurisés)",
              "Terraform apply — provisionnement de l'infra",
              "Build & push des images vers ACR",
              "Scan de sécurité Trivy (bloquant)",
              "Installation Ingress + supervision",
              "Déploiement Helm de l'application",
              "Configuration MinIO on-premise (Ansible)"]

# ============================================================ ZAAFIR
individual(
    "PE-2526_%s_MougammadouZaafir.pdf" % CODE,
    "Zaafir Mougammadou Zaccaria", "Infrastructure cloud & déploiement applicatif",
    "Infrastructure as code Terraform, application FastAPI/React, déploiement",
    [
    ("H1", "1. Contexte et rôle dans le projet"),
    ("P", "Au sein de l'équipe, j'ai assumé la responsabilité de deux briques indissociables : "
     "l'infrastructure Azure décrite sous forme de code, et l'application elle-même, de son développement "
     "jusqu'à son déploiement sur le cluster. Mon fil conducteur a été un principe simple mais exigeant : "
     "partir d'un dépôt vide, il devait être possible de reconstruire l'intégralité de l'environnement — "
     "réseau, cluster, base de données, application — de façon entièrement automatique et strictement "
     "reproductible, sans qu'aucune étape ne repose sur une manipulation manuelle mémorisée par un membre de "
     "l'équipe."),
    ("P", "Ce positionnement me plaçait à la charnière entre le développement et l'exploitation, ce qui "
     "correspond exactement à l'esprit DevOps : je devais comprendre les besoins fonctionnels du cabinet pour "
     "concevoir l'application, tout en anticipant les contraintes d'hébergement, de sécurité et de coût qui "
     "conditionnent sa mise en production. Cette double casquette a nourri l'ensemble de mes choix "
     "techniques, du modèle de données jusqu'à la façon d'injecter les secrets dans les conteneurs."),
    ("P", "Concrètement, mon travail conditionnait celui des autres membres : sans infrastructure "
     "provisionnée et sans application conteneurisée, ni la chaîne d'intégration, ni la supervision, ni le "
     "plan de reprise n'avaient d'objet. J'ai donc veillé, dès le début du projet, à livrer rapidement une "
     "première version fonctionnelle afin que chacun puisse avancer sur son périmètre."),

    ("H1", "2. Ma contribution détaillée"),
    ("H2", "2.1 Conception de l'infrastructure Terraform"),
    ("P", "J'ai écrit les modules Terraform qui décrivent l'ensemble des ressources Azure du projet : le "
     "groupe de ressources qui les regroupe, le cluster Kubernetes managé (AKS), le registre d'images Azure "
     "Container Registry, le serveur PostgreSQL Flexible, ainsi que la configuration réseau et le budget de "
     "surveillance des coûts. Chaque ressource est paramétrée par des variables afin de pouvoir ajuster la "
     "région, la taille des machines ou l'activation de certains composants sans modifier le code."),
    ("P", "Un soin particulier a été porté à l'<b>idempotence</b> de cette description : appliquée plusieurs "
     "fois, elle doit converger vers le même état sans effet de bord. C'est cette propriété qui permet à la "
     "chaîne d'intégration de rejouer le déploiement en toute confiance, et qui garantit qu'un membre de "
     "l'équipe obtiendra exactement la même infrastructure qu'un autre. J'ai également veillé à ce que les "
     "dépendances entre ressources soient correctement exprimées, afin que Terraform les crée dans le bon "
     "ordre : par exemple, le registre d'images et le rôle d'accès associé doivent exister avant le cluster "
     "qui devra tirer les images."),
    ("P", "La gestion de l'état Terraform a fait l'objet d'une attention spécifique. Plutôt qu'un état local, "
     "fragile et non partageable, nous avons opté pour un état distant stocké dans un compte de stockage "
     "Azure, ce qui permet le travail à plusieurs et évite les conflits d'écriture. J'ai conçu la "
     "configuration de sorte que ce compte de stockage soit créé automatiquement s'il n'existe pas, "
     "supprimant ainsi toute étape préalable manuelle et rendant le premier déploiement aussi simple que les "
     "suivants."),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", flow_vertical(["terraform apply", "Groupe de ressources Azure",
                            "AKS · ACR · PostgreSQL Flexible",
                            "VM on-premise · budget FinOps"])),

    ("H2", "2.2 Développement de l'application"),
    ("P", "J'ai développé le cœur applicatif avec le framework FastAPI, en Python. L'API expose les "
     "ressources métier du cabinet : les patients, les appareils auditifs qui leur sont associés et les "
     "rendez-vous de suivi. J'ai structuré le code en couches claires — modèles de données, schémas de "
     "validation, logique d'accès aux données et routes HTTP — afin qu'il reste lisible et maintenable. La "
     "validation des entrées est confiée à Pydantic, ce qui garantit qu'aucune donnée mal formée n'atteint "
     "la base et que les erreurs sont renvoyées au client de façon explicite."),
    ("P", "J'ai doté l'API de <b>sondes de santé</b> distinctes : une sonde de vivacité qui confirme que le "
     "service répond, et une sonde de disponibilité qui vérifie en outre que la base de données est "
     "joignable. Cette distinction est essentielle pour Kubernetes, qui s'appuie sur ces sondes pour décider "
     "de redémarrer un conteneur ou de lui envoyer du trafic. J'ai également exposé un point de terminaison "
     "de métriques, consommé par la supervision mise en place par Adame, ce qui illustre l'interdépendance de "
     "nos périmètres."),
    ("P", "Côté interface, j'ai réalisé un frontend React servi par un serveur nginx. Au-delà de la gestion "
     "des patients (consultation, création, suppression), chaque dossier patient donne accès à deux rubriques "
     "métier essentielles au cabinet : l'<b>enregistrement des appareils auditifs</b> (marque, modèle, numéro "
     "de série, oreille appareillée et date de pose) et la <b>prise de rendez-vous</b> de suivi (date, heure "
     "et motif), complétée par une vue d'ensemble des rendez-vous à venir. L'interface consomme l'API via un "
     "chemin unique, ce qui simplifie considérablement le routage en production, où le frontend et le backend "
     "sont exposés derrière le même point d'entrée. J'ai porté attention à ce que l'expérience reste fluide "
     "même en cas d'erreur réseau, en affichant des messages compréhensibles à l'utilisateur."),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", screenshot("assets/app_dossier.png")),
    ("FLOW", Spacer(1, 2)),
    ("P", "<i>Capture d'écran de l'application : le dossier d'un patient réunit les deux rubriques métier — "
     "l'enregistrement d'un appareil auditif (avec la liste des appareils déjà posés) et la prise de "
     "rendez-vous de suivi.</i>"),
    ("P", "J'ai structuré l'application en couches nettement séparées, chacune n'ayant connaissance que de la "
     "couche immédiatement inférieure. Cette organisation, illustrée ci-dessous, rend le code lisible, "
     "testable et évolutif : on peut par exemple faire évoluer la logique d'accès aux données sans toucher "
     "aux routes HTTP."),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", layered_stack([
        ["Frontend React (nginx)", "consultation & saisie des patients"],
        ["Routes HTTP FastAPI", "points d'entrée REST + /healthz /readyz /metrics"],
        ["Schémas Pydantic", "validation & typage des données entrantes/sortantes"],
        ["Couche d'accès aux données (SQLAlchemy)", "requêtes et transactions"],
        ["PostgreSQL Flexible", "stockage relationnel chiffré (TLS)"]])),
    ("FLOW", Spacer(1, 4)),
    ("P", "<i>Architecture applicative en couches : chaque niveau isole une responsabilité, du rendu de "
     "l'interface jusqu'au stockage relationnel.</i>"),

    ("H2", "2.3 Conteneurisation et déploiement"),
    ("P", "J'ai conteneurisé les deux composants au moyen d'images Docker construites en plusieurs étapes "
     "(multi-stage), afin de séparer la phase de compilation de l'image finale et d'obtenir des images "
     "légères, plus rapides à distribuer et à démarrer. Ces images s'exécutent avec un utilisateur non "
     "privilégié, conformément aux bonnes pratiques de sécurité, un point sur lequel j'ai collaboré "
     "étroitement avec le responsable sécurité de l'équipe."),
    ("P", "Le déploiement sur le cluster s'appuie sur le chart Helm conçu avec Anis : j'ai veillé à ce que "
     "l'application reçoive sa configuration — notamment la chaîne de connexion à la base — par "
     "l'intermédiaire d'un secret Kubernetes injecté au moment du déploiement, et jamais écrit en clair dans "
     "le dépôt. J'ai enfin coordonné l'enchaînement complet du déploiement de bout en bout et vérifié, après "
     "chaque livraison, le bon fonctionnement de l'application, de la base et de l'interface. Le flux de "
     "traitement d'une requête utilisateur suit le chemin suivant :"),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", flow_horizontal([["Utilisateur"], ["Ingress", "NGINX"],
                              ["Frontend /", "Backend"], ["PostgreSQL", "(TLS)"]], color=BLUE)),

    ("H1", "3. Choix technologiques : pourquoi ces technologies plutôt que d'autres"),
    ("P", "Chacune des briques dont j'avais la charge a fait l'objet d'une comparaison explicite avec ses "
     "alternatives. Je détaille ci-dessous les trois décisions les plus structurantes — l'outil "
     "d'infrastructure, le framework applicatif et le moteur de base de données — sous forme de tableaux "
     "comparatifs suivis de leur justification."),

    ("H2", "3.1 Infrastructure as code : Terraform plutôt que Bicep ou Pulumi"),
    ("FLOW", wrap_table([
        ["Critère", "Terraform (retenu)", "Bicep / ARM", "Pulumi"],
        ["Portabilité", "Agnostique (multi-cloud)", "Azure uniquement", "Multi-cloud"],
        ["Langage", "HCL déclaratif, lisible", "DSL Azure / JSON verbeux", "Langages généraux (TS, Go…)"],
        ["Gestion de l'état", "État distant mûr et partagé", "Pas d'état (géré par Azure)", "État propriétaire, récent"],
        ["Écosystème / modules", "Très large, communauté active", "Limité à Azure", "Plus restreint"],
        ["Adéquation au projet", "Standard du marché DevOps", "Enfermement Azure", "Surdimensionné ici"],
    ], [3.1 * cm, 4.5 * cm, 4.6 * cm, CONTENT_W - 12.2 * cm])),
    ("P", "J'ai retenu <b>Terraform</b> parce qu'il est le standard de fait de l'infrastructure as code et "
     "qu'il reste agnostique du fournisseur : si le cabinet devait un jour migrer une partie de sa plateforme "
     "vers un autre cloud, la logique de description resterait valable. Bicep, bien qu'élégant et sans état à "
     "gérer, aurait enfermé le projet dans l'écosystème Azure ; Pulumi, qui permet de décrire l'infrastructure "
     "dans un langage de programmation classique, apportait une puissance dont nous n'avions pas besoin pour "
     "un MVP et introduisait une dépendance à un état propriétaire. La lisibilité déclarative du HCL et la "
     "maturité de la gestion d'état distant ont donc été décisives."),

    ("H2", "3.2 Framework applicatif : FastAPI plutôt que Flask ou Django"),
    ("FLOW", wrap_table([
        ["Critère", "FastAPI (retenu)", "Flask", "Django"],
        ["Validation / typage", "Native via Pydantic", "Manuelle ou extensions", "Forms / DRF"],
        ["Documentation d'API", "OpenAPI générée seule", "À ajouter manuellement", "DRF, plus lourd"],
        ["Performances", "Élevées (asynchrone, ASGI)", "Synchrone (WSGI)", "Synchrone par défaut"],
        ["Poids pour un MVP API", "Léger, ciblé sur l'API", "Léger mais peu structurant", "Lourd (ORM, admin, templates)"],
    ], [3.4 * cm, 4.4 * cm, 4.2 * cm, CONTENT_W - 12.0 * cm])),
    ("P", "Le choix de <b>FastAPI</b> s'explique par sa validation typée native, sa documentation OpenAPI "
     "générée automatiquement et sa nature asynchrone, qui offre de bonnes performances sur des machines "
     "volontairement modestes. Flask aurait exigé d'assembler manuellement validation et documentation, au "
     "risque d'une moindre rigueur ; Django, très complet, aurait apporté un ORM, une interface "
     "d'administration et un moteur de templates dont une API pure n'a pas l'usage, alourdissant inutilement "
     "l'image conteneur et la surface d'attaque. FastAPI offrait le meilleur rapport entre robustesse et "
     "sobriété pour notre besoin."),

    ("H2", "3.3 Base de données : PostgreSQL plutôt que MySQL ou MongoDB"),
    ("FLOW", wrap_table([
        ["Critère", "PostgreSQL (retenu)", "MySQL", "MongoDB"],
        ["Modèle de données", "Relationnel riche", "Relationnel", "Documentaire"],
        ["Adéquation métier", "Idéal (patients ↔ appareils ↔ RDV)", "Convient", "Peu adapté aux relations"],
        ["Offre managée Azure", "Flexible Server, peu coûteux", "Flexible Server", "Cosmos DB, plus cher"],
        ["Intégrité", "ACID, contraintes fortes", "ACID", "Cohérence plus souple"],
    ], [3.4 * cm, 4.6 * cm, 4.0 * cm, CONTENT_W - 12.0 * cm])),
    ("P", "Les données du cabinet sont fortement relationnelles : un patient possède des appareils et des "
     "rendez-vous, avec des contraintes d'intégrité qu'une base documentaire comme MongoDB gérerait mal. "
     "<b>PostgreSQL</b> s'est imposé pour sa richesse relationnelle, son respect strict des propriétés ACID et "
     "son offre managée peu coûteuse sur Azure (Flexible Server), qui nous décharge des sauvegardes, des "
     "correctifs et de la supervision de bas niveau. MySQL aurait convenu, mais PostgreSQL offre des types et "
     "des contraintes plus riches ; MongoDB, orienté documents, aurait compliqué la modélisation de relations "
     "pourtant naturelles ici, et sa déclinaison managée Azure (Cosmos DB) est nettement plus onéreuse."),

    ("H2", "3.4 Hébergement de la base et conteneurs : arbitrages de sécurité"),
    ("P", "Concernant l'hébergement de la base, nous avons retenu un accès public restreint par un pare-feu "
     "n'autorisant que les ressources internes à Azure, avec chiffrement TLS obligatoire. C'est un compromis "
     "assumé : un réseau entièrement privé aurait été plus sûr, mais aurait ajouté une complexité — réseau "
     "virtuel dédié, résolution DNS privée, points de terminaison privés — difficilement justifiable pour un "
     "MVP au budget serré. J'ai documenté ce compromis afin qu'il soit clairement identifié comme un axe "
     "d'amélioration prioritaire pour une éventuelle mise en production réelle."),
    ("P", "Enfin, le choix d'images Docker multi-stage et non privilégiées relève à la fois de la sécurité et "
     "de la sobriété : des images plus petites consomment moins de stockage dans le registre, se transfèrent "
     "plus vite et réduisent la surface d'attaque, autant de bénéfices alignés avec les objectifs "
     "transversaux du projet."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "La principale difficulté a été d'<b>industrialiser le provisionnement</b> pour qu'il soit "
     "réellement rejouable par la chaîne d'intégration. Les premières exécutions ont révélé des situations "
     "délicates : un déploiement interrompu laissait l'état Terraform verrouillé, empêchant toute reprise "
     "ultérieure. En collaboration avec Elyess, responsable de la chaîne, nous avons ajouté un mécanisme "
     "libérant automatiquement ce verrou résiduel avant chaque application, ce qui a rendu la chaîne robuste "
     "face aux interruptions."),
    ("P", "Une deuxième difficulté a concerné la cohérence entre la version de l'application déployée et la "
     "configuration attendue. J'ai résolu ce point en faisant en sorte que chaque déploiement utilise une "
     "étiquette d'image unique, ce qui force le remplacement propre des conteneurs et garantit que la "
     "nouvelle configuration — y compris les secrets — est bien prise en compte, sans réutilisation "
     "silencieuse d'une ancienne image mise en cache."),
    ("P", "Un troisième problème, plus subtil, est apparu au moment de la sauvegarde de la base : un "
     "caractère spécial présent dans le mot de passe généré cassait l'interprétation de l'URL de connexion "
     "par l'outil de sauvegarde. Après diagnostic, j'ai imposé la génération d'un mot de passe strictement "
     "alphanumérique — l'entropie restant largement suffisante sur vingt-quatre caractères — ce qui a éliminé "
     "toute une classe d'erreurs d'interprétation, aussi bien pour l'application que pour les outils annexes."),
    ("P", "Chacune de ces difficultés m'a appris qu'une infrastructure fiable ne se conçoit pas d'un seul "
     "jet : elle se durcit par itérations, au contact des cas réels, en traitant chaque incident à sa racine "
     "plutôt qu'en le contournant ponctuellement."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "À court terme, je remplacerais l'authentification de la chaîne d'intégration par une fédération "
     "d'identité OIDC entre GitHub et Azure. Ce mécanisme substitue aux identifiants stockés des jetons "
     "éphémères délivrés à la demande, ce qui constitue l'état de l'art en matière de sécurité et lèverait "
     "l'actuelle contrainte d'un compte sans double authentification."),
    ("P", "Je ferais également évoluer la base vers un accès strictement privé, sans aucune exposition "
     "publique, en plaçant l'application et la base dans un réseau virtuel commun relié par des points de "
     "terminaison privés. Cette évolution renforcerait significativement l'isolation des données de santé et "
     "rapprocherait l'architecture des exigences d'un véritable contexte de production soumis au RGPD."),
    ("P", "À moyen terme, j'introduirais un outil de migrations de schéma versionnées, qui remplacerait "
     "avantageusement la création automatique du schéma au démarrage : toute évolution de la structure de la "
     "base serait alors tracée, revue et réversible, ce qui est indispensable dès lors que des données réelles "
     "sont en jeu."),
    ("P", "Enfin, si le périmètre fonctionnel s'élargissait — facturation, tiers payant, notifications aux "
     "patients — l'API monolithique pourrait être découpée en services plus fins, au prix d'une complexité "
     "accrue à mettre en balance avec les bénéfices attendus."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "La limite la plus notable de mon périmètre tient au compromis réseau déjà évoqué : l'accès public "
     "restreint de la base, bien que sécurisé par un pare-feu et par TLS, reste moins satisfaisant qu'une "
     "isolation réseau complète, et ne conviendrait pas en l'état à un hébergement de données de santé "
     "réglementé."),
    ("P", "La création du schéma au démarrage de l'application constitue une seconde limite : pratique pour "
     "un MVP, elle devient risquée en exploitation, où toute modification de structure doit être maîtrisée. "
     "De même, le dimensionnement en machines « burstable » plafonne la capacité sous une charge soutenue et "
     "prolongée ; ce choix, parfaitement adapté à une démonstration, devrait être réévalué pour un usage réel "
     "et continu par le cabinet."),
    ("P", "Enfin, la couverture de tests automatisés de l'application, bien que présente et exécutée à chaque "
     "intégration, gagnerait à être étendue : les scénarios nominaux sont couverts, mais les cas d'erreur, "
     "les cas limites et les tests de charge mériteraient d'être développés pour fiabiliser davantage le "
     "service avant une ouverture à des utilisateurs réels."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Prérequis et configuration"),
    ("P", "Avant tout déploiement, l'équipe renseigne dans les secrets du dépôt les identifiants Azure "
     "(identifiant, mot de passe, tenant, abonnement) ainsi que l'adresse de courriel destinée aux alertes "
     "budgétaires. Ces informations, chiffrées par GitHub, ne sont jamais visibles dans le code ni dans les "
     "journaux d'exécution. Aucune autre préparation n'est nécessaire : le compte de stockage de l'état "
     "Terraform est créé automatiquement lors du premier lancement."),
    ("H2", "7.2 Déployer l'environnement"),
    ("P", "Le déploiement se lance depuis l'onglet Actions du dépôt, ou automatiquement par un envoi de code "
     "sur la branche principale. La chaîne provisionne l'infrastructure, construit et publie les images, puis "
     "déploie l'application. À la fin de l'exécution, l'adresse publique d'accès est affichée. L'ensemble ne "
     "demande aucune intervention manuelle intermédiaire."),
    ("H2", "7.3 Utiliser l'application"),
    ("P", "L'application est accessible à l'adresse publique de l'Ingress. L'interface web permet de gérer les "
     "patients, d'enregistrer leurs appareils auditifs et de planifier leurs rendez-vous de suivi depuis le "
     "dossier de chaque patient. La documentation interactive de l'API, utile pour les tests ou une future "
     "intégration avec d'autres logiciels du cabinet, est publiée sous le chemin « /api/docs ». Les points "
     "« /healthz » et « /readyz » permettent de vérifier en une commande que le service et sa base répondent "
     "correctement."),
    ("H2", "7.4 Reconstruire ou détruire"),
    ("P", "L'ensemble de l'infrastructure peut être reconstruit à l'identique par une seule action, ou "
     "détruit en choisissant l'action de destruction du workflow, ce qui interrompt immédiatement toute "
     "facturation. Cette reproductibilité garantit que le projet est duplicable et réutilisable, comme "
     "l'exige le cahier des charges."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de passer d'une logique de « code qui fonctionne sur ma machine » à une "
     "logique d'infrastructure et de déploiement entièrement automatisés et reproductibles. Cela m'a demandé "
     "de raisonner en permanence sur les cas d'échec et les états intermédiaires, et d'accepter plusieurs "
     "itérations avant d'obtenir une chaîne réellement fiable."),
    ("P", "J'ai également dû apprendre à collaborer sur un périmètre partagé : nombre de problèmes que j'ai "
     "rencontrés se situaient à la frontière avec les responsabilités d'Elyess ou d'Anis, ce qui m'a appris à "
     "communiquer précisément et à documenter mes choix pour que l'équipe puisse s'appuyer dessus."),
    ("H2", "Forces"),
    ("P", "Je retiens comme force ma capacité à avoir une vision d'ensemble reliant le développement "
     "applicatif et son hébergement, ce qui m'a permis de concevoir une application pensée dès le départ pour "
     "être déployée et exploitée, et non adaptée après coup."),
    ("P", "J'ai aussi fait preuve de persévérance face aux difficultés d'industrialisation, en cherchant "
     "systématiquement la cause racine d'un incident plutôt qu'un contournement rapide, ce qui a bénéficié à "
     "la robustesse globale du projet."),
    ("H2", "Faiblesses"),
    ("P", "J'ai parfois eu tendance à vouloir déployer l'ensemble en une seule fois plutôt qu'à valider par "
     "petits incréments testés, ce qui a occasionné des allers-retours qui auraient pu être évités par une "
     "approche plus progressive."),
    ("P", "Par ailleurs, mes compétences en sécurité réseau cloud, directement sollicitées par le choix "
     "d'hébergement de la base, restent perfectibles et constituent un domaine que je dois approfondir."),
    ("H2", "Compétences développées"),
    ("P", "Ce projet m'a permis de consolider ma maîtrise de Terraform et de la conception d'infrastructure "
     "Azure, de la conteneurisation Docker et du déploiement via Helm, ainsi que du développement d'une API "
     "moderne intégrée à une base de données relationnelle."),
    ("P", "Au-delà des outils, j'ai acquis une compréhension concrète de l'articulation entre le code, "
     "l'infrastructure et l'exploitation, qui est au cœur du métier DevOps et que seule la réalisation d'un "
     "projet complet de bout en bout permet réellement d'intégrer."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Pour de futurs projets, je souhaite adopter une approche plus incrémentale et testée des "
     "changements d'infrastructure, en validant chaque évolution isolément avant de l'intégrer à l'ensemble. "
     "Je compte également renforcer mes connaissances en réseau cloud — réseaux virtuels, points de "
     "terminaison privés, pare-feux applicatifs — afin de concevoir dès la première version des architectures "
     "plus sûres et plus proches des standards de production."),
    ],
)

# ============================================================ ELYESS
individual(
    "PE-2526_%s_RjafellahElyess.pdf" % CODE,
    "Elyess Rjafellah", "CI/CD & automatisation",
    "Chaîne GitHub Actions, état distant, pipeline auto-réparant",
    [
    ("H1", "1. Contexte et rôle dans le projet"),
    ("P", "Ma mission a porté sur le cœur de la démarche DevOps : la chaîne d'intégration et de déploiement "
     "continus. L'objectif fixé collectivement était ambitieux — obtenir un déploiement « en un clic » où "
     "l'intégralité du cycle de vie s'exécute automatiquement, sans intervention manuelle, et se rétablit "
     "seul en cas d'aléa : provisionnement de l'infrastructure, construction et analyse des images, "
     "déploiement de l'application, configuration du stockage de sauvegarde."),
    ("P", "Ce rôle est transversal par nature : la chaîne que j'ai construite orchestre le travail de tous "
     "les autres membres, en assemblant au bon moment l'infrastructure de Zaafir, le chart de déploiement "
     "d'Anis, la supervision et les scans de sécurité d'Adame. J'ai donc dû comprendre chaque brique pour "
     "l'intégrer correctement, ce qui m'a offert une vue d'ensemble précieuse sur l'articulation de la "
     "solution."),
    ("P", "L'automatisation n'est pas une commodité : c'est elle qui rend le projet reproductible, "
     "auditable et économe. Un déploiement manuel serait long, source d'erreurs et non traçable ; une chaîne "
     "automatisée garantit au contraire que chaque mise en production suit exactement les mêmes étapes, "
     "vérifiées et enregistrées, ce qui est une exigence forte du cahier des charges."),

    ("H1", "2. Ma contribution détaillée"),
    ("H2", "2.1 Architecture de la chaîne GitHub Actions"),
    ("P", "J'ai conçu plusieurs workflows complémentaires. Le workflow d'intégration valide chaque "
     "modification par l'analyse statique du code et l'exécution des tests, côté backend comme côté frontend. "
     "Le workflow de sécurité exécute les analyses de vulnérabilités. Le workflow de déploiement orchestre "
     "l'ensemble de la mise en production. Enfin, un workflow de sauvegarde, planifié quotidiennement, "
     "déclenche la réplication des données vers le site on-premise."),
    ("P", "Cette séparation en workflows spécialisés répond à un souci de clarté et d'efficacité : les "
     "vérifications rapides — tests, analyses — s'exécutent à chaque proposition de modification, tandis que "
     "les opérations lourdes et coûteuses — provisionnement, déploiement — ne sont déclenchées que de manière "
     "maîtrisée, sur la branche principale ou manuellement. Ce découpage limite aussi la consommation de "
     "minutes d'exécution, ce qui participe indirectement à la sobriété du projet. Le schéma ci-dessous "
     "montre comment chaque type d'événement déclenche le workflow approprié :"),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", fan_out(["Événements", "GitHub"],
                     [["Pull Request", "→ Intégration (tests, lint)"],
                      ["Push sur main", "→ Sécurité + Déploiement"],
                      ["Déclenchement manuel", "→ Déploiement / Destruction"],
                      ["Planification (cron)", "→ Sauvegarde quotidienne"]])),
    ("FLOW", Spacer(1, 4)),
    ("P", "<i>Chaque événement (proposition de modification, envoi sur la branche principale, action manuelle "
     "ou planification) déclenche automatiquement le workflow adapté, sans intervention humaine.</i>"),

    ("H2", "2.2 Automatisation du provisionnement et de l'état"),
    ("P", "J'ai automatisé la préparation de l'état distant de Terraform : le workflow crée si nécessaire le "
     "compte de stockage dédié, puis initialise Terraform sur cet état avant d'appliquer l'infrastructure. "
     "Cette étape, souvent laissée manuelle dans les projets, a été entièrement scriptée pour que rien ne "
     "doive être préparé à l'avance, ce qui rend le tout premier déploiement aussi simple que les suivants."),
    ("P", "L'authentification à Azure au sein de la chaîne s'appuie sur des identifiants stockés dans les "
     "secrets chiffrés de GitHub, jamais exposés dans les journaux. J'ai veillé à masquer explicitement les "
     "valeurs sensibles — chaînes de connexion, mots de passe — dans les traces d'exécution, afin qu'elles "
     "n'apparaissent jamais en clair, même lors d'une session de débogage. Cette discipline est essentielle "
     "car les journaux de CI sont souvent consultés et partagés."),

    ("H2", "2.3 Orchestration et ordonnancement des étapes"),
    ("P", "Le déploiement complet enchaîne, dans un ordre précis, la connexion à Azure, l'application "
     "Terraform, la récupération des informations produites — adresses, identifiants — la construction et la "
     "publication des images, leur analyse de sécurité, l'installation des briques du cluster, puis le "
     "déploiement de l'application et la configuration du site on-premise."),
    ("P", "J'ai dû gérer finement les dépendances entre ces étapes. L'exemple le plus parlant concerne la "
     "supervision : les définitions de ressources personnalisées qu'elle introduit doivent être installées "
     "<b>avant</b> l'application qui les référence, faute de quoi le déploiement échoue. Comprendre et "
     "ordonner correctement ces dépendances a représenté une part importante de mon travail. La séquence "
     "complète du pipeline est la suivante :"),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", flow_vertical(CICD_STEPS)),

    ("H2", "2.4 Optimisation et fiabilisation"),
    ("P", "J'ai optimisé les temps d'exécution en supprimant des attentes bloquantes inutiles : plutôt que "
     "d'attendre que chaque composant de supervision soit totalement prêt, la chaîne applique les manifestes "
     "et laisse les composants converger en arrière-plan, ce qui a réduit la durée du déploiement de façon "
     "sensible tout en garantissant que les éléments réellement indispensables sont bien en place avant de "
     "poursuivre."),
    ("P", "La partie la plus exigeante a consisté à rendre le pipeline robuste face aux états intermédiaires. "
     "Un déploiement interrompu pouvait laisser un verrou sur l'état de l'infrastructure, ou une livraison "
     "Helm figée dans un état instable empêchant toute reprise. J'ai introduit des mécanismes qui détectent "
     "ces situations et les corrigent automatiquement : libération du verrou résiduel, nettoyage d'une "
     "livraison bloquée avant réinstallation. Grâce à ces garde-fous, la chaîne est devenue "
     "<b>auto-réparante</b> et se remet d'elle-même d'un incident, sans qu'un opérateur ait à intervenir."),

    ("H2", "2.5 Journal des incidents et correctifs durables"),
    ("P", "Plutôt que de contourner les échecs au cas par cas, j'ai tenu un véritable journal des incidents "
     "rencontrés lors des premières mises en production, en traitant chacun à sa racine par un correctif "
     "intégré définitivement au pipeline. Le tableau ci-dessous récapitule les principaux incidents, leur "
     "cause profonde et la correction durable apportée :"),
    ("FLOW", wrap_table([
        ["Incident rencontré", "Cause racine", "Correctif durable intégré"],
        ["Action de scan introuvable", "Référence de version inexistante", "Épinglage sur une référence valide"],
        ["Namespace déjà existant", "Créé par l'outil et par le chart", "Création confiée à un seul mécanisme"],
        ["Verrou d'état résiduel", "Déploiement interrompu", "Libération automatique avant chaque apply"],
        ["Livraison Helm bloquée", "Release dans un état instable", "Détection puis réinstallation propre"],
        ["Supervision en échec", "Définitions de ressources absentes", "Réordonnancement : CRD avant l'application"],
        ["Sauvegarde en échec", "Caractère spécial dans le mot de passe", "Mot de passe strictement alphanumérique"],
    ], [4.6 * cm, 4.6 * cm, CONTENT_W - 9.2 * cm])),
    ("P", "Chaque correctif a été validé par une exécution complète de la chaîne avant d'être considéré comme "
     "acquis. Ce journal illustre concrètement ma démarche : un pipeline fiable ne naît pas d'un seul jet, il "
     "se durcit incident après incident, et chaque problème résolu à sa racine bénéficie durablement à "
     "l'ensemble de l'équipe."),

    ("H2", "2.6 Concurrence, déclencheurs et sobriété d'exécution"),
    ("P", "J'ai également soigné la gestion de la concurrence : une contrainte empêche deux déploiements de "
     "s'exécuter simultanément sur le même environnement, ce qui éviterait des états incohérents si deux envois "
     "de code se succédaient rapidement. Les déclencheurs ont par ailleurs été calibrés avec soin — envoi sur "
     "la branche principale, exécution manuelle avec choix de l'action, ou planification pour les sauvegardes — "
     "afin qu'aucun déploiement coûteux ne parte par inadvertance. Cette maîtrise des déclencheurs participe "
     "directement à la démarche FinOps de l'équipe, en évitant de consommer inutilement des ressources cloud "
     "ou des minutes d'exécution."),

    ("H1", "3. Choix technologiques : pourquoi ces technologies plutôt que d'autres"),
    ("P", "Deux décisions ont structuré mon périmètre : le choix de la plateforme d'intégration et de "
     "déploiement continus, et le modèle de déploiement (piloté par la chaîne ou par un opérateur GitOps). "
     "Je les justifie ci-dessous par comparaison directe avec leurs alternatives."),

    ("H2", "3.1 Plateforme CI/CD : GitHub Actions plutôt que GitLab CI ou Jenkins"),
    ("FLOW", wrap_table([
        ["Critère", "GitHub Actions (retenu)", "GitLab CI", "Jenkins"],
        ["Intégration au dépôt", "Native (dépôt sur GitHub)", "Native si dépôt GitLab", "Externe, à connecter"],
        ["Hébergement", "Runners gérés, sans serveur", "Runners gérés ou auto-hébergés", "Serveur à installer et maintenir"],
        ["Catalogue réutilisable", "Très large (Marketplace)", "Templates", "Plugins (maintenance lourde)"],
        ["Gestion des secrets", "Intégrée et chiffrée", "Intégrée", "Via plugins / credentials"],
        ["Coût pour le projet", "Inclus, minutes gratuites", "Inclus si GitLab", "Coût d'un serveur permanent"],
    ], [3.1 * cm, 4.6 * cm, 4.5 * cm, CONTENT_W - 12.2 * cm])),
    ("P", "Le cahier des charges évoquait GitLab CI ; le dépôt étant hébergé sur GitHub, j'ai retenu "
     "<b>GitHub Actions</b>, dont le principe est rigoureusement identique — build, test, analyse, déploiement "
     "orchestré. Sa proximité avec le dépôt, son vaste catalogue d'actions réutilisables et sa gestion "
     "intégrée des secrets en font l'outil le plus naturel et le plus économe ici. Jenkins, très puissant, "
     "aurait imposé d'héberger et de maintenir en permanence un serveur dédié — un coût récurrent et une "
     "charge d'exploitation incompatibles avec un budget de 85 dollars. Le choix a donc été pragmatique et "
     "sans perte fonctionnelle par rapport à l'outil cité en exemple."),

    ("H2", "3.2 Modèle de déploiement : approche « push » plutôt que GitOps"),
    ("FLOW", wrap_table([
        ["Critère", "Push par la chaîne (retenu)", "GitOps (ArgoCD / Flux)"],
        ["Composant sur le cluster", "Aucun (la CI pousse)", "Opérateur permanent à héberger"],
        ["Simplicité pour un MVP", "Élevée, immédiate", "Plus complexe à mettre en place"],
        ["Coût / ressources", "Nul en plus", "Consomme CPU/RAM en continu"],
        ["Traçabilité de l'état", "Journaux de la chaîne", "État réconcilié en continu (supérieur)"],
        ["Retour arrière", "Re-déploiement d'une version", "Réconciliation automatique"],
    ], [3.6 * cm, 6.0 * cm, CONTENT_W - 9.6 * cm])),
    ("P", "J'ai privilégié un déploiement piloté par la chaîne, selon une approche « <b>push</b> », plutôt "
     "qu'un opérateur GitOps, afin de rester simple et économe. Un opérateur tel qu'ArgoCD ou Flux aurait "
     "introduit un composant permanent à héberger sur le cluster, consommant des ressources en continu — "
     "difficilement justifiable au regard du budget. Le GitOps offre une traçabilité et une réconciliation "
     "d'état supérieures, que j'ai clairement identifiées comme la suite logique une fois le projet "
     "stabilisé et le budget desserré ; pour un MVP, l'approche push apportait l'essentiel du bénéfice sans "
     "le surcoût."),
    ("P", "Enfin, le choix de séparer les workflows plutôt que de tout concentrer dans un pipeline unique "
     "répond à un principe de responsabilité claire : chaque workflow a un objectif précis, se déclenche sur "
     "les bons événements et peut être compris et maintenu indépendamment des autres, ce qui facilite le "
     "travail à plusieurs et la reprise du projet par un tiers."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "J'ai été confronté à une série d'échecs typiques d'une première mise en production : une action "
     "dont la version référencée n'existait pas, un conflit lié à une ressource déjà existante, un verrou "
     "d'état résiduel après une interruption, une livraison Helm bloquée, un mauvais ordonnancement des "
     "dépendances. Plutôt que de les contourner au cas par cas, j'ai choisi de traiter chaque incident à sa "
     "racine, en ajoutant dans le pipeline le correctif durable correspondant."),
    ("P", "Par exemple, le conflit de création du namespace applicatif — créé à la fois par l'outil et par le "
     "chart — a été résolu en confiant cette création à un seul mécanisme. De même, le déploiement de la "
     "supervision qui échouait faute de définitions de ressources préalables a été corrigé en réordonnant les "
     "étapes. Chacune de ces corrections a été validée par une exécution complète de la chaîne."),
    ("P", "Cette approche m'a beaucoup appris : un pipeline robuste ne se conçoit pas d'un seul jet, il se "
     "durcit par itérations successives, au contact des situations réelles. Le résultat est une chaîne qui, "
     "aujourd'hui, se déroule de bout en bout de façon fiable, reproductible et rapide, et qui se rétablit "
     "seule en cas de problème."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "La première évolution que je viserais est l'adoption du GitOps, avec un outil tel qu'ArgoCD : "
     "l'état souhaité du cluster serait décrit dans le dépôt, et un opérateur se chargerait en continu de "
     "faire converger le cluster vers cet état, offrant une traçabilité complète et des retours arrière "
     "instantanés."),
    ("P", "J'introduirais ensuite une authentification fédérée OIDC pour supprimer définitivement les secrets "
     "de longue durée, remplacés par des jetons éphémères, ce qui lèverait la contrainte actuelle d'un compte "
     "sans double authentification et renforcerait nettement la sécurité de la chaîne."),
    ("P", "Je mettrais également en place des environnements distincts — développement, pré-production et "
     "production — avec une promotion contrôlée des versions de l'un à l'autre, afin que les essais ne se "
     "déroulent plus directement sur l'unique cluster de production."),
    ("P", "Enfin, j'ajouterais des tests de bout en bout exécutés automatiquement après chaque déploiement : "
     "vérifier, avant d'ouvrir le service, que les parcours utilisateurs essentiels fonctionnent réellement "
     "constituerait un filet de sécurité supplémentaire et compléterait naturellement les tests unitaires "
     "déjà en place."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "Regrouper le provisionnement et le déploiement dans un même workflow est pratique pour la "
     "démonstration, mais allonge la durée d'exécution ; un découpage en jobs parallélisés, voire en "
     "pipelines distincts pour l'infrastructure et l'application, serait plus efficace à l'échelle et "
     "permettrait de ne rejouer que ce qui a changé."),
    ("P", "L'authentification par identifiant et mot de passe, retenue pour sa simplicité de mise en route, "
     "impose un compte sans double authentification, ce qui n'est pas acceptable dans un contexte de "
     "production et constitue la limite de sécurité la plus importante de mon périmètre."),
    ("P", "Enfin, l'absence d'environnement de pré-production fait que les essais se déroulent directement sur "
     "l'unique cluster, et un déclenchement automatique sur chaque envoi de code pourrait lancer des "
     "déploiements coûteux ; un garde-fou explicite — validation manuelle, restriction par branche ou par "
     "chemin de fichiers — mériterait d'être renforcé pour éviter toute dépense involontaire."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Configurer les secrets"),
    ("P", "Le fonctionnement de la chaîne repose sur quelques secrets à renseigner une seule fois dans les "
     "paramètres du dépôt : les identifiants de connexion à Azure, l'identifiant de l'abonnement et du "
     "tenant, et l'adresse de courriel des alertes budgétaires. Ces valeurs sont chiffrées par GitHub et "
     "utilisées par les workflows sans jamais apparaître en clair."),
    ("H2", "7.2 Lancer un déploiement"),
    ("P", "Depuis l'onglet Actions, l'utilisateur sélectionne le workflow de déploiement et l'exécute en "
     "choisissant l'action de déploiement ; la chaîne se charge de tout et affiche l'adresse d'accès à la "
     "dernière étape. Un déploiement peut aussi être déclenché automatiquement par un envoi de code sur la "
     "branche principale."),
    ("H2", "7.3 Détruire l'infrastructure"),
    ("P", "Le même workflow, exécuté avec l'action de destruction, supprime l'ensemble des ressources et "
     "arrête la facturation. L'opération est sûre et reproductible : un déploiement ultérieur reconstruit "
     "l'environnement à l'identique en une douzaine de minutes."),
    ("H2", "7.4 Sauvegarder et restaurer"),
    ("P", "Le workflow de sauvegarde s'exécute automatiquement chaque jour et peut être déclenché "
     "manuellement, en mode sauvegarde ou en mode restauration. Il gère l'export chiffré des données vers le "
     "site on-premise et leur réinjection en cas de besoin, sans qu'aucune connaissance technique "
     "particulière ne soit requise de l'utilisateur."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de transformer une succession de scripts en une chaîne réellement fiable, "
     "capable d'absorber les aléas sans intervention humaine. Chaque échec rencontré était une énigme à "
     "résoudre à la racine, ce qui a exigé rigueur, méthode et persévérance."),
    ("P", "J'ai aussi dû composer avec le caractère transversal de mon rôle : dépendant du travail de chacun, "
     "j'ai appris à coordonner mes évolutions avec celles des autres membres et à communiquer clairement sur "
     "l'état de la chaîne, afin de ne pas bloquer l'équipe."),
    ("H2", "Forces"),
    ("P", "Je retiens ma rigueur dans l'ordonnancement et l'idempotence des étapes, ainsi que ma capacité à "
     "diagnostiquer rapidement l'origine d'un échec de pipeline à partir des journaux d'exécution."),
    ("P", "J'ai également su privilégier des corrections durables plutôt que des contournements ponctuels, ce "
     "qui a durablement renforcé la fiabilité de l'ensemble et bénéficié à tout le groupe."),
    ("H2", "Faiblesses"),
    ("P", "Mes workflows sont encore trop monolithiques et gagneraient à être modularisés en briques "
     "réutilisables, ce qui en faciliterait la maintenance et la réutilisation."),
    ("P", "Par ailleurs, j'ai concentré mes efforts sur le bon fonctionnement de la chaîne, parfois au "
     "détriment de sa propre sécurisation — notamment l'authentification — que je dois encore approfondir."),
    ("H2", "Compétences développées"),
    ("P", "J'ai gagné en maîtrise sur GitHub Actions — workflows, secrets, déclencheurs, gestion de la "
     "concurrence — ainsi que sur l'automatisation de Terraform et le diagnostic des pipelines."),
    ("P", "J'ai surtout compris ce qui distingue une automatisation fragile d'une chaîne réellement "
     "industrielle : la capacité à se rétablir seule et à produire un résultat identique à chaque exécution."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Je souhaite modulariser mes pipelines à l'aide de workflows réutilisables et mettre en place une "
     "véritable stratégie multi-environnements avec promotion contrôlée des versions."),
    ("P", "Je compte également adopter le GitOps et renforcer mes compétences en sécurité de la chaîne "
     "d'approvisionnement logicielle, afin de tendre vers des pratiques de livraison continue de niveau "
     "professionnel."),
    ],
)

print("=== ZAAFIR + ELYESS générés ===")
