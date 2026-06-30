# -*- coding: utf-8 -*-
from gen_pdf import *  # noqa

# ====================================================================== GROUPE
team = table([
    ["Membre", "Rôle principal", "Périmètre"],
    ["Zaafir Mougammadou Zaccaria", "Infrastructure & déploiement",
     "Terraform (AKS, ACR, PostgreSQL, réseau, budget), application FastAPI + React, déploiement applicatif"],
    ["Elyess Rjafellah", "CI/CD & automatisation",
     "GitHub Actions (deploy, backup, CI, sécurité), état Terraform distant, pipeline auto-réparant"],
    ["Adame Nianghane", "Observabilité & sécurité",
     "Prometheus / Grafana / Loki / Alertmanager, DevSecOps (Trivy, CodeQL, Gitleaks), RBAC, TLS, RGPD"],
    ["Anis Douadi", "Kubernetes & on-premise / PRA",
     "Chart Helm, HPA, NetworkPolicies, VM on-premise, MinIO chiffré, Ansible, sauvegarde / restauration"],
], col_widths=[5 * cm, 3.6 * cm, 8.4 * cm])

g = cover(["Document technique final"],
          "Plateforme de gestion de cabinet d'audioprothèse — Solution DevOps hybride",
          extra=team)

# 1
g += [Paragraph("1. Présentation de l'entreprise et de l'équipe", H1),
      P("<b>Le client.</b> « AudioPro » est un cabinet d'audioprothèse qui assure le suivi de patients "
        "appareillés. Le cabinet doit gérer un référentiel de patients, leurs appareils auditifs et les "
        "rendez-vous de suivi, tout en garantissant la confidentialité des données de santé, la disponibilité "
        "du service et la maîtrise des coûts informatiques."),
      P("<b>La mission.</b> Concevoir et déployer, dans une démarche DevOps complète, une plateforme web "
        "fiable, sécurisée et supervisée, reproductible et automatisée de bout en bout."),
      P("<b>L'équipe projet.</b> Quatre étudiants de Mastère DevOps, avec une répartition des rôles "
        "complémentaire couvrant l'ensemble de la chaîne (développement, infrastructure, automatisation, "
        "observabilité, sécurité, orchestration, reprise d'activité) :"),
      team]

# 2
g += [PageBreak(), Paragraph("2. Analyse de la problématique et solution proposée", H1),
      Paragraph("2.1 Problématique", H2),
      bullets([
          "<b>Données sensibles</b> : informations de santé soumises au RGPD (confidentialité, traçabilité).",
          "<b>Disponibilité</b> : le service doit rester accessible et se rétablir seul en cas d'incident.",
          "<b>Sécurité</b> : chaîne logicielle et exécution durcies, secrets jamais exposés.",
          "<b>Scalabilité</b> : absorber des pics de charge sans intervention manuelle.",
          "<b>Coûts</b> : rester dans le budget d'un compte Azure for Students (85 $).",
          "<b>Reproductibilité</b> : pouvoir reconstruire l'ensemble à l'identique et automatiquement.",
      ]),
      Paragraph("2.2 Solution proposée", H2),
      P("Une application web conteneurisée (API FastAPI, frontend React, base PostgreSQL) déployée sur un "
        "cluster <b>Kubernetes managé (Azure AKS)</b>, encadrée par une chaîne DevOps complète : "
        "infrastructure as code (Terraform), intégration et déploiement continus (GitHub Actions), "
        "supervision (Prometheus / Grafana / Loki), sécurité intégrée (DevSecOps) et plan de reprise "
        "d'activité. L'architecture est <b>hybride</b> : le cloud héberge l'application, un site "
        "<b>on-premise simulé</b> (réseau séparé) héberge le stockage objet chiffré (MinIO) des sauvegardes."),
      Paragraph("2.3 Architecture (vue d'ensemble)", H2),
      P("Développeur → <b>GitHub</b> → <b>GitHub Actions</b> (lint, tests, scans de sécurité, build, "
        "déploiement) → images poussées sur <b>Azure Container Registry</b> → déploiement <b>Helm</b> sur "
        "<b>AKS</b>. Les utilisateurs accèdent à l'application via un <b>Ingress NGINX</b> ; le backend "
        "communique avec <b>PostgreSQL Flexible Server</b> (TLS). La supervision (Prometheus/Grafana/Loki/"
        "Alertmanager) et la sécurité (RBAC, NetworkPolicies, secrets) sont intégrées au cluster. Les "
        "sauvegardes chiffrées sont répliquées vers une <b>VM on-premise</b> (MinIO), pilotée par Ansible."),
      ]

# 3
cost = table([
    ["Ressource", "Dimensionnement", "Coût indicatif 24/7"],
    ["AKS — plan de contrôle", "Free tier", "0 $"],
    ["AKS — nœuds", "2 × Standard_B2s_v2", "~60-70 $/mois"],
    ["PostgreSQL Flexible", "B_Standard_B1ms", "~13 $/mois"],
    ["Azure Container Registry", "Basic", "~5 $/mois"],
    ["VM on-premise (MinIO)", "Standard_B2s_v2", "~30 $/mois"],
    ["Équilibreurs / IP publiques", "Standard", "~6-9 $/mois"],
], col_widths=[6 * cm, 5 * cm, 6 * cm])
g += [PageBreak(), Paragraph("3. Gestion des coûts — FinOps (spécifique M2)", H1),
      P("Le compte Azure for Students est limité à <b>85 $</b>, sans carte bancaire : la maîtrise des coûts "
        "est une contrainte de conception."),
      cost,
      Paragraph("3.1 Leviers d'optimisation", H2),
      bullets([
          "Plan de contrôle AKS gratuit, nœuds <b>burstable</b> (série B), SKU minimaux partout.",
          "<b>Loki</b> à la place d'ELK (indexation des labels uniquement) : coût d'exploitation très réduit.",
          "Secrets dans GitHub Actions plutôt qu'un Key Vault hébergé : moins de ressources facturées.",
          "Rétention courte (métriques 3 j, sauvegardes 7 j) et autoscaling <b>borné</b> (HPA max 2).",
          "Grafana exposé via l'Ingress existant (pas d'IP publique supplémentaire).",
      ]),
      Paragraph("3.2 Garde-fous et extinction", H2),
      bullets([
          "<b>Budget Azure</b> avec alertes e-mail à 50 / 80 / 100 % du plafond mensuel.",
          "Étiquetage (tags) de toutes les ressources pour le suivi analytique (Cost Management).",
          "<b>Teardown en un clic</b> (workflow Deploy → action <i>destroy</i>) : facturation ramenée à ~0 $ "
          "hors période de démonstration ; reconstruction complète en ~12-14 min.",
      ])]

# 4
gantt = table([
    ["Jalon", "Échéance", "Livrable"],
    ["M1 — Cadrage", "Kick-off +1 mois", "Backlog, architecture, choix FinOps"],
    ["M2 — MVP applicatif", "+3 mois", "Application conteneurisée + tests"],
    ["M3 — Déploiement cloud", "+4,5 mois", "Infra Terraform + CI/CD + monitoring"],
    ["M4 — Vidéo MVP", "+6 mois", "Démonstration en production"],
    ["M5 — Rendu technique", "+6 mois", "Dépôt + documentation + analyse"],
], col_widths=[4.5 * cm, 4 * cm, 8.5 * cm])
g += [PageBreak(), Paragraph("4. Organisation, planification et méthodologie", H1),
      Paragraph("4.1 Méthodologie", H2),
      P("Démarche <b>agile (Scrum/Kanban)</b> en sprints de deux semaines, priorisation MoSCoW. "
        "Outils professionnels : Git/GitHub (versioning + revues de code via Pull Requests), GitHub Actions "
        "(CI/CD), Terraform et Ansible (gestion de configuration), Helm (packaging Kubernetes)."),
      Paragraph("4.2 Planification", H2),
      gantt,
      Paragraph("4.3 Contributions individuelles", H2),
      P("Le travail a été réparti de façon équilibrée ; chaque membre est responsable d'un domaine de la "
        "chaîne DevOps et a contribué au dépôt versionné (commits, PR, revues). La traçabilité est visible "
        "dans l'historique Git et l'onglet <i>Insights → Contributors</i> de GitHub."),
      team]

# 5
stack = table([
    ["Domaine", "Technologies"],
    ["Backend", "Python 3.11, FastAPI, SQLAlchemy, Pydantic"],
    ["Frontend", "React 18, Vite (servi par nginx non-root)"],
    ["Base de données", "PostgreSQL 16 (Azure Flexible Server, TLS)"],
    ["Conteneurs / Orchestration", "Docker (images non-root), Kubernetes (AKS), Helm"],
    ["IaC / Configuration", "Terraform (azurerm), Ansible"],
    ["CI/CD", "GitHub Actions (deploy, backup, CI, sécurité)"],
    ["Observabilité", "Prometheus, Grafana, Loki, Alertmanager"],
    ["Sécurité", "Trivy, CodeQL, Gitleaks, RBAC, NetworkPolicies, TLS"],
    ["On-premise / PRA", "VM Linux, MinIO chiffré (SSE), sauvegarde/restauration Ansible"],
], col_widths=[5 * cm, 12 * cm])
g += [PageBreak(), Paragraph("5. Présentation de la solution technique", H1),
      stack,
      Paragraph("5.1 CI/CD — déploiement 100 % automatisé", H2),
      P("Un <b>push sur la branche principale</b> (ou un déclenchement manuel) provisionne l'infrastructure "
        "(Terraform), construit et scanne les images, puis déploie l'application via Helm — sans aucune étape "
        "manuelle. Étapes : connexion Azure → état Terraform → <i>apply</i> → build/push ACR → scan Trivy "
        "(bloquant si vulnérabilité critique) → installation Ingress + monitoring → déploiement de l'app → "
        "configuration MinIO (Ansible). Le pipeline est <b>auto-réparant</b> (gestion des verrous d'état et "
        "des releases bloquées)."),
      Paragraph("5.2 Orchestration Kubernetes", H2),
      bullets([
          "Chart <b>Helm</b> paramétrable (Deployments, Services, Ingress, Secret, HPA).",
          "<b>HPA</b> (autoscaling CPU), sondes <i>liveness/readiness</i>, auto-réparation des pods.",
          "<b>RBAC</b>, <b>NetworkPolicies</b> et <i>securityContext</i> durci (non-root, capabilities drop).",
      ]),
      Paragraph("5.3 Observabilité", H2),
      P("Métriques exposées par l'API (<code>/metrics</code>) et collectées par Prometheus ; tableaux de bord "
        "Grafana (débit, latence p95, taux d'erreurs, disponibilité) ; logs centralisés via Loki ; alertes "
        "routées par Alertmanager vers Slack/Teams."),
      Paragraph("5.4 Sécurité (DevSecOps)", H2),
      P("Scans automatiques à chaque exécution : Trivy (dépendances, IaC, images), CodeQL (analyse statique), "
        "Gitleaks (fuite de secrets). Chiffrement TLS de la base, secrets jamais versionnés, hébergement en "
        "région européenne (RGPD)."),
      Paragraph("5.5 PRA / PCA — testé et prouvé", H2),
      P("Sauvegarde chiffrée de la base vers MinIO (on-premise) et restauration automatisée via Ansible. "
        "Le cycle complet a été <b>validé en conditions réelles</b> : création d'une donnée témoin → "
        "sauvegarde → suppression (perte simulée) → restauration → donnée récupérée. La continuité de service "
        "(PCA) est assurée par l'auto-réparation Kubernetes."),
      Paragraph("5.6 Validation", H2),
      P("La solution a été déployée et testée de bout en bout : application et API fonctionnelles, base "
        "joignable, supervision active, résilience vérifiée (recréation automatique des pods), scans de "
        "sécurité au vert, et PRA prouvé. L'ensemble est reproductible automatiquement.")]

build("PE-2526_%s_Mougammadou_Rjafellah_Nianghane_Douadi.pdf" % CODE, g)


# ================================================================== INDIVIDUELS
def individual(nom_fichier, nom_complet, role, domaine_intro, realisations,
               perspectives, limites, doc_utilisateur, defis, forces, faiblesses,
               competences, axes):
    s = cover(["Rendu individuel"], "%s — %s" % (nom_complet, role),
              extra=Paragraph("Document technique final — partie individuelle", CENTER))
    s += [Paragraph("1. Contribution au projet", H1), P(domaine_intro),
          Paragraph("Réalisations principales", H2), bullets(realisations),
          Paragraph("2. Perspectives d'évolution", H1),
          P("Réflexion sur l'avenir de l'infrastructure / de la solution sur mon périmètre :"),
          bullets(perspectives),
          PageBreak(),
          Paragraph("3. Analyse critique des limites techniques rencontrées", H1),
          bullets(limites),
          Paragraph("4. Annexes", H1),
          Paragraph("4.1 Documentation utilisateur (extrait de mon périmètre)", H2),
          bullets(doc_utilisateur),
          Paragraph("4.2 Analyse personnelle", H2),
          Paragraph("Défis rencontrés", H2), P(defis),
          Paragraph("Forces", H2), bullets(forces),
          Paragraph("Faiblesses / points de vigilance", H2), bullets(faiblesses),
          Paragraph("Compétences développées", H2), bullets(competences),
          Paragraph("Axes d'amélioration personnels", H2), bullets(axes)]
    build(nom_fichier, s)


# ---- Zaafir
individual(
    "PE-2526_%s_MougammadouZaafir.pdf" % CODE,
    "Zaafir Mougammadou Zaccaria", "Infrastructure cloud & déploiement applicatif",
    "J'ai pris en charge l'infrastructure Azure en tant que code (Terraform) et l'application elle-même "
    "(API FastAPI + frontend React + PostgreSQL), ainsi que son déploiement de bout en bout sur le cluster.",
    ["Écriture des modules Terraform : groupe de ressources, AKS, Azure Container Registry, PostgreSQL "
     "Flexible Server, mise en réseau et budget FinOps.",
     "Développement de l'API FastAPI (patients, appareils auditifs, rendez-vous), sondes de santé et "
     "exposition des métriques ; frontend React de gestion.",
     "Conteneurisation (images Docker multi-stage, non-root) et déploiement applicatif via Helm.",
     "Coordination du déploiement complet sur Azure et vérification fonctionnelle (API, base, UI)."],
    ["Migration de l'authentification cloud vers un service principal + OIDC (sans mot de passe stocké).",
     "Passage à une base PostgreSQL en réseau privé (sans accès public) pour renforcer l'isolation.",
     "Découpage de l'API en microservices si le périmètre fonctionnel s'élargit.",
     "Mise en place de migrations de schéma versionnées (Alembic) en remplacement de la création au démarrage."],
    ["L'authentification Azure par identifiant/mot de passe en CI est simple mais moins robuste qu'OIDC.",
     "La base en accès public restreint par pare-feu est un compromis budget/sécurité (réseau privé écarté).",
     "La création du schéma au démarrage de l'application convient au MVP mais pas à la production.",
     "Le dimensionnement (nœuds burstable) limite les performances sous forte charge prolongée."],
    ["Déploiement : configurer les secrets Azure puis lancer le workflow ; l'URL d'accès s'affiche en fin de job.",
     "L'application est accessible via l'Ingress ; la documentation interactive de l'API est sous /api/docs.",
     "Toute l'infrastructure est recréable à l'identique via Terraform (commande unique)."],
    "Le principal défi a été d'industrialiser le provisioning Terraform pour qu'il soit idempotent et "
    "rejouable automatiquement par la CI, tout en restant dans le budget. La gestion de l'état distant et la "
    "cohérence entre l'infrastructure et le déploiement applicatif ont demandé plusieurs itérations.",
    ["Bonne vision d'ensemble infra + application.",
     "Capacité à rendre l'infrastructure reproductible et automatisée."],
    ["Tendance à vouloir tout déployer en une fois plutôt que par incréments testés.",
     "Approfondir la sécurisation réseau (privé) au-delà du MVP."],
    ["Terraform (azurerm), conception d'infrastructure Azure.",
     "Conteneurisation et déploiement Helm.",
     "Développement d'API REST (FastAPI) et intégration base de données."],
    ["Adopter une approche plus incrémentale et testée des changements d'infrastructure.",
     "Renforcer mes compétences en sécurité réseau cloud (VNet, private endpoints)."],
)

# ---- Elyess
individual(
    "PE-2526_%s_RjafellahElyess.pdf" % CODE,
    "Elyess Rjafellah", "CI/CD & automatisation",
    "J'ai conçu et fiabilisé la chaîne d'intégration et de déploiement continus (GitHub Actions), afin que "
    "tout le cycle — provisionnement, build, scan, déploiement, sauvegarde — soit entièrement automatisé.",
    ["Conception des workflows GitHub Actions : intégration (lint + tests), sécurité, déploiement complet "
     "et sauvegarde planifiée.",
     "Automatisation du provisionnement (Terraform) et création automatique de l'état distant.",
     "Mise en place d'un pipeline <b>auto-réparant</b> : libération des verrous d'état, nettoyage des "
     "releases Helm bloquées, ordre d'installation des dépendances (CRDs avant l'application).",
     "Optimisation des temps d'exécution (suppression des attentes bloquantes inutiles)."],
    ["Passage en GitOps (ArgoCD) pour un déploiement déclaratif piloté par l'état du dépôt.",
     "Authentification OIDC fédérée GitHub → Azure (suppression des secrets longue durée).",
     "Environnements multiples (dev/staging/prod) avec promotion contrôlée.",
     "Tests de bout en bout (E2E) automatisés post-déploiement dans le pipeline."],
    ["L'enchaînement provision + déploiement dans un seul workflow est pratique mais long ; un découpage "
     "en jobs/étapes parallélisés serait plus efficace.",
     "La connexion Azure par identifiant/mot de passe impose un compte sans MFA — peu adapté à la production.",
     "L'absence d'environnement de staging fait que les tests se font directement sur l'unique cluster.",
     "Les déclencheurs sur push peuvent lancer des déploiements coûteux : un garde-fou serait souhaitable."],
    ["Déploiement : Actions → workflow Deploy → <i>deploy</i> ; destruction : action <i>destroy</i>.",
     "Sauvegarde/restauration : workflow Backup (modes <i>backup</i> / <i>restore</i>), planifié quotidiennement.",
     "Les secrets nécessaires (identifiants Azure) sont décrits dans la documentation d'installation."],
    "Le défi majeur a été de rendre le pipeline robuste face aux états intermédiaires (run interrompu, "
    "release Helm en échec, verrou d'état Terraform résiduel). J'ai progressivement ajouté des mécanismes "
    "d'auto-réparation pour que la chaîne se rétablisse seule sans intervention manuelle.",
    ["Rigueur dans l'enchaînement et l'idempotence des étapes.",
     "Capacité à diagnostiquer et corriger rapidement les échecs de pipeline."],
    ["Workflows monolithiques à découper davantage.",
     "Sécurisation de l'authentification CI à approfondir (OIDC)."],
    ["GitHub Actions (workflows, secrets, déclencheurs, concurrency).",
     "Automatisation Terraform et gestion d'état distant.",
     "Diagnostic et résilience des pipelines CI/CD."],
    ["Modulariser les pipelines (jobs réutilisables, environnements).",
     "Mettre en place une stratégie multi-environnements et le GitOps."],
)

# ---- Adame
individual(
    "PE-2526_%s_NianghaneAdame.pdf" % CODE,
    "Adame Nianghane", "Observabilité & sécurité",
    "J'ai mis en place la supervision complète (métriques, logs, alertes) et la sécurité de la chaîne "
    "(DevSecOps) ainsi que le durcissement de l'exécution.",
    ["Déploiement de la stack d'observabilité : Prometheus, Grafana, Loki/Promtail, Alertmanager.",
     "Création du tableau de bord applicatif (débit, latence p95, taux d'erreurs, disponibilité) et "
     "intégration des logs ; règles d'alerte et routage vers Slack/Teams.",
     "Intégration des scans de sécurité dans la CI : Trivy (vulnérabilités), CodeQL (analyse statique), "
     "Gitleaks (fuite de secrets).",
     "Durcissement : conteneurs non-root, RBAC, NetworkPolicies, TLS sur la base, gestion des secrets."],
    ["Ajout du traçage distribué (OpenTelemetry → Tempo/Jaeger) pour le suivi transactionnel.",
     "Passage à une gestion centralisée des secrets (Azure Key Vault / Vault) avec rotation automatique.",
     "Politiques de sécurité avancées (Pod Security Standards, OPA/Gatekeeper, signature d'images).",
     "Tableaux de bord SLO/SLA et alerting affiné par service."],
    ["Le routage des alertes vers Slack nécessite un webhook externe non encore branché en production.",
     "Les NetworkPolicies fournies nécessitent un CNI qui les applique (Calico/Azure CNI), non activé "
     "sur le cluster MVP (kubenet).",
     "La conformité HDS (données de santé) impose une région et des services certifiés non retenus ici.",
     "La rétention courte des métriques/logs limite l'analyse rétrospective."],
    ["Accès à Grafana via son URL (identifiants fournis) ; les tableaux de bord sont préchargés.",
     "Les logs applicatifs sont consultables dans Grafana via la source de données Loki.",
     "Les rapports de sécurité sont disponibles dans l'onglet Security du dépôt (format SARIF)."],
    "Le principal défi a été de faire tenir une stack de supervision complète sur un cluster de taille "
    "réduite (contrainte FinOps) tout en gardant des tableaux de bord exploitables, et de garantir que les "
    "métriques de l'application soient automatiquement découvertes et collectées.",
    ["Sens du détail sur la sécurité et la conformité.",
     "Capacité à rendre un système observable et compréhensible."],
    ["Activer concrètement le routage d'alertes et les NetworkPolicies en conditions réelles.",
     "Approfondir les standards de sécurité Kubernetes avancés."],
    ["Prometheus / Grafana / Loki / Alertmanager.",
     "DevSecOps : Trivy, CodeQL, Gitleaks.",
     "Durcissement Kubernetes (RBAC, securityContext, NetworkPolicies)."],
    ["Mettre en œuvre le traçage distribué et des SLO.",
     "Industrialiser la gestion des secrets et la signature d'images."],
)

# ---- Anis
individual(
    "PE-2526_%s_DouadiAnis.pdf" % CODE,
    "Anis Douadi", "Orchestration Kubernetes / Helm & on-premise / PRA",
    "J'ai pris en charge l'orchestration Kubernetes (packaging Helm, autoscaling, politiques) et le volet "
    "hybride on-premise avec le plan de reprise d'activité (MinIO chiffré + Ansible).",
    ["Conception du chart Helm de l'application (Deployments, Service, Ingress, Secret, HPA, ServiceMonitor).",
     "Mise en place de l'autoscaling (HPA), des NetworkPolicies et du contexte de sécurité des conteneurs.",
     "Provisionnement de la VM <b>on-premise simulée</b> (réseau séparé) hébergeant MinIO chiffré (SSE).",
     "Playbooks Ansible de configuration MinIO et de sauvegarde/restauration PostgreSQL (PRA)."],
    ["Migration vers un CNI appliquant les NetworkPolicies (Calico) pour un vrai cloisonnement réseau.",
     "Haute disponibilité multi-zones et réplication géographique des sauvegardes.",
     "Externalisation des sauvegardes vers un stockage objet redondant + tests de restauration planifiés.",
     "Mise en place d'un vrai site on-premise (au-delà de la simulation) relié par VPN/ExpressRoute."],
    ["Le site on-premise est <b>simulé</b> par une VM Azure dans un réseau séparé : l'isolation est "
     "représentative mais ce n'est pas un datacenter physique.",
     "La restauration ramène l'état du moment de la sauvegarde (RPO = fréquence des backups).",
     "MinIO mono-instance : pas de redondance du stockage de sauvegarde dans le MVP.",
     "Le cluster mono-pool (kubenet) limite l'application stricte des politiques réseau."],
    ["La console MinIO permet de visualiser les sauvegardes chiffrées (bucket dédié).",
     "Sauvegarde et restauration sont déclenchables via le workflow dédié (modes backup/restore).",
     "Le chart Helm est paramétrable (registre d'images, hôte, activation des politiques)."],
    "Le défi principal a été d'orchestrer la réplication cloud → on-premise de façon fiable et rejouable : "
    "rendre la restauration idempotente (afin qu'elle fonctionne même sur une base déjà peuplée) et "
    "automatiser entièrement la configuration de la VM via Ansible.",
    ["Maîtrise du packaging et des objets Kubernetes.",
     "Vision claire de la reprise d'activité et de l'architecture hybride."],
    ["Passer d'un on-premise simulé à une intégration réseau plus réaliste.",
     "Renforcer la redondance du stockage de sauvegarde."],
    ["Kubernetes et Helm (templating, HPA, RBAC, NetworkPolicies).",
     "Ansible (playbooks, gestion de configuration).",
     "Conception d'un PRA (sauvegarde/restauration, MinIO/S3)."],
    ["Mettre en œuvre la HA multi-zones et la géo-réplication.",
     "Automatiser des tests de restauration réguliers (vérification du PRA)."],
)

print("=== TOUS LES PDF GÉNÉRÉS ===")
