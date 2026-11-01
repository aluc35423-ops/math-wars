# Guía de contribución — Math Wars

Este documento define las **políticas de Pull Request** y el **procedimiento estándar de revisión de código** del equipo.

## 1. Ramas

| Rama | Uso |
|---|---|
| `main` | Rama protegida. Solo recibe código aprobado mediante PR. Nadie hace push directo. |
| `feature/<nombre>` | Nueva funcionalidad |
| `fix/<nombre>` | Corrección de errores |
| `docs/<nombre>` | Documentación |

Los nombres van en minúsculas y con guiones: `feature/tablero-y-jugador`.

## 2. Commits semánticos

Formato: `tipo(alcance opcional): descripción en infinitivo`

Tipos: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`.
Ejemplo: `feat(quiz): agregar ventana de preguntas`

## 3. Políticas de Pull Request

1. **Un PR = un objetivo.** Idealmente menos de 400 líneas cambiadas.
2. **Siempre desde una rama** hacia `main`. Nunca se hace push directo a `main`.
3. **Título semántico**, por ejemplo `feat(combat): agregar combate por líneas`.
4. **Usar la plantilla** de PR completa: descripción, evidencia visual, pasos para probar y checklist.
5. **Vincular un issue** con `Closes #n` cuando exista.
6. **Asignar 2 Reviewers.** El autor nunca se revisa a sí mismo.
7. **Se requiere al menos 1 aprobación** y que todas las conversaciones estén resueltas antes del merge.
8. **Nuevos commits invalidan las aprobaciones** anteriores: hay que volver a revisar.
9. **El autor resuelve los conflictos** con `main` antes de pedir revisión.
10. **Tiempo de respuesta:** el revisor responde en un máximo de 48 horas.
11. **Merge con "Squash and merge"** y se elimina la rama al terminar.
12. Ante un desacuerdo, se discute en el PR y, si no se resuelve, se lleva a la reunión de equipo.

## 4. Procedimiento estándar de revisión (Peer Review)

**Pasos del revisor**
1. Descargar la rama: `git fetch origin && git checkout <rama>`
2. Ejecutar el juego con `python main.py` y probar los pasos de la plantilla.
3. Leer los cambios en la pestaña **Files changed**.
4. Dejar comentarios en línea usando prefijos:
   - 🔴 **Bloqueante:** debe corregirse antes del merge.
   - 🟡 **Sugerencia:** mejora recomendada.
   - 🟢 **Elogio / detalle menor:** reconocimiento o nitpick.
5. Emitir el dictamen: **Approve**, **Request changes** o **Comment**.

**Qué revisar en este proyecto (pygame)**
- El juego abre y corre sin errores en consola.
- La lógica (`player`, `combat`, `questions`) está separada del dibujo (`ui`, `game`).
- No se crean fuentes ni superficies nuevas en cada frame (usar caché).
- Las constantes viven en `settings.py`, sin números mágicos.
- Los nombres son claros y no hay código comentado ni archivos basura.
- Las preguntas educativas son correctas y sus explicaciones coinciden con la respuesta.

**Formato del dictamen final**

```markdown
### 🔍 Resumen del Peer Review
**Revisor:**
**Autor:**
**Módulo:**

#### 🌟 Puntos fuertes
-

#### ⚠️ Oportunidades de mejora / correcciones requeridas
-

#### 🧪 Pruebas realizadas
- [ ] El juego corre sin errores
- [ ] Se probaron los pasos de la plantilla
- [ ] Se verificó que no hay regresiones

#### 📊 Rúbrica (__ / 20)
- Arquitectura y estructura: _ / 4
- Calidad de código: _ / 4
- Funcionalidad y rendimiento: _ / 4
- Calidad del PR y commits: _ / 4
- Retroalimentación profesional: _ / 4

**Dictamen final:** [ ] APROBADO / [ ] REQUIERE CAMBIOS
```

## 5. Reporte de errores y propuestas

Usa las plantillas de **Issues** (`bug_report` y `feature_request`) y agrega la etiqueta correspondiente.
