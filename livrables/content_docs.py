# -*- coding: utf-8 -*-
from generate_docs import *  # noqa

TEAM = [
    ["Membre", "Rôle", "Périmètre principal"],
    ["Zaafir Mougammadou Zaccaria", "Infrastructure & déploiement",
     "Infrastructure as code Terraform (AKS, ACR, PostgreSQL, réseau, budget), application FastAPI/React, déploiement applicatif."],
    ["Elyess Rjafellah", "CI/CD & automatisation",
     "Chaîne GitHub Actions (provisionnement, build, scans, déploiement, sauvegarde), état Terraform distant, pipeline auto-réparant."],
    ["Adame Nianghane", "Observabilité & sécurité",
     "Supervision Prometheus/Grafana/Loki/Alertmanager, DevSecOps (Trivy, CodeQL, Gitleaks), RBAC, TLS, conformité RGPD."],
    ["Anis Douadi", "Kubernetes & on-premise / PRA",
     "Packaging Helm, autoscaling et politiques, site on-premise simulé, MinIO chiffré, Ansible, plan de reprise d'activité."],
]
W1 = 4.6 * cm
TEAMW = [W1, 3.5 * cm, CONTENT_W - W1 - 3.5 * cm]


# =================================================================== GROUPE
g = cover(
    "Document technique final",
    "Plateforme de gestion d'un cabinet d'audioprothèse\nSolution DevOps hybride sur Microsoft Azure",
    [["Équipe", "Zaafir Mougammadou Zaccaria · Elyess Rjafellah · Adame Nianghane · Anis Douadi"],
     ["Période", PERIODE],
     ["Client", "Cabinet d'audioprothèse « AudioPro » (commanditaire)"],
     ["Dépôt", "github.com/Rifaazs27/projet-audioprothese"],
     ["Nature", "Rendu de groupe — solution technique complète"]])

# 1
g += [H1("1. Présentation de l'entreprise et de l'équipe"),
      P("« AudioPro » est un cabinet d'audioprothèse qui accompagne ses patients tout au long de leur "
        "appareillage. Son activité quotidienne repose sur le suivi d'un ensemble d'informations sensibles : "
        "le dossier de chaque patient, les appareils auditifs qui lui sont posés, et le calendrier des "
        "rendez-vous de contrôle. Jusqu'ici gérées de façon dispersée, ces données méritaient une plateforme "
        "centralisée, fiable et sécurisée, capable de garantir la confidentialité exigée par la réglementation "
        "sur les données de santé tout en restant disponible et simple d'usage pour les praticiens."),
      P("Le cabinet a confié à notre équipe la conception et la mise en production de cette plateforme, non pas "
        "comme une simple application isolée, mais comme un <b>système complet exploité selon les pratiques "
        "DevOps</b> : automatisation des déploiements, infrastructure décrite sous forme de code, supervision "
        "permanente, sécurité intégrée à chaque étape et capacité à se rétablir après incident. L'objectif "
        "pédagogique sous-jacent était de démontrer notre maîtrise de l'ensemble de la chaîne, du code source "
        "jusqu'à l'exploitation en conditions réelles."),
      P("Notre équipe est composée de quatre étudiants du Mastère DevOps. Afin de couvrir l'intégralité du "
        "périmètre sans recouvrement inutile, nous avons réparti les responsabilités par grands domaines "
        "techniques, chacun étant pilote sur son sujet tout en contribuant aux revues de code et aux décisions "
        "d'architecture communes :"),
      wrap_table(TEAM, TEAMW)]

# 2
g += [H1("2. Analyse de la problématique et solution proposée"),
      P("La problématique dépasse le simple développement d'un logiciel. Les données manipulées étant des "
        "données de santé, la <b>confidentialité</b> et la <b>traçabilité</b> sont impératives. Le service "
        "devant être utilisé au quotidien par le cabinet, sa <b>disponibilité</b> et sa capacité d'<b>auto-"
        "rétablissement</b> sont essentielles. La solution doit en outre rester <b>économe</b> — le projet "
        "s'inscrit dans le cadre d'un compte Azure for Students plafonné à 85 dollars — et entièrement "
        "<b>reproductible</b>, afin de pouvoir être reconstruite à l'identique à tout moment."),
      P("Pour répondre à ces exigences, nous avons conçu une application web conteneurisée — une interface "
        "React, une API FastAPI et une base PostgreSQL managée — déployée sur un cluster Kubernetes managé "
        "(Azure AKS) et encadrée par une chaîne DevOps de bout en bout. L'infrastructure est décrite en "
        "Terraform, les déploiements sont automatisés par GitHub Actions, la supervision repose sur "
        "Prometheus, Grafana et Loki, et la sécurité est vérifiée automatiquement à chaque livraison. "
        "Conformément au cahier des charges, l'architecture est <b>hybride</b> : le cloud héberge "
        "l'application tandis qu'un site on-premise (simulé par un réseau séparé) accueille le stockage objet "
        "chiffré des sauvegardes, illustrant la gestion des données sensibles hors du cloud public."),
      P("Le schéma ci-dessous synthétise cette architecture, depuis le poste du développeur jusqu'à "
        "l'exécution supervisée en production et la réplication des sauvegardes vers l'on-premise :"),
      Spacer(1, 4), architecture(), Spacer(1, 6),
      P("Le flux est le suivant : chaque modification poussée par un développeur déclenche le pipeline "
        "d'intégration et de déploiement, qui teste le code, en vérifie la sécurité, construit les images, "
        "les publie dans le registre Azure Container Registry puis les déploie sur le cluster via Helm. "
        "L'application est exposée aux utilisateurs par un Ingress unique ; le backend dialogue avec la base "
        "PostgreSQL en TLS ; la supervision et les sauvegardes fonctionnent en continu et de façon autonome.")]

# 3
COST = [
    ["Ressource", "Dimensionnement", "Coût indicatif (24/7)"],
    ["AKS — plan de contrôle", "Free tier", "0 $"],
    ["AKS — nœuds de calcul", "2 × Standard_B2s_v2", "≈ 60–70 $ / mois"],
    ["Base de données", "PostgreSQL Flexible B1ms", "≈ 13 $ / mois"],
    ["Registre d'images", "Azure Container Registry Basic", "≈ 5 $ / mois"],
    ["VM on-premise (MinIO)", "Standard_B2s_v2", "≈ 30 $ / mois"],
    ["Équilibreurs & IP publiques", "Standard", "≈ 6–9 $ / mois"],
]
g += [H1("3. Gestion des coûts — démarche FinOps (M2)"),
      P("La maîtrise des coûts a été traitée comme une contrainte de conception et non comme une "
        "préoccupation de fin de projet. Le budget disponible — 85 dollars de crédit étudiant, sans "
        "renouvellement — nous a imposé des arbitrages permanents entre exhaustivité technique et sobriété. "
        "Le tableau suivant présente l'estimation des coûts de l'infrastructure lorsqu'elle fonctionne en "
        "continu :"),
      wrap_table(COST, [6 * cm, 6.5 * cm, CONTENT_W - 12.5 * cm]),
      P("Plusieurs leviers d'optimisation ont été appliqués. Le plan de contrôle Kubernetes est gratuit et "
        "les nœuds reposent sur des machines « burstable » de la série B, peu coûteuses. Pour la "
        "centralisation des journaux, nous avons délibérément retenu Loki plutôt que la pile ELK : Loki "
        "n'indexe que les métadonnées et consomme une fraction des ressources d'Elasticsearch, ce qui était "
        "incompatible avec notre budget. Les secrets sont conservés dans GitHub Actions plutôt que dans un "
        "coffre hébergé en permanence, et les durées de rétention (métriques, sauvegardes) ont été réduites "
        "au strict nécessaire."),
      P("Surtout, l'infrastructure n'est pas destinée à tourner en permanence. Un budget Azure assorti "
        "d'alertes par courriel à 50, 80 et 100 % du plafond prévient toute dérive, et l'ensemble peut être "
        "<b>détruit en un clic</b> puis reconstruit en une douzaine de minutes. En pratique, l'environnement "
        "n'est allumé que pendant les phases de test et de démonstration, ramenant le coût réel à quelques "
        "dollars sur toute la durée du projet.")]

# 4
GANTT_NOTE = ("Le projet s'est déroulé sur le second semestre de l'année universitaire, de janvier à juin "
              "2026, selon une démarche agile en sprints de deux semaines. Le diagramme de Gantt ci-dessous "
              "retrace l'enchaînement des grandes phases, du cadrage initial à la rédaction des livrables et "
              "à l'enregistrement de la vidéo de démonstration.")
CONTRIB = [
    ["Membre", "Contributions concrètes au projet"],
    ["Zaafir Mougammadou Zaccaria",
     "Conception des modules Terraform (groupe de ressources, AKS, ACR, PostgreSQL, réseau, budget), développement de l'API FastAPI et du frontend, conteneurisation et déploiement applicatif Helm."],
    ["Elyess Rjafellah",
     "Conception des workflows GitHub Actions (intégration, sécurité, déploiement, sauvegarde planifiée), automatisation du provisionnement, état distant et mécanismes d'auto-réparation du pipeline."],
    ["Adame Nianghane",
     "Mise en place de la supervision (Prometheus, Grafana, Loki, Alertmanager) et des tableaux de bord, intégration des scans de sécurité dans la CI, durcissement (RBAC, TLS, secrets, conteneurs non-root)."],
    ["Anis Douadi",
     "Packaging Helm de l'application, autoscaling et politiques réseau, provisionnement de la VM on-premise, configuration de MinIO chiffré et des playbooks Ansible de sauvegarde et de restauration."],
]
g += [H1("4. Organisation de l'équipe, planification et méthodologie"),
      P("Nous avons adopté une organisation agile inspirée de Scrum et de Kanban, rythmée par des sprints de "
        "deux semaines et une priorisation des tâches selon la méthode MoSCoW. Le dépôt Git a servi de point "
        "central : chaque évolution passait par une branche puis une revue de code (Pull Request) avant "
        "d'être intégrée, garantissant la qualité et le partage de connaissances entre les membres. Les "
        "outils mobilisés sont représentatifs d'une chaîne DevOps professionnelle : Git et GitHub Actions "
        "pour l'intégration et le déploiement continus, Terraform et Ansible pour la gestion de "
        "configuration, et Helm pour le packaging Kubernetes."),
      P(GANTT_NOTE),
      Spacer(1, 4), gantt(), Spacer(1, 8),
      P("La répartition des contributions, équilibrée entre les quatre membres, est détaillée ci-dessous. "
        "Chaque contributeur a piloté un domaine tout en participant aux décisions transverses ; la "
        "traçabilité individuelle est consultable dans l'historique du dépôt et la vue « Contributors » de "
        "GitHub."),
      wrap_table(CONTRIB, [4.6 * cm, CONTENT_W - 4.6 * cm])]

# 5
STACK = [
    ["Domaine", "Technologies retenues"],
    ["Application", "Python 3.11, FastAPI, SQLAlchemy, Pydantic ; React 18 + Vite"],
    ["Données", "PostgreSQL 16 (Azure Flexible Server, TLS obligatoire)"],
    ["Conteneurs / Orchestration", "Docker (images multi-stage non-root), Kubernetes (AKS), Helm"],
    ["Infra & configuration", "Terraform (provider azurerm), Ansible"],
    ["CI/CD", "GitHub Actions (déploiement, sauvegarde, intégration, sécurité)"],
    ["Observabilité", "Prometheus, Grafana, Loki, Alertmanager"],
    ["Sécurité", "Trivy, CodeQL, Gitleaks, RBAC, NetworkPolicies, TLS, secrets chiffrés"],
    ["On-premise / PRA", "VM Linux, MinIO chiffré (SSE), sauvegarde et restauration Ansible"],
]
g += [H1("5. Présentation de la solution technique"),
      P("La solution repose sur un ensemble cohérent de technologies, chacune choisie pour sa pertinence et "
        "son coût d'exploitation :"),
      wrap_table(STACK, [5 * cm, CONTENT_W - 5 * cm]),
      P("<b>Déploiement automatisé.</b> Un simple envoi de code sur la branche principale, ou un "
        "déclenchement manuel, suffit à provisionner l'infrastructure, construire et analyser les images, "
        "puis déployer l'application — sans aucune manipulation à la main. Le pipeline enchaîne la connexion "
        "à Azure, l'application Terraform, la construction et la publication des images, un scan de "
        "vulnérabilités bloquant, l'installation de l'Ingress et de la supervision, le déploiement de "
        "l'application puis la configuration du stockage de sauvegarde. Il est conçu pour se rétablir seul en "
        "cas d'interruption (gestion des verrous d'état et des déploiements restés en échec)."),
      P("<b>Orchestration et résilience.</b> L'application est packagée sous forme de chart Helm et exécutée "
        "sur Kubernetes, qui assure le redémarrage automatique des conteneurs défaillants et l'ajustement du "
        "nombre de répliques en fonction de la charge. Les conteneurs s'exécutent sans privilèges, le réseau "
        "interne est cloisonné et l'accès à l'API du cluster est régi par des rôles (RBAC)."),
      P("<b>Observabilité et sécurité.</b> L'API expose ses propres métriques, collectées par Prometheus et "
        "visualisées dans Grafana (débit, latence, taux d'erreurs, disponibilité) ; les journaux sont "
        "centralisés via Loki et les alertes routées vers une messagerie d'équipe. À chaque livraison, le "
        "code et les images sont analysés par Trivy, CodeQL et Gitleaks, et aucune image présentant une "
        "vulnérabilité critique n'est déployée."),
      P("<b>Reprise d'activité.</b> Les données de la base sont sauvegardées de façon chiffrée vers le "
        "stockage MinIO hébergé sur le site on-premise, et peuvent être restaurées automatiquement par "
        "Ansible. Ce mécanisme a été <b>validé en conditions réelles</b> : après avoir créé une donnée "
        "témoin, l'avoir sauvegardée puis volontairement supprimée, la restauration a permis de la retrouver "
        "à l'identique — preuve concrète de l'efficacité du plan de reprise. L'ensemble de la solution a été "
        "déployé, testé de bout en bout et jugé conforme aux attentes du cahier des charges.")]

build("PE-2526_%s_Mougammadou_Rjafellah_Nianghane_Douadi.pdf" % CODE, g)


# =============================================================== INDIVIDUELS
def individual(fichier, nom, role, intro, contrib, perspectives, limites,
               doc_user, analyse):
    s = cover("Rendu individuel", "%s\n%s" % (nom, role),
              [["Auteur", nom], ["Rôle", role], ["Période", PERIODE],
               ["Projet", "Plateforme de gestion d'un cabinet d'audioprothèse"]])
    s += [H1("1. Ma contribution au projet"), P(intro)]
    for para in contrib:
        s.append(P(para))
    s += [H1("2. Perspectives d'évolution")]
    for para in perspectives:
        s.append(P(para))
    s += [H1("3. Analyse critique des limites techniques rencontrées")]
    for para in limites:
        s.append(P(para))
    s += [H1("4. Annexes"), P("<b>Documentation utilisateur (mon périmètre).</b>")]
    s.append(P(doc_user))
    s.append(P("<b>Analyse personnelle.</b>"))
    for para in analyse:
        s.append(P(para))
    build(fichier, s)


individual(
    "PE-2526_%s_MougammadouZaafir.pdf" % CODE,
    "Zaafir Mougammadou Zaccaria", "Infrastructure cloud & déploiement applicatif",
    "Au sein de l'équipe, j'ai pris la responsabilité de l'infrastructure Azure décrite en code et de "
    "l'application elle-même, ainsi que de son déploiement de bout en bout. Mon objectif était de garantir "
    "qu'à partir d'un dépôt vide, l'environnement complet puisse être reconstruit automatiquement et de façon "
    "identique.",
    ["Concrètement, j'ai écrit les modules Terraform qui décrivent l'ensemble des ressources Azure : le "
     "groupe de ressources, le cluster AKS, le registre d'images, le serveur PostgreSQL managé, la mise en "
     "réseau et le budget de surveillance des coûts. J'ai veillé à ce que cette description soit idempotente, "
     "c'est-à-dire rejouable sans effet de bord, afin que la chaîne d'intégration puisse l'appliquer en toute "
     "confiance.",
     "J'ai également développé le cœur applicatif : l'API FastAPI qui gère les patients, leurs appareils et "
     "leurs rendez-vous, accompagnée de ses sondes de santé et de l'exposition de ses métriques, ainsi que "
     "l'interface React permettant au cabinet de manipuler ces données. J'ai enfin conteneurisé ces "
     "composants dans des images Docker légères et non privilégiées, puis assuré leur déploiement sur le "
     "cluster via Helm."],
    ["À court terme, je remplacerais l'authentification de la chaîne d'intégration par une fédération "
     "d'identité OIDC, qui supprime tout mot de passe stocké et constitue l'état de l'art en matière de "
     "sécurité du déploiement. Je ferais également migrer la base de données vers un accès strictement privé, "
     "sans exposition publique, afin de renforcer l'isolation des données de santé.",
     "À plus long terme, si le périmètre fonctionnel s'élargit, l'API monolithique pourrait être découpée en "
     "services plus fins, et la gestion du schéma de base confiée à un outil de migrations versionnées plutôt "
     "qu'à une création au démarrage, mieux adaptée à une exploitation durable."],
    ["La principale limite de mon périmètre tient aux compromis imposés par le budget. L'accès public à la "
     "base, restreint par un pare-feu n'autorisant que les ressources Azure, reste moins satisfaisant qu'un "
     "réseau entièrement privé que nous avons dû écarter pour rester simples et économes.",
     "De même, la création du schéma au démarrage de l'application convient parfaitement à un MVP mais "
     "montrerait ses limites en production, et le dimensionnement en machines « burstable » plafonne les "
     "performances sous une charge soutenue prolongée."],
    "Le déploiement se résume, côté utilisateur, à renseigner les identifiants Azure dans le dépôt puis à "
    "lancer le workflow de déploiement : l'URL d'accès à l'application s'affiche à la fin de l'exécution. "
    "L'application est ensuite accessible via son Ingress, sa documentation interactive étant publiée à "
    "l'adresse « /api/docs ». L'infrastructure entière peut être recréée à l'identique par une seule commande "
    "Terraform.",
    ["Mon principal défi a été d'industrialiser le provisionnement pour qu'il soit pleinement automatisé et "
     "rejouable, tout en gardant la cohérence entre l'infrastructure et le déploiement applicatif ; cela a "
     "demandé plusieurs itérations, notamment sur la gestion de l'état distant.",
     "Cette expérience a renforcé ma maîtrise de Terraform, de la conteneurisation et du déploiement Helm, "
     "ainsi que ma compréhension d'une API moderne. Je retiens comme axe d'amélioration la nécessité "
     "d'adopter une approche plus incrémentale et systématiquement testée des changements d'infrastructure, "
     "et l'envie d'approfondir la sécurisation réseau du cloud (réseaux privés, points de terminaison "
     "privés)."],
)

individual(
    "PE-2526_%s_RjafellahElyess.pdf" % CODE,
    "Elyess Rjafellah", "CI/CD & automatisation",
    "Ma responsabilité a porté sur la chaîne d'intégration et de déploiement continus. L'ambition était que "
    "l'intégralité du cycle de vie — provisionnement, construction, analyse, déploiement et sauvegarde — "
    "s'exécute automatiquement, sans intervention manuelle, et se rétablisse seul en cas d'aléa.",
    ["J'ai conçu les différents workflows GitHub Actions : celui d'intégration qui valide le code par le "
     "linting et les tests, celui de sécurité qui exécute les analyses, celui de déploiement complet qui "
     "orchestre l'ensemble de la mise en production, et enfin un workflow de sauvegarde planifié "
     "quotidiennement. J'ai aussi automatisé la création de l'emplacement de stockage de l'état Terraform, de "
     "sorte que rien ne doive être préparé à la main au préalable.",
     "Une part importante de mon travail a consisté à fiabiliser ce pipeline face aux situations "
     "intermédiaires : un déploiement interrompu pouvait laisser un verrou sur l'état de l'infrastructure ou "
     "une livraison Helm dans un état instable. J'ai introduit des mécanismes d'auto-réparation qui "
     "détectent et corrigent ces situations, ainsi qu'un ordonnancement correct des dépendances afin que les "
     "composants nécessaires soient toujours installés avant ceux qui en dépendent."],
    ["La première évolution que je viserais est l'adoption du GitOps, avec un outil comme ArgoCD, afin que "
     "l'état du cluster soit piloté de manière déclarative par le contenu du dépôt plutôt que par des "
     "commandes de déploiement. J'introduirais également une authentification fédérée OIDC pour supprimer "
     "tout secret de longue durée.",
     "Je mettrais ensuite en place des environnements distincts — développement, pré-production et "
     "production — avec une promotion contrôlée des versions, ainsi que des tests de bout en bout exécutés "
     "automatiquement après chaque déploiement pour valider la non-régression."],
    ["Le fait de regrouper le provisionnement et le déploiement dans un workflow unique est pratique pour la "
     "démonstration mais allonge la durée d'exécution ; un découpage en étapes parallélisées serait plus "
     "efficace. Par ailleurs, l'authentification par identifiant et mot de passe impose un compte sans "
     "double authentification, ce qui n'est pas adapté à un contexte de production.",
     "Enfin, l'absence d'environnement de pré-production fait que les essais se déroulent directement sur "
     "l'unique cluster, et un déclenchement sur chaque envoi de code pourrait lancer des déploiements "
     "coûteux : un garde-fou mériterait d'être ajouté."],
    "Pour l'utilisateur, tout passe par l'onglet « Actions » du dépôt : le workflow de déploiement met "
    "l'application en production, le même workflow permet de tout détruire en choisissant l'action de "
    "destruction, et le workflow de sauvegarde gère la sauvegarde comme la restauration. Les secrets requis "
    "sont décrits dans la documentation d'installation.",
    ["Mon principal défi a été de rendre le pipeline robuste : à mesure que je rencontrais des échecs liés à "
     "des états intermédiaires, j'ai progressivement ajouté les correctifs nécessaires jusqu'à obtenir une "
     "chaîne qui se rétablit d'elle-même.",
     "J'ai gagné en aisance sur GitHub Actions, l'automatisation de Terraform et le diagnostic des pipelines. "
     "Je retiens comme axe de progression la modularisation des workflows et la mise en place d'une véritable "
     "stratégie multi-environnements associée au GitOps."],
)

individual(
    "PE-2526_%s_NianghaneAdame.pdf" % CODE,
    "Adame Nianghane", "Observabilité & sécurité",
    "J'ai pris en charge la supervision de la plateforme et la sécurité de la chaîne logicielle, deux volets "
    "complémentaires qui conditionnent la confiance que l'on peut accorder à un système en production.",
    ["Du côté de l'observabilité, j'ai déployé la pile Prometheus, Grafana, Loki et Alertmanager. J'ai conçu "
     "un tableau de bord dédié à l'application présentant son débit de requêtes, sa latence au 95e centile, "
     "son taux d'erreurs et sa disponibilité, et j'ai relié les journaux applicatifs afin qu'ils soient "
     "consultables et corrélables depuis la même interface. Des règles d'alerte préviennent l'équipe en cas "
     "d'incident.",
     "Du côté de la sécurité, j'ai intégré dans la chaîne d'intégration des analyses automatiques : Trivy "
     "pour les vulnérabilités des dépendances, de l'infrastructure et des images, CodeQL pour l'analyse "
     "statique du code et Gitleaks pour détecter toute fuite de secret. J'ai complété ce dispositif par un "
     "durcissement de l'exécution : conteneurs non privilégiés, rôles d'accès restreints, cloisonnement "
     "réseau et chiffrement des communications avec la base."],
    ["Je souhaiterais ajouter le traçage distribué, au moyen d'OpenTelemetry et d'un outil tel que Tempo ou "
     "Jaeger, afin de suivre une requête à travers les différents composants et de diagnostiquer finement les "
     "lenteurs. J'aimerais également centraliser la gestion des secrets dans un coffre dédié, avec rotation "
     "automatique.",
     "Enfin, je renforcerais la posture de sécurité du cluster par des politiques avancées — standards de "
     "sécurité des pods, contrôleur d'admission, signature des images — et par des tableaux de bord orientés "
     "objectifs de niveau de service (SLO)."],
    ["Le routage des alertes vers une messagerie d'équipe nécessite un point d'entrée externe qui n'a pas "
     "encore été connecté en production. De même, les politiques de cloisonnement réseau que j'ai préparées "
     "supposent un module réseau capable de les appliquer, qui n'est pas activé sur notre cluster d'étude "
     "afin de rester léger.",
     "Par ailleurs, une véritable conformité à l'hébergement de données de santé imposerait une région et "
     "des services certifiés que nous n'avons pas retenus dans ce cadre, et la rétention volontairement "
     "courte des métriques et journaux limite l'analyse rétrospective."],
    "L'utilisateur accède à la supervision via l'interface Grafana, dont les tableaux de bord sont déjà "
    "chargés ; les journaux y sont consultables grâce à la source de données Loki. Les rapports de sécurité, "
    "quant à eux, sont disponibles dans l'onglet « Security » du dépôt, au format standard SARIF.",
    ["Mon principal défi a été de faire tenir une pile de supervision complète sur un cluster volontairement "
     "réduit, tout en conservant des tableaux de bord réellement exploitables et en garantissant que les "
     "métriques de l'application soient découvertes et collectées automatiquement.",
     "J'ai approfondi ma maîtrise de Prometheus, Grafana et Loki ainsi que des outils DevSecOps, et je "
     "retiens comme axes de progression la mise en œuvre concrète du routage d'alertes et des politiques "
     "réseau, ainsi que l'industrialisation de la gestion des secrets."],
)

individual(
    "PE-2526_%s_DouadiAnis.pdf" % CODE,
    "Anis Douadi", "Orchestration Kubernetes / Helm & on-premise / PRA",
    "J'ai été responsable de l'orchestration des conteneurs sur Kubernetes et du volet hybride du projet, "
    "c'est-à-dire le site on-premise et le plan de reprise d'activité, deux sujets qui touchent directement "
    "à la résilience et à la pérennité des données.",
    ["J'ai conçu le chart Helm qui décrit l'ensemble des objets Kubernetes de l'application : les "
     "déploiements, le service, l'exposition par l'Ingress, le secret de connexion, l'autoscaling et la "
     "définition de la supervision. J'ai paramétré l'ajustement automatique du nombre de répliques, les "
     "politiques de cloisonnement réseau et le contexte de sécurité des conteneurs.",
     "Pour le volet hybride, j'ai provisionné une machine virtuelle représentant un site on-premise, placée "
     "dans un réseau totalement séparé de celui du cluster. J'y ai installé, au moyen de playbooks Ansible, "
     "un stockage objet MinIO chiffré qui reçoit les sauvegardes de la base, et j'ai écrit les procédures "
     "automatisées de sauvegarde et de restauration."],
    ["La première évolution consisterait à activer un module réseau appliquant réellement les politiques de "
     "cloisonnement, pour obtenir une isolation effective entre composants. Je viserais ensuite une haute "
     "disponibilité répartie sur plusieurs zones et une réplication géographique des sauvegardes.",
     "Je souhaiterais également externaliser les sauvegardes vers un stockage redondant et planifier des "
     "tests de restauration réguliers et automatiques, afin de vérifier en continu l'efficacité du plan de "
     "reprise, ainsi que relier un véritable site physique par un lien sécurisé de type VPN."],
    ["Le site on-premise est ici simulé par une machine virtuelle placée dans un réseau distinct : "
     "l'isolation est représentative d'un site séparé, mais il ne s'agit pas d'un véritable centre de "
     "données physique. De plus, la restauration ramène l'état au moment de la dernière sauvegarde, si bien "
     "que la perte de données potentielle dépend de la fréquence des sauvegardes.",
     "Enfin, le stockage MinIO fonctionne en instance unique, sans redondance, et l'architecture réseau "
     "retenue pour le cluster limite l'application stricte des politiques de cloisonnement."],
    "Concrètement, la console MinIO permet de visualiser les sauvegardes chiffrées présentes dans leur "
    "espace dédié, et les opérations de sauvegarde comme de restauration se déclenchent depuis le workflow "
    "prévu à cet effet. Le chart Helm est entièrement paramétrable, ce qui permet d'adapter le registre "
    "d'images, le nom d'hôte ou l'activation des politiques selon l'environnement.",
    ["Mon principal défi a été d'orchestrer la réplication des données du cloud vers l'on-premise de façon "
     "fiable et rejouable : j'ai notamment dû rendre la restauration idempotente, afin qu'elle fonctionne "
     "même sur une base déjà peuplée, et automatiser entièrement la configuration de la machine distante.",
     "J'ai consolidé mes compétences sur Kubernetes, Helm et Ansible, ainsi que sur la conception d'un plan "
     "de reprise d'activité. Je retiens comme axes de progression le passage à une haute disponibilité "
     "multi-zones et l'automatisation de tests de restauration réguliers."],
)

print("=== TERMINÉ ===")
