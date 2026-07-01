# -*- coding: utf-8 -*-
"""Rendus individuels détaillés — Adame & Anis."""
from content_docs import individual, CODE  # noqa

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
    ("P", "Ce positionnement m'a amené à travailler sur l'ensemble du périmètre : j'ai instrumenté "
     "l'application développée par Zaafir, intégré mes analyses dans la chaîne d'Elyess, et sécurisé les "
     "objets Kubernetes packagés par Anis. La sécurité et l'observabilité sont en effet des préoccupations "
     "transverses, qui ne peuvent être traitées en silo."),

    ("H1", "2. Ma contribution détaillée"),
    ("H2", "2.1 Collecte des métriques (Prometheus)"),
    ("P", "J'ai déployé Prometheus, qui collecte périodiquement les métriques exposées par les différents "
     "composants. L'application publie ses propres indicateurs — nombre de requêtes, latence, code de "
     "réponse — que j'ai fait découvrir automatiquement par Prometheus grâce à un objet de configuration "
     "dédié. Ainsi, dès qu'une nouvelle instance de l'application démarre, elle est automatiquement prise en "
     "compte par la supervision, sans configuration manuelle."),
    ("P", "J'ai veillé à limiter la cardinalité des métriques, c'est-à-dire à éviter une explosion du nombre "
     "de séries temporelles, en agrégeant les mesures par route plutôt que par requête individuelle. Ce souci "
     "rejoint la démarche FinOps de l'équipe, car une supervision mal maîtrisée peut consommer beaucoup de "
     "mémoire et de stockage."),

    ("H2", "2.2 Visualisation (Grafana) et tableaux de bord"),
    ("P", "J'ai déployé Grafana et conçu un tableau de bord dédié à l'application, présentant les indicateurs "
     "clés : le débit de requêtes par route, la latence au 95e centile, le taux d'erreurs serveur et la "
     "disponibilité du backend. Ces quatre indicateurs correspondent aux « signaux dorés » de la supervision "
     "d'un service, et permettent de diagnostiquer rapidement une dégradation."),
    ("P", "J'ai automatisé l'import de ce tableau de bord afin qu'il soit présent dès l'installation, sans "
     "manipulation. J'ai également exposé Grafana de façon accessible via l'Ingress existant, en réutilisant "
     "l'adresse publique du cluster — un choix qui évite de provisionner une seconde adresse IP et participe "
     "donc à la maîtrise des coûts."),

    ("H2", "2.3 Centralisation des journaux (Loki)"),
    ("P", "Pour les journaux, j'ai déployé Loki accompagné de son agent de collecte, qui récupère les traces "
     "de tous les composants et les rend consultables et corrélables depuis Grafana. L'application produit "
     "des journaux structurés, ce qui facilite leur exploitation. Le choix de Loki plutôt qu'une pile "
     "Elasticsearch a été motivé, en accord avec l'équipe, par son empreinte réduite : Loki n'indexe que les "
     "étiquettes, ce qui le rend bien plus économe pour un usage équivalent."),

    ("H2", "2.4 Alerting (Alertmanager)"),
    ("P", "J'ai défini des règles d'alerte qui se déclenchent lorsque le service devient indisponible, "
     "lorsque le taux d'erreurs dépasse un seuil ou lorsque la latence se dégrade. Ces alertes sont routées "
     "par Alertmanager vers une messagerie d'équipe (Slack ou Teams) au moyen d'un point d'entrée dédié. "
     "L'objectif est de prévenir l'équipe d'un incident avant même que les utilisateurs ne s'en aperçoivent."),

    ("H2", "2.5 Sécurité de la chaîne (DevSecOps)"),
    ("P", "J'ai intégré dans la chaîne d'intégration trois analyses complémentaires. Trivy examine les "
     "dépendances, les fichiers d'infrastructure et les images à la recherche de vulnérabilités connues, et "
     "bloque le déploiement en cas de faille critique. CodeQL réalise une analyse statique du code source "
     "pour détecter des schémas dangereux. Gitleaks recherche toute fuite de secret dans l'historique. Les "
     "résultats sont publiés dans l'onglet de sécurité du dépôt, au format standard SARIF."),

    ("H2", "2.6 Durcissement de l'exécution"),
    ("P", "Au-delà des analyses, j'ai durci l'exécution : les conteneurs s'exécutent sans privilèges et sans "
     "possibilité d'élévation, les capacités système superflues sont retirées, et l'accès à l'API du cluster "
     "est régi par des rôles restreints (RBAC). Les communications avec la base sont chiffrées en TLS, et les "
     "secrets ne sont jamais écrits dans le dépôt : ils transitent chiffrés et sont injectés au dernier "
     "moment. J'ai également préparé des politiques de cloisonnement réseau limitant les communications entre "
     "composants au strict nécessaire."),

    ("H1", "3. Choix techniques et justifications"),
    ("P", "Le triptyque Prometheus / Grafana / Loki s'est imposé comme la référence open source de "
     "l'observabilité cloud-native, avec une intégration étroite entre métriques et journaux au sein d'une "
     "interface unique. Pour la sécurité, j'ai retenu des outils gratuits et largement adoptés, "
     "complémentaires dans leur périmètre (dépendances, code, secrets), afin de couvrir la chaîne sans coût "
     "de licence."),
    ("P", "J'ai fait le choix d'intégrer ces analyses directement dans la chaîne d'intégration, plutôt que de "
     "les exécuter ponctuellement : la sécurité devient ainsi une propriété vérifiée à chaque livraison, "
     "selon le principe du « décalage vers la gauche » (shift-left) qui consiste à détecter les problèmes au "
     "plus tôt."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "La principale difficulté a été de faire tenir une pile de supervision complète sur un cluster "
     "volontairement réduit pour des raisons budgétaires. J'ai dû dimensionner soigneusement les ressources "
     "allouées à chaque composant et accepter des durées de rétention courtes, afin que la supervision "
     "n'entre pas en concurrence avec l'application pour les ressources du cluster."),
    ("P", "Une autre difficulté a concerné la découverte automatique des métriques de l'application : il a "
     "fallu s'assurer que Prometheus sélectionne bien l'objet de configuration produit par le déploiement, ce "
     "qui supposait un bon ordonnancement de l'installation (les définitions de ressources devant précéder "
     "l'application). Ce point a été résolu en coordination avec le responsable de la chaîne d'intégration."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "Je souhaiterais ajouter le <b>traçage distribué</b>, au moyen d'OpenTelemetry et d'un outil comme "
     "Tempo ou Jaeger, afin de suivre une requête à travers les composants et de diagnostiquer finement les "
     "lenteurs — un troisième pilier de l'observabilité, complémentaire des métriques et des journaux."),
    ("P", "Je centraliserais également la gestion des secrets dans un coffre dédié offrant rotation "
     "automatique, et je renforcerais la posture de sécurité du cluster par des politiques avancées : "
     "standards de sécurité des pods, contrôleur d'admission validant les manifestes, et signature des images "
     "pour garantir leur provenance. Enfin, je définirais des objectifs de niveau de service (SLO) assortis "
     "d'un suivi de leur consommation."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "Le routage des alertes vers une messagerie nécessite un point d'entrée externe qui n'a pas été "
     "connecté en production dans le cadre du projet ; le mécanisme est en place mais sa validation de bout "
     "en bout reste à finaliser. De même, les politiques de cloisonnement réseau que j'ai préparées supposent "
     "un module réseau capable de les appliquer, que nous n'avons pas activé sur le cluster d'étude pour "
     "rester légers : elles sont donc fournies mais non strictement appliquées."),
    ("P", "Par ailleurs, une véritable conformité à l'hébergement de données de santé imposerait une région "
     "et des services certifiés que nous n'avons pas retenus dans ce cadre, et la rétention volontairement "
     "courte des métriques et journaux limite l'analyse rétrospective des incidents anciens."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Consulter la supervision"),
    ("P", "L'utilisateur accède à Grafana via son adresse dédiée, avec les identifiants fournis. Le tableau "
     "de bord « Vue d'ensemble » est disponible immédiatement et présente l'état de santé de l'application. "
     "Pour observer l'évolution des courbes, il suffit de générer un peu de trafic sur l'API."),
    ("H2", "7.2 Explorer les journaux"),
    ("P", "Depuis Grafana, la vue d'exploration permet d'interroger la source de données Loki et de filtrer "
     "les journaux par composant, ce qui est précieux pour diagnostiquer un comportement anormal."),
    ("H2", "7.3 Consulter les rapports de sécurité"),
    ("P", "Les résultats des analyses de sécurité sont consultables dans l'onglet « Security » du dépôt, où "
     "chaque vulnérabilité détectée est listée avec sa gravité et sa localisation, permettant un suivi et une "
     "priorisation des corrections."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de concilier une observabilité riche et une sécurité exigeante avec la "
     "contrainte de sobriété du projet. Il m'a fallu arbitrer en permanence entre l'exhaustivité souhaitable "
     "et ce que le cluster pouvait raisonnablement supporter."),
    ("H2", "Forces"),
    ("P", "Je retiens mon sens du détail sur les questions de sécurité et de conformité, ainsi que ma "
     "capacité à rendre un système transparent et compréhensible pour l'ensemble de l'équipe, ce qui a "
     "facilité le diagnostic collectif des incidents."),
    ("H2", "Faiblesses"),
    ("P", "Je dois concrétiser jusqu'au bout certaines mises en œuvre que j'ai préparées mais pas totalement "
     "activées, comme le routage effectif des alertes et l'application stricte des politiques réseau. J'ai "
     "parfois privilégié la mise en place sur la validation finale."),
    ("H2", "Compétences développées"),
    ("P", "J'ai approfondi ma maîtrise de Prometheus, Grafana et Loki, ainsi que des outils DevSecOps (Trivy, "
     "CodeQL, Gitleaks) et du durcissement Kubernetes. J'ai surtout intégré la sécurité et l'observabilité "
     "comme des réflexes de conception, et non comme des ajouts de dernière minute."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Je souhaite mettre en œuvre le traçage distribué et des objectifs de niveau de service, "
     "industrialiser la gestion des secrets et la signature des images, et automatiser la validation de bout "
     "en bout de la chaîne d'alerte afin de fournir une observabilité complète et éprouvée."),
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
     "la plateforme à survivre à une panne et à protéger les informations sensibles du cabinet."),
    ("P", "Mon travail a consisté à transformer les images produites par l'équipe en un déploiement "
     "Kubernetes cohérent, résilient et paramétrable, puis à concevoir la chaîne de sauvegarde reliant le "
     "cloud à un site on-premise simulé. J'ai donc collaboré étroitement avec Zaafir sur l'application, "
     "Elyess sur l'intégration du déploiement dans la chaîne, et Adame sur les aspects de sécurité et de "
     "supervision du cluster."),

    ("H1", "2. Ma contribution détaillée"),
    ("H2", "2.1 Conception du chart Helm"),
    ("P", "J'ai conçu le chart Helm qui décrit l'ensemble des objets Kubernetes de l'application : les "
     "déploiements du backend et du frontend, les services qui les exposent, l'Ingress qui route le trafic "
     "entrant, le secret contenant la chaîne de connexion, l'autoscaling et la définition de supervision. Le "
     "chart est entièrement paramétrable : le registre d'images, l'étiquette de version, le nom d'hôte ou "
     "l'activation de certaines fonctionnalités se règlent par des valeurs, ce qui permet de l'adapter à "
     "différents environnements sans en modifier le code."),
    ("P", "Ce packaging répond à un objectif de reproductibilité et de portabilité : le même chart, avec des "
     "valeurs différentes, peut déployer l'application en local, en pré-production ou en production. J'ai "
     "veillé à ce que le déploiement soit idempotent et à ce que la mise à jour d'une version se fasse par "
     "remplacement progressif des conteneurs, sans interruption de service."),

    ("H2", "2.2 Résilience et autoscaling"),
    ("P", "J'ai configuré des sondes de vivacité et de disponibilité qui permettent à Kubernetes de "
     "redémarrer automatiquement un conteneur défaillant et de ne router le trafic que vers les instances "
     "prêtes. J'ai mis en place un autoscaler horizontal qui ajuste le nombre de répliques du backend en "
     "fonction de la charge processeur, dans une limite haute stricte afin de préserver la maîtrise des "
     "coûts."),
    ("P", "Cette combinaison assure la continuité de service (PCA) : nous avons vérifié en conditions réelles "
     "que la suppression manuelle d'une instance entraîne sa recréation automatique en quelques secondes, "
     "sans intervention. J'ai également défini le contexte de sécurité des conteneurs et des politiques de "
     "cloisonnement réseau, en concertation avec le responsable sécurité."),

    ("H2", "2.3 Le site on-premise simulé"),
    ("P", "Conformément au cahier des charges, qui décrit une architecture hybride mêlant cloud et serveurs "
     "on-premise pour les données sensibles, j'ai provisionné une machine virtuelle représentant un site "
     "on-premise. Point essentiel : cette machine est placée dans un <b>réseau totalement séparé</b> de celui "
     "du cluster, sans interconnexion directe, ce qui la fait se comporter comme un site distant joint depuis "
     "le cloud — à l'image de ce que serait un vrai site relié par Internet ou par un lien sécurisé."),
    ("P", "Ce choix de simulation nous a permis d'illustrer concrètement le principe d'une architecture "
     "hybride sans disposer d'un centre de données physique, tout en gardant la maîtrise des coûts puisque la "
     "machine peut être désactivée par une simple variable lorsque ce volet n'est pas démontré."),

    ("H2", "2.4 Stockage objet chiffré (MinIO)"),
    ("P", "Sur cette machine, j'ai installé MinIO, un stockage objet compatible avec le standard S3, au "
     "moyen de playbooks Ansible. J'ai activé le chiffrement côté serveur, de sorte que les sauvegardes "
     "soient chiffrées au repos, répondant ainsi à l'exigence de protection des données sensibles. Un espace "
     "de stockage dédié reçoit les sauvegardes de la base."),

    ("H2", "2.5 Automatisation par Ansible et plan de reprise"),
    ("P", "J'ai écrit les playbooks Ansible qui configurent la machine on-premise et automatisent les "
     "opérations de sauvegarde et de restauration. La sauvegarde réalise un export de la base et le dépose, "
     "chiffré, dans le stockage MinIO ; la restauration récupère la sauvegarde la plus récente et la "
     "réinjecte dans la base. Ansible assure ici la gestion de configuration, en complément de Terraform qui "
     "gère le provisionnement — une répartition classique et saine des responsabilités."),
    ("P", "J'ai rendu la restauration <b>idempotente</b>, c'est-à-dire rejouable même sur une base déjà "
     "peuplée, en incluant dans l'export les instructions de remise à zéro nécessaires. C'est cette propriété "
     "qui rend le plan de reprise réellement fiable et non seulement théorique."),

    ("H1", "3. Choix techniques et justifications"),
    ("P", "Helm s'est imposé comme le gestionnaire de paquets de référence pour Kubernetes, car il permet de "
     "décrire un ensemble d'objets de façon paramétrable et versionnée, et de gérer proprement les mises à "
     "jour et les retours arrière. MinIO a été retenu pour le stockage des sauvegardes car il est léger, "
     "compatible avec l'écosystème S3 et facile à déployer sur une simple machine, ce qui convenait "
     "parfaitement à notre site on-premise simulé."),
    ("P", "Le recours à Ansible pour la configuration de la machine distante, plutôt qu'à des scripts ad hoc, "
     "garantit que cette configuration est déclarative, rejouable et documentée. Cette combinaison Terraform "
     "(provisionnement) + Ansible (configuration) est une pratique éprouvée qui sépare clairement la création "
     "des ressources de leur paramétrage."),

    ("H1", "4. Difficultés rencontrées et solutions apportées"),
    ("P", "La difficulté centrale a été d'orchestrer une réplication cloud vers on-premise à la fois fiable "
     "et rejouable. La première version de la restauration échouait sur une base déjà peuplée, en raison de "
     "conflits ; je l'ai corrigée en rendant l'export auto-suffisant, capable de réinitialiser les objets "
     "avant de les recréer. Ce détail, en apparence mineur, fait toute la différence entre un plan de reprise "
     "qui fonctionne en démonstration et un plan réellement exploitable."),
    ("P", "J'ai également dû fiabiliser la connexion automatisée à la machine distante : la configuration "
     "Ansible devait attendre que la machine soit prête à accepter les connexions avant de la configurer. "
     "En coordination avec le responsable de la chaîne d'intégration, nous avons ajouté une temporisation "
     "d'attente qui garantit la robustesse de cette étape lorsqu'elle est exécutée automatiquement."),

    ("H1", "5. Perspectives d'évolution"),
    ("P", "La première évolution consisterait à activer un module réseau appliquant réellement les politiques "
     "de cloisonnement que nous avons préparées, afin d'obtenir une isolation effective entre les composants "
     "du cluster. Je viserais ensuite une haute disponibilité répartie sur plusieurs zones, ainsi qu'une "
     "réplication géographique des sauvegardes pour se prémunir contre la perte d'un site entier."),
    ("P", "Je souhaiterais également planifier des tests de restauration réguliers et automatiques, afin de "
     "vérifier en continu l'efficacité du plan de reprise, et externaliser les sauvegardes vers un stockage "
     "redondant. Enfin, remplacer le site on-premise simulé par une véritable intégration réseau, reliée par "
     "un lien sécurisé de type VPN, rapprocherait encore la maquette d'une architecture de production."),

    ("H1", "6. Analyse critique des limites"),
    ("P", "Le site on-premise est ici simulé par une machine virtuelle placée dans un réseau distinct : "
     "l'isolation est représentative d'un site séparé, mais il ne s'agit pas d'un véritable centre de données "
     "physique, et l'interconnexion réelle par VPN n'a pas été mise en œuvre. De plus, la restauration ramène "
     "l'état au moment de la dernière sauvegarde, si bien que la perte de données potentielle dépend "
     "directement de la fréquence des sauvegardes (objectif de point de reprise)."),
    ("P", "Par ailleurs, le stockage MinIO fonctionne en instance unique, sans redondance interne, ce qui "
     "constituerait un point de défaillance en production ; et l'architecture réseau retenue pour le cluster, "
     "choisie pour sa légèreté, limite l'application stricte des politiques de cloisonnement que j'ai "
     "définies."),

    ("H1", "7. Annexe — documentation utilisateur (mon périmètre)"),
    ("H2", "7.1 Consulter le stockage de sauvegarde"),
    ("P", "La console web de MinIO, accessible sur la machine on-premise, permet de visualiser l'espace de "
     "stockage dédié et d'y retrouver les sauvegardes chiffrées, chacune horodatée. C'est le moyen le plus "
     "simple de vérifier qu'une sauvegarde a bien été produite."),
    ("H2", "7.2 Déclencher une sauvegarde ou une restauration"),
    ("P", "Les opérations de sauvegarde et de restauration se déclenchent depuis le workflow prévu à cet "
     "effet, en choisissant le mode souhaité. La sauvegarde est par ailleurs planifiée quotidiennement de "
     "façon automatique. La restauration récupère et réinjecte la sauvegarde la plus récente."),
    ("H2", "7.3 Adapter le déploiement"),
    ("P", "Le chart Helm étant paramétrable, il est possible d'ajuster le registre d'images, le nom d'hôte "
     "d'accès ou l'activation de certaines fonctionnalités par de simples valeurs, sans modifier le code du "
     "chart, ce qui facilite l'adaptation à un nouvel environnement."),

    ("H1", "8. Analyse personnelle"),
    ("H2", "Défis rencontrés"),
    ("P", "Mon principal défi a été de concevoir une réplication cloud vers on-premise fiable et rejouable, "
     "et de rendre la restauration réellement idempotente. Il m'a fallu comprendre en profondeur le "
     "comportement de l'outil de sauvegarde pour transformer une procédure fragile en un plan de reprise "
     "digne de confiance."),
    ("H2", "Forces"),
    ("P", "Je retiens ma maîtrise du packaging Kubernetes et des objets qui le composent, ainsi qu'une "
     "vision claire des enjeux de résilience et d'architecture hybride, qui m'a permis de relier des sujets "
     "souvent traités séparément (orchestration, réseau, sauvegarde)."),
    ("H2", "Faiblesses"),
    ("P", "Je dois passer d'un on-premise simulé à une intégration réseau plus réaliste, ce qui suppose "
     "d'approfondir mes compétences en interconnexion réseau (VPN, routage). Par ailleurs, la redondance du "
     "stockage de sauvegarde reste à renforcer."),
    ("H2", "Compétences développées"),
    ("P", "Ce projet a consolidé mes compétences sur Kubernetes et Helm (templating, autoscaling, rôles, "
     "politiques réseau), sur Ansible (playbooks, gestion de configuration) et sur la conception d'un plan de "
     "reprise d'activité complet, de la sauvegarde chiffrée à la restauration automatisée."),
    ("H2", "Axes d'amélioration personnels"),
    ("P", "Je souhaite mettre en œuvre une haute disponibilité multi-zones, automatiser des tests de "
     "restauration réguliers pour garantir le plan de reprise dans la durée, et me former à l'interconnexion "
     "sécurisée de sites afin de concevoir de véritables architectures hybrides."),
    ],
)

print("=== ADAME + ANIS générés ===")
