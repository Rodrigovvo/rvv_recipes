# RVV-RECIPES

#### A Stack utilizada
* Python 3.10
* Framework: Django: 4.0.4
* Django-rest-framework 3.13.1
* Postgresql
* Docker
* Docker-compose

#### Das considerações sobre o projeto
Este capítulo do README é de documentação pessoal, sobre como foi/é a evolução projeto, contendo informações sobre decisões técnicas e como foi a maneira de pensar o projeto, além de sugestões/ideias para eventuais melhorias futuras. 

* A autenticação do projeto: 'somente alguém autenticado deve cadastrar receitas e demais itens', os demais (não credenciados) terão acesso de leitura.
 - Não houve tempo para implementar um sistema de autenticação mais completo, inicialmente a ideia era implementar via JWT com acesso via TOKEN, pode ser viável em futuras implementações. Foi decidido por utilizar a autenticação padrão, com usuario e senha.
* Modelos: As receitas possuem ingredientes, desta forma, verificar a implementação do um vínculo ManyToMany ou verificar a aplicação de ArrayField, considerando o uso Postgresql como db.
    - Houve escolha pela relação ManyToMany, considerando que a implementação de ArrayField cabe um pouco mais de estudo, mas a análise inicial é de que seria muito custosa para o banco de dados, traria alguma dificuldade com a integração com o ORM e complexidade a mais ao projeto.
* Views: Verificar se utilizarei o ModelViewSet ou as views 'generics'. 
    - Optei pelo ModelViewSet por considerar a forma mais adequada para prototipação, carregando funções básicas pré-desenvolvidas, a opção foi por ganho de tempo. As views 'generics' se mostram mais versáteis, contudo, a opção foi para maior dinâmicidade na entrega.
    - Na ViewSet do Chef sobrescrevi o método de deleção para que seja somente um 'soft_delete' com a alteração do boleano 
    'active' para o valor False, evitando a perda de dados do Chef, no sistema. 
* Da opção pela action de search e uma rota para todas as buscas:
    - Optei por controlar as verificações da search de receitas através de uma única rota, facilitando o agrupamento de parâmentros de pesquisa. 
* Dos testes, testes para CRUD de todas as rotas, testar as funções de pesquisa e todos os parâmetros, testar com mais de um parâmetro de pesquisa, verificar a obrigatoriedade de autenticação nas rotas. 


#### GitHub - clone do projeto 

```bash
git clone https://github.com/Rodrigovvo/rvv_recipes.git
```

#### Configure o arquivo .env

O arquivo .env contém dados do enviroment do sistema.

```bash
cp .env_sample .env
```

#### Executando a aplicação pela primeira vez

É necessário criar o banco de dados antes da aplicação, o banco de dados padrão é denominado **rvv_recipes**.

Inicie o projeto, executando o build:
```bash
sudo docker-compose build
```

Após, em um terminal suba o banco de dados:

```bash
sudo docker-compose up db 
```

Em um outro terminal rode a migração do Django:

```bash
sudo docker-compose run --rm backend python manage.py migrate
```

Depois de rodar a migração pode derrubar o service da database:

```bash
sudo docker-compose down
```

E agora pode subir o projeto normalmente:

```bash
sudo docker-compose up
```

Os endereços e portas das aplicações são:

Backend - Django:

```bash
http://0.0.0.0:8000
```
#### Documentação da API

Com o docker em execução poderá ser verificada a documentação da api, pela URL: http://0.0.0.0:8000/api/schema/redoc/


#### Executando comandos do framework Django:

Para executar qualquer comando do Django (startapp, createsuperuser, makemigrations, migrate etc) deve considerar se os services estão *no ar* ou não.

Se o service **backend** estiver *no ar* e *rodando* corretamente, basta utilizar o próprio service para executar o comando desejado.
Exemplos:

```bash
sudo docker-compose exec backend python manage.py startapp novo_app
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```

#### Testes
Para executar os testes execute o comando:
```bash
sudo docker-compose run --rm backend python manage.py test api.v1.tests.test_categories_api
sudo docker-compose run --rm backend python manage.py test api.v1.tests.test_ingredients_api
sudo docker-compose run --rm backend python manage.py test api.v1.tests.test_recipes_api
sudo docker-compose run --rm backend python manage.py test api.v1.tests.test_users_api

```


#### Permissões ao arquivos criados utilizando o docker-compose

Ao executar comandos utilizando **docker-compose** que geram novos arquivos, é necessário alterar as configurações de permissionamento dos arquivos criados utilizando o comando linux **chown**. Na raiz do projeto execute o comando abaixo:

```bash
sudo chown -R $USER:$USER ./
```
