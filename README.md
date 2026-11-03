# CLYVO Vet IA — Sprint 4

Protótipo funcional do **SOLIN Insights**, componente de inteligência artificial para apoiar o acompanhamento da saúde urinária de pets. A demonstração combina eventos de exemplo inspirados no SOLIN com dados clínicos simulados, calcula uma pontuação de risco explicável e apresenta recomendações distintas para tutor e clínica veterinária.

> **Importante:** este repositório contém um protótipo acadêmico. Os dados são simulados e as regras não são diagnóstico veterinário nem foram validadas clinicamente. Não use as recomendações para tomar decisões reais de saúde animal.

## Entrega e vídeo

- **Repositório Sprint 4:** https://github.com/Rcsilva05/clyvo-vet-ia-sprint4
- **Vídeo pitch no YouTube:** _pendente de gravação e publicação; inserir aqui o link não listado._

## O que está implementado

- API web em Flask e interface de demonstração em português.
- Motor local de regras que calcula um score de 0 a 100 e classifica a prioridade em Baixa, Média, Alta ou Crítica.
- Uso de perfil demonstrativo do pet (idade, peso, condições, medicações e padrão urinário) e eventos de exemplo (micção normal/frequente, ausência de urina e consumo elevado de água).
- Mensagens separadas para tutor e clínica, além de uma ação sugerida.
- Integração opcional com a API de chat completions da OpenAI, se `OPENAI_API_KEY` estiver configurada. Sem chave ou se o serviço externo falhar, o app continua usando a análise local.
- Testes automatizados das regras de classificação.

## O que ainda é simulado / limitações

- Os pets e eventos estão em `src/sample_data.py`; não há banco de dados conectado.
- Não há conexão MQTT, firmware, leitura de sensor SOLIN nem integração real com o aplicativo CLYVO Vet.
- O motor usa regras fixas demonstrativas; os limites e pesos não são um modelo clínico validado.
- A chamada ao LLM é complementar e opcional. A demo deve funcionar sem chave de API.
- O vídeo precisa ser gravado pelo grupo, publicado como **não listado** e ter seu link inserido nesta página e no material final de entrega.

## Imagens e documentação

Os arquivos visuais da proposta da Sprint 3 foram mantidos no repositório:

- [Diagrama de arquitetura SOLIN Insights](Figura_Arquitetura_SOLIN_IA.png)
- [Mockup das telas de IA](Figura_Mockup_Telas_IA.png)
- [Documentação anterior da solução](CLYVO_VET_Documentacao_IA.docx)

Documentação desta implementação:

- [Arquitetura e fluxo de dados](docs/ia_architecture.md)
- [Roteiro do vídeo pitch de aproximadamente 5 minutos](docs/pitch_script.md)

## Tecnologias e estrutura

- Python 3.10 ou superior
- Flask — servidor web e API REST
- Requests — chamada HTTP opcional à API OpenAI
- Pytest — testes
- HTML, CSS e JavaScript — interface da demonstração

```text
.
├── app.py                       # aplicação Flask e endpoints
├── src/
│   ├── ia_engine.py             # score, regras e integração LLM opcional
│   └── sample_data.py           # pets e eventos fictícios
├── templates/
│   └── index.html               # tela da demonstração
├── tests/
│   └── test_ia_engine.py        # testes automatizados
├── docs/
│   ├── ia_architecture.md       # arquitetura e fluxo
│   └── pitch_script.md          # roteiro do vídeo
├── Figura_Arquitetura_SOLIN_IA.png
├── Figura_Mockup_Telas_IA.png
├── CLYVO_VET_Documentacao_IA.docx
├── requirements.txt
└── .env.example
```

## Como executar no Windows (passo a passo)

### 1. Instalar Python

Instale Python 3.10 ou superior e, durante a instalação no Windows, marque a opção para adicionar Python ao `PATH`. No terminal do VS Code, confirme:

```powershell
python --version
```

### 2. Baixar o repositório e abrir a pasta

No GitHub, clique em **Code > Download ZIP**, extraia o arquivo e abra a pasta extraída no VS Code. Alternativamente, se Git estiver instalado:

```powershell
git clone https://github.com/Rcsilva05/clyvo-vet-ia-sprint4.git
cd clyvo-vet-ia-sprint4
```

No VS Code, abra **Terminal > New Terminal**. Confira se o terminal está na pasta do projeto (o caminho termina com `clyvo-vet-ia-sprint4`).

### 3. Criar e ativar um ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Quando ativo, o terminal mostra `(.venv)` antes do prompt. Se o PowerShell bloquear a ativação, execute apenas nesta janela:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependências

Com `(.venv)` ativo:

```powershell
python -m pip install -r requirements.txt
```

Espere até aparecer `Successfully installed`. Avisos sobre atualização do `pip` ou cache não significam necessariamente falha; confira se o comando terminou sem erro.

### 5. Executar os testes

```powershell
python -m pytest -q
```

Resultado esperado:

```text
2 passed
```

### 6. Iniciar a aplicação

```powershell
python app.py
```

Deixe esse terminal aberto. Quando aparecer `Running on http://127.0.0.1:5000`, o servidor está pronto.

### 7. Abrir e testar a tela

No navegador, acesse <http://127.0.0.1:5000/>. Selecione um pet e clique em **Gerar recomendação IA**. Confira se o nome selecionado corresponde ao nome apresentado no resultado, e observe score, prioridade, ação, resumo do tutor e resumo clínico.

Os dados de demonstração são:

| ID | Pet | Cenário de exemplo |
|---|---|---|
| `pet-001` | Luna | eventos de micção frequente e consumo elevado de água |
| `pet-002` | Thor | eventos de micção normal |
| `pet-003` | Mimi | eventos de ausência prolongada de urina |

Para encerrar o servidor, volte ao terminal onde `python app.py` está rodando e pressione `Ctrl+C`.

## Como testar a API

Mantenha o servidor em execução e abra um **segundo terminal** no VS Code. Consulte a saúde do serviço:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
```

Liste os pets:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/pets
```

Peça uma recomendação para Mimi:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:5000/api/recommendation `
  -ContentType "application/json" `
  -Body '{"petId":"pet-003"}'
```

Na resposta, confira `pet.name` (`Mimi`), `risk_score`, `priority`, `recommendation`, `tutor_summary` e `clinical_summary`. IDs inexistentes retornam erro 404; uma requisição sem `petId` retorna erro 400.

## Integração opcional com LLM

A aplicação usa o motor local mesmo sem configurar serviço externo. Para demonstrar a integração generativa, obtenha uma chave de API por conta própria e configure-a somente na sua máquina. **Nunca publique a chave no GitHub, no README, em capturas de tela ou no vídeo.**

No PowerShell, na mesma janela em que vai iniciar o app:

```powershell
$env:OPENAI_API_KEY = "SUA_CHAVE"
$env:OPENAI_MODEL = "gpt-4o-mini"
python app.py
```

Se nenhuma chave estiver configurada, a tela pode mostrar “Resumo offline do motor de regras”; isso é o modo demonstrativo local, não uma falha da API da aplicação. Não é necessário configurar LLM para testar a interface e os testes automatizados.

## Capturas de tela e demonstração em vídeo

Seu amigo pode seguir estes passos para preparar as evidências:

1. Inicie o app e abra `http://127.0.0.1:5000/`.
2. Tire uma captura da tela inicial e da demonstração de cada cenário (Luna, Thor e Mimi). No Windows, use `Win + Shift + S`, selecione a área do app e salve a imagem na pasta de evidências.
3. Mostre também a documentação visual desta proposta abrindo `Figura_Arquitetura_SOLIN_IA.png` e `Figura_Mockup_Telas_IA.png` no VS Code ou no visualizador de imagens.
4. Grave a tela com narração usando uma ferramenta disponível no computador. Antes de gravar, feche terminais que revelem caminhos pessoais, notificações e qualquer segredo. Não exiba chaves de API.
5. Explique com clareza quais dados são simulados e que a integração MQTT/banco real não faz parte deste protótipo.
6. Revise o vídeo, áudio e duração (aproximadamente 5 minutos) antes de publicar.
7. No YouTube Studio, envie o vídeo e selecione a visibilidade **Não listado**. Aguarde o processamento e teste o link em uma janela anônima.
8. Substitua o texto “pendente” na seção **Entrega e vídeo** acima pelo link real e atualize também o ZIP exigido pela disciplina.

### Sugestão de sequência para cerca de 5 minutos

- **0:00–0:30 — Apresentação:** equipe, CLYVO Vet e SOLIN Insights.
- **0:30–1:10 — Problema:** dificuldade de perceber alterações na rotina do pet.
- **1:10–2:00 — Como funciona:** eventos e perfil entram no motor de regras; score gera prioridade e mensagens específicas.
- **2:00–3:30 — Demonstração:** selecionar Luna, Thor e Mimi, gerar recomendações e comparar os resultados; mostrar a API ou os testes brevemente.
- **3:30–4:20 — Benefícios e arquitetura:** mostrar diagrama e mockup; explicar apoio ao tutor e à clínica.
- **4:20–5:00 — Limites e conclusão:** dados simulados, LLM opcional e protótipo acadêmico; concluir sem afirmar diagnóstico real.

Um roteiro de fala mais detalhado está em [`docs/pitch_script.md`](docs/pitch_script.md).

## Endpoints da API

| Método | Caminho | Uso |
|---|---|---|
| `GET` | `/` | Interface web |
| `GET` | `/health` | Verificação do serviço |
| `GET` | `/api/pets` | Lista de pets demonstrativos |
| `POST` | `/api/recommendation` | Calcula score e gera recomendação |

Exemplo do corpo para `POST /api/recommendation`:

```json
{
  "petId": "pet-001"
}
```

## Resultados de validação

- Testes automatizados: `python -m pytest -q` — **2 testes passaram** no ambiente de desenvolvimento.
- API: `/health`, listagem de pets e geração de recomendação exercitadas localmente.
- Interface: demonstração local confirma a exibição do pet selecionado e dos campos de recomendação.

Os resultados demonstram o funcionamento do protótipo com dados artificiais; não representam validação clínica nem integração com dispositivos reais.

## Integrantes

| Nome | RM |
|---|---:|
| Natália Cristina | 564099 |
| Nickolas Davi | 564105 |
| Rodrigo Silva | 565162 |
| Samara Vilela | 566133 |
| Otávio Ferreira | 565960 |
