"""Estado dos sensores didáticos e do relé da bomba."""

from farmtech.cultura import ldr_para_ph, ph_para_ldr, ph_sugerido
from farmtech.irrigacao import Decisao, decidir


class SistemaIrrigacao:
    """Simula os três botões, o LDR, o DHT22 e o relé azul."""

    def __init__(self, umidade: float = 45.0, temperatura: float = 26.0) -> None:
        self.umidade = _validar_umidade(umidade)
        self.temperatura = _validar_temperatura(temperatura)
        self.nitrogenio = False
        self.fosforo = False
        self.potassio = False
        self.leitura_ldr: int | None = None
        self.ph_confirmado = False
        self.bomba_ligada = False
        self.nivel_chuva = 0
        self.ultima_decisao: Decisao = self.avaliar()

    @property
    def ph(self) -> float | None:
        if self.leitura_ldr is None:
            return None
        return ldr_para_ph(self.leitura_ldr)

    @property
    def ph_sugerido(self) -> float:
        return ph_sugerido(self.nitrogenio, self.fosforo, self.potassio)

    @property
    def ldr_sugerido(self) -> int:
        return ph_para_ldr(self.ph_sugerido)

    def alternar_nitrogenio(self) -> None:
        self.nitrogenio = not self.nitrogenio
        self._invalidar_ph()

    def alternar_fosforo(self) -> None:
        self.fosforo = not self.fosforo
        self._invalidar_ph()

    def alternar_potassio(self) -> None:
        self.potassio = not self.potassio
        self._invalidar_ph()

    def ajustar_ldr(self, leitura: int) -> None:
        ldr_para_ph(leitura)
        self.leitura_ldr = leitura
        self.ph_confirmado = True
        self.avaliar()

    def ajustar_umidade(self, umidade: float) -> None:
        self.umidade = _validar_umidade(umidade)
        self.avaliar()

    def ajustar_temperatura(self, temperatura: float) -> None:
        self.temperatura = _validar_temperatura(temperatura)

    def definir_nivel_chuva(self, nivel: float) -> None:
        self.nivel_chuva = _validar_chuva(nivel)
        self.avaliar()

    def avaliar(self) -> Decisao:
        decisao = decidir(
            umidade=self.umidade,
            ph=self.ph,
            ph_confirmado=self.ph_confirmado,
            nitrogenio=self.nitrogenio,
            fosforo=self.fosforo,
            potassio=self.potassio,
            bomba_ligada=self.bomba_ligada,
            nivel_chuva=self.nivel_chuva,
        )
        self.bomba_ligada = decisao.ligar_bomba
        self.ultima_decisao = decisao
        return decisao

    def _invalidar_ph(self) -> None:
        self.ph_confirmado = False
        self.avaliar()


def _validar_chuva(nivel: float) -> int:
    if isinstance(nivel, bool) or not isinstance(nivel, (int, float)):
        raise TypeError("O nível de chuva deve ser numérico.")
    if nivel < 0 or nivel > 100:
        raise ValueError("O nível de chuva deve estar entre 0 e 100%.")
    return int(round(nivel))


def _validar_umidade(umidade: float) -> float:
    if isinstance(umidade, bool) or not isinstance(umidade, (int, float)):
        raise TypeError("A umidade deve ser numérica.")
    if umidade < 0 or umidade > 100:
        raise ValueError("A umidade do DHT22 deve estar entre 0 e 100%.")
    return float(umidade)


def _validar_temperatura(temperatura: float) -> float:
    if isinstance(temperatura, bool) or not isinstance(temperatura, (int, float)):
        raise TypeError("A temperatura deve ser numérica.")
    if temperatura < -40 or temperatura > 80:
        raise ValueError("A temperatura do DHT22 deve estar entre -40 e 80 °C.")
    return float(temperatura)
