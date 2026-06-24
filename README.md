# SERS 2026 — Sistema de Monitoramento de Missão Espacial

## Global Solution — FIAP
**Disciplina:** Soluções em Energias Renováveis e Sustentáveis
**Curso:** Ciência da Computação — Turmas 1CCPG

## Integrantes
- Guilherme Reiche — RM: 569918
- Enzo Guislandi — RM: 569885
- Nicolas Nishi — RM: 572242

## Descrição do Projeto
O SERS 2026 é um sistema automatizado de monitoramento para múltiplos módulos de
uma missão espacial experimental. A solução simula o acompanhamento de variáveis
críticas para a sustentabilidade e segurança energética da missão, aplicando
conceitos de energia, potência e eficiência operacional na análise dos dados.

O sistema recebe (manualmente ou via simulação automática) dados de sensores de
cada módulo da nave, classifica a severidade das condições detectadas e recomenda
ações automáticas de resposta, com foco em decisões que preservam a operação dos
sistemas energéticos e de suporte à vida da missão.

## Funcionalidades

### Monitoramento de Dados
O sistema monitora 6 parâmetros operacionais por módulo:
- **Temperatura** (°C)
- **Energia** (%)
- **Pressão** (atm)
- **Oxigênio** (%)
- **Comunicação** com a Terra (normal / degradada / falha total)
- **Status estrutural** do módulo (operacional / avaria / falha crítica)

Os módulos disponíveis para monitoramento são: Propulsão, Habitação,
Comunicação, Energia e Científico.

### Geração de Alertas
Cada parâmetro é avaliado contra limiares pré-definidos e classificado em três
níveis de severidade:
- **OK** — parâmetro dentro da faixa normal de operação.
- **ATENÇÃO** — parâmetro fora do ideal, mas sem risco imediato.
- **CRÍTICO** — condição que exige intervenção de emergência.

A severidade geral de cada módulo é definida pelo alerta mais grave encontrado
entre todos os parâmetros analisados.

### Tomada de Decisão Automática
Para cada alerta gerado, o sistema recomenda automaticamente ações de resposta
coerentes com o cenário simulado — por exemplo, acionamento de resfriamento de
emergência em caso de superaquecimento, ativação de células de combustível de
reserva em caso de energia crítica, ou isolamento do módulo em caso de falha
estrutural.

### Visualização e Relatório
- Exibição individual e detalhada do status de cada módulo verificado, com
  parâmetros, alertas (agrupados por severidade) e ações recomendadas.
- Relatório final consolidado da sessão de monitoramento, com estatísticas
  (temperatura média/máxima, energia média/mínima), total de módulos em cada
  nível de severidade e avaliação global da missão (nominal, com alertas, em
  risco ou em perigo).

### Modos de Operação
- **Entrada manual:** o usuário informa os valores de cada sensor via terminal,
  com validação de tipo e faixa de valores.
- **Simulação automática:** o sistema gera valores aleatórios para os sensores,
  permitindo testar o comportamento do sistema sem necessidade de entrada manual.

## Aplicação dos Conceitos da Disciplina
O sistema aplica os conceitos de energia e sustentabilidade da missão ao tratar
o nível de energia como um parâmetro crítico de decisão: condições de energia
baixa ou crítica acionam automaticamente respostas de economia energética e
priorização de sistemas essenciais, refletindo estratégias reais de gestão
eficiente de recursos energéticos limitados em ambientes espaciais.
