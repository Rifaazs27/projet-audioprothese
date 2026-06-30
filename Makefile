.PHONY: help up down logs seed test test-back test-front lint deploy teardown

help:
	@echo "Cibles disponibles :"
	@echo "  up         Lance la stack locale (docker compose)"
	@echo "  down       Arrête la stack locale"
	@echo "  seed       Insère les données de démonstration"
	@echo "  test       Lance tous les tests (back + front)"
	@echo "  lint       Lint backend (ruff) + frontend (eslint)"
	@echo "  deploy     Déploie sur Azure (Terraform + Helm)"
	@echo "  teardown   Détruit l'infra Azure (FinOps)"

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

seed:
	docker compose exec backend python -m app.seed

test: test-back test-front

test-back:
	cd app/backend && pip install -q -r requirements-dev.txt && pytest

test-front:
	cd app/frontend && npm install && npm run test

lint:
	cd app/backend && ruff check .
	cd app/frontend && npm run lint

deploy:
	./scripts/deploy.sh

teardown:
	./scripts/teardown.sh
