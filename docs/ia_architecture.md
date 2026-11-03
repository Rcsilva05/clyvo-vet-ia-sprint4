# Arquitetura da solução CLYVO Vet IA

## Visão geral

A solução de IA do CLYVO Vet integra sensores do SOLIN com a aplicação de gestão veterinária para reforçar a tomada de decisão clínica. O foco é identificar risco de problemas urinários e transformar essa análise em orientações simples para tutor e técnico.

## Componentes

1. Sensor SOLIN
   - coleta dados de rotina urinária
   - envia eventos relevantes para a plataforma

2. Backend CLYVO Vet
   - recebe eventos e dados do pet
   - realiza persistência e regras de negócio

3. Motor de recomendação
   - calcula score de risco com base em padrões de urina, idade, condições e medicações
   - classifica prioridade em Baixa, Média, Alta e Crítica

4. LLM opcional
   - transforma a recomendação em linguagem natural
   - executa apenas quando a API do provedor estiver configurada

5. Interface do usuário
   - exibe status do pet e recomendação do tutor
   - disponibiliza painel clínico

## Fluxo

1. O pet gera eventos de uso (normal, frequente ou ausência de urina).
2. O backend consolida esses eventos e o perfil do pet.
3. O motor de regras calcula um score de risco.
4. O sistema gera duas mensagens: tutor e clínica.
5. Se configurado, o LLM reformula o conteúdo em linguagem natural.
6. A interface exibe a recomendação e o plano de acompanhamento.

## Vantagens

- auditável e explicável
- fácil de evoluir sem histórico massivo
- adequada para primeiro ciclo de dados do projeto
- mantém baixa dependência de modelos generativos em produção

## Limitações

- depende de qualidade e consistência dos dados do sensor
- sem histórico longitudinal grande, o modelo não substitui avaliação veterinária
- o LLM é complementar ao motor de regras
- neste protótipo, os pets e eventos são simulados; não há conexão real com MQTT, dispositivo ou banco de dados
- o score é demonstrativo e não foi validado clinicamente; não deve orientar tratamento ou restrição de água

## Mapa de dados

- ID do pet
- espécie e raça
- idade em meses
- peso
- condições clínicas
- medicações atuais
- padrão urinário
- eventos diários e intensidade

## Resultado esperado

O sistema ajuda o tutor a perceber sinais de alerta precocemente e auxilia o veterinário a priorizar atendimentos e acompanhamento.
