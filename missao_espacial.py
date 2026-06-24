"""
=============================================================
  SISTEMA DE MONITORAMENTO DE MISSAO ESPACIAL - SERS 2026
  Global Solution - FIAP
=============================================================
  Descricao: Sistema automatizado para monitoramento de
  multiplos modulos de uma missao espacial, com registro
  de historico, classificacao de alertas por severidade
  e geracao de relatorio final.
=============================================================
"""

import random
from datetime import datetime

# ─────────────────────────────────────────────
#  CONSTANTES DE CONFIGURACAO DO SISTEMA
# ─────────────────────────────────────────────
TEMP_CRITICA   = 90.0   # °C  - nivel critico de temperatura
TEMP_ALTA      = 75.0   # °C  - nivel de atencao de temperatura
ENERGIA_CRITICA = 10.0  # %   - nivel critico de energia
ENERGIA_BAIXA  = 25.0   # %   - nivel de atencao de energia
PRESSAO_MIN    = 0.8    # atm - pressao minima aceitavel
PRESSAO_MAX    = 1.2    # atm - pressao maxima aceitavel
OXIGENIO_MIN   = 18.0   # %   - percentual minimo de oxigenio

MODULOS_NAVE = ["Propulsao", "Habitacao", "Comunicacao", "Energia", "Cientifico"]

historico_leituras = []  # armazena todas as leituras da sessao


# ─────────────────────────────────────────────
#  FUNCAO: CLASSIFICAR NIVEL DE ALERTA
# ─────────────────────────────────────────────
def classificar_severidade(alertas):
    """
    Recebe uma lista de tuplas (mensagem, nivel) e retorna
    o nivel mais alto encontrado: CRITICO > ATENCAO > OK
    """
    niveis = [nivel for _, nivel in alertas]
    if "CRITICO" in niveis:
        return "CRITICO"
    if "ATENCAO" in niveis:
        return "ATENCAO"
    return "OK"


# ─────────────────────────────────────────────
#  FUNCAO: VERIFICAR CADA PARAMETRO
# ─────────────────────────────────────────────
def verificar_temperatura(temp):
    alertas = []
    acoes   = []
    if temp >= TEMP_CRITICA:
        alertas.append(("Temperatura CRITICA: " + str(temp) + " C", "CRITICO"))
        acoes.append("EMERGENCIA: Acionar sistema de resfriamento de emergencia")
        acoes.append("Redirecionar energia para dissipadores termicos")
    elif temp >= TEMP_ALTA:
        alertas.append(("Temperatura elevada: " + str(temp) + " C", "ATENCAO"))
        acoes.append("Ligar ventiladores auxiliares")
        acoes.append("Reduzir carga dos processadores em 20%")
    else:
        alertas.append(("Temperatura normal: " + str(temp) + " C", "OK"))
    return alertas, acoes


def verificar_energia(energia):
    alertas = []
    acoes   = []
    if energia <= ENERGIA_CRITICA:
        alertas.append(("Energia CRITICA: " + str(energia) + "%", "CRITICO"))
        acoes.append("EMERGENCIA: Ativar celulas de combustivel de reserva")
        acoes.append("Desligar sistemas nao essenciais imediatamente")
    elif energia <= ENERGIA_BAIXA:
        alertas.append(("Energia baixa: " + str(energia) + "%", "ATENCAO"))
        acoes.append("Ativar modo de economia de energia")
        acoes.append("Priorizar sistemas de suporte a vida")
    else:
        alertas.append(("Energia normal: " + str(energia) + "%", "OK"))
    return alertas, acoes


def verificar_pressao(pressao):
    alertas = []
    acoes   = []
    if pressao < PRESSAO_MIN:
        alertas.append(("Pressao baixa: " + str(pressao) + " atm", "CRITICO"))
        acoes.append("EMERGENCIA: Verificar vazamento de pressao nos compartimentos")
        acoes.append("Ativar vedacoes automaticas")
    elif pressao > PRESSAO_MAX:
        alertas.append(("Pressao alta: " + str(pressao) + " atm", "ATENCAO"))
        acoes.append("Abrir valvulas de alivio de pressao")
    else:
        alertas.append(("Pressao normal: " + str(pressao) + " atm", "OK"))
    return alertas, acoes


def verificar_oxigenio(oxigenio):
    alertas = []
    acoes   = []
    if oxigenio < OXIGENIO_MIN:
        alertas.append(("Oxigenio CRITICO: " + str(oxigenio) + "%", "CRITICO"))
        acoes.append("EMERGENCIA: Ativar geradores de oxigenio de reserva")
        acoes.append("Acionar protocolo de evacuacao do modulo")
    elif oxigenio < 20.0:
        alertas.append(("Oxigenio abaixo do ideal: " + str(oxigenio) + "%", "ATENCAO"))
        acoes.append("Aumentar fluxo nos geradores de oxigenio principais")
    else:
        alertas.append(("Oxigenio normal: " + str(oxigenio) + "%", "OK"))
    return alertas, acoes


def verificar_comunicacao(status_com):
    alertas = []
    acoes   = []
    if status_com == "falha_total":
        alertas.append(("Comunicacao com Terra PERDIDA", "CRITICO"))
        acoes.append("EMERGENCIA: Ativar radio de emergencia VHF")
        acoes.append("Enviar sinal de socorro automatico (SOS)")
        acoes.append("Registrar incidente no log da missao")
    elif status_com == "degradada":
        alertas.append(("Comunicacao degradada com Terra", "ATENCAO"))
        acoes.append("Comutar para antena secundaria")
        acoes.append("Reduzir taxa de transmissao de dados")
    else:
        alertas.append(("Comunicacao normal com Terra", "OK"))
    return alertas, acoes


def verificar_modulo_estrutural(status_mod):
    alertas = []
    acoes   = []
    if status_mod == "falha_critica":
        alertas.append(("FALHA CRITICA no modulo estrutural", "CRITICO"))
        acoes.append("EMERGENCIA: Isolar modulo imediatamente")
        acoes.append("Transferir tripulacao para modulo seguro")
        acoes.append("Ativar sistemas de contingencia")
    elif status_mod == "avaria":
        alertas.append(("Avaria detectada no modulo", "ATENCAO"))
        acoes.append("Iniciar diagnostico automatico completo")
        acoes.append("Reduzir carga operacional do modulo em 50%")
    else:
        alertas.append(("Modulo estrutural operacional", "OK"))
    return alertas, acoes


# ─────────────────────────────────────────────
#  FUNCAO: VERIFICACAO COMPLETA DO SISTEMA
# ─────────────────────────────────────────────
def verificar_sistema_completo(nome_modulo, temp, energia, pressao,
                                oxigenio, comunicacao, status_mod):
    """
    Consolida todas as verificacoes em um dicionario de resultado.
    Registra no historico global da sessao.
    """
    todos_alertas = []
    todas_acoes   = []

    # Executa cada verificacao e acumula resultados
    for verificar, args in [
        (verificar_temperatura,       (temp,)),
        (verificar_energia,           (energia,)),
        (verificar_pressao,           (pressao,)),
        (verificar_oxigenio,          (oxigenio,)),
        (verificar_comunicacao,       (comunicacao,)),
        (verificar_modulo_estrutural, (status_mod,)),
    ]:
        a, ac = verificar(*args)
        todos_alertas.extend(a)
        todas_acoes.extend(ac)

    severidade_geral = classificar_severidade(todos_alertas)

    resultado = {
        "modulo":          nome_modulo,
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperatura":     temp,
        "energia":         energia,
        "pressao":         pressao,
        "oxigenio":        oxigenio,
        "comunicacao":     comunicacao,
        "status_modulo":   status_mod,
        "alertas":         todos_alertas,
        "acoes":           todas_acoes,
        "severidade":      severidade_geral,
    }

    historico_leituras.append(resultado)
    return resultado


# ─────────────────────────────────────────────
#  FUNCAO: EXIBIR RESULTADO NO CONSOLE
# ─────────────────────────────────────────────
def exibir_resultado(resultado):
    sep = "=" * 60

    # Cabecalho com nome do modulo e severidade
    print("\n" + sep)
    print("  MODULO: " + resultado["modulo"].upper())
    print("  Data/Hora: " + resultado["timestamp"])
    print("  Status Geral: [" + resultado["severidade"] + "]")
    print(sep)

    # Dados coletados
    print("\n  PARAMETROS MONITORADOS:")
    print("  " + "-" * 40)
    print("  Temperatura  : " + str(resultado["temperatura"]) + " C")
    print("  Energia      : " + str(resultado["energia"]) + "%")
    print("  Pressao      : " + str(resultado["pressao"]) + " atm")
    print("  Oxigenio     : " + str(resultado["oxigenio"]) + "%")
    print("  Comunicacao  : " + resultado["comunicacao"])
    print("  Status Modulo: " + resultado["status_modulo"])

    # Alertas separados por severidade
    criticos  = [(m, n) for m, n in resultado["alertas"] if n == "CRITICO"]
    atencoes  = [(m, n) for m, n in resultado["alertas"] if n == "ATENCAO"]
    normais   = [(m, n) for m, n in resultado["alertas"] if n == "OK"]

    print("\n  ALERTAS:")
    print("  " + "-" * 40)
    if criticos:
        print("  [CRITICO]")
        for msg, _ in criticos:
            print("    * " + msg)
    if atencoes:
        print("  [ATENCAO]")
        for msg, _ in atencoes:
            print("    * " + msg)
    if normais:
        print("  [OK]")
        for msg, _ in normais:
            print("    * " + msg)

    # Acoes recomendadas
    print("\n  ACOES AUTOMATICAS RECOMENDADAS:")
    print("  " + "-" * 40)
    acoes_filtradas = [a for a in resultado["acoes"] if a]
    if not acoes_filtradas:
        print("  Nenhuma acao necessaria - sistema operando normalmente.")
    else:
        for acao in acoes_filtradas:
            print("  > " + acao)

    print(sep)


# ─────────────────────────────────────────────
#  FUNCAO: RELATORIO FINAL DA SESSAO
# ─────────────────────────────────────────────
def gerar_relatorio_final():
    print("\n\n" + "=" * 60)
    print("        RELATORIO FINAL DA SESSAO DE MONITORAMENTO")
    print("=" * 60)

    total     = len(historico_leituras)
    criticos  = sum(1 for r in historico_leituras if r["severidade"] == "CRITICO")
    atencoes  = sum(1 for r in historico_leituras if r["severidade"] == "ATENCAO")
    normais   = total - criticos - atencoes

    print("\n  Total de modulos verificados : " + str(total))
    print("  Modulos em status CRITICO    : " + str(criticos))
    print("  Modulos em status ATENCAO    : " + str(atencoes))
    print("  Modulos em status OK         : " + str(normais))

    if criticos > 0:
        print("\n  MODULOS CRITICOS DETECTADOS:")
        for r in historico_leituras:
            if r["severidade"] == "CRITICO":
                print("    - " + r["modulo"] + " (verificado em " + r["timestamp"] + ")")

    # Estatisticas de temperatura e energia
    temps    = [r["temperatura"] for r in historico_leituras]
    energias = [r["energia"]     for r in historico_leituras]

    print("\n  ESTATISTICAS:")
    print("  Temperatura media   : " + str(round(sum(temps)    / total, 1)) + " C")
    print("  Temperatura maxima  : " + str(max(temps))                       + " C")
    print("  Energia media       : " + str(round(sum(energias) / total, 1)) + "%")
    print("  Energia minima      : " + str(min(energias))                   + "%")

    # Avaliacao global da missao
    print("\n  AVALIACAO GLOBAL DA MISSAO:")
    if criticos == 0 and atencoes == 0:
        print("  [MISSAO NOMINAL] - Todos os sistemas operando perfeitamente.")
    elif criticos == 0:
        print("  [MISSAO COM ALERTAS] - Situacao sob controle, mas requer atencao.")
    elif criticos <= total // 2:
        print("  [MISSAO EM RISCO] - Falhas criticas detectadas. Intervencao necessaria.")
    else:
        print("  [MISSAO EM PERIGO] - Maioria dos modulos criticos! Acionar protocolo de emergencia!")

    print("\n" + "=" * 60)


# ─────────────────────────────────────────────
#  FUNCAO: COLETAR DADOS DE UM MODULO
# ─────────────────────────────────────────────
def coletar_dados_modulo(nome_modulo):
    """Solicita ao usuario os valores de cada sensor do modulo."""
    print("\n--- Inserindo dados para o modulo: " + nome_modulo + " ---")

    while True:
        try:
            temp = float(input("  Temperatura (°C) [ex: 72.5]: "))
            break
        except ValueError:
            print("  Valor invalido. Digite um numero.")

    while True:
        try:
            energia = float(input("  Energia (%) [0-100]: "))
            if 0 <= energia <= 100:
                break
            print("  Valor deve estar entre 0 e 100.")
        except ValueError:
            print("  Valor invalido. Digite um numero.")

    while True:
        try:
            pressao = float(input("  Pressao (atm) [ex: 1.0]: "))
            break
        except ValueError:
            print("  Valor invalido. Digite um numero.")

    while True:
        try:
            oxigenio = float(input("  Oxigenio (%) [0-100]: "))
            if 0 <= oxigenio <= 100:
                break
            print("  Valor deve estar entre 0 e 100.")
        except ValueError:
            print("  Valor invalido. Digite um numero.")

    print("  Comunicacao: normal / degradada / falha_total")
    while True:
        com = input("  Status da comunicacao: ").strip().lower()
        if com in ("normal", "degradada", "falha_total"):
            break
        print("  Opcoes validas: normal, degradada, falha_total")

    print("  Status do modulo: operacional / avaria / falha_critica")
    while True:
        mod = input("  Status do modulo: ").strip().lower()
        if mod in ("operacional", "avaria", "falha_critica"):
            break
        print("  Opcoes validas: operacional, avaria, falha_critica")

    return temp, energia, pressao, oxigenio, com, mod


# ─────────────────────────────────────────────
#  MODO SIMULACAO AUTOMATICA
# ─────────────────────────────────────────────
def simular_modulo(nome_modulo):
    """Gera dados aleatorios para simular um modulo sem entrada do usuario."""
    temp     = round(random.uniform(40.0, 100.0), 1)
    energia  = round(random.uniform(5.0, 100.0),  1)
    pressao  = round(random.uniform(0.5, 1.5),    2)
    oxigenio = round(random.uniform(15.0, 25.0),  1)
    com      = random.choice(["normal", "normal", "degradada", "falha_total"])
    mod      = random.choice(["operacional", "operacional", "avaria", "falha_critica"])

    print("\n  [SIMULACAO] Dados gerados automaticamente para: " + nome_modulo)
    print("    Temperatura: " + str(temp) + " C | Energia: " + str(energia) +
          "% | Pressao: " + str(pressao) + " atm")
    print("    Oxigenio: " + str(oxigenio) + "% | Comunicacao: " + com +
          " | Modulo: " + mod)

    return temp, energia, pressao, oxigenio, com, mod


# ─────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────
def main():
    print("\n" + "=" * 60)
    print("   SISTEMA DE MONITORAMENTO DE MISSAO ESPACIAL - SERS")
    print("   Versao 2.0 | FIAP Global Solution 2026")
    print("=" * 60)

    print("\nModo de operacao:")
    print("  1 - Entrada manual de dados")
    print("  2 - Simulacao automatica (dados aleatorios)")

    while True:
        modo = input("\nEscolha o modo (1 ou 2): ").strip()
        if modo in ("1", "2"):
            break
        print("Opcao invalida. Digite 1 ou 2.")

    print("\nModulos disponiveis da nave:")
    for i, m in enumerate(MODULOS_NAVE, 1):
        print("  " + str(i) + ". " + m)

    print("\nDigite os numeros dos modulos a monitorar separados por virgula.")
    print("Exemplo: 1,3,5  |  ou  'todos' para monitorar todos")

    while True:
        escolha = input("Modulos: ").strip().lower()
        if escolha == "todos":
            modulos_escolhidos = MODULOS_NAVE[:]
            break
        try:
            indices = [int(x.strip()) for x in escolha.split(",")]
            if all(1 <= i <= len(MODULOS_NAVE) for i in indices):
                modulos_escolhidos = [MODULOS_NAVE[i - 1] for i in indices]
                break
            print("Indices fora do intervalo. Tente novamente.")
        except ValueError:
            print("Entrada invalida. Use numeros separados por virgula.")

    print("\nMonitorando " + str(len(modulos_escolhidos)) + " modulo(s): " +
          ", ".join(modulos_escolhidos))

    # Processa cada modulo escolhido
    for modulo in modulos_escolhidos:
        if modo == "1":
            temp, energia, pressao, oxigenio, com, mod = coletar_dados_modulo(modulo)
        else:
            temp, energia, pressao, oxigenio, com, mod = simular_modulo(modulo)

        resultado = verificar_sistema_completo(
            modulo, temp, energia, pressao, oxigenio, com, mod
        )
        exibir_resultado(resultado)

    # Gera relatorio ao final
    gerar_relatorio_final()

    print("\nSistema de monitoramento encerrado. Bons voos!\n")


# ─────────────────────────────────────────────
#  PONTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
