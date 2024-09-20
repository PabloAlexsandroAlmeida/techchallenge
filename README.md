# Techchallenge
FIAP TECH CHALLENGE

# QA e Security
 Quaisquer acoes nas branch dispara um workflow de validacao de codigo

# Deploy:
 -- Criar branch com profixo ˜app/*˜

  -- Criar branch com prefixo ˜infra/*˜



# RUN APP

-- Docker build
    docker build -f techchallenge .

-- Docker run
    docker run -p 8000:8000 techchallenge 

-- Acesso
    http://localhost:8000
