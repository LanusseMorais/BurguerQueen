# BurgerQueen 

Esse repositório contém um aplicativo de uma lanchonete fictícia chamada BurgerQueen que faz parte de um TechChallenge da FIAP.

## Pré-requisitos

- Docker
- Docker Compose

## Instalação

1. Clone o repositório:

```
git clone https://github.com/LanusseMorais/BurguerQueen.git
```

2. Navegue até o diretório do projeto:
``` 
cd BurguerQueen
```

3. Execute o Docker Compose para criar os contêineres do aplicativo e do banco de dados:

```
docker-compose up --build
```


4. Acesse a API em [http://localhost:5000](http://localhost:5000) e você verá a documentação das API's nessa documentação é possível interagir com a API enviando requisições, mas caso prefira usar o [postman](https://www.postman.com/) tem uma collection no dirétorio [/docs](/docs) que você pode importar 

## Uso

A API Burger Queen é dividida em três principais recursos: Menu, Clientes e Pedidos. Você pode acessar os seguintes endpoints:

- `/menu`: Operações no menu, incluindo adição, edição e exclusão de itens.
- `/customer`: Operações de gerenciamento de clientes, como adicionar e listar clientes.
- `/order`: Criação e gerenciamento de pedidos, incluindo adicionar, listar e pagar.

Exemplo de como criar um pedido:
```bash
curl -L 'http://localhost:5000/order' \
-H 'Content-Type: application/json' \
-d '{
    "customer_cpf": "111.222.333-44",
    "order_items": [
        {
            "item_id": 1,
            "extras": ["Bacon"],
            "removed_ingredients": ["alface"]
        },
        {
            "item_id": 2,
            "extras": [],
            "removed_ingredients": []
        },
        {
            "item_id": 4,
            "extras": ["chantilly"],
            "removed_ingredients": []
        }
    ]
}
'
```

## Estrutura de Diretórios e Arquivos
[/src/app](/src/app) | Contém o código-fonte da aplicação.  
[/docs](/docs) | Contém os arquivos JSON utilizados para importar dados iniciais.  
[Dockerfile](Dockerfile) | Arquivo que gera a imagem docker da aplicação.  
[docker-compose.yml](docker-compose.yml) | Arquivo que sobe todos os serviços necessários para aplicação funcionar.

## Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE.md para mais detalhes.

## Autores
Thalita Lanusse (@LanusseMorais)


## Status do Projeto

Esse projeto segue em desenvolvimento.

## Contato
Para obter mais informações, entre em contato com thalita.lanusse@gmailc.com