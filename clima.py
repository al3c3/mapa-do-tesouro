"""Consulta a previsão da OpenWeather e produz o nível de chuva da irrigação."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

API_PREVISAO = "https://api.openweathermap.org/data/2.5/forecast"
CIDADE_PADRAO = "Ribeirao Preto,BR"
PERIODOS_12H = 4


class ClimaError(Exception):
    """Falha ao consultar ou interpretar a previsão."""


@dataclass(frozen=True)
class Previsao:
    cidade: str
    nivel_chuva: int
    chuva_mm: float
    descricao: str

    def resumo(self) -> str:
        return (
            f"{self.cidade}: maior chance de chuva nas próximas 12 h é "
            f"{self.nivel_chuva}%, com cerca de {self.chuva_mm:.1f} mm. "
            f"Condição: {self.descricao}."
        )


def consultar_openweather(cidade: str, api_key: str) -> Previsao:
    """Lê a previsão de 5 dias e resume as próximas 12 horas."""
    if not api_key.strip():
        raise ClimaError("A chave da OpenWeather está vazia.")
    if not cidade.strip():
        raise ClimaError("Informe a cidade da lavoura.")

    parametros = urllib.parse.urlencode(
        {
            "q": cidade.strip(),
            "appid": api_key.strip(),
            "units": "metric",
            "lang": "pt_br",
            "cnt": PERIODOS_12H,
        }
    )
    pedido = urllib.request.Request(
        f"{API_PREVISAO}?{parametros}",
        headers={"User-Agent": "FarmTechSolutions/1.0"},
    )
    try:
        with urllib.request.urlopen(pedido, timeout=15) as resposta:
            dados = json.loads(resposta.read().decode())
    except urllib.error.HTTPError as erro:
        raise ClimaError(_mensagem_http(erro)) from None
    except urllib.error.URLError:
        raise ClimaError("Não foi possível alcançar a OpenWeather.") from None
    except TimeoutError:
        raise ClimaError("A OpenWeather demorou demais para responder.") from None
    except json.JSONDecodeError:
        raise ClimaError("A OpenWeather devolveu uma resposta inválida.") from None

    periodos = dados.get("list")
    if not isinstance(periodos, list) or not periodos:
        raise ClimaError("A OpenWeather não devolveu períodos de previsão.")

    cidade_resposta = dados.get("city", {}).get("name") or cidade.strip()
    return Previsao(
        cidade=cidade_resposta,
        nivel_chuva=nivel_chuva_da_lista(periodos),
        chuva_mm=round(_chuva_mm(periodos), 1),
        descricao=_descricao(periodos),
    )


def nivel_chuva_da_lista(periodos: list[dict]) -> int:
    """Converte a previsão em um inteiro de 0 a 100.

    O valor é a maior probabilidade de precipitação do intervalo.
    Tempestade conta no mínimo como 80, porque é condição adversa.
    """
    if not periodos:
        raise ClimaError("A previsão veio sem períodos.")

    nivel = 0
    for periodo in periodos:
        probabilidade = float(periodo.get("pop", 0) or 0)
        nivel = max(nivel, int(round(probabilidade * 100)))
        for condicao in periodo.get("weather", []):
            codigo = int(condicao.get("id", 0) or 0)
            if 200 <= codigo < 300:
                nivel = max(nivel, 80)
    return min(100, max(0, nivel))


def linha_para_esp32(nivel_chuva: int) -> str:
    """Linha pronta para colar no sketch do ESP32 no Wokwi."""
    return f"int nivelChuva = {int(nivel_chuva)};"


def carregar_env(caminho: Path) -> None:
    """Carrega um .env local sem substituir variáveis já definidas."""
    if not caminho.is_file():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        texto = linha.strip()
        if not texto or texto.startswith("#") or "=" not in texto:
            continue
        chave, valor = texto.split("=", 1)
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")
        if chave and chave not in os.environ:
            os.environ[chave] = valor


def chave_openweather() -> str:
    return os.environ.get("OPENWEATHER_API_KEY", "").strip()


def cidade_padrao() -> str:
    return os.environ.get("CIDADE", CIDADE_PADRAO).strip() or CIDADE_PADRAO


def _chuva_mm(periodos: list[dict]) -> float:
    total = 0.0
    for periodo in periodos:
        chuva = periodo.get("rain") or {}
        if isinstance(chuva, dict):
            total += float(chuva.get("3h", 0) or 0)
    return total


def _descricao(periodos: list[dict]) -> str:
    mais_chuvoso = max(periodos, key=lambda periodo: float(periodo.get("pop", 0) or 0))
    clima = mais_chuvoso.get("weather") or []
    if clima and isinstance(clima[0], dict):
        return str(clima[0].get("description") or "sem descrição")
    return "sem descrição"


def _mensagem_http(erro: urllib.error.HTTPError) -> str:
    if erro.code == 401:
        return (
            "A OpenWeather recusou a chave. Confira OPENWEATHER_API_KEY. "
            "Uma chave nova pode levar alguns minutos para valer."
        )
    if erro.code == 404:
        return "A OpenWeather não encontrou essa cidade."
    detalhe = ""
    try:
        corpo = json.loads(erro.read().decode())
        if isinstance(corpo, dict):
            detalhe = str(corpo.get("message", "")).strip()
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        detalhe = ""
    if detalhe:
        return f"A OpenWeather respondeu com o código {erro.code}: {detalhe}."
    return f"A OpenWeather respondeu com o código {erro.code}."
