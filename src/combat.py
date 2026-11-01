"""Resolución de combate: cada criatura ataca a la que está en su misma línea."""


def resolve_attacks(attacker, defender, events=None):
    """events (opcional) recibe tuplas (línea, daño, golpe_directo) para animar el daño."""
    log = []
    for lane, card in enumerate(attacker.board):
        if card is None:
            continue
        target = defender.board[lane]
        if target is None:
            defender.hp -= card.attack
            if events is not None:
                events.append((lane, card.attack, True))
            log.append(f"{card.name} golpea directo: -{card.attack} de vida")
        else:
            target.hp -= card.attack
            if events is not None:
                events.append((lane, card.attack, False))
            if target.hp <= 0:
                defender.board[lane] = None
                log.append(f"{card.name} derrota a {target.name}")
            else:
                log.append(f"{card.name} daña a {target.name} (-{card.attack})")
    return log


def winner(player, enemy):
    """Devuelve 'player', 'enemy' o None."""
    if enemy.hp <= 0:
        return "player"
    if player.hp <= 0:
        return "enemy"
    return None
