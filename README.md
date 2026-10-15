# Ordenha — Vacas leiteiras

Aplicação em Python para calcular e gerenciar a alimentação (ração) de um rebanho de vacas leiteiras. Fornece um menu interativo que permite cadastrar vacas, carregar um rebanho inicial, listar a ordenha, alterar produção, excluir animais, visualizar a tabela de memória e exportar/importar dados em texto/JSON. Pode persistir os registros em uma tabela Oracle ou trabalhar apenas em memória e gerar arquivos em disco.

## Stack
- Language(s): Python 3
- Notable library: oracledb (conexão com banco Oracle)

## Principais funcionalidades
- Cálculo da ração diária a partir dos litros de leite (referência: 30 L → 9 kg).
- Quebra da ração em manhã/tarde e decomposição da mistura em milho/soja/concentrado conforme proporções (75/25/5).
- Persistência opcional em tabela Oracle (`ordenha`) com CRUD básico.
- Export/Import de rebanho em JSON e geração de relatório em texto.
- Exibição de estrutura de dados (lista, tupla, dicionário, tabela de memória) para fins didáticos.

## Como está organizado (resumo)
```
main.py                 -> Aplicação principal (menu, fluxo de execução)
funcoes.py              -> Funções puras: cálculo de ração, montagem de registro, resumo
procedimentos.py        -> Procedimentos: saída formatada, pausa, limpeza de tela
rebanho.py              -> Estruturas iniciais e transformação (tuplas → dicionários)
arquivos.py             -> Leitura/gravação de texto e JSON (pasta `dados/`)
banco.py                -> Operações SQL para a tabela `ordenha` (Oracle)
conexao.py              -> Conexão com o Oracle (atualmente com parâmetros hardcoded)
requirements.txt        -> Dependências (oracledb)
dados/                  -> (pasta criada em tempo de execução) armazenará ordenha.txt / ordenha.json
```

Como o programa se comporta no runtime:
- `main.py` abre a conexão com o Oracle (se disponível), garante a existência da tabela `ordenha` e apresenta um menu interativo.
- As opções do menu usam funções de `funcoes.py` e procedimentos de `procedimentos.py`. A persistência em banco é feita por `banco.py`. Se o Oracle não estiver acessível, o programa pode operar somente em memória e gerar os arquivos em `dados/`.

## Requisitos
- Python 3.8+
- Biblioteca: oracledb
Instale dependências:
```bash
pip install -r requirements.txt
```

## Como executar
1. Ajuste a configuração de conexão com o Oracle (ver seção seguinte).
2. Do diretório do projeto:
```bash
python main.py
```

Ao executar, um menu interativo será exibido com as opções:
- 1 — Cadastrar vaca
- 2 — Carregar as 25 vacas (rebanho inicial)
- 3 — Listar ordenha
- 4 — Alterar litros de leite
- 5 — Excluir vaca
- 6 — Mostrar tabela de memória (explica estruturas)
- 7 — Gravar arquivo texto (gera `dados/ordenha.txt`)
- 8 — Gravar arquivo JSON (gera `dados/ordenha.json`)
- 9 — Ler arquivo texto
- 10 — Ler arquivo JSON (importa e, opcionalmente, grava no banco)
- 0 — Sair

## Configuração do banco (Oracle)
O código atual de conexão está em `conexao.py` e, neste repositório, contém parâmetros diretamente no arquivo. Por segurança e portabilidade, recomenda-se alterar para usar variáveis de ambiente em vez de credenciais hardcoded.

Exemplo sugerido (substituir `conexao.py` por algo como):
```python
import os
import oracledb

def conectar():
    host = os.getenv("ORACLE_HOST", "oracle.fiap.com.br")
    port = int(os.getenv("ORACLE_PORT", "1521"))
    sid = os.getenv("ORACLE_SID", "ORCL")
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    dsn = oracledb.makedsn(host, port, sid=sid)
    return oracledb.connect(user=user, password=password, dsn=dsn, tcp_connect_timeout=20)
```

Variáveis de ambiente recomendadas:
- ORACLE_HOST
- ORACLE_PORT
- ORACLE_SID
- ORACLE_USER
- ORACLE_PASSWORD

Observação: se não houver um Oracle disponível (ou a conexão falhar), o programa lida com o erro e pode trabalhar com o rebanho em memória; muitos comandos continuam funcionando (e os arquivos JSON/txt podem ser usados para salvar/recuperar dados).

## Arquivos principais (descrição rápida)
- main.py — fluxo principal, menu e integração entre módulos.
- funcoes.py — cálculo da ração, montagem de registro de vaca, resumo do rebanho.
- procedimentos.py — funções de I/O e exibição.
- rebanho.py — rebanho inicial (25 vacas) e helpers para criar a tabela de memória.
- arquivos.py — geração e leitura de `ordenha.txt` e `ordenha.json` na pasta `dados/`.
- banco.py — SQL para criar a tabela `ordenha` e operações CRUD.
- conexao.py — ponto único de conexão com Oracle (substituir para usar variáveis de ambiente).
- requirements.txt — dependência: oracledb

