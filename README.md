# Math Wars ⚔️🃏

> Un juego de cartas por turnos donde **las matemáticas son tu poder**.
> Inspirado en *Card Wars*, el juego de cartas de Jake y Finn en *Hora de Aventura*.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![pygame](https://img.shields.io/badge/pygame-2.5%2B-green)
![Estado](https://img.shields.io/badge/estado-en%20desarrollo-orange)

## 📖 ¿De qué trata?

Math Wars es un videojuego educativo hecho con **pygame**. Dos duelistas se enfrentan
invocando criaturas en un tablero de 4 líneas, igual que en Card Wars.
La diferencia: **para invocar una criatura tienes que resolver un reto de matemáticas**.
Mientras más poderosa (y cara) es la carta, más difícil es el reto.

Así, practicar operaciones deja de ser una tarea y se convierte en la estrategia del juego:
quien domina las mates, domina el tablero.

## 🎯 Objetivo del juego

Reducir la vida del rival de **25 a 0** antes de que él lo haga contigo.

## 🕹️ Cómo se juega

1. **Elige una carta** de tu mano (parte inferior) haciendo clic sobre ella.
2. **Haz clic en una de tus 4 líneas libres** para intentar invocarla.
3. **Resuelve el reto de matemáticas** que aparece:
   - ✅ Si aciertas, la criatura entra al campo y se descuenta su coste de energía.
   - ❌ Si fallas, pierdes **1 de energía** y la carta se queda en tu mano. Puedes intentarlo de nuevo con otra pregunta.
4. **Pulsa "Terminar turno"** cuando termines. Entonces:
   - Tus criaturas atacan a la criatura rival de **su misma línea**.
   - Si esa línea rival está vacía, el golpe va **directo a la vida** del rival.
   - Después juega el rival (invoca y ataca).
   - Al empezar tu nuevo turno robas 1 carta y recuperas la energía.

### Reglas rápidas

| Regla | Valor |
|---|---|
| Vida inicial | 25 |
| Cartas iniciales en mano | 4 (máximo 7) |
| Líneas de batalla | 4 por jugador |
| Energía | 3 en el primer turno, +1 cada turno, máximo 6 |
| Daño | El daño a las criaturas se conserva entre turnos |
| Fin del juego | Gana quien deje al otro en 0 de vida |

### Controles

| Acción | Control |
|---|---|
| Seleccionar carta / línea / respuesta | Clic izquierdo |
| Terminar turno | Botón "Terminar turno" |
| Reiniciar tras ganar o perder | Tecla `R` |
| Salir | Tecla `ESC` |

## 🧠 Componente educativo

La dificultad del reto depende del **coste de la carta**:

| Coste | Tema | Ejemplo |
|---|---|---|
| 1 | Sumas y restas | `12 + 7 = ?` |
| 2 | Tablas de multiplicar | `6 × 8 = ?` |
| 3 | Jerarquía de operaciones | `4 + 3 × 5 = ?` |
| 4 | Divisiones y potencias | `56 ÷ 7 = ?` · `9² = ?` |
| 5 | Ecuaciones simples | `3x + 4 = 19 → x = ?` |

Después de responder, el juego muestra **la explicación** del resultado,
tanto si acertaste como si fallaste, para aprender del error.

## 🃏 Cartas

| Carta | Coste | Ataque | Vida |
|---|---|---|---|
| Sapo Suma | 1 | 1 | 2 |
| Gato Resta | 1 | 2 | 1 |
| Mago Multi | 2 | 2 | 3 |
| Robot Divide | 2 | 3 | 2 |
| Dino Decimal | 3 | 3 | 4 |
| Ninja Potencia | 3 | 4 | 3 |
| Golem Raíz | 4 | 5 | 5 |
| Dragón Pi | 4 | 6 | 4 |
| Rey Álgebra | 5 | 7 | 6 |

## 🚀 Instalación y ejecución

Requisitos: **Python 3.9 o superior**.

```bash
git clone https://github.com/<tu-usuario>/math-wars.git
cd math-wars

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

## 🗂️ Estructura del proyecto

```
math-wars/
├── main.py              # Punto de entrada
├── requirements.txt
├── CONTRIBUTING.md      # Políticas de PR y revisión
├── .github/             # Plantillas de PR e issues
└── src/
    ├── settings.py      # Constantes, reglas y colores
    ├── game.py          # Bucle principal, tablero y turnos
    ├── card.py          # Clase Card
    ├── card_data.py     # Catálogo de cartas
    ├── deck.py          # Mazo
    ├── player.py        # Vida, mano, tablero y energía
    ├── ui.py            # Funciones de dibujo
    ├── questions.py     # Generador de preguntas por nivel
    ├── quiz.py          # Ventana emergente del reto
    ├── combat.py        # Resolución de ataques y ganador
    └── ai.py            # IA del rival
```

## 🔧 Personalizar el juego

- **Agregar una carta:** añade una línea en `src/card_data.py`.
- **Agregar un tipo de pregunta:** crea una rama nueva dentro de `generate_question` en `src/questions.py`.
- **Cambiar reglas:** ajusta los valores de `src/settings.py` (vida, energía, tamaño de mano).

## 🌿 Flujo de trabajo (Git)

El proyecto sigue un flujo con **ramas `feature/*`** y **Pull Requests** hacia `main`.
Las reglas completas están en [CONTRIBUTING.md](CONTRIBUTING.md).

### Ciclo de desarrollo

```
Issue → Rama → Commits → Pull Request → Peer Review → Merge a main
```

1. **Issue:** se registra la tarea con la plantilla de *Nueva funcionalidad* o *Reporte de error*.
2. **Rama:** se crea desde `main` actualizado.
   ```bash
   git checkout main && git pull origin main
   git checkout -b feature/nombre-de-la-tarea
   ```
3. **Commits semánticos:** `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
   ```bash
   git add .
   git commit -m "feat: agregar combate por líneas"
   git push -u origin feature/nombre-de-la-tarea
   ```
4. **Pull Request:** se abre hacia `main` con la plantilla (descripción, evidencia visual, pasos para probar, checklist) y **2 Reviewers**.
5. **Peer Review:** los revisores descargan la rama, prueban el juego y dejan comentarios en línea. Emiten el dictamen *Approve* o *Request changes*.
6. **Merge:** con al menos 1 aprobación y conversaciones resueltas, se usa **Squash and merge** y se elimina la rama.

### Protección de la rama `main`

| Regla | Estado |
|---|---|
| Requerir Pull Request antes de hacer merge | ✅ |
| Requerir al menos 1 aprobación | ✅ |
| Descartar aprobaciones al subir nuevos commits | ✅ |
| Requerir que las conversaciones estén resueltas | ✅ |
| Bloquear force push y eliminación de `main` | ✅ |
| Aplicar las reglas también a administradores | ✅ |

### Plantillas

- Pull Request: [`templates/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)
- Issues: [`templates/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) (reporte de error y nueva funcionalidad)

### Ramas del desarrollo inicial

| Rama | Contenido |
|---|---|
| `main` | Ventana y configuración base |
| `feature/cartas-y-mazo` | Cartas, catálogo y mazo |
| `feature/tablero-y-jugador` | Jugador, tablero, energía y turnos |
| `feature/preguntas-educativas` | Retos de matemáticas |
| `feature/combate-e-ia` | Combate, IA y fin de juego |

## 🗺️ Ideas futuras

- [ ] Preguntas de otras materias (ciencias, inglés, historia)
- [ ] Selector de dificultad
- [ ] Efectos de sonido y animaciones de ataque
- [ ] Cartas con habilidades especiales
- [ ] Modo de dos jugadores locales
- [ ] Estadísticas de aciertos para el estudiante

## 👥 Autores

Proyecto académico desarrollado por el siguiente equipo:

| Desarrollador | GitHub |
|---|---|
| Ulises Guadalupe Escareño Vega | [aluc35423-ops](https://github.com/aluc35423-ops) |
| José Braulio Martinez Mora | [Braulio-Mtz-M](https://github.com/Braulio-Mtz-M) |
| Javier Humberto Cisneros Vela | [JaviiVela](https://github.com/JaviiVela) |

## 📄 Licencia

Proyecto con fines educativos. Inspirado en *Card Wars* de *Hora de Aventura*
(© Cartoon Network); no tiene afiliación oficial.