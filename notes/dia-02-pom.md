# Día 02 — Page Object Model (POM) maduro

## 1. Arquitectura del framework (4 capas)

```
┌─────────────────────────────────────────────────────┐
│                   CAPA 4 — TESTS                    │
│  tests/test_login_pom.py                            │
│  Orquesta flujos de negocio. Solo llama métodos     │
│  de alto nivel. Sin locators, sin Playwright directo│
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                CAPA 3 — PAGE OBJECTS                │
│  pages/login_page.py  · pages/secure_page.py        │
│  Encapsulan acciones por página. Retornan otros     │
│  Page Objects (fluent navigation). Usan componentes │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│              CAPA 2 — COMPONENTES                   │
│  pages/flash_message.py                             │
│  Elementos reutilizables entre páginas.             │
│  Encapsulan locator + aserciones + estado (@property)│
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│             CAPA 1 — INFRAESTRUCTURA                │
│  conftest.py  · requirements.txt                    │
│  Fixtures de browser/page/login_page, opciones CLI  │
│  (--headed). Base que todas las capas consumen.     │
└─────────────────────────────────────────────────────┘
```

> Estado actual: capas 1, 2 y 3 implementadas. Capa 4 activa con 4 tests.

---

## 2. POM ingenuo vs POM maduro

| Aspecto | POM ingenuo | POM maduro |
|---|---|---|
| **Locators** | Definidos dentro de cada método (`page.locator("#flash")` repetido) | Definidos una vez en `__init__` y reutilizados como atributos de instancia |
| **Navegación entre páginas** | El test hace `page.goto()` manualmente después de cada acción | El método devuelve el Page Object de la siguiente página (`login_with` → `SecurePage`) |
| **Componentes compartidos** | El código del flash message se duplica en `LoginPage` y `SecurePage` | Extraído a `FlashMessage` como componente reutilizable inyectado vía composición |
| **Estado del elemento** | Se accede al atributo `class` inline en cada test con lógica condicional | Encapsulado en `@property` (`is_success`, `is_error`) — el test solo lee un booleano |
| **Data de prueba** | Strings de usuario/contraseña hardcodeados en cada test | `@dataclass User` tipado, instanciado una vez como constante `VALID_USER` |
| **Fixtures** | Browser y page creados dentro de cada función de test | `conftest.py` gestiona el ciclo de vida (session/function scope) con `yield` |
| **Separación de responsabilidades** | El test conoce locators y hace aserciones sobre HTML crudo | El test solo expresa intención de negocio; los detalles de DOM quedan en POM/componentes |

---

## 3. Reflexión — ¿Qué fue más difícil del refactor?

Lo más difícil no fue el código en sí, sino **decidir dónde poner el límite de cada capa**. El momento más tenso fue con `FlashMessage`: al principio lo dejé como métodos dentro de `LoginPage`, porque "solo se usa en login". Cuando llegué a `SecurePage` y vi que necesitaba exactamente la misma lógica, el duplicado me forzó a extraerlo. En retrospectiva, el componente era obvio, pero en el momento no lo era porque solo tenía una página en mente.

La decisión que más me costó justificar fue usar **composición en lugar de herencia** para compartir el flash. Técnicamente `LoginPage` y `SecurePage` podrían heredar de un `BasePage` que tenga `self.flash`. Pero herencia implica acoplamiento vertical: cualquier cambio en `BasePage` afecta a todos los hijos. Con composición, `FlashMessage` es un objeto independiente que cada página elige incluir. Eso lo hace más testeable y más explícito, aunque al principio parece más código.

El otro aprendizaje fue el retorno fluido en `login_with`: devolver `SecurePage` desde un método de `LoginPage` se siente "raro" cuando lo ves por primera vez, pero es lo que permite al test leer como una cadena de intenciones, sin que el test sepa nada del DOM ni de URLs.
