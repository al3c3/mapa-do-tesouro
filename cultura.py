"""Parâmetros do tomateiro e conversão da leitura do LDR em pH."""

LDR_MAX = 4095

# Faixa ideal do tomateiro. A cultura se desenvolve de 5,5 a 6,8;
# o grupo só liga o relé dentro do intervalo ideal, 6,0 a 6,5.
PH_MIN = 6.0
PH_MAX = 6.5

# O DHT22 representa a umidade do solo. A referência da cultura é cerca
# de 80% da água útil, sem encharcar. Abaixo de 70% há déficit.
UMIDADE_LIGAR = 70.0
UMIDADE_DESLIGAR = 80.0

# Chance de chuva, em porcentagem, a partir da qual o relé fica desligado.
CHUVA_SUSPENDER = 60

CULTURA = "Tomate (Solanum lycopersicum)"

# pH didático em décimos: solo sem correção começa em 7,2.
_PH_BASE_DECIMOS = 72
_EFEITO_N = -6
_EFEITO_P = -3
_EFEITO_K = -2


def ph_sugerido(nitrogenio: bool, fosforo: bool, potassio: bool) -> float:
    """pH esperado depois da combinação atual dos botões N, P e K.

    O modelo é didático: cada nutriente aplicado acidifica um pouco o solo.
    Serve para indicar qual leitura o LDR deve receber após a mudança do NPK.
    """
    decimos = _PH_BASE_DECIMOS
    if nitrogenio:
        decimos += _EFEITO_N
    if fosforo:
        decimos += _EFEITO_P
    if potassio:
        decimos += _EFEITO_K
    decimos = max(0, min(140, decimos))
    return decimos / 10


def ldr_para_ph(leitura: int) -> float:
    """Converte a escala analógica 0–4095 do LDR para pH 0,00–14,00."""
    if isinstance(leitura, bool) or not isinstance(leitura, int):
        raise TypeError("A leitura do LDR deve ser um número inteiro.")
    if leitura < 0 or leitura > LDR_MAX:
        raise ValueError(f"A leitura do LDR deve estar entre 0 e {LDR_MAX}.")
    return round(leitura * 14 / LDR_MAX, 2)


def ph_para_ldr(ph: float) -> int:
    """Converte um pH de 0 a 14 na leitura inteira correspondente do LDR."""
    if isinstance(ph, bool) or not isinstance(ph, (int, float)):
        raise TypeError("O pH deve ser numérico.")
    if ph < 0 or ph > 14:
        raise ValueError("O pH deve estar entre 0 e 14.")
    return round(ph / 14 * LDR_MAX)
