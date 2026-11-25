---
name: create-endpoint
description: Cria um novo endpoint HTTP em FastAPI/Python seguindo o padrão deste repositório (controller, service, domain, validação com Pydantic e tratamento de erro com HTTPException)
---

# Skill: create-endpoint

## Objetivo
Criar um endpoint HTTP novo no padrão do projeto, com mudanças mínimas e sem inventar arquitetura.

## Entradas obrigatórias
- `method`: GET | POST | PUT | PATCH | DELETE
- `path`: rota HTTP (ex.: `/api/v1/mensagens`)
- `controllerTarget`: arquivo/controller alvo (reaproveitar em `src/controller` ou criar novo somente se necessário)
- `serviceName`: nome do service alvo (ou criar novo em `src/services`)
- `requestDomain`: estrutura do request (campos, tipos e contrato JSON)
- `responseDomain`: estrutura do response (campos, tipos e contrato JSON)
- `businessRules`: regras de negócio essenciais
- `errorCases`: lista de erros esperados (400/404/409/422/500)

## Entradas opcionais
- `headers`: headers obrigatórios
- `queryParams`: query params
- `pathParams`: path params
- `idempotency`: se exige comportamento idempotente
- `auth`: requisitos de autenticação/autorização
- `openApiDocs`: necessidade de anotação/atualização OpenAPI

## Regras obrigatórias deste repositório
1. Não criar camadas/padrões novos além dos já existentes.
2. Reutilizar validação/erro/log já adotados (Pydantic/FastAPI, `HTTPException`, logger ECS em `src/infrastructure/logger.py`).
3. Posicionar arquivos nestes pacotes:
   - Controller: `src/controller`
   - Service: `src/services`
   - Domain (request/response): `src/domain`
   - Inicialização/registro de rotas: `src/app/startup.py`
   - Infra/observabilidade (se necessário): `src/infrastructure`
4. Preservar telemetria/logging/configuração atuais (`src/infrastructure/otel.py`, `src/infrastructure/logger.py`, `src/config`).
5. Não alterar endpoints existentes sem necessidade explícita.
6. Tratamento de erro deve seguir padrão atual via exceções HTTP (`HTTPException`) e respostas FastAPI.
7. Criar/atualizar testes unitários para controller e service para cada endpoint novo (preferencialmente em `tests/`).

## Procedimento
1. Verificar se já existe controller/service compatível para reaproveitar.
2. Criar/atualizar models de request/response em `src/domain` usando Pydantic.
3. Implementar/atualizar regra de negócio no service alvo em `src/services`.
4. Implementar endpoint no controller usando `APIRouter` (`@router.get/post/put/patch/delete`).
5. Mapear `path/query/body` com tipagem adequada (Pydantic + parâmetros FastAPI).
6. Garantir registro correto da rota em `src/app/startup.py` quando necessário.
7. Aplicar validações de entrada no model Pydantic e regras adicionais no service.
8. Mapear falhas de negócio para `HTTPException` apropriada para retorno HTTP padronizado.
9. Garantir resposta HTTP e payload aderentes ao contrato solicitado.
10. Criar/atualizar testes cobrindo cenários de sucesso e erro.

## Padrão de implementação esperado

### Controller
- Usar `APIRouter` e prefixo no padrão existente (ex.: `APIRouter(prefix="/api/v1")`).
- Receber e validar entrada via model Pydantic.
- Chamar o service sem concentrar regra de negócio no controller.
- Retornar payload compatível com model de resposta.

### Service
- Concentrar regra de negócio.
- Converter request -> response quando necessário.
- Lançar `HTTPException` com status apropriado (`400`, `404`, `409`, `422`, etc.) conforme contrato.

### Testes Unitários
- Criar/atualizar testes para controller e service envolvidos.
- Cobrir ao menos: 1 cenário de sucesso, 1 cenário de validação/erro de negócio e 1 cenário de erro inesperado (quando aplicável).
- No teste de controller, mockar o service; no teste de service, validar regra de negócio diretamente.

### Domain (Pydantic)
- Models em `src/domain` com tipagem e validações simples (`Field`, `min_length`, etc. quando necessário).
- Nomes consistentes com o padrão já existente no projeto.

## Saída esperada
- Lista objetiva de arquivos criados/alterados.
- Resumo curto do endpoint criado.
- Comandos de validação executáveis.

## Checklist de validação
- Aplicação sobe sem erro.
- Endpoint responde status correto para sucesso e erros mapeados.
- Models de request/response e validações refletem o contrato solicitado.
- Logging/telemetria/config seguem padrão atual.
- Testes do endpoint e service passam localmente.

## Comandos de validação
- `pytest`
- `uvicorn src.app.main:app --reload`

## Prompt de uso (exemplo)
Use a skill `create-endpoint` para criar o endpoint `POST /api/v1/mensagens`.

Detalhes:
- controllerTarget: `src/controller/mensagem_controller.py`
- serviceName: `MensagemService`
- requestDomain: `{ "conteudo": "string" }`
- responseDomain: `{ "mensagem": "string" }`
- businessRules: `conteudo obrigatório; rejeitar vazio`
- errorCases: `400 para payload inválido; 422 para regra de negócio; 500 para inesperado`
- tests: `criar testes unitários de controller e service com cenários de sucesso e erro`
