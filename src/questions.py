"""Generador de preguntas educativas. Nivel 1 (fácil) a 5 (difícil)."""
import random
from dataclasses import dataclass


@dataclass
class Question:
    text: str
    options: list      # opciones como texto
    answer: int        # índice de la opción correcta
    explanation: str
    level: int = 1      # dificultad (1 a 5)
    topic: str = ""     # tema que se practica


def _build(text, correct, explanation):
    opts = {correct}
    while len(opts) < 4:
        opts.add(correct + random.choice([-1, 1]) * random.randint(1, 6))
    opts = list(opts)
    random.shuffle(opts)
    return Question(text, [str(o) for o in opts], opts.index(correct), explanation)


TOPICS = {
    1: "Sumas y restas",
    2: "Tablas de multiplicar",
    3: "Jerarquía de operaciones",
    4: "Divisiones y potencias",
    5: "Ecuaciones simples",
}


def generate_question(level):
    level = max(1, min(level, 5))
    question = _generate(level)
    question.level = level
    question.topic = TOPICS[level]
    return question


def _generate(level):
    level = max(1, min(level, 5))
    if level == 1:  # sumas y restas
        a, b = random.randint(2, 15), random.randint(2, 15)
        if random.random() < 0.5:
            return _build(f"{a} + {b} = ?", a + b, f"{a} + {b} = {a + b}")
        a, b = max(a, b), min(a, b)
        return _build(f"{a} - {b} = ?", a - b, f"{a} - {b} = {a - b}")
    if level == 2:  # tablas de multiplicar
        a, b = random.randint(2, 9), random.randint(2, 9)
        return _build(f"{a} × {b} = ?", a * b, f"{a} × {b} = {a * b}")
    if level == 3:  # jerarquía de operaciones
        a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
        return _build(f"{a} + {b} × {c} = ?", a + b * c,
                      f"Primero se multiplica: {b} × {c} = {b * c}. Luego: {a} + {b * c} = {a + b * c}")
    if level == 4:  # divisiones y potencias
        if random.random() < 0.5:
            b, q = random.randint(2, 9), random.randint(2, 12)
            return _build(f"{b * q} ÷ {b} = ?", q, f"{b} × {q} = {b * q}, así que {b * q} ÷ {b} = {q}")
        a = random.randint(2, 12)
        return _build(f"{a}² = ?", a * a, f"{a}² = {a} × {a} = {a * a}")
    # nivel 5: ecuaciones simples
    x, a, b = random.randint(2, 9), random.randint(2, 5), random.randint(1, 9)
    return _build(f"{a}x + {b} = {a * x + b}   →   x = ?", x,
                  f"{a}x = {a * x + b} - {b} = {a * x}, entonces x = {a * x} ÷ {a} = {x}")
