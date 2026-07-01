# -*- coding: utf-8 -*-
"""Contenu détaillé des rendus individuels (~10 pages chacun)."""
from content_docs import individual, CODE  # noqa

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
     "conditionnent sa mise en production. Cette double casquette a nourri l'ensemble de mes choix techniques."),

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
     "ordre (par exemple, le registre et le rôle d'accès avant le cluster qui doit tirer les images)."),
    ("P", "La gestion de l'état Terraform a fait l'objet d'une attention spécifique : plutôt qu'un état local "
     "fragile, nous avons opté pour un état distant stocké dans un compte de stockage Azure, ce qui permet le "
     "travail à plusieurs et évite les conflits. J'ai conçu la configuration de sorte que ce stockage soit "
     "créé automatiquement s'il n'existe pas, supprimant toute étape préalable manuelle."),

    ("H2", "2.2 Développement de l'application"),
    ("P", "J'ai développé le cœur applicatif avec le framework FastAPI, en Python. L'API expose les "
     "ressources métier du cabinet : les patients, les appareils auditifs qui leur sont associés et les "
     "rendez-vous de suivi. J'ai structuré le code en couches claires — modèles de données, schémas de "
     "validation, logique d'accès aux données et routes HTTP — afin qu'il reste lisible et maintenable. La "
     "validation des entrées est confiée à Pydantic, ce qui garantit qu'aucune donnée mal formée n'atteint la "
     "base."),
    ("P", "J'ai doté l'API de <b>sondes de santé</b> distinctes : une sonde de vivacité qui confirme que le "
     "service répond, et une sonde de disponibilité qui vérifie en outre que la base de données est joignable. "
     "Cette distinction est essentielle pour Kubernetes, qui s'appuie sur ces sondes pour décider de "
     "redémarrer un conteneur ou de lui envoyer du trafic. J'ai également exposé un point de terminaison de "
     "métriques, consommé par la supervision mise en place par un autre membre de l'équipe."),
    ("P", "Côté interface, j'ai réalisé un frontend React servi par un serveur nginx, permettant au cabinet "
     "de consulter et de gérer ses patients de façon simple. L'interface consomme l'API via un chemin unique, "
     "ce qui simplifie le routage en production où frontend et backend sont exposés derrière le même point "
     "d'entrée."),

    ("H2", "2.3 Conteneurisation et déploiement"),
    ("P", "J'ai conteneurisé les deux composants au moyen d'images Docker construites en plusieurs étapes "
     "(multi-stage), afin de séparer la phase de compilation de l'image finale et d'obtenir des images "
     "légères. Ces images s'exécutent avec un utilisateur non privilégié, conformément aux bonnes pratiques "
     "de sécurité, un point sur lequel j'ai collaboré avec le responsable sécurité de l'équipe."),
    ("P", "Le déploiement sur le cluster s'appuie sur le chart Helm conçu avec le responsable Kubernetes : "
     "j'ai veillé à ce que l'application reçoive sa configuration (notamment la chaîne de connexion à la base) "
     "par l'intermédiaire d'un secret Kubernetes injecté au moment du déploiement, et jamais écrit en clair "
     "dans le dépôt. J'ai enfin coordonné l'enchaînement complet du déploiement de bout en bout et vérifié, "
     "après chaque livraison, le bon fonctionnement de l'application, de la base et de l'interface."),

    ("H1", "3. Choix techniques et justifications"),
    ("P", "Le choix de FastAPI s'explique par sa rapidité de mise en œuvre, sa documentation automatique de "
     "l'API et sa robustesse grâce à la validation typée, autant d'atouts pour un projet à durée contrainte. "
     "PostgreSQL s'est imposé comme base relationnelle éprouvée, disponible en version managée sur Azure, ce "
     "qui nous décharge de son exploitation (sauvegardes, correctifs) tout en restant peu coûteux au palier "
     "le plus bas."),
    ("P", "Concernant l'hébergement de la base, nous avons retenu un accès public restreint par un pare-feu "
     "n'autorisant que les ressources internes à Azure, avec chiffrement TLS obligatoire. C'est un compromis "
     "assumé : un réseau entièrement privé aurait été plus sûr, mais aurait ajouté une complexité (réseau "
     "virtuel dédié, résolution DNS privée) difficilement justifiable pour un MVP au budget serré. J'ai "
     "documenté ce compromis pour qu'il soit clairement identifié comme un axe d'amélioration."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "La principale difficulté a été d'<b>industrialiser le provisionnement</b> pour qu'il soit "
     "réellement rejouable par la chaîne d'intégration. Les premières exécutions ont révélé des situations "
     "délicates : un déploiement interrompu laissait l'état Terraform verrouillé, empêchant toute reprise. "
     "En collaboration avec le responsable CI/CD, nous avons ajouté un mécanisme libérant automatiquement ce "
     "verrou résiduel avant chaque application, rendant la chaîne robuste."),
    ("P", "Une seconde difficulté a concerné la cohérence entre la version de l'application déployée et la "
     "configuration attendue : j'ai résolu ce point en faisant en sorte que chaque déploiement utilise une "
     "étiquette d'image unique, ce qui force le remplacement propre des conteneurs et garantit que la "
     "nouvelle configuration est bien prise en compte. Enfin, un souci subtil de compatibilité entre le "
     "format du mot de passe de la base et l'outil de sauvegarde m'a conduit à générer un mot de passe "
     "strictement alphanumérique, éliminant toute une classe d'erreurs d'interprétation d'URL."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "À court terme, je remplacerais l'authentification de la chaîne d'intégration par une fédération "
     "d'identité OIDC entre GitHub et Azure. Ce mécanisme supprime tout mot de passe stocké au profit de "
     "jetons éphémères, ce qui constitue l'état de l'art et lèverait la contrainte actuelle d'un compte sans "
     "double authentification."),
    ("P", "Je ferais également évoluer la base vers un accès strictement privé, sans exposition publique, en "
     "plaçant l'application et la base dans un réseau virtuel commun avec des points de terminaison privés. "
     "Cette évolution renforcerait significativement l'isolation des données de santé, conformément aux "
     "attentes d'un véritable contexte de production."),
    ("P", "À plus long terme, si le périmètre fonctionnel s'élargissait (facturation, tiers payant, "
     "notifications), l'API monolithique pourrait être découpée en services plus fins et indépendamment "
     "déployables. J'introduirais aussi un outil de migrations de schéma versionnées, mieux adapté qu'une "
     "création au démarrage pour faire évoluer la base sans risque en production."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "La limite la plus notable de mon périmètre tient au compromis réseau évoqué plus haut : l'accès "
     "public restreint reste moins satisfaisant qu'une isolation complète. De même, la création du schéma au "
     "démarrage de l'application est pratique pour un MVP mais inadaptée à une exploitation durable, où toute "
     "modification de structure doit être maîtrisée et réversible."),
    ("P", "Sur le plan des performances, le choix de machines burstable plafonne la capacité sous une charge "
     "soutenue et prolongée ; ce dimensionnement, pertinent pour une démonstration, devrait être réévalué "
     "pour un usage réel du cabinet. Enfin, la couverture de tests automatisés de l'application, bien que "
     "présente, gagnerait à être étendue aux scénarios d'erreur et aux cas limites."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Déployer l'environnement"),
    ("P", "Le déploiement se résume, pour l'utilisateur, à trois étapes. D'abord, renseigner les identifiants "
     "Azure dans les secrets du dépôt (identifiant, mot de passe, tenant, abonnement). Ensuite, lancer le "
     "workflow de déploiement depuis l'onglet Actions, ou pousser du code sur la branche principale. Enfin, "
     "récupérer l'adresse d'accès affichée à la fin de l'exécution. L'infrastructure complète est alors "
     "provisionnée puis l'application déployée, sans autre intervention."),
    ("H2", "7.2 Utiliser l'application"),
    ("P", "L'application est accessible à l'adresse publique de l'Ingress. L'interface web permet de créer, "
     "consulter et supprimer des patients ; la documentation interactive de l'API, utile pour les tests ou "
     "l'intégration, est publiée sous le chemin « /api/docs ». Les sondes « /healthz » et « /readyz » "
     "permettent de vérifier rapidement, en ligne de commande, que le service et sa base répondent."),
    ("H2", "7.3 Reconstruire ou détruire"),
    ("P", "L'ensemble de l'infrastructure peut être reconstruit à l'identique par une seule commande, ou "
     "détruit en choisissant l'action de destruction du workflow — ce qui stoppe toute facturation. Cette "
     "reproductibilité est la garantie que le projet est duplicable et réutilisable, comme l'exige le cahier "
     "des charges."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de passer d'une logique de « code qui fonctionne sur ma machine » à une "
     "logique d'infrastructure et de déploiement entièrement automatisés et reproductibles. Cela m'a demandé "
     "de raisonner en permanence sur les cas d'échec et les états intermédiaires, et d'accepter plusieurs "
     "itérations avant d'obtenir une chaîne réellement fiable."),
    ("H2", "Forces"),
    ("P", "Je retiens comme force ma capacité à avoir une vision d'ensemble reliant le développement "
     "applicatif et son hébergement, ce qui m'a permis de concevoir une application pensée dès le départ pour "
     "être déployée et exploitée. J'ai également su collaborer étroitement avec les responsables CI/CD et "
     "Kubernetes pour résoudre des problèmes situés à la frontière de nos périmètres."),
    ("H2", "Faiblesses"),
    ("P", "J'ai parfois eu tendance à vouloir déployer l'ensemble en une seule fois plutôt qu'à valider par "
     "petits incréments testés, ce qui a occasionné des allers-retours. Par ailleurs, mes compétences en "
     "sécurité réseau cloud, sollicitées par le choix d'hébergement de la base, restent à approfondir."),
    ("H2", "Compétences développées"),
    ("P", "Ce projet m'a permis de consolider ma maîtrise de Terraform et de la conception d'infrastructure "
     "Azure, de la conteneurisation Docker et du déploiement via Helm, ainsi que du développement d'une API "
     "moderne intégrée à une base de données. J'ai surtout acquis une compréhension concrète de "
     "l'articulation entre code, infrastructure et exploitation."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Pour de futurs projets, je souhaite adopter une approche plus incrémentale et systématiquement "
     "testée des changements d'infrastructure, et renforcer mes connaissances en réseau cloud (réseaux "
     "virtuels, points de terminaison privés, pare-feux applicatifs) afin de concevoir des architectures "
     "plus sûres dès la première version."),
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
     "continus. L'objectif fixé collectivement était ambitieux : obtenir un déploiement « en un clic », où "
     "l'intégralité du cycle de vie — provisionnement de l'infrastructure, construction et analyse des "
     "images, déploiement de l'application, configuration du stockage de sauvegarde — s'exécute "
     "automatiquement, sans aucune intervention manuelle, et se rétablit seul en cas d'aléa."),
    ("P", "Ce rôle est transversal par nature : la chaîne que j'ai construite orchestre le travail de tous les "
     "autres membres, en assemblant l'infrastructure de Zaafir, le chart de déploiement d'Anis, la "
     "supervision et les scans de sécurité d'Adame. J'ai donc dû comprendre chaque brique pour l'intégrer au "
     "bon moment et dans le bon ordre au sein du pipeline."),

    ("H1", "2. Ma contribution détaillée"),
    ("H2", "2.1 Architecture de la chaîne GitHub Actions"),
    ("P", "J'ai conçu plusieurs workflows complémentaires. Le workflow d'intégration valide chaque "
     "modification par l'analyse statique du code et l'exécution des tests, côté backend comme côté frontend. "
     "Le workflow de sécurité exécute les analyses de vulnérabilités. Le workflow de déploiement orchestre "
     "l'ensemble de la mise en production. Enfin, un workflow de sauvegarde, planifié quotidiennement, "
     "déclenche la réplication des données vers le site on-premise."),
    ("P", "Cette séparation en workflows spécialisés répond à un souci de clarté et d'efficacité : les "
     "vérifications rapides (tests, analyses) s'exécutent à chaque proposition de modification, tandis que les "
     "opérations lourdes et coûteuses (provisionnement, déploiement) ne sont déclenchées que de manière "
     "maîtrisée, sur la branche principale ou manuellement."),

    ("H2", "2.2 Automatisation du provisionnement et de l'état"),
    ("P", "J'ai automatisé la préparation de l'état distant de Terraform : le workflow crée si nécessaire le "
     "compte de stockage dédié, puis initialise Terraform sur cet état avant d'appliquer l'infrastructure. "
     "Cette étape, souvent laissée manuelle dans les projets, a été entièrement scriptée pour que rien ne "
     "doive être préparé à l'avance."),
    ("P", "L'authentification à Azure au sein de la chaîne s'appuie sur des identifiants stockés dans les "
     "secrets chiffrés de GitHub, jamais exposés dans les journaux. J'ai veillé à masquer explicitement les "
     "valeurs sensibles (chaînes de connexion, mots de passe) dans les traces d'exécution, afin qu'elles "
     "n'apparaissent jamais en clair, même en cas de débogage."),

    ("H2", "2.3 Orchestration et ordonnancement des étapes"),
    ("P", "Le déploiement complet enchaîne, dans un ordre précis, la connexion à Azure, l'application "
     "Terraform, la récupération des informations produites (adresses, identifiants), la construction et la "
     "publication des images, leur analyse de sécurité, l'installation des briques du cluster puis le "
     "déploiement de l'application et la configuration du site on-premise. J'ai dû gérer finement les "
     "dépendances : par exemple, m'assurer que les définitions de ressources nécessaires à la supervision "
     "sont installées <b>avant</b> l'application qui les référence, sous peine d'échec."),
    ("P", "J'ai également optimisé les temps d'exécution en supprimant des attentes bloquantes inutiles : "
     "plutôt que d'attendre que chaque composant de supervision soit totalement prêt, la chaîne applique les "
     "manifestes et laisse les composants converger en arrière-plan, ce qui a réduit la durée du déploiement "
     "de façon significative."),

    ("H2", "2.4 Fiabilisation et auto-réparation"),
    ("P", "La partie la plus exigeante de mon travail a consisté à rendre le pipeline robuste face aux états "
     "intermédiaires. Un déploiement interrompu pouvait laisser un verrou sur l'état de l'infrastructure, ou "
     "une livraison Helm figée dans un état instable empêchant toute reprise. J'ai introduit des mécanismes "
     "qui détectent ces situations et les corrigent automatiquement : libération du verrou résiduel, "
     "nettoyage d'une livraison bloquée avant réinstallation."),
    ("P", "Grâce à ces garde-fous, la chaîne est devenue <b>auto-réparante</b> : elle se remet d'elle-même "
     "d'un incident sans qu'un opérateur ait à intervenir sur l'infrastructure, ce qui est une propriété "
     "essentielle pour une exploitation sereine et conforme à l'esprit DevOps."),

    ("H1", "3. Choix techniques et justifications"),
    ("P", "Le cahier des charges évoquait GitLab CI ; nous avons retenu GitHub Actions, le dépôt étant "
     "hébergé sur GitHub. Le principe reste identique — build, test, analyse, déploiement orchestré — et "
     "GitHub Actions offre une intégration native avec le dépôt, un large catalogue d'actions réutilisables "
     "et une gestion des secrets intégrée. Ce choix a donc été pragmatique et sans perte fonctionnelle."),
    ("P", "J'ai privilégié un déploiement piloté par la chaîne (approche « push ») plutôt qu'un outil de "
     "déploiement continu dédié, afin de rester simple et économe pour un MVP. Cette décision est réversible : "
     "j'ai identifié le passage à une approche déclarative de type GitOps comme évolution naturelle une fois "
     "le projet stabilisé."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "J'ai été confronté à une série d'échecs typiques d'une première mise en production : une action "
     "dont la version n'existait pas, un conflit de création de ressource déjà existante, un verrou d'état "
     "résiduel, une livraison bloquée, un mauvais ordonnancement des dépendances. Plutôt que de les contourner "
     "au cas par cas, j'ai traité chaque incident à la racine, en ajoutant le correctif durable "
     "correspondant dans le pipeline."),
    ("P", "Cette approche m'a beaucoup appris : un pipeline robuste ne se conçoit pas d'un seul jet, il se "
     "durcit par itérations successives face aux situations réelles. Le résultat est une chaîne qui, "
     "aujourd'hui, se déroule de bout en bout de façon fiable et reproductible."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "La première évolution que je viserais est l'adoption du GitOps, avec un outil tel qu'ArgoCD : "
     "l'état souhaité du cluster serait décrit dans le dépôt et un opérateur se chargerait de faire "
     "converger le cluster vers cet état, offrant traçabilité et retours arrière simplifiés."),
    ("P", "J'introduirais ensuite une authentification fédérée OIDC pour supprimer les secrets de longue "
     "durée, ainsi que des environnements distincts — développement, pré-production, production — avec une "
     "promotion contrôlée des versions. Enfin, j'ajouterais des tests de bout en bout exécutés "
     "automatiquement après chaque déploiement, afin de valider le bon fonctionnement de l'ensemble avant "
     "d'ouvrir le service aux utilisateurs."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "Regrouper le provisionnement et le déploiement dans un même workflow est pratique pour la "
     "démonstration, mais allonge la durée d'exécution ; un découpage en jobs parallélisés, voire en pipelines "
     "distincts pour l'infrastructure et l'application, serait plus efficace à l'échelle. L'authentification "
     "par identifiant et mot de passe, quant à elle, impose un compte sans double authentification, ce qui "
     "n'est pas acceptable en production."),
    ("P", "Par ailleurs, l'absence d'environnement de pré-production fait que les essais se déroulent "
     "directement sur l'unique cluster, et un déclenchement automatique sur chaque envoi de code pourrait "
     "lancer des déploiements coûteux : un garde-fou explicite (validation manuelle, restriction de branche) "
     "mériterait d'être renforcé."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Lancer un déploiement"),
    ("P", "Depuis l'onglet Actions du dépôt, l'utilisateur sélectionne le workflow de déploiement et "
     "l'exécute en choisissant l'action de déploiement. La chaîne se charge de tout ; l'adresse d'accès à "
     "l'application est affichée à la dernière étape. Un déploiement peut aussi être déclenché automatiquement "
     "par un envoi de code sur la branche principale."),
    ("H2", "7.2 Détruire l'infrastructure"),
    ("P", "Le même workflow, exécuté avec l'action de destruction, supprime l'ensemble des ressources et "
     "arrête la facturation. L'opération est sûre et reproductible : un déploiement ultérieur reconstruit "
     "l'environnement à l'identique."),
    ("H2", "7.3 Sauvegarder et restaurer"),
    ("P", "Le workflow de sauvegarde s'exécute automatiquement chaque jour, et peut être déclenché "
     "manuellement en mode sauvegarde ou restauration. Les secrets nécessaires à ces workflows sont décrits "
     "dans la documentation d'installation du dépôt."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de transformer une succession de scripts en une chaîne réellement fiable, "
     "capable d'absorber les aléas sans intervention humaine. Chaque échec rencontré était une énigme à "
     "résoudre à la racine, ce qui a demandé rigueur et persévérance."),
    ("H2", "Forces"),
    ("P", "Je retiens ma rigueur dans l'ordonnancement et l'idempotence des étapes, ainsi que ma capacité à "
     "diagnostiquer rapidement l'origine d'un échec de pipeline à partir des journaux d'exécution et à y "
     "apporter un correctif durable plutôt qu'un contournement ponctuel."),
    ("H2", "Faiblesses"),
    ("P", "Mes workflows sont encore trop monolithiques et gagneraient à être modularisés en briques "
     "réutilisables. Par ailleurs, j'ai concentré mes efforts sur le fonctionnement au détriment, parfois, "
     "de la sécurisation de la chaîne elle-même (authentification), que je dois approfondir."),
    ("H2", "Compétences développées"),
    ("P", "J'ai gagné en maîtrise sur GitHub Actions (workflows, secrets, déclencheurs, gestion de la "
     "concurrence), sur l'automatisation de Terraform et sur le diagnostic et la résilience des pipelines. "
     "J'ai surtout compris ce qui distingue une automatisation fragile d'une chaîne réellement industrielle."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Je souhaite modulariser mes pipelines à l'aide de workflows réutilisables, mettre en place une "
     "véritable stratégie multi-environnements et adopter le GitOps, afin de tendre vers des pratiques de "
     "livraison continue de niveau professionnel."),
    ],
)

print("=== ZAAFIR + ELYESS générés ===")
