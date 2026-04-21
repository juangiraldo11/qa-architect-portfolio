# Week 1 — Playwright + POM Framework

Framework de automatización de UI construido con Playwright y pytest, aplicando el patrón Page Object Model (POM) con componentes reutilizables.

## Instalación

```bash
pip install -r requirements.txt
playwright install chromium
```

## Correr los tests

```bash
# Headless (por defecto, apto para CI)
pytest

# Con browser visible (debug)
pytest --headed

# Solo los tests POM
pytest tests/test_login_pom.py -v
```

## Estructura

```
week1-framework/
├── conftest.py              # Fixtures: browser, page, login_page
├── requirements.txt
├── pages/
│   ├── login_page.py        # Page Object de /login + dataclass User
│   ├── secure_page.py       # Page Object de /secure
│   └── flash_message.py     # Componente reutilizable del banner flash
└── tests/
    ├── test_login_pom.py    # 4 tests con POM maduro
    └── test_procedural.py   # Versión procedural (referencia de comparación)
```

## Capas del framework

| Capa | Qué hace |
|------|----------|
| **Infraestructura** (`conftest.py`) | Ciclo de vida del browser y fixtures compartidos |
| **Componentes** (`flash_message.py`) | Elementos de UI reutilizables entre páginas |
| **Page Objects** (`login_page`, `secure_page`) | Acciones y navegación por página |
| **Tests** (`tests/`) | Flujos de negocio, sin locators ni Playwright directo |
