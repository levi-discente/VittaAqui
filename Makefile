# Makefile

# Binário de produção
BINARY=bin/server

# Diretórios
CMD_DIR=cmd/
PKG=./...

GOBIN ?= $(shell go env GOBIN)
ifeq ($(GOBIN),)
  GOBIN := $(shell go env GOPATH)/bin
endif

export PATH := $(GOBIN):$(PATH)

.PHONY: dev build run test clean swagger docker

## dev     
dev:
	@echo "📦 Instalando ou atualizando o watcher..."
	go install github.com/air-verse/air@latest
	@echo "▶️ Iniciando o modo dev (hot-reload)..."
	air

## build   
build:
	@echo "🏗️  Building production binary"
	go build -o $(BINARY) $(CMD_DIR)

## run    
run: build
	@echo "▶️  Running $(BINARY)"
	./$(BINARY)

## test   
test:
	@echo "🧪 Running tests"
	go test $(PKG) ./test

## clean     Remove binários e artefatos
clean:
	@echo "🧹 Cleaning up"
	rm -rf bin/ tmp/ $(BINARY)


## docker    Builda imagens Docker em modo produção
docker:
	@echo "🐳 Building Docker image"
	docker-compose build
