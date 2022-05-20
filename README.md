# bsb

A ETL pipeline using Apache Airflow to extract, transform and load top5 best sellers books from New York Times

## Visão geral

O BSB é um projeto que faz o uso de uma pipeline de dados para extrair, transformar e carregar os top5 livros Best Sellers de ficção do New York Times. Toda a orquestração da pipeline é feito com o uso do framework Apache Airflow 2.0, e tanto o datalake quanto o data warehouse faz o uso do banco de dados Não Relacional MongoDB.

Para a extração dos best sellers no New York Times, fez-se o uso de webscraping com a biblioteca _requests_ para obter o HTML da página. Para extrair os dados do HTML, por sua vez, utilizou-se a biblioteca Beautiful Soup.

A transformação dos dados é composta pelas seguintes etapas:

- Formatar o nome da pessoa autora do livro, removendo a palavra _by_ antes do nome propriamente dito;
- Formatar o título do livro, convertendo todo o título anteriormente em maiúsculo para minúsculo, e depois convertendo toda a primeira letra de cada palavra para maiúscula;
- Convertendo o campo _weeks on the list_ para um número inteiro, removendo o texto e deixando apenas o número da semana;

Por fim, o carregamento dos dados constitui-se em salvar os livros best sellers anteriormente transformados para o data warehouse.

## Início rápido

Todo o desenvolvimento do projeto foi realizado com base em conteinerização via Docker. O arquivo _docker-compose.yml_ já é encarregado por montar o cluster do projeto, subindo o banco de dados Postgres e Redis para uso interno e, depois, subindo o banco de dados MongoDB para datalake e datawarehouse.

A seguir estão as etapas para iniciar o projeto via Docker:

1. Clone o projeto do GitHub para sua máquina:

   `$ git clone https://github.com/geazi-anc/bsb.git´`

   `$ cd bsb`

2. Na raiz do projeto, crie um arquivo chamado _.env_ e adicione o seguinte conteúdo:

   **.env**

   AIRFLOW_UID = 50000

   MONGO_URI = "bsb_mongodb_1:27017"

3. Feito isso, basta apenas inicializar o banco de dados do Airflow e subir todo o cluster:

   `$ docker-compose up airflow-init`

   `$ docker-compose up -d`

4. Com o cluster rodando, execute o dag para iniciar a extração, transformação e o carregamento dos livros best sellers do New York Times:

   `$ docker-compose exec airflow-worker bash`

   `$ airflow dags test bsb_dag 2022-01-01

5. Depois da execução do dag, acesse o data warehouse no MongoDB para visualizar os top5 best sellers do New York Times:

   `$ docker-compose exec mongodb mongo`

   `$ use bsb_datawarehouse`

   `$ db.best_sellers.find().pretty()`

6. Caso queira executar o dag via GUI, vá para seu navegador e acesse _http://localhost:8080_.
