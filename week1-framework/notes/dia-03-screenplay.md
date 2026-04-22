# Día 03 – Screenplay Pattern desde cero

## 1. Comparación lado a lado

### POM (`test_login_pom.py`)
```python
def test_valid_login(login_page):          # fixture inyecta la página ya inicializada
    secure = login_page.login_with(VALID_USER)  # el Page Object sabe CÓMO hacer login
    secure.flash.should_be_success()            # el Page Object sabe CÓMO verificar
    secure.flash.should_contain("You logged into a secure area!")
```
**Más claro en POM:** Las aserciones expresivas (`should_be_success`) hacen el error muy legible.
La firma del método `login_with` esconde toda la mecánica de llenado de campos.

### Screenplay (`test_login_screenplay.py`)
```python
def test_valid_login(maria):               # fixture es el Actor, no la página
    maria.attempts_to(                     # se lee como una historia de usuario
        Navigate.to(LOGIN_URL),            # cada paso es explícito e independiente
        LogIn.with_credentials("tomsmith", "SuperSecretPassword!"),
    )
    assert "You logged into a secure area!" in maria.asks(TheText.of(FLASH_MESSAGE))
    # ↑ la Question separa "obtener dato" de "verificar dato"
```
**Más claro en Screenplay:** La secuencia `attempts_to / asks` separa de forma nítida
*hacer* de *observar*. El test se lee como un guión de aceptación, no como código técnico.
Añadir un segundo actor (ej. un admin) no requiere tocar ningún Page Object.

---

## 2. Tabla de decisión personal

| Característica del proyecto | ¿POM o Screenplay? | Razón |
|---|---|---|
| Equipo nuevo en automation (< 6 meses de experiencia) | POM | La curva de Screenplay (Protocols, abilities, factory methods) puede bloquear el onboarding. POM es más directo de explicar. |
| Sistema con 3 roles distintos (admin, user, guest) | Screenplay | Cada actor encapsula sus propias abilities. Con POM tendrías que duplicar o heredar Page Objects por rol. |
| 15 páginas y un único rol de usuario | POM | La complejidad extra de Screenplay no aporta suficiente valor. Un Page Object por página es mantenible y fácil de leer. |
| Suite con 200+ tests donde reutilizar pasos es crítico | Screenplay | Las Tasks y Actions son componibles sin herencia. `LogIn` puede reutilizarse dentro de cualquier test sin acoplar Page Objects. |
| Proyecto con deadline muy ajustado (2-3 semanas) | POM | Menor overhead de diseño inicial. Se puede refactorizar a Screenplay cuando el proyecto estabilice. |
| App con flujos de negocio complejos (e-commerce, banca) | Screenplay | Las Tasks traducen directamente a historias de usuario. Facilita la revisión con Product Owners no técnicos. |
| Framework existente ya en POM con cobertura alta | POM (mantener) | Migrar trae riesgo sin beneficio inmediato. Solo migrar si el POM ya es "obeso" (ver reflexión abajo). |

---

## 3. Reflexión

**¿Qué me costó más entender de Screenplay?**

Lo más difícil fue interiorizar que `LogIn` no es una página ni un helper: es una *Task*,
y su única responsabilidad es delegar en Actions más pequeñas. Al principio quería poner
el `page.fill()` directamente dentro del `perform_as` de `LogIn`, que es exactamente lo
que haría un POM "obeso". El patrón fuerza a preguntarse en cada paso: "¿esto es una
acción atómica (Action) o una composición de acciones (Task)?". Esa distinción no es
obvia hasta que la vives en código.

El segundo punto difícil fueron los `Protocol` con `runtime_checkable`. Vienen de typing
estructural, que es un concepto menos común en Python que en TypeScript o Go. Una vez
que entendí que son contratos sin herencia obligatoria, el resto fluyó.

**¿Migraría un POM obeso a Screenplay?**

Sí, bajo condiciones concretas: (1) los Page Objects tienen más de 30-40 métodos y empezamos
a ver herencia entre páginas para reutilizar lógica, señal clara de que el modelo se rompió;
(2) hay múltiples roles de usuario que hoy se manejan con flags o subclases; (3) el equipo
tiene al menos un miembro que ya conoce el patrón y puede hacer de referente durante la
migración. La migración no sería big-bang: extraería Actions de los métodos más reutilizados,
luego agruparía en Tasks, y dejaría los Page Objects legacy conviviendo hasta que los tests
nuevos cubran el área. Hacerlo de golpe sin cobertura existente es reemplazar deuda técnica
por deuda técnica diferente.

**¿Por qué POM sigue siendo más popular?**

Tres razones prácticas: primero, la documentación oficial de Selenium y Playwright usa POM
en todos sus ejemplos, así que es lo que aprende el 90 % de los QA de entrada. Segundo,
el mapeado mental "una página = un objeto" es intuitivo para alguien que viene de cualquier
OOP clásico. Tercero, Screenplay exige disciplina de diseño sostenida: es fácil empezar
bien y terminar convirtiendo las Tasks en mini Page Objects con lógica de negocio incrustada.
POM falla de forma más visible (objeto gigante) y la refactorización es más obvia. Screenplay
puede fallar silenciosamente si el equipo no internaliza los principios SOLID que lo sustentan.
