"""Regra que liga ou desliga o relé azul da bomba d'água."""

from dataclasses import dataclass

from farmtech.cultura import CHUVA_SUSPENDER, PH_MAX, PH_MIN, UMIDADE_DESLIGAR, UMIDADE_LIGAR


@dataclass(frozen=True)
class Decisao:
    ligar_bomba: bool
    motivo: str


def decidir(
    umidade: float,
    ph: float | None,
    ph_confirmado: bool,
    nitrogenio: bool,
    fosforo: bool,
    potassio: bool,
    bomba_ligada: bool,
    nivel_chuva: int = 0,
) -> Decisao:
    """Decide o relé azul da bomba a partir do DHT22, do pH, do NPK e da chuva.

    Com previsão de chuva de 60% ou mais, o relé desliga para economizar água.
    Sem essa previsão, a umidade manda: abaixo de 70% o solo está seco e o
    relé pode ligar; a partir de 80% ele desliga. Entre 70% e 80% o relé
    conserva o estado anterior. Mesmo com solo seco, só há irrigação se o pH
    estiver na faixa ideal e os três botões estiverem pressionados.
    """
    if nivel_chuva >= CHUVA_SUSPENDER:
        return Decisao(
            False,
            f"Previsão de chuva em {nivel_chuva}%. "
            f"A partir de {CHUVA_SUSPENDER}% a irrigação é suspensa e o relé azul desliga.",
        )

    if not ph_confirmado or ph is None:
        return Decisao(
            False,
            "NPK alterado: ajuste o LDR para registrar o novo pH do solo antes de irrigar.",
        )

    if umidade >= UMIDADE_DESLIGAR:
        return Decisao(
            False,
            f"DHT22 em {umidade:.1f}%. A partir de {UMIDADE_DESLIGAR:.0f}% "
            "o solo atingiu a umidade desejada e o relé azul desliga.",
        )

    ph_ok = PH_MIN <= ph <= PH_MAX
    faltando = [
        nome
        for nome, presente in (("N", nitrogenio), ("P", fosforo), ("K", potassio))
        if not presente
    ]

    if umidade >= UMIDADE_LIGAR:
        if bomba_ligada and ph_ok and not faltando:
            return Decisao(
                True,
                f"DHT22 em {umidade:.1f}%, entre {UMIDADE_LIGAR:.0f}% e "
                f"{UMIDADE_DESLIGAR:.0f}%. O relé azul continua ligado.",
            )
        if bomba_ligada:
            return Decisao(False, _interromper(ph, ph_ok, faltando))
        return Decisao(
            False,
            f"DHT22 em {umidade:.1f}%, entre {UMIDADE_LIGAR:.0f}% e "
            f"{UMIDADE_DESLIGAR:.0f}%. O relé azul continua desligado até a umidade "
            f"cair abaixo de {UMIDADE_LIGAR:.0f}%.",
        )

    if not ph_ok or faltando:
        return Decisao(False, _bloquear_solo_seco(umidade, ph, ph_ok, faltando))

    return Decisao(
        True,
        f"DHT22 em {umidade:.1f}% com pH {ph:.2f} e N, P e K presentes. Relé azul ligado.",
    )


def _descrever_problema(ph: float, ph_ok: bool, faltando: list[str]) -> str:
    partes: list[str] = []
    if not ph_ok:
        partes.append(
            f"pH {ph:.2f} está fora da faixa {PH_MIN:.1f}–{PH_MAX:.1f} do tomate"
        )
    if faltando:
        partes.append("faltam os nutrientes " + ", ".join(faltando))
    return "; ".join(partes)


def _bloquear_solo_seco(
    umidade: float, ph: float, ph_ok: bool, faltando: list[str]
) -> str:
    return (
        f"DHT22 em {umidade:.1f}%: o solo está seco, mas o relé azul fica desligado: "
        f"{_descrever_problema(ph, ph_ok, faltando)}."
    )


def _interromper(ph: float, ph_ok: bool, faltando: list[str]) -> str:
    return f"O relé azul foi desligado: {_descrever_problema(ph, ph_ok, faltando)}."
