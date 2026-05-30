# Oracle Doc Generator

Ferramenta desenvolvida em Python que se conecta diretamente a um banco Oracle e gera documentação técnica completa de forma automática. A documentação é produzida em HTML navegável, com menu lateral, busca por nome, links entre objetos e diagramas de relacionamento gerados via PlantUML.

O projeto nasceu da necessidade real de documentar um banco Oracle de produção com dezenas de tabelas, views, procedures, functions, packages, triggers, sequences, indexes, synonyms e jobs — sem nenhuma documentação formal existente.


## Motivação

Bancos de dados Oracle crescem ao longo dos anos sem documentação formal. Alterações são feitas sem conhecimento das dependências entre objetos, e novos desenvolvedores levam semanas para entender o schema. Esta ferramenta resolve esse problema lendo os metadados diretamente do dicionário de dados do Oracle e gerando uma documentação navegável que pode ser aberta no browser sem instalar nada.


## Estrutura do Projeto

```
oracle_doc_gen/
│
├── main.py                        
├── config.py                      
├── config_example.py              
├── requirements.txt              
│
├── extractor/                     
│   ├── tables.py                  
│   ├── views.py                   
│   ├── sequences.py               
│   ├── procedures.py              
│   ├── functions.py               
│   ├── packages.py                
│   ├── triggers.py                
│   ├── types.py                   
│   ├── indexes.py                 
│   ├── synonyms.py                
│   ├── dependencies.py            
│   └── jobs.py                    
│
├── processor/                     
│   ├── relations.py               
│   ├── deps_graph.py              
│   └── schema_map.py              
│
├── generator/                     
│   ├── html/
│   │   ├── assets/
│   │   │   ├── style.css          
│   │   │   └── search.js          
│   │   ├── templates/
│   │   │   └── base.html          
│   │   ├── builder.py             
│   │   ├── index.py               
│   │   ├── builder_tables.py      
│   │   ├── builder_views.py       
│   │   ├── builder_procedures.py  
│   │   ├── builder_functions.py   
│   │   ├── builder_packages.py    
│   │   ├── builder_triggers.py    
│   │   ├── builder_sequences.py   
│   │   ├── builder_indexes.py     
│   │   ├── builder_synonyms.py    
│   │   └── builder_jobs.py        
│   └── plantuml.py                
│
└── output/ (Gerada ao rodar o sistema)                       
    
```

Cada camada tem uma responsabilidade única e não ultrapassa seus limites:

- `extractor/` faz exclusivamente consultas SQL ao banco via dicionário de dados Oracle (`USER_*`). Não sabe que HTML existe.
- `processor/` recebe os dados extraídos e os cruza — monta o mapa de relacionamentos entre tabelas via chaves estrangeiras e o grafo de dependências entre objetos.
- `generator/` recebe os dados já processados e escreve os arquivos de saída. Não faz nenhuma consulta ao banco.
- `output/` contém apenas arquivos gerados automaticamente. Nunca deve ser editado manualmente.


## Pré-requisitos

- Python 3.11 ou superior
- Acesso a um banco Oracle (usuário, senha, host e service name)
- Conexão de rede com o servidor Oracle
- Conexão com a internet para renderizar os diagramas PlantUML


## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/oracle_doc_gen.git
cd oracle_doc_gen
pip install -r requirements.txt
```

Crie o arquivo de configuração a partir do exemplo:

```bash
cp config_example.py config.py
```

Edite o `config.py` com os dados do seu banco:

```python
HOST     = ""
PORTA    = 1521
SERVICE  = "ORCL"
USUARIO  = "SCHEMA_USER"
SENHA    = "SUA_SENHA"
SCHEMA   = "SCHEMA_NAME"
```


## Como Usar

Execute o `main.py` e escolha uma das opções do menu:

```bash
python main.py
```

```
MENU
0  - Sair
1  - Gerar Documentação HTML
```

Quando terminar, abra o arquivo `output/index.html` no browser.


## O que é Documentado

### Tabelas
- Nome, status e total de registros
- Colunas com tipo, tamanho, nullable e valor default
- Constraints com identificação de chaves primárias e estrangeiras
- Links clicáveis para as tabelas referenciadas nas chaves estrangeiras
- Diagrama de relacionamentos gerado automaticamente via PlantUML

### Views
- Colunas com tipo, tamanho e nullable
- Dependências com links para os objetos referenciados
- Código fonte da view

### Procedures
- Status e data da última alteração
- Argumentos com tipo e direção (IN, OUT, IN/OUT)
- Dependências com links para os objetos referenciados
- Código fonte completo

### Functions
- Status e data da última alteração
- Argumentos com tipo, direção e posição — o retorno é identificado como RETURN
- Dependências com links para os objetos referenciados
- Código fonte completo

### Packages
- Status e data da última alteração
- Lista de subprogramas (procedures e functions internas) com seus argumentos
- Dependências com links para os objetos referenciados
- Header (especificação) e Body (implementação) completos

### Triggers
- Tabela associada, evento disparador e tipo
- Status e data da última alteração
- Dependências com links para os objetos referenciados
- Código fonte completo

### Sequences
- Valor mínimo, máximo e último valor gerado
- Incremento, cache, flag cíclico e flag ordenado

### Indexes
- Organizados por tabela — cada tabela tem sua própria página listando todos os indexes
- Tipo, unicidade e status de cada index
- Colunas que compõem o index com posição e ordem

### Synonyms
- Owner e objeto referenciado
- DB Link quando aplicável

### Jobs
- Tipo, estado e flag de habilitado
- Intervalo de repetição
- Datas de última e próxima execução
- Quantidade de execuções e falhas
- Ação executada pelo job


## Como Funciona a Geração de Diagramas

Os diagramas de relacionamento são gerados para cada tabela usando o protocolo de encoding do PlantUML. O código `.puml` é comprimido com `zlib`, codificado com o alfabeto proprietário do PlantUML e enviado como parâmetro de URL para o servidor público `plantuml.com/plantuml/svg/`. O diagrama é renderizado como SVG diretamente no browser, sem necessidade de instalar o PlantUML localmente.

Cada diagrama mostra a tabela atual com todas as suas colunas (identificando PKs e FKs) e as tabelas diretamente relacionadas — apenas com o nome, sem listar as colunas — para manter a legibilidade. O código `.puml` completo fica disponível na própria página em um bloco expansível.


## Como Funciona a Busca

Todas as páginas de listagem possuem um campo de busca que filtra os resultados em tempo real. A busca é implementada em JavaScript puro no arquivo `search.js` e percorre todas as células da tabela visível, ocultando as linhas que não correspondem ao texto digitado. Não há dependência de bibliotecas externas.


## Como Funcionam os Links entre Objetos

A função `linkObjeto` no `builder.py` recebe o nome e o tipo de um objeto referenciado e verifica se o arquivo HTML correspondente foi gerado antes de criar o link. Se o arquivo não existir — seja porque é um objeto interno do Oracle como `STANDARD` ou `DBMS_OUTPUT`, ou por qualquer outro motivo — o nome é exibido como texto puro sem link, evitando erros de navegação.


## Segurança

O arquivo `config.py` contém as credenciais do banco e está listado no `.gitignore` — ele nunca é versionado. O repositório contém apenas o `config_example.py` com os campos vazios para orientar a configuração.

A pasta `output/` também está no `.gitignore` — os arquivos gerados não são versionados, apenas o código que os gera.


## Dependências

```
oracledb
openpyxl
```

As bibliotecas `zlib` e `base64` utilizadas na geração dos diagramas PlantUML são nativas do Python e não precisam ser instaladas.


## Observações

- A ferramenta utiliza exclusivamente views `USER_*` do dicionário de dados Oracle, documentando apenas os objetos do schema do usuário conectado.
- O campo `num_rows` da `USER_TABLES` não é utilizado — a contagem de registros é feita com `COUNT(*)` em cada tabela para garantir valores precisos.
- Objetos com status `INVALID` no banco são destacados visualmente com tag vermelha na documentação gerada.
- O gerador ainda está na sua primeira versão, novas melhorias serão implementadas futuramente.