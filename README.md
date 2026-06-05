# Sistema-Completo-de-Atendimento-e-Analise

## Objetivo
Construir um software completo de gerenciamento de atendimentos, com cadastro, filas, historico, relatorios e analise de desempenho. Deve usar conteudos de todas as secoes (Python basico, Big-O, vetores, pilhas/filas/deques, listas encadeadas, recursao e ordenacao).

## Contexto (dia a dia)
Sistema para uma clinica ou central de atendimento com fila comum, fila de prioridade e historico de atendimentos.

## Progresso atual
- ✅ Cadastro de clientes e atendentes
- ✅ Busca binária por ID usando vetor ordenado
- ✅ Lista encadeada de clientes ativos
- ✅ Filas comum e de prioridade
- ✅ Abertura e chamada de atendimento
- ✅ Finalização de atendimento com registro
- ✅ Histórico de atendimentos por cliente
- ✅ Desfazer última finalização com pilha
- ✅ Cálculo de tempo médio de atendimento
- ✅ Exportar relatórios em CSV implementado no serviço, interface ainda será integrada

## Requisitos funcionais (obrigatorios)
1. Cadastro de clientes (id, nome, telefone, prioridade).
2. Cadastro de atendentes (id, nome).
3. Abertura de atendimento (cliente entra em fila).
4. Fila comum e fila de prioridade.
5. Chamada do proximo atendimento considerando prioridade.
6. Finalizacao do atendimento com registro (data, duracao, atendente).
7. Historico de atendimentos por cliente.
8. Desfazer a ultima finalizacao (pilha).
9. Remover clientes inativos (lista encadeada).
10. Relatorio de tempo medio de atendimento.
11. Exportar relatorios em CSV.
12. Busca rapida por cliente (vetor ordenado por id + busca binaria).

## Requisitos funcionais (extras)
- Filtro por data.
- Top 5 clientes mais atendidos.
- Alertas para tempo de espera alto.

## Requisitos nao funcionais (obrigatorios)
- Interface por terminal ou simples GUI em texto.
- Persistencia de dados em arquivo.
- Codigo modularizado em pastas.
- Tratamento completo de erros de entrada.
- Performance: justificar estruturas usadas com Big-O.
- Cobertura de testes basicos (unitarios).

## Estruturas e algoritmos obrigatorios
- Vetor ordenado para busca binaria por id.
- Vetor nao ordenado para cadastros temporarios.
- Fila de prioridade para atendimentos urgentes.
- Fila comum para atendimentos normais.
- Pilha para desfazer ultima acao.
- Lista encadeada para lista de clientes ativos.
- Ordenacao (insertion/merge/quick) para relatorios.
- Recursao em pelo menos uma rotina (ex: busca em estrutura ou relatorio).

## Regras de negocio
- Cliente prioridade sempre na frente, mas manter ordem de chegada.
- Atendente so atende um cliente por vez.
- Nao permitir finalizar atendimento sem cliente em fila.
- Nao permitir remover cliente com atendimento em aberto.

## Requisitos de qualidade
- Separar camada de dados, regras e interface.
- Funcoes pequenas e responsaveis.
- Nomes claros.
- Logs de operacoes importantes.

## Versionamento e boas praticas (obrigatorio)
- Repositorio GitHub publico ou privado com acesso ao professor.
- Commits frequentes com mensagens objetivas.
- README com objetivos, requisitos e como executar.
- Arquivo requirements.txt (mesmo que vazio).
- Seguir PEP 8 e boas praticas de organizacao.

## Entregaveis
- Codigo completo e organizado.
- README detalhado.
- Dados de exemplo.
- Relatorio curto explicando estruturas, Big-O e escolhas.

## Criterios de avaliacao
- Atendimento de todos os requisitos obrigatorios.
- Uso correto das estruturas exigidas.
- Estabilidade (sem travar em entradas invalidas).
- Qualidade do codigo e organizacao.
- Capacidade de explicar as decisoes tecnicas.
