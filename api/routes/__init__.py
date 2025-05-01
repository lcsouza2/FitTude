"""
Módulo de Rotas da API

Este módulo inicializa as rotas disponíveis na aplicação. Abaixo estão listadas todas as rotas
presentes nos submódulos desta pasta, organizadas por método HTTP e com os schemas utilizados.

Rotas disponíveis:

GET:
- /api/data/groups: Retorna todos os grupamentos musculares. (Sem schema)
- /api/data/muscles: Retorna todos os músculos. (Sem schema)
- /api/data/equipment: Retorna todos os equipamentos. (Sem schema)
- /api/data/exercises: Retorna todos os exercícios. (Sem schema)
- /api/data/workout/sheets: Retorna todas as fichas de treino. (Sem schema)
- /api/data/workout/divisions: Retorna todas as divisões de treino. (Sem schema)
- /api/data/workout/division-exercises: Retorna todos os exercícios de uma divisão. (Sem schema)
- /api/data/workout/reports: Retorna todos os relatórios de treino. (Sem schema)

POST:
- /api/user/register: Inicia o processo de registro de um usuário. (Schema: UserRegistro)
- /api/user/login: Realiza o login de um usuário. (Schema: UserLogin)
- /api/user/logout: Realiza o logout de um usuário. (Sem schema)
- /api/user/password_change: Inicia o processo de alteração de senha. (Schema: UserPwdChange)
- /api/user/refresh_token: Renova o token de sessão do usuário. (Sem schema)
- /api/data/groups/new: Cria um novo grupamento muscular. (Schema: Grupamento)
- /api/data/equipment/new: Cria um novo equipamento. (Schema: Aparelho)
- /api/data/muscle/new: Cria um novo músculo. (Schema: Musculo)
- /api/data/exercise/new: Cria um novo exercício. (Schema: Exercicio)
- /api/data/workout/sheet/new: Cria uma nova ficha de treino. (Schema: FichaTreino)
- /api/data/workout/division/new: Cria uma nova divisão de treino. (Schema: DivisaoTreino)
- /api/data/workout/division/add_exercise: Adiciona exercícios a uma divisão. (Schema: DivisaoExercicio)
- /api/data/workout/report/new_report: Cria um novo relatório de treino. (Schema: RelatorioTreino)
- /api/data/workout/report/add_exercise: Adiciona exercícios a um relatório. (Schema: SerieRelatorio)

PUT:
- /api/data/groups/update/{group_name}: Atualiza um grupamento muscular. (Schema: GrupamentoAlterar)
- /api/data/muscle/update/{muscle_id}: Atualiza um músculo. (Schema: MusculoAlterar)
- /api/data/equipment/update/{equipment_id}: Atualiza um equipamento. (Schema: AparelhoAlterar)
- /api/data/exercise/update/{exercise_id}: Atualiza um exercício. (Schema: ExercicioAlterar)
- /api/data/workout/sheet/update/{sheet_id}: Atualiza uma ficha de treino. (Schema: FichaTreinoAlterar)
- /api/data/workout/division/update/{division}/{new_division_name}: Atualiza uma divisão de treino. (Sem schema)
- /api/data/workout/division/exercise/update/: Atualiza um exercício em uma divisão. (Schema: DivisaoExercicioAlterar)

DELETE:
- /api/data/groups/inactivate/{group_name}: Inativa um grupamento muscular. (Sem schema)
- /api/data/muscle/inactivate/{muscle_id}: Inativa um músculo. (Sem schema)
- /api/data/equipment/inactivate/{equipment_id}: Inativa um equipamento. (Sem schema)
- /api/data/exericse/inactivate/{exercise_id}: Inativa um exercício. (Sem schema)
- /api/data/workout/sheet/inactivate/{sheet_id}: Inativa uma ficha de treino. (Sem schema)
- /api/data/workout/division/inactivate/{division}: Inativa uma divisão de treino. (Sem schema)
- /api/data/workout/division/exercise/inactivate: Inativa um exercício em uma divisão. (Schema: DivisaoExercicioInativar)
- /api/data/workout/report/delete/{report_id}: Exclui um relatório de treino. (Sem schema)
"""