# -*- coding: utf-8 -*-
"""Rendus individuels détaillés — Adame & Anis (~10-13 pages)."""
from content_docs import individual, CODE, wrap_table  # noqa
from generate_docs import (obs_diagram, helm_diagram, flow_horizontal, fan_out,  # noqa
                           network_topology, Spacer, CONTENT_W, cm, BLUE)  # noqa

# ============================================================ ADAME
individual(
    "PE-2526_%s_NianghaneAdame.pdf" % CODE,
    "Adame Nianghane", "Observabilité & sécurité",
    "Supervision (Prometheus/Grafana/Loki), DevSecOps, durcissement",
    [
    ("H1", "1. Contexte et rôle dans le projet"),
    ("P", "J'ai pris en charge deux volets complémentaires qui déterminent la confiance que l'on peut "
     "accorder à un système en production : l'<b>observabilité</b>, c'est-à-dire la capacité à comprendre ce "
     "que fait la plateforme à tout instant, et la <b>sécurité</b>, tant celle de la chaîne logicielle que "
     "celle de l'exécution. Ces deux sujets partagent une même philosophie : anticiper les problèmes plutôt "
     "que les subir, en rendant le système transparent et en le durcissant à chaque étape."),
    ("P", "Ce positionnement m'a conduit à intervenir sur l'ensemble du périmètre : j'ai instrumenté "
     "l'application développée par Zaafir, intégré mes analyses de sécurité dans la chaîne d'Elyess, et "
     "sécurisé les objets Kubernetes packagés par Anis. L'observabilité et la sécurité sont en effet des "
     "préoccupations transverses, qui ne peuvent être traitées en silo mais doivent irriguer tout le projet."),
    ("P", "Dans un contexte de données de santé, ces deux volets prennent une importance particulière : la "
     "supervision garantit la disponibilité attendue d'un service de soin, tandis que la sécurité protège des "
     "informations sensibles et contribue au respect du cadre réglementaire. Mon travail visait donc autant "
     "la performance opérationnelle que la conformité."),

    ("H1", "2. Ma contribution détaillée"),
    ("H2", "2.1 Collecte des métriques (Prometheus)"),
    ("P", "J'ai déployé Prometheus, qui collecte périodiquement les métriques exposées par les différents "
     "composants. L'application publie ses propres indicateurs — nombre de requêtes, latence, code de "
     "réponse — que j'ai fait découvrir automatiquement par Prometheus grâce à un objet de configuration "
     "dédié. Ainsi, dès qu'une nouvelle instance de l'application démarre, elle est automatiquement prise en "
     "compte par la supervision, sans configuration manuelle."),
    ("P", "J'ai veillé à limiter la cardinalité des métriques, c'est-à-dire à éviter une explosion du nombre "
     "de séries temporelles, en agrégeant les mesures par route plutôt que par requête individuelle. Ce souci "
     "rejoint directement la démarche FinOps de l'équipe, car une supervision mal maîtrisée peut consommer "
     "énormément de mémoire et de stockage, au point de coûter plus cher que l'application elle-même."),

    ("H2", "2.2 Visualisation (Grafana) et tableaux de bord"),
    ("P", "J'ai déployé Grafana et conçu un tableau de bord dédié à l'application, présentant les indicateurs "
     "clés : le débit de requêtes par route, la latence au 95e centile, le taux d'erreurs serveur et la "
     "disponibilité du backend. Ces quatre indicateurs correspondent aux « signaux dorés » de la supervision "
     "d'un service, reconnus comme les plus révélateurs de son état de santé."),
    ("P", "J'ai automatisé l'import de ce tableau de bord afin qu'il soit présent dès l'installation, sans "
     "aucune manipulation. J'ai également exposé Grafana de façon accessible via l'Ingress existant, en "
     "réutilisant l'adresse publique du cluster grâce à un nom d'hôte dynamique — un choix qui évite de "
     "provisionner une seconde adresse IP publique et participe donc concrètement à la maîtrise des coûts, "
     "illustrant que sécurité, observabilité et FinOps se pensent ensemble."),

    ("H2", "2.3 Centralisation des journaux (Loki)"),
    ("P", "Pour les journaux, j'ai déployé Loki accompagné de son agent de collecte, qui récupère les traces "
     "de tous les composants et les rend consultables et corrélables depuis Grafana, au même endroit que les "
     "métriques. L'application produit des journaux structurés, ce qui facilite leur exploitation et leur "
     "filtrage."),
    ("P", "Le choix de Loki plutôt qu'une pile Elasticsearch a été motivé, en accord avec l'équipe, par son "
     "empreinte réduite : là où Elasticsearch indexe l'intégralité du contenu et réclame plusieurs "
     "gigaoctets de mémoire, Loki n'indexe que les étiquettes et se contente de ressources modestes, pour un "
     "usage — centralisation, recherche, visualisation — équivalent dans notre contexte. Ce choix a été "
     "déterminant pour tenir dans le budget."),

    ("H2", "2.4 Alerting (Alertmanager)"),
    ("P", "J'ai défini des règles d'alerte qui se déclenchent lorsque le service devient indisponible, "
     "lorsque le taux d'erreurs dépasse un seuil ou lorsque la latence se dégrade durablement. Ces alertes "
     "sont routées par Alertmanager vers une messagerie d'équipe (Slack ou Teams) au moyen d'un point "
     "d'entrée dédié. L'objectif est de prévenir l'équipe d'un incident avant même que les utilisateurs ne "
     "s'en aperçoivent, ce qui transforme une supervision passive en un dispositif réellement proactif."),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", obs_diagram()),
    ("P", "<i>Chaîne d'observabilité : l'application émet métriques et journaux, collectés par Prometheus et "
     "Loki, visualisés dans Grafana ; les alertes sont routées par Alertmanager vers la messagerie de "
     "l'équipe.</i>"),

    ("H2", "2.5 Sécurité de la chaîne (DevSecOps)"),
    ("P", "J'ai intégré dans la chaîne d'intégration trois analyses complémentaires. Trivy examine les "
     "dépendances, les fichiers d'infrastructure et les images à la recherche de vulnérabilités connues, et "
     "bloque le déploiement en cas de faille critique. CodeQL réalise une analyse statique du code source "
     "pour détecter des schémas potentiellement dangereux. Gitleaks recherche toute fuite de secret dans "
     "l'historique du dépôt. Les résultats sont publiés dans l'onglet de sécurité du dépôt, au format "
     "standard SARIF, ce qui permet un suivi structuré."),
    ("P", "Le fait d'exécuter ces analyses à chaque livraison, et non ponctuellement, matérialise le principe "
     "du « décalage vers la gauche » (<i>shift-left</i>) : les problèmes de sécurité sont détectés au plus "
     "tôt, quand ils sont les moins coûteux à corriger, plutôt qu'une fois le système en production. Les "
     "trois contrôles s'insèrent comme autant de barrières successives sur le trajet du code vers la "
     "production :"),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", flow_horizontal([["Commit", "développeur"], ["Gitleaks", "fuite de secrets"],
                              ["CodeQL", "analyse du code"], ["Trivy", "images & deps"],
                              ["Déploiement", "si tout est vert"]], color=BLUE)),
    ("FLOW", Spacer(1, 4)),
    ("P", "<i>Portes de sécurité successives : un secret exposé, une faille de code ou une vulnérabilité "
     "critique d'image bloque la chaîne avant toute mise en production.</i>"),

    ("H2", "2.6 Durcissement de l'exécution"),
    ("P", "Au-delà des analyses, j'ai durci l'exécution des conteneurs : ils s'exécutent sans privilèges et "
     "sans possibilité d'élévation, les capacités système superflues sont retirées, et l'accès à l'API du "
     "cluster est régi par des rôles restreints selon le principe du moindre privilège. Les communications "
     "avec la base sont chiffrées en TLS, et les secrets ne sont jamais écrits dans le dépôt : ils transitent "
     "chiffrés et sont injectés dans les conteneurs au dernier moment."),
    ("P", "J'ai également préparé des politiques de cloisonnement réseau limitant les communications entre "
     "composants au strict nécessaire, de sorte qu'une éventuelle compromission d'un pod ne puisse pas se "
     "propager librement dans le cluster. Ces politiques constituent une défense en profondeur, complémentaire "
     "des autres mesures."),

    ("H1", "3. Choix technologiques : pourquoi ces technologies plutôt que d'autres"),
    ("P", "Mon périmètre reposait sur deux familles d'outils : la pile d'observabilité et les analyseurs de "
     "sécurité. Chacune a été choisie après comparaison explicite avec ses alternatives, en pesant "
     "systématiquement le service rendu contre l'empreinte en ressources — un critère décisif compte tenu du "
     "budget."),

    ("H2", "3.1 Journalisation : Loki plutôt qu'Elasticsearch (pile ELK)"),
    ("FLOW", wrap_table([
        ["Critère", "Loki (retenu)", "Elasticsearch / ELK"],
        ["Indexation", "Étiquettes seulement", "Contenu intégral des logs"],
        ["Mémoire requise", "Modeste (quelques centaines de Mo)", "Plusieurs Go de RAM"],
        ["Stockage", "Compressé, peu volumineux", "Index volumineux"],
        ["Intégration Grafana", "Native, source de données directe", "Via Kibana (interface séparée)"],
        ["Adéquation au budget", "Excellente", "Nécessiterait des nœuds plus gros"],
    ], [3.4 * cm, 6.2 * cm, CONTENT_W - 9.6 * cm])),
    ("P", "J'ai retenu <b>Loki</b> plutôt qu'une pile Elasticsearch parce qu'il n'indexe que les étiquettes "
     "des journaux, là où Elasticsearch indexe l'intégralité du contenu et réclame plusieurs gigaoctets de "
     "mémoire. Pour un usage identique dans notre contexte — centralisation, recherche, visualisation dans "
     "Grafana — Loki offre une empreinte très inférieure, ce qui a été déterminant pour tenir sur des nœuds "
     "modestes. Elasticsearch aurait imposé des machines plus puissantes et donc bien plus coûteuses, sans "
     "bénéfice tangible à notre échelle."),

    ("H2", "3.2 Métriques : Prometheus plutôt qu'Azure Monitor"),
    ("FLOW", wrap_table([
        ["Critère", "Prometheus (retenu)", "Azure Monitor"],
        ["Modèle", "Open source, standard cloud-native", "Service managé propriétaire"],
        ["Coût", "Gratuit (auto-hébergé)", "Facturé à l'ingestion / rétention"],
        ["Portabilité", "Indépendant du cloud", "Lié à Azure"],
        ["Découverte des cibles", "Automatique (ServiceMonitor)", "Agents / configuration Azure"],
        ["Intégration Grafana", "Native", "Possible mais moins directe"],
    ], [3.4 * cm, 5.6 * cm, CONTENT_W - 9.0 * cm])),
    ("P", "<b>Prometheus</b> s'est imposé comme le standard open source de la métrologie cloud-native, avec "
     "une découverte automatique des cibles et une intégration native à Grafana. Azure Monitor, bien "
     "qu'intégré à la plateforme, facture l'ingestion et la rétention des données et enferme la supervision "
     "dans l'écosystème Azure ; Prometheus est gratuit, portable et parfaitement adapté à Kubernetes. Le "
     "triptyque Prometheus / Grafana / Loki forme ainsi un ensemble cohérent où l'exploitant corrèle en un "
     "seul endroit courbes et journaux."),

    ("H2", "3.3 Analyse de sécurité : Trivy, CodeQL et Gitleaks plutôt que des alternatives"),
    ("FLOW", wrap_table([
        ["Besoin", "Outil retenu", "Alternative écartée", "Raison du choix"],
        ["Images & dépendances", "Trivy", "Clair, Snyk", "Gratuit, rapide, couvre IaC + images"],
        ["Analyse du code", "CodeQL", "SonarQube", "Intégré à GitHub, sans serveur"],
        ["Fuite de secrets", "Gitleaks", "TruffleHog", "Léger, simple à intégrer en CI"],
    ], [3.4 * cm, 2.8 * cm, 3.2 * cm, CONTENT_W - 9.4 * cm])),
    ("P", "Pour la sécurité, j'ai retenu des outils gratuits, largement adoptés et complémentaires : "
     "<b>Trivy</b> pour les dépendances, les fichiers d'infrastructure et les images, <b>CodeQL</b> pour le "
     "code et <b>Gitleaks</b> pour les secrets. Snyk et SonarQube, plus riches, imposent respectivement un "
     "abonnement et un serveur à héberger ; Clair est plus limité que Trivy sur l'infrastructure as code. "
     "Cette combinaison couvre l'essentiel de la surface d'exposition sans coût de licence ni serveur "
     "supplémentaire, ce qui était impératif dans notre cadre. Intégrer ces contrôles directement dans la "
     "chaîne, plutôt que de les laisser à la discrétion de chacun, garantit enfin que la sécurité devient une "
     "propriété systématiquement vérifiée."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "La principale difficulté a été de faire tenir une pile de supervision complète sur un cluster "
     "volontairement réduit pour des raisons budgétaires. J'ai dû dimensionner soigneusement les ressources "
     "allouées à chaque composant — Prometheus, Grafana, Loki, Alertmanager — et accepter des durées de "
     "rétention courtes, afin que la supervision n'entre pas en concurrence avec l'application pour les "
     "ressources limitées du cluster."),
    ("P", "Une autre difficulté a concerné la découverte automatique des métriques de l'application. Il a "
     "fallu s'assurer que Prometheus sélectionne bien l'objet de configuration produit par le déploiement, "
     "ce qui supposait un bon ordonnancement de l'installation : les définitions de ressources nécessaires "
     "devaient précéder l'application. Ce point, situé à la frontière avec le périmètre d'Elyess, a été résolu "
     "en réorganisant l'ordre des étapes de la chaîne."),
    ("P", "Enfin, exposer Grafana sans provisionner de ressource réseau supplémentaire a demandé de "
     "réutiliser l'Ingress existant avec un nom d'hôte dynamique : une solution élégante, mais qu'il a fallu "
     "mettre au point après avoir constaté qu'une exposition directe consommait une adresse IP publique "
     "supplémentaire, contraire à notre objectif de sobriété."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "Je souhaiterais ajouter le <b>traçage distribué</b>, au moyen d'OpenTelemetry et d'un outil comme "
     "Tempo ou Jaeger, afin de suivre une requête à travers les composants et de diagnostiquer finement les "
     "lenteurs. Ce troisième pilier de l'observabilité, complémentaire des métriques et des journaux, "
     "deviendrait particulièrement utile si l'application se complexifiait ou se découpait en services."),
    ("P", "Je centraliserais également la gestion des secrets dans un coffre dédié offrant une rotation "
     "automatique des identifiants, ce qui réduirait la fenêtre d'exposition en cas de fuite et allégerait "
     "leur gestion manuelle."),
    ("P", "Je renforcerais par ailleurs la posture de sécurité du cluster par des politiques avancées : "
     "standards de sécurité des pods, contrôleur d'admission validant automatiquement chaque manifeste, et "
     "signature des images pour garantir leur provenance et empêcher le déploiement d'artefacts non vérifiés."),
    ("P", "Enfin, je définirais des objectifs de niveau de service (SLO) assortis d'un suivi de leur "
     "consommation, afin de piloter la fiabilité de manière quantifiée et d'objectiver les priorités "
     "d'amélioration."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "Le routage des alertes vers une messagerie nécessite un point d'entrée externe qui n'a pas été "
     "connecté en production dans le cadre du projet : le mécanisme est en place et fonctionnel, mais sa "
     "validation de bout en bout, jusqu'à la réception effective d'une notification, reste à finaliser."),
    ("P", "De même, les politiques de cloisonnement réseau que j'ai préparées supposent un module réseau "
     "capable de les appliquer, que nous n'avons pas activé sur le cluster d'étude afin de rester légers et "
     "économes : elles sont donc fournies et prêtes, mais non strictement appliquées dans la configuration "
     "actuelle, ce qui constitue un écart assumé entre la conception et l'exécution."),
    ("P", "Enfin, une véritable conformité à l'hébergement de données de santé imposerait une région et des "
     "services certifiés que nous n'avons pas retenus dans ce cadre, et la rétention volontairement courte "
     "des métriques et des journaux limite l'analyse rétrospective des incidents les plus anciens."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Consulter la supervision"),
    ("P", "L'utilisateur accède à Grafana via son adresse dédiée, avec les identifiants fournis. Le tableau "
     "de bord « Vue d'ensemble » est disponible immédiatement et présente l'état de santé de l'application. "
     "Pour observer l'évolution des courbes, il suffit de générer un peu de trafic sur l'API : le débit, la "
     "latence et le taux d'erreurs se mettent alors à jour en temps quasi réel."),
    ("H2", "7.2 Explorer les journaux"),
    ("P", "Depuis Grafana, la vue d'exploration permet d'interroger la source de données Loki et de filtrer "
     "les journaux par composant ou par période, ce qui est précieux pour diagnostiquer un comportement "
     "anormal et remonter à sa cause sans se connecter directement aux conteneurs."),
    ("H2", "7.3 Consulter les rapports de sécurité"),
    ("P", "Les résultats des analyses de sécurité sont consultables dans l'onglet « Security » du dépôt, où "
     "chaque vulnérabilité détectée est listée avec sa gravité et sa localisation. Cette présentation permet "
     "de suivre l'évolution de la posture de sécurité dans le temps et de prioriser les corrections selon "
     "leur criticité."),
    ("H2", "7.4 Réagir à une alerte"),
    ("P", "Lorsqu'une règle se déclenche, une notification est émise vers la messagerie de l'équipe. La marche "
     "à suivre consiste alors à ouvrir le tableau de bord correspondant pour qualifier l'incident, puis à "
     "consulter les journaux associés afin d'en identifier l'origine avant d'engager la correction."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de concilier une observabilité riche et une sécurité exigeante avec la "
     "contrainte de sobriété du projet. Il m'a fallu arbitrer en permanence entre l'exhaustivité souhaitable "
     "et ce que le cluster pouvait raisonnablement supporter, sans jamais sacrifier l'essentiel."),
    ("P", "J'ai aussi dû dialoguer étroitement avec les autres membres, car la sécurité et la supervision "
     "touchent à tout : instrumenter l'application, ordonner la chaîne, sécuriser les objets Kubernetes "
     "supposaient un travail concerté plutôt qu'isolé."),
    ("H2", "Forces"),
    ("P", "Je retiens mon sens du détail sur les questions de sécurité et de conformité, ainsi que ma "
     "capacité à rendre un système transparent et compréhensible pour l'ensemble de l'équipe."),
    ("P", "J'ai également su intégrer la dimension économique dans mes choix, en préférant systématiquement "
     "les solutions les plus sobres à service équivalent, ce qui a contribué à l'équilibre budgétaire global."),
    ("H2", "Faiblesses"),
    ("P", "Je dois concrétiser jusqu'au bout certaines mises en œuvre que j'ai préparées mais pas totalement "
     "activées, comme le routage effectif des alertes ou l'application stricte des politiques réseau."),
    ("P", "J'ai parfois privilégié la mise en place d'un dispositif sur sa validation finale, ce qui laisse "
     "quelques maillons à éprouver de bout en bout avant de les considérer comme pleinement opérationnels."),
    ("H2", "Compétences développées"),
    ("P", "J'ai approfondi ma maîtrise de Prometheus, Grafana et Loki, ainsi que des outils DevSecOps que "
     "sont Trivy, CodeQL et Gitleaks, et des mécanismes de durcissement de Kubernetes."),
    ("P", "Surtout, j'ai intégré la sécurité et l'observabilité comme des réflexes de conception, présents dès "
     "les premières décisions d'architecture, et non comme des ajouts de dernière minute."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Je souhaite mettre en œuvre le traçage distribué et des objectifs de niveau de service, afin de "
     "compléter les deux piliers déjà couverts et de piloter la fiabilité de façon quantifiée."),
    ("P", "Je compte également industrialiser la gestion des secrets et la signature des images, et automatiser "
     "la validation de bout en bout de la chaîne d'alerte pour fournir une observabilité complète et éprouvée."),
    ],
)

# ============================================================ ANIS
individual(
    "PE-2526_%s_DouadiAnis.pdf" % CODE,
    "Anis Douadi", "Orchestration Kubernetes / Helm & on-premise / PRA",
    "Chart Helm, autoscaling, site on-premise, MinIO chiffré, Ansible",
    [
    ("H1", "1. Contexte et rôle dans le projet"),
    ("P", "J'ai été responsable de l'orchestration des conteneurs sur Kubernetes et du volet hybride du "
     "projet, c'est-à-dire le site on-premise et le plan de reprise d'activité. Ces sujets touchent "
     "directement à la résilience et à la pérennité des données : ce sont eux qui déterminent la capacité de "
     "la plateforme à survivre à une panne et à protéger durablement les informations du cabinet."),
    ("P", "Mon travail a consisté à transformer les images produites par l'équipe en un déploiement "
     "Kubernetes cohérent, résilient et paramétrable, puis à concevoir la chaîne de sauvegarde reliant le "
     "cloud à un site on-premise simulé. J'ai donc collaboré étroitement avec Zaafir sur l'application, "
     "Elyess sur l'intégration du déploiement dans la chaîne, et Adame sur la sécurité et la supervision du "
     "cluster."),
    ("P", "Le cahier des charges décrivant explicitement une architecture hybride mêlant cloud public et "
     "serveurs on-premise pour les données sensibles, mon rôle était aussi de donner corps à cette vision, en "
     "démontrant concrètement comment des sauvegardes chiffrées peuvent être répliquées hors du cloud, sur un "
     "site maîtrisé par l'organisation."),

    ("H1", "2. Ma contribution détaillée"),
    ("H2", "2.1 Conception du chart Helm"),
    ("P", "J'ai conçu le chart Helm qui décrit l'ensemble des objets Kubernetes de l'application : les "
     "déploiements du backend et du frontend, les services qui les exposent, l'Ingress qui route le trafic "
     "entrant, le secret contenant la chaîne de connexion, l'autoscaling et la définition de supervision. Le "
     "chart est entièrement paramétrable : le registre d'images, l'étiquette de version, le nom d'hôte ou "
     "l'activation de certaines fonctionnalités se règlent par de simples valeurs, sans modifier le code du "
     "chart."),
    ("P", "Ce packaging répond à un objectif de reproductibilité et de portabilité : le même chart, avec des "
     "valeurs différentes, peut déployer l'application en local, en pré-production ou en production. J'ai "
     "veillé à ce que le déploiement soit idempotent et à ce que la mise à jour d'une version se fasse par "
     "remplacement progressif des conteneurs, sans interruption de service perceptible par les utilisateurs."),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", helm_diagram()),
    ("P", "<i>Objets Kubernetes décrits et déployés par le chart Helm de l'application.</i>"),

    ("H2", "2.2 Résilience et autoscaling"),
    ("P", "J'ai configuré des sondes de vivacité et de disponibilité qui permettent à Kubernetes de "
     "redémarrer automatiquement un conteneur défaillant et de ne router le trafic que vers les instances "
     "prêtes à le recevoir. J'ai mis en place un autoscaler horizontal qui ajuste le nombre de répliques du "
     "backend en fonction de la charge processeur, dans une limite haute stricte afin de préserver la "
     "maîtrise des coûts — la scalabilité ne devant jamais se transformer en dérive budgétaire."),
    ("P", "Cette combinaison assure la continuité de service, c'est-à-dire le volet PCA du projet. Nous avons "
     "vérifié en conditions réelles que la suppression manuelle d'une instance entraîne sa recréation "
     "automatique en quelques secondes, sans aucune intervention. J'ai par ailleurs défini le contexte de "
     "sécurité des conteneurs et les politiques de cloisonnement réseau, en concertation avec le responsable "
     "sécurité."),

    ("H2", "2.3 Le site on-premise simulé"),
    ("P", "Conformément au cahier des charges, j'ai provisionné une machine virtuelle représentant un site "
     "on-premise. Point essentiel : cette machine est placée dans un <b>réseau totalement séparé</b> de celui "
     "du cluster, sans interconnexion directe, ce qui la fait se comporter comme un site distant joint depuis "
     "le cloud — à l'image de ce que serait un véritable site relié par Internet ou par un lien sécurisé. Le "
     "schéma ci-dessous illustre cette isolation réseau volontaire :"),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", network_topology()),
    ("FLOW", Spacer(1, 4)),
    ("P", "<i>Deux réseaux virtuels distincts, sans peering : le cloud héberge le cluster et la base, "
     "l'on-premise héberge MinIO ; seuls les flux de sauvegarde chiffrée les relient.</i>"),
    ("P", "Ce choix de simulation nous a permis d'illustrer concrètement le principe d'une architecture "
     "hybride sans disposer d'un centre de données physique, tout en gardant la maîtrise des coûts : la "
     "machine peut être désactivée par une simple variable lorsque ce volet n'est pas démontré, ce qui évite "
     "toute dépense superflue en dehors des périodes d'utilisation."),

    ("H2", "2.4 Stockage objet chiffré (MinIO)"),
    ("P", "Sur cette machine, j'ai installé MinIO, un stockage objet compatible avec le standard S3, au moyen "
     "de playbooks Ansible. J'ai activé le chiffrement côté serveur, de sorte que les sauvegardes soient "
     "chiffrées au repos, répondant ainsi à l'exigence de protection des données sensibles formulée dans le "
     "cahier des charges. Un espace de stockage dédié, créé automatiquement, reçoit l'ensemble des "
     "sauvegardes de la base."),

    ("H2", "2.5 Automatisation par Ansible et plan de reprise"),
    ("P", "J'ai écrit les playbooks Ansible qui configurent la machine on-premise et automatisent les "
     "opérations de sauvegarde et de restauration. La sauvegarde réalise un export complet de la base et le "
     "dépose, chiffré, dans le stockage MinIO ; la restauration récupère la sauvegarde la plus récente et la "
     "réinjecte dans la base. Ansible assure ici la gestion de configuration, en complément de Terraform qui "
     "gère le provisionnement — une répartition classique et saine des responsabilités entre les deux outils."),
    ("P", "J'ai rendu la restauration <b>idempotente</b>, c'est-à-dire rejouable même sur une base déjà "
     "peuplée, en incluant dans l'export les instructions de remise à zéro nécessaires. C'est cette propriété "
     "qui rend le plan de reprise réellement fiable et non seulement théorique : nous l'avons éprouvé de bout "
     "en bout selon le cycle suivant."),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", flow_horizontal([["Donnée", "créée"], ["Sauvegarde", "MinIO chiffré"],
                              ["Perte", "simulée"], ["Restauration", "(Ansible)"],
                              ["Donnée", "récupérée"]])),

    ("H1", "3. Choix technologiques : pourquoi ces technologies plutôt que d'autres"),
    ("P", "Trois décisions ont structuré mon périmètre : le gestionnaire de déploiement Kubernetes, la "
     "solution de stockage des sauvegardes et l'outil de configuration du site distant. Je les justifie "
     "ci-dessous par comparaison directe avec leurs alternatives."),

    ("H2", "3.1 Déploiement Kubernetes : Helm plutôt que Kustomize ou kubectl brut"),
    ("FLOW", wrap_table([
        ["Critère", "Helm (retenu)", "Kustomize", "kubectl (manifs bruts)"],
        ["Paramétrage", "Valeurs + templates puissants", "Superpositions (overlays)", "Aucun (statique)"],
        ["Réutilisabilité", "Chart versionné, portable", "Bonne", "Faible (copier-coller)"],
        ["Retour arrière", "Natif (helm rollback)", "Manuel", "Manuel"],
        ["Multi-environnements", "Un chart, N jeux de valeurs", "Overlays par env.", "Fichiers dupliqués"],
    ], [3.2 * cm, 4.6 * cm, 4.0 * cm, CONTENT_W - 11.8 * cm])),
    ("P", "<b>Helm</b> s'est imposé comme le gestionnaire de paquets de référence pour Kubernetes : il décrit "
     "un ensemble d'objets de façon paramétrable et versionnée, et gère proprement mises à jour et retours "
     "arrière. Kustomize, plus simple, ne propose pas de véritable gestion de version ni de commande de "
     "retour arrière ; déployer des manifestes bruts avec kubectl aurait imposé de dupliquer les fichiers "
     "pour chaque environnement. La capacité de <b>rollback</b> natif de Helm, précieuse en exploitation, et "
     "son modèle « un chart, plusieurs jeux de valeurs » ont été décisifs."),

    ("H2", "3.2 Stockage des sauvegardes : MinIO plutôt qu'Azure Blob Storage"),
    ("FLOW", wrap_table([
        ["Critère", "MinIO (retenu)", "Azure Blob Storage"],
        ["Localisation", "On-premise (site maîtrisé)", "Cloud Azure"],
        ["Démonstration hybride", "Illustre le cahier des charges", "Resterait dans le cloud"],
        ["Compatibilité S3", "Native", "API propre (SDK Azure)"],
        ["Chiffrement au repos", "SSE activé", "Oui (géré par Azure)"],
        ["Portabilité", "Déployable partout", "Lié à Azure"],
    ], [3.4 * cm, 5.6 * cm, CONTENT_W - 9.0 * cm])),
    ("P", "<b>MinIO</b> a été retenu pour le stockage des sauvegardes car le cahier des charges imposait une "
     "architecture hybride : les données sensibles devaient être répliquées sur un site maîtrisé par "
     "l'organisation, hors du cloud. Azure Blob Storage aurait maintenu les sauvegardes dans le cloud, "
     "manquant l'objectif de démonstration hybride. MinIO est léger, compatible avec l'écosystème S3 — donc "
     "interopérable — et facile à déployer sur une simple machine ; sa compatibilité S3 faciliterait en outre "
     "une migration ultérieure vers un stockage objet cloud si le besoin s'en faisait sentir."),

    ("H2", "3.3 Configuration du site distant : Ansible plutôt que des scripts ou cloud-init"),
    ("FLOW", wrap_table([
        ["Critère", "Ansible (retenu)", "Scripts shell ad hoc", "cloud-init"],
        ["Idempotence", "Native", "À coder manuellement", "Limitée (au 1er démarrage)"],
        ["Lisibilité", "Déclaratif (YAML)", "Impératif, dispersé", "Déclaratif mais figé"],
        ["Rejouabilité", "À tout moment", "Risquée", "Au démarrage seulement"],
        ["Réutilisation", "Rôles / playbooks", "Faible", "Faible"],
    ], [3.2 * cm, 4.4 * cm, 4.2 * cm, CONTENT_W - 11.8 * cm])),
    ("P", "Le recours à <b>Ansible</b> pour configurer la machine distante, plutôt qu'à des scripts ad hoc ou "
     "à cloud-init, garantit une configuration déclarative, idempotente, rejouable à tout moment et "
     "documentée. Des scripts shell auraient exigé de coder manuellement l'idempotence ; cloud-init ne "
     "s'exécute qu'au premier démarrage et n'aurait pas permis de rejouer la configuration ni les opérations "
     "de sauvegarde. La combinaison Terraform (provisionnement) et Ansible (configuration) est une pratique "
     "éprouvée qui sépare clairement la création des ressources de leur paramétrage."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "La difficulté centrale a été d'orchestrer une réplication du cloud vers l'on-premise à la fois "
     "fiable et rejouable. La première version de la restauration échouait sur une base déjà peuplée, en "
     "raison de conflits sur les objets existants ; je l'ai corrigée en rendant l'export auto-suffisant, "
     "capable de réinitialiser les structures avant de les recréer. Ce détail, en apparence mineur, fait "
     "toute la différence entre un plan de reprise qui ne fonctionne qu'en démonstration et un plan réellement "
     "exploitable en conditions dégradées."),
    ("P", "J'ai également dû fiabiliser la connexion automatisée à la machine distante : la configuration "
     "Ansible devait attendre que la machine soit effectivement prête à accepter les connexions avant de la "
     "configurer. En coordination avec Elyess, nous avons ajouté une temporisation d'attente qui garantit la "
     "robustesse de cette étape lorsqu'elle est exécutée automatiquement par la chaîne, sans supposer que la "
     "machine est immédiatement disponible."),
    ("P", "Enfin, la compatibilité de l'export de base avec la version du serveur a nécessité d'utiliser un "
     "outil aligné sur la version de PostgreSQL déployée, afin d'éviter tout écart susceptible de rendre une "
     "sauvegarde inutilisable — un point de vigilance essentiel pour un plan de reprise digne de confiance."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "La première évolution consisterait à activer un module réseau appliquant réellement les politiques "
     "de cloisonnement préparées, afin d'obtenir une isolation effective entre les composants du cluster et "
     "de renforcer la sécurité interne."),
    ("P", "Je viserais ensuite une haute disponibilité répartie sur plusieurs zones, de sorte que la panne "
     "d'une zone n'interrompe pas le service, ainsi qu'une réplication géographique des sauvegardes pour se "
     "prémunir contre la perte d'un site entier."),
    ("P", "Je souhaiterais également planifier des tests de restauration réguliers et automatiques : un plan "
     "de reprise ne vaut que s'il est éprouvé périodiquement, faute de quoi l'on découvre ses failles au pire "
     "moment. Externaliser les sauvegardes vers un stockage redondant compléterait ce dispositif."),
    ("P", "Enfin, remplacer le site on-premise simulé par une véritable intégration réseau, reliée par un "
     "lien sécurisé de type VPN, rapprocherait encore la maquette d'une architecture hybride de production et "
     "permettrait d'éprouver les problématiques réelles de latence et de sécurité des échanges."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "Le site on-premise est ici simulé par une machine virtuelle placée dans un réseau distinct : "
     "l'isolation est représentative d'un site séparé, mais il ne s'agit pas d'un véritable centre de données "
     "physique, et l'interconnexion réelle par VPN n'a pas été mise en œuvre dans ce cadre."),
    ("P", "De plus, la restauration ramène l'état de la base au moment de la dernière sauvegarde : la perte "
     "de données potentielle dépend donc directement de la fréquence des sauvegardes, ce que l'on désigne par "
     "l'objectif de point de reprise. Une fréquence plus élevée réduirait cette perte, au prix d'un stockage "
     "et d'un trafic accrus."),
    ("P", "Enfin, le stockage MinIO fonctionne en instance unique, sans redondance interne, ce qui "
     "constituerait un point de défaillance en production ; et l'architecture réseau retenue pour le cluster, "
     "choisie pour sa légèreté, limite l'application stricte des politiques de cloisonnement que j'ai "
     "définies. Ces limites sont assumées au regard du caractère MVP du projet et clairement documentées."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Consulter le stockage de sauvegarde"),
    ("P", "La console web de MinIO, accessible sur la machine on-premise, permet de visualiser l'espace de "
     "stockage dédié et d'y retrouver les sauvegardes chiffrées, chacune horodatée. C'est le moyen le plus "
     "simple de vérifier qu'une sauvegarde a bien été produite et d'en connaître la date."),
    ("H2", "7.2 Déclencher une sauvegarde"),
    ("P", "Les sauvegardes sont planifiées quotidiennement de façon automatique, mais peuvent aussi être "
     "déclenchées à la demande depuis le workflow prévu à cet effet, en choisissant le mode de sauvegarde. "
     "L'opération réalise l'export chiffré de la base et son dépôt dans MinIO."),
    ("H2", "7.3 Restaurer les données"),
    ("P", "En cas de perte, la restauration se déclenche depuis le même workflow en choisissant le mode de "
     "restauration : la sauvegarde la plus récente est récupérée puis réinjectée dans la base. Grâce au "
     "caractère idempotent de l'opération, elle peut être relancée sans risque même si la base contient déjà "
     "des données."),
    ("H2", "7.4 Adapter le déploiement"),
    ("P", "Le chart Helm étant paramétrable, il est possible d'ajuster le registre d'images, le nom d'hôte "
     "d'accès, le nombre de répliques ou l'activation de certaines fonctionnalités par de simples valeurs, "
     "sans modifier le code du chart, ce qui facilite l'adaptation de l'application à un nouvel environnement."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de concevoir une réplication du cloud vers l'on-premise fiable et "
     "rejouable, et de rendre la restauration réellement idempotente. Il m'a fallu comprendre en profondeur "
     "le comportement de l'outil de sauvegarde pour transformer une procédure fragile en un plan de reprise "
     "digne de confiance."),
    ("P", "Le caractère hybride du sujet, à cheval entre le cluster cloud et une machine distante, a "
     "également représenté un défi d'intégration : il a fallu faire dialoguer proprement deux environnements "
     "conçus pour être séparés."),
    ("H2", "Forces"),
    ("P", "Je retiens ma maîtrise du packaging Kubernetes et des objets qui le composent, ainsi qu'une vision "
     "claire des enjeux de résilience et d'architecture hybride."),
    ("P", "J'ai su relier des sujets souvent traités séparément — orchestration, réseau, sauvegarde — pour en "
     "faire un ensemble cohérent, ce qui témoigne d'une capacité à prendre de la hauteur sur l'architecture "
     "globale."),
    ("H2", "Faiblesses"),
    ("P", "Je dois passer d'un on-premise simulé à une intégration réseau plus réaliste, ce qui suppose "
     "d'approfondir mes compétences en interconnexion réseau, notamment les VPN et le routage entre sites."),
    ("P", "Par ailleurs, la redondance du stockage de sauvegarde reste à renforcer : une instance unique, "
     "bien que suffisante pour une démonstration, ne serait pas acceptable pour un usage réel."),
    ("H2", "Compétences développées"),
    ("P", "Ce projet a consolidé mes compétences sur Kubernetes et Helm — templating, autoscaling, rôles, "
     "politiques réseau — sur Ansible, et sur la conception d'un plan de reprise d'activité complet, de la "
     "sauvegarde chiffrée jusqu'à la restauration automatisée."),
    ("P", "J'ai aussi appris à raisonner en termes d'objectifs de reprise — délai et point de reprise — qui "
     "structurent toute réflexion sérieuse sur la continuité d'activité."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Je souhaite mettre en œuvre une haute disponibilité multi-zones et automatiser des tests de "
     "restauration réguliers, afin de garantir la validité du plan de reprise dans la durée et non seulement "
     "à un instant donné."),
    ("P", "Je compte enfin me former à l'interconnexion sécurisée de sites, pour être capable de concevoir de "
     "véritables architectures hybrides reliant un centre de données à un cloud public."),
    ],
)

print("=== ADAME + ANIS générés ===")
