<h2><u>Teste Python Backend</u></h2>

<p>
Você deverá construir uma API que faça jogos da mega sena, 
o usuario deverá escolher a quantidade de dezenas por jogo e sua
API irá gerar aleatoriamente dezenas para o usuário. 
O usuário poderá consultar o resultado do ultimo jogo e comparar com suas dezenas 
para conferir quantos numeros acertou.
</p>

<p>Settings básicos para api estão definidos por default no .env, que pode ser alterado..</p>

```bash
    SECRET_KEY=CBEDA7091AC0E9B90901C7AA2EEB5BCD0272167E96F792A36F457010759212C3

    DEBUG=true
    ENABLE_LOGGING=true
    
    # Data base settings
    
    DB_ENGINE=django.db.backends.postgresql_psycopg2
    DB_NAME=lottery
    DB_USER=postgres
    DB_PASS=postgres
    DB_SERVICE=db
    DB_PORT=5432
```

Compile a imagem Docker executando o comando abaixo no mesmo local onde os arquivos são encontrados ```Dockerfile``` e ``` docker-compose.yml```

```
docker-compose build
```

```
docker-compose up
docker-compose up -d
```

Comando para executar o migrate
```
docker exec -it teste_python_backend_api python ./api/manage.py migrate
```

Comando para executar os testes
```
docker exec -it teste_python_backend_api python ./api/manage.py test
```

A url base da api é:
```
http://localhost:8000
```

<h4>Documentação das Apis</h4>
https://documenter.getpostman.com/view/2835965/TzseK6q5
