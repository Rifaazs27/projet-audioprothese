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


def blocks(items):
    """items : liste de (type, valeur). type in H1,H2,P,FLOW."""
    out = []
    for kind, val in items:
        if kind == "H1":
            # Ne saute une page que s'il reste peu de place : évite les
            # titres orphelins en bas de page sans créer de pages vides.
            out.append(CondPageBreak(6 * cm))
            out.append(H1(val))
        elif kind == "H2":
            out.append(Paragraph(val, H2))
        elif kind == "P":
            out.append(P(val))
        elif kind == "FLOW":
            out.append(val)
    return out


# =================================================================== GROUPE
g = cover(
    "Document technique final",
    "Plateforme de gestion d'un cabinet d'audioprothèse\nSolution DevOps hybride sur Microsoft Azure",
    [["Équipe", "Zaafir Mougammadou Zaccaria · Elyess Rjafellah · Adame Nianghane · Anis Douadi"],
     ["Classe / Promo", "M2 DO C — 2025-2026"],
     ["Période", PERIODE],
     ["Client", "Cabinet d'audioprothèse « AudioPro » (commanditaire)"],
     ["Dépôt", "github.com/Rifaazs27/projet-audioprothese"],
     ["Nature", "Rendu de groupe — solution technique complète"]])

g += blocks([
    ("H1", "1. Présentation de l'entreprise et de l'équipe"),
    ("P", "« AudioPro » est un cabinet d'audioprothèse qui accompagne ses patients tout au long de leur "
     "appareillage. Son activité quotidienne repose sur le suivi d'un ensemble d'informations sensibles : le "
     "dossier de chaque patient, les appareils auditifs qui lui sont posés et le calendrier des rendez-vous de "
     "contrôle. Jusqu'ici gérées de façon dispersée, ces données méritaient une plateforme centralisée, "
     "fiable et sécurisée, capable de garantir la confidentialité exigée par la réglementation sur les données "
     "de santé tout en restant disponible et simple d'usage pour les praticiens."),
    ("P", "Le cabinet a confié à notre équipe la conception et la mise en production de cette plateforme, non "
     "pas comme une simple application isolée, mais comme un <b>système complet exploité selon les pratiques "
     "DevOps</b> : automatisation des déploiements, infrastructure décrite sous forme de code, supervision "
     "permanente, sécurité intégrée à chaque étape et capacité à se rétablir après incident."),
    ("P", "Notre équipe est composée de quatre étudiants de la classe M2 DO C. Afin de couvrir l'intégralité "
     "du périmètre sans recouvrement inutile, nous avons réparti les responsabilités par grands domaines "
     "techniques, chacun étant pilote sur son sujet tout en contribuant aux revues de code et aux décisions "
     "d'architecture communes :"),
    ("FLOW", wrap_table(TEAM, TEAMW)),
])

g += blocks([
    ("H1", "2. Analyse de la problématique et solution proposée"),
    ("P", "La problématique dépasse le simple développement d'un logiciel. Les données manipulées étant des "
     "données de santé, la <b>confidentialité</b> et la <b>traçabilité</b> sont impératives. Le service devant "
     "être utilisé au quotidien par le cabinet, sa <b>disponibilité</b> et sa capacité d'<b>auto-"
     "rétablissement</b> sont essentielles. La solution doit en outre rester <b>économe</b> — le projet "
     "s'inscrit dans le cadre d'un compte Azure for Students plafonné à 85 dollars — et entièrement "
     "<b>reproductible</b>."),
    ("P", "Pour répondre à ces exigences, nous avons conçu une application web conteneurisée — une interface "
     "React, une API FastAPI et une base PostgreSQL managée — déployée sur un cluster Kubernetes managé "
     "(Azure AKS) et encadrée par une chaîne DevOps de bout en bout. Conformément au cahier des charges, "
     "l'architecture est <b>hybride</b> : le cloud héberge l'application tandis qu'un site on-premise (simulé "
     "par un réseau séparé) accueille le stockage objet chiffré des sauvegardes."),
    ("P", "Le schéma ci-dessous synthétise cette architecture, du poste du développeur jusqu'à l'exécution "
     "supervisée en production et la réplication des sauvegardes vers l'on-premise :"),
    ("FLOW", Spacer(1, 4)), ("FLOW", architecture()), ("FLOW", Spacer(1, 6)),
    ("P", "Le flux est le suivant : chaque modification poussée par un développeur déclenche le pipeline "
     "d'intégration et de déploiement, qui teste le code, en vérifie la sécurité, construit les images, les "
     "publie dans Azure Container Registry puis les déploie sur le cluster via Helm. L'application est exposée "
     "aux utilisateurs par un Ingress unique ; le backend dialogue avec PostgreSQL en TLS ; la supervision et "
     "les sauvegardes fonctionnent en continu et de façon autonome."),
])

# ---------------------------------------------------- 3. FINOPS (très détaillé)
COST = [
    ["Ressource", "Dimensionnement", "Coût 24/7", "Justification du choix"],
    ["AKS — plan de contrôle", "Free tier", "0 $", "Kubernetes managé sans SLA payant : suffisant pour un MVP."],
    ["AKS — nœuds", "2 × Standard_B2s_v2", "≈ 60–70 $", "Machines « burstable » ; 2 nœuds pour héberger app + ingress + monitoring."],
    ["Base de données", "PostgreSQL Flexible B1ms", "≈ 13 $", "Palier burstable le moins cher, adapté à un volume modéré."],
    ["Registre d'images", "ACR Basic", "≈ 5 $", "SKU minimal, quota d'images largement suffisant."],
    ["VM on-premise", "Standard_B2s_v2", "≈ 30 $", "Héberge MinIO ; éteignable ou désactivable via une variable."],
    ["Réseau (LB + IP)", "Standard", "≈ 6–9 $", "Un seul point d'entrée public mutualisé par l'Ingress."],
    ["Stockage état + backups", "Standard_LRS", "≈ 1 $", "Redondance locale, volumétrie faible."],
]
SCEN = [
    ["Scénario d'exploitation", "Principe", "Coût estimé sur le semestre"],
    ["Tout allumé en continu (24/7)", "Infrastructure jamais arrêtée pendant 6 mois",
     "≈ 650–750 $ — dépasse très largement le crédit de 85 $"],
    ["Allumage à la demande (start/stop)", "Cluster et VM démarrés seulement pour travailler/tester",
     "≈ 30–50 $ sur le semestre"],
    ["Destruction après chaque session (retenu)", "terraform destroy après chaque démo, reconstruction en ~14 min",
     "≈ 10–20 $ sur le semestre"],
]
ARB = [
    ["Besoin", "Option « complète » (cahier)", "Option retenue (MVP)", "Gain FinOps"],
    ["Logs", "ELK (Elasticsearch)", "Loki + Promtail", "≈ −70 % de RAM et de stockage indexé"],
    ["Secrets", "Vault auto-hébergé", "GitHub Secrets + Secret K8s", "Aucun pod ni stockage à héberger"],
    ["Haute dispo. base", "Multi-zone (réplique)", "Zone unique", "≈ −50 % sur la base"],
    ["Exposition Grafana", "LoadBalancer dédié", "Ingress mutualisé (nip.io)", "−1 adresse IP publique"],
    ["Traçage", "Jaeger + backend dédié", "Reporté (perspective)", "Ressources économisées"],
]
KPI = [
    ["Indicateur FinOps", "Valeur cible / observée"],
    ["Coût mensuel si allumé en continu", "≈ 110–125 $ / mois"],
    ["Coût réel estimé sur le semestre", "≈ 10–20 $ (grâce à la destruction à la demande)"],
    ["Part du crédit de 85 $ consommée", "≈ 15–25 %"],
    ["Temps de reconstruction complète", "≈ 12–14 minutes (automatisé)"],
    ["Seuils d'alerte budgétaire", "50 % / 80 % / 100 % (courriel)"],
]
g += blocks([
    ("H1", "3. Gestion des coûts — démarche FinOps (M2)"),
    ("P", "Le FinOps (Financial Operations) désigne la discipline consistant à donner à une équipe technique "
     "la responsabilité et la visibilité de ses dépenses cloud, afin de prendre des décisions d'architecture "
     "éclairées par leur coût. Dans notre projet, cette discipline n'a pas été un exercice théorique : le "
     "crédit étudiant est plafonné à <b>85 dollars, non rechargeable et sans carte bancaire de secours</b>. "
     "Chaque choix technique a donc été pesé à l'aune de son impact financier, ce qui correspond précisément "
     "à l'esprit de la spécialisation M2."),

    ("H2", "3.1 La démarche adoptée : informer, optimiser, opérer"),
    ("P", "Nous avons structuré notre travail selon les trois phases du cycle FinOps de référence. La phase "
     "d'<b>information</b> a consisté à rendre chaque coût visible : étiquetage systématique des ressources, "
     "estimation préalable avant tout déploiement et suivi via Azure Cost Management. La phase "
     "d'<b>optimisation</b> a porté sur le dimensionnement au plus juste et le choix d'alternatives moins "
     "coûteuses à service équivalent. La phase d'<b>opération</b> a industrialisé la maîtrise des coûts : "
     "budget avec alertes, extinction et reconstruction automatisées, de sorte que la sobriété ne repose pas "
     "sur la discipline manuelle mais sur des mécanismes outillés."),

    ("H2", "3.2 Inventaire et estimation détaillée des coûts"),
    ("P", "Le tableau ci-dessous détaille, ressource par ressource, le dimensionnement retenu, le coût "
     "indicatif mensuel si la ressource fonctionnait en continu, et la justification du choix. Les montants "
     "sont donnés en dollars, à titre indicatif, sur la base des tarifs de la région Poland Central :"),
    ("FLOW", wrap_table(COST, [3.6 * cm, 3.4 * cm, 2.0 * cm, CONTENT_W - 9.0 * cm])),
    ("FLOW", Spacer(1, 8)),
    ("P", "La répartition mensuelle de ces coûts (en fonctionnement continu) fait clairement ressortir la "
     "prédominance du calcul, sur lequel se sont concentrés nos efforts d'optimisation :"),
    ("FLOW", barh([("AKS (2 nœuds)", 65), ("VM on-premise", 30), ("PostgreSQL", 13),
                   ("Réseau (LB + IP)", 8), ("Registre ACR", 5), ("Stockage", 1)])),
    ("FLOW", Spacer(1, 6)),
    ("P", "Le poste le plus lourd est le pool de nœuds AKS, suivi de la machine virtuelle on-premise. C'est "
     "logiquement sur ces deux postes que nous avons concentré nos efforts d'optimisation, en privilégiant des "
     "machines « burstable » de la série B — dont le tarif est réduit tant que la charge moyenne reste faible, "
     "ce qui est le cas d'un MVP — et en rendant la VM on-premise entièrement optionnelle grâce à une variable "
     "Terraform permettant de la désactiver lorsque le volet hybride n'est pas démontré."),

    ("H2", "3.3 Scénarios d'exploitation et projection budgétaire"),
    ("P", "Le coût réel d'un projet cloud dépend moins du dimensionnement que de la <b>durée pendant laquelle "
     "les ressources restent allumées</b>. Nous avons donc raisonné en scénarios plutôt qu'en simple montant "
     "mensuel :"),
    ("FLOW", wrap_table(SCEN, [4.6 * cm, 5.4 * cm, CONTENT_W - 10.0 * cm])),
    ("P", "Ce raisonnement a été déterminant : laisser l'infrastructure allumée en permanence aurait épuisé le "
     "crédit en moins d'un mois. En adoptant une logique de <b>destruction après chaque session</b> — rendue "
     "indolore par l'automatisation, puisque l'ensemble se reconstruit en une douzaine de minutes — nous "
     "avons ramené la dépense réelle à une fraction du crédit disponible, tout en conservant la capacité de "
     "démontrer une infrastructure complète à tout moment."),

    ("H2", "3.4 Leviers d'optimisation appliqués"),
    ("P", "Plusieurs leviers concrets ont été mis en œuvre. Le premier est le <b>rightsizing</b> : nous "
     "n'avons provisionné que la puissance strictement nécessaire (plan de contrôle Kubernetes gratuit, nœuds "
     "burstable, base au palier le plus bas), quitte à accepter des performances plafonnées sous forte charge, "
     "acceptables pour un MVP. Le deuxième levier est le <b>choix d'outils économes</b> : pour la "
     "centralisation des journaux, nous avons retenu Loki plutôt qu'Elasticsearch, car Loki n'indexe que les "
     "métadonnées et consomme une fraction des ressources — un point développé au paragraphe suivant."),
    ("P", "Le troisième levier concerne la <b>rétention des données</b> : les métriques ne sont conservées que "
     "quelques jours et les sauvegardes une semaine, ce qui limite le stockage facturé. Le quatrième est un "
     "<b>autoscaling borné</b> : le nombre de répliques de l'API peut augmenter automatiquement sous charge, "
     "mais dans une limite haute stricte, afin qu'un pic — ou une erreur — ne puisse jamais provoquer une "
     "dérive de coût. Enfin, nous avons <b>mutualisé l'exposition réseau</b> : Grafana est publié via "
     "l'Ingress existant grâce à un nom d'hôte nip.io, ce qui évite de provisionner une seconde adresse IP "
     "publique facturée."),

    ("H2", "3.5 Arbitrages structurants et alternatives écartées"),
    ("P", "Certains choix relèvent d'un arbitrage assumé entre l'exhaustivité décrite dans le cahier des "
     "charges et la sobriété imposée par le budget. Le tableau suivant récapitule ces arbitrages, l'option "
     "« complète » qui aurait été retenue sans contrainte, l'option effectivement mise en œuvre et le gain "
     "obtenu :"),
    ("FLOW", wrap_table(ARB, [2.6 * cm, 4.2 * cm, 4.6 * cm, CONTENT_W - 11.4 * cm])),
    ("P", "Le cas d'ELK contre Loki est le plus illustratif : une pile Elasticsearch réclame plusieurs "
     "gigaoctets de mémoire et un stockage indexé volumineux, ce qui aurait nécessité des nœuds plus puissants "
     "et donc bien plus coûteux. Loki, en n'indexant que les étiquettes, offre les mêmes usages "
     "(centralisation, recherche, visualisation dans Grafana) pour une empreinte très inférieure. De même, un "
     "coffre de secrets auto-hébergé aurait ajouté des composants à faire tourner et à sauvegarder, alors que "
     "les secrets de la chaîne sont parfaitement gérés par le mécanisme intégré de GitHub, sans coût "
     "d'infrastructure."),

    ("H2", "3.6 Gouvernance budgétaire et suivi"),
    ("P", "La maîtrise des coûts ne repose pas seulement sur des choix de conception, mais aussi sur une "
     "<b>gouvernance</b> outillée. Un budget Azure a été défini au niveau du groupe de ressources, assorti "
     "d'alertes par courriel déclenchées à 50 %, 80 % et 100 % du plafond mensuel : l'équipe est ainsi "
     "prévenue avant toute dérive. Toutes les ressources portent des étiquettes (projet, cours, gestionnaire) "
     "qui permettent de filtrer les dépenses dans Azure Cost Management et d'attribuer chaque euro à un poste "
     "précis. Le tableau d'indicateurs ci-dessous synthétise notre pilotage financier :"),
    ("FLOW", wrap_table(KPI, [7.5 * cm, CONTENT_W - 7.5 * cm])),

    ("H2", "3.7 Bilan FinOps"),
    ("P", "Au terme du projet, la démarche FinOps a atteint son objectif : une infrastructure complète — "
     "cluster Kubernetes, base managée, registre, supervision, site on-premise — a été conçue, déployée et "
     "démontrée tout en ne consommant qu'une faible part du crédit de 85 dollars. Au-delà de l'économie "
     "réalisée, cette contrainte a eu une vertu pédagogique : elle nous a forcés à justifier chaque ressource, "
     "à comparer des alternatives et à intégrer le coût comme un critère de conception à part entière, au même "
     "titre que la performance ou la sécurité — ce qui constitue précisément la compétence attendue en M2."),
])

# ---------------------------------------------------- 4. Organisation
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
g += blocks([
    ("H1", "4. Organisation de l'équipe, planification et méthodologie"),
    ("P", "Nous avons adopté une organisation agile inspirée de Scrum et de Kanban, rythmée par des sprints de "
     "deux semaines et une priorisation des tâches selon la méthode MoSCoW. Le dépôt Git a servi de point "
     "central : chaque évolution passait par une branche puis une revue de code (Pull Request) avant d'être "
     "intégrée, garantissant la qualité et le partage de connaissances entre les membres. Les outils "
     "mobilisés sont représentatifs d'une chaîne DevOps professionnelle : Git et GitHub Actions pour "
     "l'intégration et le déploiement continus, Terraform et Ansible pour la gestion de configuration, et "
     "Helm pour le packaging Kubernetes."),
    ("P", "Le projet s'est déroulé sur le second semestre de l'année universitaire, de janvier à juin 2026. "
     "Le diagramme de Gantt ci-dessous retrace l'enchaînement des grandes phases, du cadrage initial à la "
     "rédaction des livrables et à l'enregistrement de la vidéo de démonstration :"),
    ("FLOW", Spacer(1, 4)), ("FLOW", gantt()), ("FLOW", Spacer(1, 8)),
    ("P", "La répartition des contributions, équilibrée entre les quatre membres, est détaillée ci-dessous. "
     "Chaque contributeur a piloté un domaine tout en participant aux décisions transverses ; la traçabilité "
     "individuelle est consultable dans l'historique du dépôt et la vue « Contributors » de GitHub."),
    ("FLOW", wrap_table(CONTRIB, [4.6 * cm, CONTENT_W - 4.6 * cm])),
])

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
g += blocks([
    ("H1", "5. Présentation de la solution technique"),
    ("P", "Sur le plan fonctionnel, l'application couvre les trois besoins métier du cabinet : la gestion des "
     "<b>patients</b>, l'<b>enregistrement des appareils auditifs</b> qui leur sont posés (marque, modèle, "
     "numéro de série, oreille, date de pose) et la <b>planification des rendez-vous</b> de suivi, assortie "
     "d'une vue d'ensemble des rendez-vous à venir. Ces fonctionnalités s'appuient sur l'ensemble cohérent de "
     "technologies ci-dessous, chacune choisie pour sa pertinence et son coût d'exploitation :"),
    ("FLOW", wrap_table(STACK, [5 * cm, CONTENT_W - 5 * cm])),
    ("FLOW", Spacer(1, 6)),
    ("FLOW", screenshot("assets/app_dossier.png")),
    ("FLOW", Spacer(1, 2)),
    ("P", "<i>L'application en fonctionnement : dossier patient avec l'enregistrement des appareils auditifs "
     "et la prise de rendez-vous.</i>"),
    ("P", "<b>Déploiement automatisé.</b> Un simple envoi de code sur la branche principale, ou un "
     "déclenchement manuel, suffit à provisionner l'infrastructure, construire et analyser les images, puis "
     "déployer l'application — sans aucune manipulation manuelle. Le pipeline enchaîne la connexion à Azure, "
     "l'application Terraform, la construction et la publication des images, un scan de vulnérabilités "
     "bloquant, l'installation de l'Ingress et de la supervision, le déploiement de l'application puis la "
     "configuration du stockage de sauvegarde. Il est conçu pour se rétablir seul en cas d'interruption."),
    ("FLOW", Spacer(1, 4)),
    ("FLOW", flow_vertical(["Connexion Azure (identifiants sécurisés)",
                            "Terraform apply — provisionnement de l'infra",
                            "Build & push des images vers ACR",
                            "Scan de sécurité Trivy (bloquant)",
                            "Installation Ingress + supervision",
                            "Déploiement Helm de l'application",
                            "Configuration MinIO on-premise (Ansible)"])),
    ("FLOW", Spacer(1, 6)),
    ("P", "<b>Orchestration et résilience.</b> L'application est packagée sous forme de chart Helm et exécutée "
     "sur Kubernetes, qui assure le redémarrage automatique des conteneurs défaillants et l'ajustement du "
     "nombre de répliques selon la charge. Les conteneurs s'exécutent sans privilèges, le réseau interne est "
     "cloisonné et l'accès à l'API du cluster est régi par des rôles (RBAC)."),
    ("P", "<b>Observabilité et sécurité.</b> L'API expose ses propres métriques, collectées par Prometheus et "
     "visualisées dans Grafana ; les journaux sont centralisés via Loki et les alertes routées vers une "
     "messagerie d'équipe. À chaque livraison, le code et les images sont analysés par Trivy, CodeQL et "
     "Gitleaks, et aucune image présentant une vulnérabilité critique n'est déployée."),
    ("P", "<b>Reprise d'activité.</b> Les données sont sauvegardées de façon chiffrée vers le stockage MinIO "
     "hébergé sur le site on-premise, et restaurables automatiquement via Ansible. Ce mécanisme a été "
     "<b>validé en conditions réelles</b> : après avoir créé une donnée témoin, l'avoir sauvegardée puis "
     "volontairement supprimée, la restauration a permis de la retrouver à l'identique. L'ensemble de la "
     "solution a été déployé, testé de bout en bout et jugé conforme aux attentes du cahier des charges."),
    ("FLOW", Spacer(1, 6)),
    ("FLOW", KeepTogether([
        flow_horizontal([["Donnée", "créée"], ["Sauvegarde", "MinIO chiffré"],
                         ["Perte", "simulée"], ["Restauration", "(Ansible)"],
                         ["Donnée", "récupérée"]]),
        Spacer(1, 4),
        P("<i>Cycle de reprise d'activité validé en conditions réelles : de la création d'une donnée à sa "
          "récupération après sauvegarde et perte simulée.</i>"),
    ])),
])

build("PE-2526_%s_Mougammadou_Rjafellah_Nianghane_Douadi.pdf" % CODE, g)


# =============================================================== INDIVIDUELS
def individual(fichier, nom, role, infos_role, body_blocks):
    s = cover("Rendu individuel", "%s\n%s" % (nom, role),
              [["Auteur", nom], ["Rôle", role], ["Classe / Promo", "M2 DO C — 2025-2026"],
               ["Période", PERIODE],
               ["Projet", "Plateforme de gestion d'un cabinet d'audioprothèse"],
               ["Domaine", infos_role]])
    # Le contenu s'enchaîne naturellement ; un saut de page conditionnel
    # (dans blocks) évite les titres orphelins sans laisser de pages vides.
    s += blocks(body_blocks)
    build(fichier, s)
