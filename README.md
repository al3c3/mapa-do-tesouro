# 🌱 Mapa do Tesouro — Sistema Inteligente de Irrigação

Sistema desenvolvido em Python para simular um controlador de irrigação inteligente aplicado ao cultivo de tomate. O projeto combina parâmetros de umidade do solo, pH, disponibilidade de nutrientes (NPK) e previsão de chuva para determinar quando a bomba de irrigação deve ser ligada ou desligada.

A proposta é demonstrar, de forma didática, como a programação e a automação podem contribuir para o uso mais eficiente da água na agricultura.

## 📌 Sobre o projeto

O **Mapa do Tesouro** simula uma lavoura de tomate monitorada por um sistema de irrigação automatizado. A partir dos parâmetros informados, o sistema avalia as condições de cultivo e aplica regras predefinidas para tomar decisões sobre a irrigação.

O projeto foi desenvolvido com foco em aprendizado, permitindo compreender como sensores, dados climáticos e regras de decisão podem ser integrados em uma solução de agricultura digital.

## ✨ Funcionalidades

- **Controle de irrigação:** simula o acionamento e o desligamento da bomba conforme as condições do solo.
- **Monitoramento da umidade:** utiliza valores de umidade para identificar a necessidade de irrigação.
- **Conversão de leitura do LDR:** transforma uma leitura analógica em um valor estimado de pH, conforme as regras didáticas do projeto.
- **Verificação do pH:** avalia se o solo está dentro da faixa definida para o cultivo de tomate.
- **Controle de nutrientes:** considera a disponibilidade de nitrogênio (N), fósforo (P) e potássio (K).
- **Previsão de chuva:** permite consultar dados da OpenWeather para auxiliar na decisão de irrigação.
- **Simulação de cenários:** permite alterar os parâmetros do sistema e observar as decisões resultantes.

## 🛠️ Tecnologias utilizadas

- **Python:** implementação das regras de negócio e da simulação.
- **OpenWeather API:** consulta de informações meteorológicas.
- **Variáveis de ambiente:** configuração da chave de API e da cidade de consulta.
- **Programação orientada a objetos:** organização do estado e do comportamento do sistema em classes.

> Observação: o projeto utiliza a biblioteca padrão do Python para sua lógica principal. A consulta à OpenWeather depende da implementação presente no módulo `clima.py` e pode exigir uma biblioteca externa, dependendo de como as requisições HTTP foram implementadas.

## 📂 Estrutura do projeto

```text
.
├── __init__.py
├── clima.py
├── cultura.py
├── irrigacao.py
├── sistema.py
└── README.md
```

### Responsabilidade de cada arquivo

| Arquivo | Descrição |
|---|---|
| `cultura.py` | Define os parâmetros da cultura do tomate, incluindo as faixas de pH e umidade e as regras de conversão do LDR. |
| `irrigacao.py` | Implementa as regras que determinam o estado da bomba de irrigação. |
| `sistema.py` | Gerencia o estado do sistema e disponibiliza métodos para alterar os parâmetros monitorados. |
| `clima.py` | Consulta a OpenWeather e interpreta os dados meteorológicos para obter informações sobre a possibilidade de chuva. |
| `__init__.py` | Centraliza as exportações da cultura e do sistema principal, conforme a organização dos módulos. |

## ⚙️ Regras de decisão da irrigação

O sistema utiliza parâmetros didáticos para simular as decisões de irrigação.

| Parâmetro | Regra configurada |
|---|---|
| Faixa ideal de pH | Entre 6,0 e 6,5 |
| Umidade para ligar a irrigação | Abaixo de 70% |
| Umidade para desligar a irrigação | 80% |
| Probabilidade de chuva | Acima de 60%: suspende a irrigação |
| Nutrientes | N, P e K devem estar disponíveis para permitir a irrigação |

### Como funciona?

1. O sistema recebe os valores dos parâmetros monitorados.
2. Avalia a umidade e verifica se existe necessidade de irrigação.
3. Verifica se o pH está na faixa configurada e se os nutrientes necessários estão disponíveis.
4. Considera a previsão de chuva para evitar irrigação desnecessária.
5. Atualiza a decisão e o estado simulado da bomba conforme as regras implementadas.

**Importante:** os valores apresentados são parâmetros educacionais. Eles devem ser validados agronomicamente antes de serem utilizados em uma lavoura real. O comportamento exato nas condições de limite depende das implementações de `cultura.py` e `irrigacao.py`.

## 🚀 Como executar

### Pré-requisitos

- Python 3.10 ou superior, caso compatível com a versão utilizada no desenvolvimento.
- Git, caso deseje clonar o repositório.
- Chave de API da OpenWeather, para utilizar a consulta meteorológica.


### Crie um ambiente virtual

**Windows — PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux ou macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

O exemplo abaixo demonstra a utilização da classe principal, conforme a interface apresentada no projeto:

```python
from sistema import SistemaIrrigacao

sistema = SistemaIrrigacao(
    umidade=60.0,
    temperatura=25.0
)

print(sistema.ultima_decisao)

sistema.ajustar_ldr(2000)
sistema.alternar_nitrogenio()
sistema.alternar_fosforo()
sistema.alternar_potassio()
sistema.ajustar_umidade(68)

print(sistema.ultima_decisao)
```

Esse exemplo cria uma instância do sistema, consulta a decisão inicial e modifica os parâmetros para simular um novo cenário.

**Nota:** os métodos e os parâmetros devem corresponder às assinaturas efetivamente implementadas nos arquivos do projeto.

## 🌦️ Configuração da OpenWeather

Para consultar a previsão meteorológica, obtenha uma chave de API na [OpenWeather](https://openweathermap.org/api).

Configure as variáveis de ambiente:

**Windows — PowerShell:**

```powershell
$env:OPENWEATHER_API_KEY="SUA_CHAVE_AQUI"
$env:CIDADE="Ribeirao Preto,BR"
```

**Linux ou macOS:**

```bash
export OPENWEATHER_API_KEY="SUA_CHAVE_AQUI"
export CIDADE="Ribeirao Preto,BR"
```

Em seguida, utilize a função disponibilizada pelo módulo climático:

```python
from clima import consultar_openweather

previsao = consultar_openweather(
    "Ribeirao Preto,BR",
    "SUA_CHAVE_AQUI"
)

print(previsao.resumo())
```

O módulo também disponibiliza funções para carregar configurações de ambiente:

```python
from pathlib import Path
from clima import carregar_env, cidade_padrao, chave_openweather

carregar_env(Path(".env"))

print(chave_openweather())
print(cidade_padrao())
```


## 🧪 Possibilidades de evolução

O projeto pode ser expandido gradualmente com:

- Testes automatizados das regras de irrigação.
- Histórico das decisões e das alterações dos parâmetros.
- Interface de terminal ou aplicação web para visualização dos dados.
- Integração com sensores físicos e microcontroladores, como ESP32.
- Alertas de condições inadequadas de umidade, pH ou nutrientes.
- Relatórios para comparar cenários de irrigação.
- Melhorias na interpretação dos dados meteorológicos e no tratamento de falhas da API.


