Todo List API — Backend
 
Backend da aplicação Todo List, desenvolvido em Python com FastAPI. A API gerencia usuários e tarefas, realiza autenticação e fornece dados para o Painel e a página Analytics.
1. Arquitetura do projeto
A aplicação é organizada em camadas para separar as responsabilidades:
- Routers (app/api/routers): recebem as requisições HTTP.
- Schemas (app/schemas): validam os dados e definem o formato das respostas.
- Services (app/services): concentram as regras de negócio.
- Repositories (app/repositories): acessam e alteram os dados no banco.
- Models (app/models): representam as entidades persistidas.
- Core (app/core): reúne configurações, segurança, datas e exceções.
- DB (app/db): configura a conexão e a sessão do banco.
- app/main.py: cria a aplicação FastAPI e registra as rotas.
Fluxo geral: requisição → router → service → repository/model → banco de dados → resposta JSON.
 
2. Tecnologias
Tecnologia  Utilização
Python  Linguagem do backend
FastAPI Criação da API
Uvicorn Servidor da aplicação
SQLAlchemy  Acesso ao banco de dados
Pydantic  Validação dos dados
SQLite / PostgreSQL Bancos de dados
PyJWT e bcrypt  Autenticação e proteção de senhas
Pandas  Apoio aos cálculos do Analytics
 
3. Instalação e configuração
Abra o terminal na pasta `backend` do projeto.
**1. Crie o ambiente virtual:**
```powershell
python -m venv .venv
```
**2. Ative o ambiente virtual:**
```powershell
.\.venv\Scripts\Activate
```
**3. Instale as dependências:**
```powershell
pip install -r requirements.txt
```
**4. Configure as variáveis de ambiente:**
Crie o arquivo `.env` a partir do modelo `.env.example`:
```powershell
Copy-Item .env.example .env
```
Depois, abra o arquivo `.env` e configure as variáveis necessárias, como `DATABASE_URL` e `SECRET_KEY`.
 
**5. Execute o servidor:**
```powershell
python -m uvicorn app.main:app --reload
```
A API ficará disponível em `http://127.0.0.1:8000`.
 
A documentação interativa dos endpoints pode ser acessada em `http://127.0.0.1:8000/docs`.
 
 
4. Configuração do banco de dados
Crie o arquivo .env usando .env.example como modelo:
 
Windows
Copy-Item .env.example .env
cp .env.example .env
Configure as variáveis:
- DATABASE_URL: endereço de conexão com o banco.
- JWT_SECRET: segredo privado para assinar os tokens (mínimo de 32 caracteres).
- JWT_EXPIRA_MINUTOS: tempo de validade do token.
Gere um segredo forte com:
python -c "import secrets; print(secrets.token_hex(32))"
Opção A — SQLite local
No .env:
DATABASE_URL=sqlite:///./todo_list.db
JWT_SECRET=COLOQUE_UM_SEGREDO_FORTE_AQUI
JWT_EXPIRA_MINUTOS=120
O SQLite utiliza um arquivo local e não exige um servidor de banco separado.
Opção B — PostgreSQL no Render
Crie um banco PostgreSQL no Render e utilize a URL de conexão externa. O formato esperado é:
DATABASE_URL=postgresql+psycopg://USUARIO:SENHA@HOST/BANCO?sslmode=require
Substitua os dados pelos fornecidos pelo Render. Se a URL já tiver parâmetros após ?, acrescente &sslmode=require.
 
Use apenas uma DATABASE_URL por vez. Nunca publique o .env ou credenciais no GitHub.
5. Executar a API
Com o terminal na pasta backend, ambiente virtual ativado e .env configurado:
python -m uvicorn app.main:app --reload
Endereços locais:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
O --reload reinicia o servidor quando o código muda e é destinado ao desenvolvimento.
6. Autenticação
A API utiliza JWT. O usuário faz login e recebe um token, que deve ser enviado nas rotas protegidas.
 
Cadastro — POST /usuarios
{
  "nome": "Ana",
  "email": "ana@example.com",
  "senha": "senha123"
}
Login — POST /usuarios/login
{
  "email": "ana@example.com",
  "senha": "senha123"
}
A resposta do login contém accessToken, tokenType, expiraEm e os dados públicos do usuário.
 
Envie o token no cabeçalho:
Authorization: Bearer SEU_TOKEN
GET /usuarios/me retorna os dados do usuário autenticado. O prazo padrão do token é de 120 minutos, configurável por JWT_EXPIRA_MINUTOS.
7. Endpoints
As rotas de tarefas exigem autenticação. Cadastro e login são públicos.
Método  Endpoint  Finalidade
GET / Verificar disponibilidade da API
POST  /usuarios Cadastrar usuário
POST  /usuarios/login Fazer login
GET /usuarios/me  Consultar usuário autenticado
POST  /tasks  Criar tarefa
GET /tasks  Listar tarefas
GET /tasks/resumo Obter resumo do Painel
GET /tasks/analytics  Obter indicadores do Analytics
GET /tasks/{tarefa_id}  Consultar tarefa
PATCH /tasks/{tarefa_id}  Atualizar tarefa
DELETE  /tasks/{tarefa_id}  Excluir tarefa
 
 
Filtros da listagem
GET /tasks aceita:
Parâmetro Valores/finalidade
status  pendente ou concluida
prioridade  baixa, media, alta ou urgente
prazoAte  Data limite (AAAA-MM-DD)
busca Pesquisa pelo título
ordenarPor  CriadoEm, prazo ou prioridade
ordem asc ou desc
limit / offset  Paginação
 
 
Exemplo:
GET /tasks?status=pendente&prioridade=alta&ordenarPor=prazo&ordem=asc
A quantidade total correspondente aos filtros é informada no cabeçalho X-Total-Count.
 
 
8. Contrato JSON
O contrato JSON define os campos que o front-end envia e recebe. Os schemas do projeto utilizam nomes camelCase nas entradas e respostas.
 
Usuário: no cadastro, nome é obrigatório, email deve ser válido e senha deve ter pelo menos 6 caracteres. A resposta pública contém id, nome, email e criadoEm; a senha não é retornada.
 
Tarefa: na criação, envie:
{
  "titulo": "Estudar Python",
  "prioridade": "alta",
  "prazo": "2026-12-01"
}
- titulo: obrigatório.
- prioridade: baixa, media, alta ou urgente.
- prazo: data AAAA-MM-DD ou null.
- status: pendente ou concluida; começa como pendente.
O backend identifica o dono da tarefa pelo token. O front-end não deve definir o usuario_id.
Códigos HTTP comuns
Código  Significado
200 Requisição concluída
201 Registro criado
204 Exclusão concluída, sem corpo
401 Token inválido/ausente ou login inválido
403 Acesso não permitido à tarefa
404 Recurso não encontrado
409 E-mail já cadastrado
422 Dados inválidos
 
 
9. Painel e Analytics
Resumo — GET /tasks/resumo
 
Retorna total, pendentes, concluidas e atrasadas para o usuário autenticado.
 
Analytics — GET /tasks/analytics?dias=7
 
O parâmetro dias define a janela de agrupamento diário (padrão 7; intervalo permitido de 1 a 90). O schema prevê total de tarefas, quantidade e taxa de conclusão, conclusões por dia, tarefas pendentes por prioridade, conclusões por dia da semana e percentual concluído no prazo.
 
Atenção: a implementação de Analytics precisa ser revisada. Foram identificadas divergências entre os dados produzidos pelo serviço e os campos/tipos do schema, além de um possível problema no tratamento das datas. Valide e corrija esse endpoint antes de depender dele no front-end.
 
 
10. Integração com o front-end React
A tabela relaciona as telas esperadas aos endpoints disponíveis. Como o código React não foi incluído no pacote analisado, confirme as funções e chamadas no repositório do front-end.
Tela/função do front-end  Endpoint
Cadastro (Register) POST /usuarios
Login (Login) POST /usuarios/login
Dados do usuário/sessão GET /usuarios/me
Listar tarefas (Tasks)  GET /tasks
Criar tarefa (TaskForm) POST /tasks
Visualizar tarefa GET /tasks/{tarefa_id}
Editar/concluir tarefa  PATCH /tasks/{tarefa_id}
Excluir tarefa  DELETE /tasks/{tarefa_id}
Cards do Painel (Dashboard) GET /tasks/resumo
Indicadores (Analytics) GET /tasks/analytics
 
 
Exemplo de chamada protegida:
const response = await fetch("http://127.0.0.1:8000/tasks", {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});
Para enviar JSON, inclua também Content-Type: application/json e body: JSON.stringify(dados). Em produção, use a URL publicada da API.
 
 
11. Limitações conhecidas
- Analytics: serviço e schema apresentam divergências que precisam ser corrigidas e testadas.
- CORS: a leitura de CORS_ORIGINS precisa ser conferida; a configuração analisada aparenta consultar a variável errada nesse ponto.
- Recuperação de senha: não foi identificada rota para solicitar ou concluir a redefinição.
- Testes automatizados: há dependências de teste, mas não foram localizados arquivos de testes no material analisado.
- Migrações: não foi identificada configuração do Alembic. A criação automática de tabelas não substitui migrações para mudanças futuras.
- Produção: --reload é para desenvolvimento. A publicação exige configuração própria de execução, HTTPS, banco e CORS.
 
 
12. Planejamento de 14 dias
Dia Atividade Status
1 Revisar arquitetura e documentação  Pendente
2 Testar instalação e dependências  Pendente
3 Testar SQLite local Pendente
4 Validar PostgreSQL no Render  Pendente
5 Testar cadastro e login Pendente
6 Testar autenticação nas rotas protegidas  Pendente
7 Testar endpoints de tarefas Pendente
8 Testar filtros e paginação  Pendente
9 Conferir contratos JSON Pendente
10  Corrigir Analytics  Pendente
11  Testar resumo e Analytics Pendente
12  Integrar React aos endpoints  Pendente
13  Revisar limitações e configurações  Pendente
14  Fazer teste geral e atualizar o README  Pendente
 
 
Com a API em execução, acesse http://127.0.0.1:8000/docs para consultar e testar as rotas.
 
Segurança: não publique .env, senhas, tokens ou URLs de banco com credenciais.
tem menu de contexto