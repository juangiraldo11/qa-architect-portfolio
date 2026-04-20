# Día 01 – Estrategia de pruebas: MercadoYa

## 1. Diagrama de estrategia

```
                         ╔══════════════════════════════╗
                         ║   E2E / UI  (Playwright)     ║  10%
                        ╔╩══════════════════════════════╩╗
                        ║  Performance + Security        ║  5%
                       ╔╩════════════════════════════════╩╗
                       ║   Contract Tests  (Pact)         ║  15%
                      ╔╩══════════════════════════════════╩╗
                      ║   Integration / Component          ║  35%
                     ╔╩════════════════════════════════════╩╗
                     ║        Unit Tests                    ║  35%
                     ╚══════════════════════════════════════╝

   Volumen:  ALTO ──────────────────────────────────► BAJO
   Costo:    BAJO ──────────────────────────────────► ALTO
   Feedback: RÁPIDO ─────────────────────────────► LENTO
```

---

## 2. Distribución numérica propuesta

| Capa | % del esfuerzo | Herramientas sugeridas | Qué cubre |
|------|---------------|------------------------|-----------|
| **Unit** | 35% | `pytest` + `pytest-cov` (backend), `Jest` + `React Testing Library` (frontend) | Lógica de negocio pura: cálculo de precios, reglas de descuento, validaciones de dominio, transformaciones de datos, componentes React en aislamiento |
| **Integration / Component** | 35% | `pytest` + `Testcontainers` (PostgreSQL, Redis reales), `httpx` para endpoints FastAPI | Cada microservicio con su base de datos real; flujos intra-servicio: auth → JWT, carrito → Redis, pagos → lógica pre-Stripe |
| **Contract (Consumer-Driven)** | 15% | `Pact` (Python + JS), `Pact Broker` en CI | Contratos entre los 6 microservicios y con Stripe/SendGrid; previene breaking changes silenciosos entre equipos |
| **E2E / UI** | 10% | `Playwright` (TypeScript), con fixtures contra staging | Journeys críticos de negocio: registro → búsqueda → compra → confirmación por correo |
| **Performance + Security** | 5% | `k6` (carga), `OWASP ZAP` (DAST básico en pipeline) | Tiempo de respuesta en búsqueda y checkout; inyección SQL, XSS, auth bypass en APIs públicas |

---

## 3. Justificación

### ¿Qué modelo elegí y por qué?

Elegí un **híbrido honeycomb-pirámide**, no la pirámide clásica. La diferencia clave está en elevar los contract tests a una capa explícita y darle el mismo peso a la integración que a los unit tests.

La razón es arquitectónica: MercadoYa tiene **6 microservicios con fronteras bien definidas y dependencias externas críticas** (Stripe, SendGrid). En ese contexto, la mayor fuente de fallos en producción no es la lógica interna de cada servicio — es la comunicación entre ellos. Un unit test al 100% de cobertura en el servicio de pagos no detecta que el servicio de carrito cambió el contrato del campo `total_amount` de `float` a `string`.

### ¿Qué pesó más en la decisión?

La **arquitectura** fue el factor dominante. Los microservicios penalizan la pirámide pura porque desplazan el riesgo hacia las interfaces. El **equipo también pesó**: con solo 2 QEs para 12 desarrolladores y deploys múltiples diarios, no podemos sostener una suite E2E masiva. Cada test E2E que se rompe es tiempo QE que escasea. La estrategia debe ser mantenible, no solo exhaustiva.

### Anti-patrón principal: el cono de helado invertido

El riesgo más alto aquí es el **ice cream cone**: un equipo sin cultura de testing sólida + integraciones externas complejas = tendencia natural a escribir muchos E2E y pocos tests de capas bajas. El resultado: suite lenta, frágil, cara de mantener, y que igual no detecta el bug del contrato entre servicios.

Este diseño lo previene poniendo los contract tests como ciudadanos de primera clase en el pipeline, ejecutándose en cada PR antes que los E2E.

### "Pero el libro dice que el 80% deben ser unit tests"

Le respondería: **el libro describe un principio, no una fórmula.** La pirámide de Fowler fue pensada para aplicaciones monolíticas con lógica de negocio compleja en el servidor. En una arquitectura de microservicios con integraciones externas, aplicar ese porcentaje ciegamente ignora dónde vive realmente el riesgo. Aquí el riesgo vive en las fronteras entre servicios, no dentro de ellos. Diseñar la estrategia desde el riesgo real del proyecto siempre gana sobre seguir una receta genérica.
