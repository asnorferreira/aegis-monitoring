# ==============================================================================
#  Makefile for the Aegis Monitoring Project (WINDOWS - SIMPLIFIED VERSION)
# ==============================================================================
# Use: make [target]

.DEFAULT_GOAL := help

# --- Variáveis ---
BACKEND_DIR = backend
FRONTEND_DIR = frontend
VENV_PATH = $(BACKEND_DIR)\\venv
PYTHON_IN_VENV = $(VENV_PATH)\\Scripts\\python.exe
PIP_IN_VENV = $(VENV_PATH)\\Scripts\\pip.exe
CONTAINER = aegis_backend

.PHONY: help install
help:
	@echo "------------------------------------------------------------------"
	@echo " Guia de Comandos para o Projeto Aegis Monitoring (Windows)"
	@echo "------------------------------------------------------------------"
	@echo.
	@echo "  Uso Geral:"
	@echo "    make install          -> Instala todas as dependencias (backend e frontend)."
	@echo.
	@echo "  Backend (Docker):"
	@echo "    make up               -> Sobe os conteineres Docker."
	@echo "    make down             -> Desliga os conteineres Docker."
	@echo "    make logs             -> Mostra os logs dos conteineres."
	@echo "    make shell            -> Acessa o terminal do conteiner do backend."
	@echo.
	@echo "  Backend (Simuladores Locais):"
	@echo "    make listener         -> Roda o ouvinte MQTT."
	@echo "    make simulator        -> Roda o simulador de sensores."
	@echo.
	@echo "  Frontend:"
	@echo "    make dev              -> Inicia o servidor de desenvolvimento do frontend."
	@echo "------------------------------------------------------------------"

install: backend-install frontend-install

# --- Backend Targets ---
.PHONY: up down logs shell backend-install listener simulator

up:
	@echo "Subindo os conteineres Docker (Postgres + Backend)..."
	@cd $(BACKEND_DIR) && docker-compose up --build -d

down:
	@echo "Desligando os conteineres Docker..."
	@cd $(BACKEND_DIR) && docker-compose down

logs:
	@echo "Mostrando logs... (Pressione Ctrl+C para sair)"
	@cd $(BACKEND_DIR) && docker-compose logs -f

shell:
	@echo "🔹 Acessando terminal do container $(CONTAINER)..."
	@docker exec -it $(CONTAINER) sh

backend-install:
	@echo "Configurando o ambiente Python do backend..."
	@echo "-> Criando/Atualizando ambiente virtual em $(VENV_PATH)..."
	@python -m venv $(VENV_PATH)
	@echo "-> Instalando dependencias do requirements.txt..."
	@call $(PIP_IN_VENV) install -r $(BACKEND_DIR)\\requirements.txt

# ==============================================================================
# Migrações Flask (executadas DENTRO do container)
# ==============================================================================
.PHONY: db-init db-migrate db-upgrade db-reset

db-init:
	@echo "📁 Inicializando diretório de migrações..."
	@docker exec -it $(CONTAINER) flask db init || echo "⚠️ Diretório já existe."

db-migrate:
	@echo "🧱 Criando nova migração..."
	@docker exec -it $(CONTAINER) flask db migrate -m "auto migration"

db-upgrade:
	@echo "⬆️ Aplicando migrações no banco..."
	@docker exec -it $(CONTAINER) flask db upgrade

db-seed:
	@echo "🌱 Populando o banco de dados com dados iniciais (Seeding)..."
	@docker exec -it $(CONTAINER) python -m app.infrastructure.seeding.seed_runner
	
db-reset:
	@echo "🔄 Resetando migrações (recria e aplica do zero)..."
	@docker exec -it $(CONTAINER) rm -rf migrations
	@docker exec -it $(CONTAINER) flask db init
	@docker exec -it $(CONTAINER) flask db migrate -m "reset migrations"
	@docker exec -it $(CONTAINER) flask db upgrade

# ==============================================================================
# Backend (Simuladores Locais)
# ==============================================================================

listener:
	@echo "Rodando o ouvinte MQTT..."
	@call $(PYTHON_IN_VENV) $(BACKEND_DIR)\\mqtt_listener.py

simulator:
	@echo "Rodando o simulador de sensores..."
	@call $(PYTHON_IN_VENV) $(BACKEND_DIR)\\sensor_simulator.py

# --- Frontend Targets ---
.PHONY: dev frontend-install

frontend-install:
	@echo "Instalando dependencias do frontend..."
	@cd $(FRONTEND_DIR) && npm install

dev:
	@echo "Iniciando o servidor de desenvolvimento do frontend em http://localhost:3000..."
	@cd $(FRONTEND_DIR) && npm run dev