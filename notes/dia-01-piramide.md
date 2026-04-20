# Día 01 – Estrategia de pruebas: MercadoYa

## 1. Diagrama de estrategia

Las capas crecen en ancho conforme aumenta el volumen de tests. Performance y Security corren en pistas paralelas con cadencias distintas — no son una capa más de la pirámide.

```
                             ┌─────────────────────┐
                             │    E2E / UI  12%     │
                        ┌────┴─────────────────────┴────┐
                        │    Contract Tests (Pact) 15%   │
               ┌────────┴────────────────────────────────┴────────┐
               │          Integration / Component  30%             │
┌──────────────┴──────────────────────────────────────────────────┴──────────────┐
│                               Unit Tests  35%                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

── Pistas paralelas (no apiladas) ────────────────────────────────────────────────
  Performance (k6)     → corre contra staging, periodicidad: nightly + pre-release
  Security SAST (Bandit/ESLint-security) → corre en cada commit, sin bloqueo de PR
  Security DAST (OWASP ZAP)             → corre contra staging, cadencia semanal

  Volumen: ALTO (base) ────────────────────────────────────────────► BAJO (cima)
  Costo:   BAJO ───────────────────────────────────────────────────► ALTO
  Feedback: RÁPIDO ────────────────────────────────────────────────► LENTO
```

---

## 2. Distribución numérica propuesta

| Capa | % del esfuerzo | Herramientas sugeridas | Qué cubre |
|------|---------------|------------------------|-----------|
| **Unit** | 35% | `pytest` + `pytest-cov` (backend), `Jest` + `React Testing Library` (frontend) | Lógica de negocio pura: cálculo de precios, reglas de descuento, validaciones de dominio, transformaciones de datos, componentes React en aislamiento |
| **Integration / Component** | 30% | `pytest` + `Testcontainers` (PostgreSQL, Redis reales), `httpx` para endpoints FastAPI | Cada microservicio con su base de datos real; flujos intra-servicio: auth → JWT, carrito → Redis, pagos → lógica pre-Stripe |
| **Contract (Consumer-Driven)** | 15% | `Pact` (Python + JS), `Pact Broker` en CI | Contratos entre los 6 microservicios y con Stripe/SendGrid; previene breaking changes silenciosos entre equipos |
| **E2E / UI** | 12% | `Playwright` (TypeScript), fixtures contra staging | Journeys críticos: registro → búsqueda → compra → confirmación por correo |
| **Performance** *(paralelo)* | 5% | `k6`, alertas en Grafana/CloudWatch | Latencia p95 en búsqueda y checkout bajo carga; corre nightly y pre-release, no en cada PR |
| **Security** *(paralelo)* | 3% | `Bandit` + `ESLint-plugin-security` (SAST en cada commit), `OWASP ZAP` (DAST semanal en staging) | SAST: secrets expuestos, inyecciones, dependencias vulnerables. DAST: auth bypass, XSS, IDOR en APIs públicas |

---

## 3. Justificación

### ¿Qué modelo elegí y por qué?

Elegí un **híbrido honeycomb-pirámide**, no la pirámide clásica. La diferencia clave está en elevar los contract tests a una capa explícita y reducir el peso de E2E a favor de la integración con bases de datos reales.

La razón es arquitectónica: MercadoYa tiene **6 microservicios con fronteras bien definidas y dependencias externas críticas** (Stripe, SendGrid). En ese contexto, la mayor fuente de fallos en producción no es la lógica interna de cada servicio — es la comunicación entre ellos. Un unit test al 100% de cobertura en el servicio de pagos no detecta que el servicio de carrito cambió el contrato del campo `total_amount` de `float` a `string`.

### ¿Qué pesó más en la decisión?

La **arquitectura** fue el factor dominante. Los microservicios penalizan la pirámide pura porque desplazan el riesgo hacia las interfaces. El **equipo también pesó**: con solo 2 QEs para 12 desarrolladores y deploys múltiples diarios, no podemos sostener una suite E2E masiva. Cada test E2E que se rompe es tiempo QE que escasea. La estrategia debe ser mantenible, no solo exhaustiva.

### Anti-patrones en el radar

**Ice cream cone**: el riesgo más inmediato. Un equipo sin cultura de testing consolidada + integraciones externas complejas tiende a gravitar hacia E2E porque "se ve que funciona". El resultado es una suite lenta, frágil y cara de mantener que además no detecta el bug del contrato entre servicios. Este diseño lo contrarresta poniendo los contract tests como ciudadanos de primera clase en el pipeline, ejecutándose en cada PR antes que los E2E.

**Cupcake** (ThoughtWorks, 2019): igual de relevante aquí. Con 12 devs trabajando en 6 servicios distintos y solo 2 QEs coordinando, existe el riesgo real de que cada equipo de microservicio construya su propia pirámide en silos — tests duplicados, convenciones inconsistentes, y nadie probando los flujos que cruzan fronteras. La capa de contract tests con Pact Broker centralizado es la respuesta directa: los contratos son compartidos, versionados y visibles para todos los equipos.

### "Pero el libro dice que el 80% deben ser unit tests"

Le respondería: **el libro describe un principio, no una fórmula.** La pirámide de Cohn fue pensada para aplicaciones donde la mayor complejidad vive en la lógica de negocio interna. En una arquitectura de microservicios con integraciones externas, aplicar ese porcentaje ciegamente ignora dónde vive realmente el riesgo. Aquí el riesgo vive en las fronteras entre servicios, no dentro de ellos. Diseñar la estrategia desde el riesgo real del proyecto siempre gana sobre seguir una receta genérica.

---

## 4. Reflexión del día

Antes de trabajar en arquitecturas de microservicios asumía que la pirámide era el punto de partida universal y que la discusión era solo sobre proporciones. Lo que entiendo ahora es que **el modelo de testing correcto se deriva del mapa de riesgo del sistema, no al revés**.

Lo que más me sorprendió: el argumento más fuerte para los contract tests no es técnico, es organizacional. En un equipo de 12 personas trabajando en servicios distintos, el mayor riesgo de regresión no es un bug en el código de alguien — es que dos personas con buenas intenciones cambiaron sus respectivos servicios sin coordinarse. Pact resuelve un problema de comunicación entre personas, no solo entre servicios.

También subestimaba la separación entre performance y security como flujos paralelos. Meterlos en una sola capa del 5% no solo es visualmente incorrecto — refleja una comprensión superficial de cómo se operan. Son disciplinas con cadencias, audiencias y herramientas completamente distintas.

---

## Referencias

- Cohn, M. (2009). *Succeeding with Agile*. Addison-Wesley. → Pirámide original
- Fowler, M. (2012). *Test Pyramid*. martinfowler.com → Reformulación y contexto moderno
- Dodds, K. (2019). *Write tests. Not too many. Mostly integration.* → Trophy model, énfasis en integración
- Marick, B. (2003). *Agile Testing Quadrants* → Marco de clasificación por objetivo de negocio vs. técnico
- ThoughtWorks (2019). *Test Cupcake Anti-Pattern* → Riesgo de silos en equipos distribuidos
- Pact Foundation. *Consumer-Driven Contract Testing* → pact.io
