DROP TABLE IF EXISTS serie_relatorio;   
DROP TABLE IF EXISTS relatorio_treino;
DROP TABLE IF EXISTS divisao_exercicio;
DROP TABLE IF EXISTS divisao_treino;
DROP TABLE IF EXISTS ficha_treino;
DROP TABLE IF EXISTS exercicio;
DROP TABLE IF EXISTS musculo;
DROP TABLE IF EXISTS aparelho;
DROP TABLE IF EXISTS grupamento;
DROP TABLE IF EXISTS usuario;



CREATE TABLE usuario(
    id_usuario    INTEGER        GENERATED ALWAYS AS IDENTITY,
    username      VARCHAR(40)    NOT NULL,
    email         VARCHAR(100)   NOT NULL,
    nome          VARCHAR(100)   NOT NULL,
    password      VARCHAR(512)   NOT NULL,
    
    CONSTRAINT pk_usuario
        PRIMARY KEY (id_usuario),
    
    CONSTRAINT uq_usuario_email
        UNIQUE (email)
    );
    
    

CREATE TABLE grupamento (
    nome_grupamento   VARCHAR(50) NOT NULL,
    id_usuario        INTEGER   NULL,
    ativo             BOOLEAN   DEFAULT TRUE,

    CONSTRAINT pk_grupamento
        PRIMARY KEY (nome_grupamento),
    CONSTRAINT uq_grupamento
        UNIQUE (id_usuario, nome_grupamento),
    CONSTRAINT fk_grupamento_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    );



CREATE TABLE aparelho(
    id_aparelho       INTEGER       GENERATED ALWAYS AS IDENTITY,
    id_usuario        INTEGER       NULL,
    nome_grupamento   VARCHAR(50)   NOT NULL,
    nome_aparelho     VARCHAR(50)   NOT NULL,
    ativo             BOOLEAN       DEFAULT TRUE,
    
    CONSTRAINT pk_aparelho 
        PRIMARY KEY (id_aparelho),
    
    CONSTRAINT uq_aparelho
        UNIQUE (id_usuario, nome_grupamento, nome_aparelho),
        
    CONSTRAINT fk_aparelho_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    
    CONSTRAINT fk_aparelho_grupamento
        FOREIGN KEY (nome_grupamento) REFERENCES grupamento(nome_grupamento) 
    );



CREATE TABLE musculo(
    id_musculo        INTEGER       GENERATED ALWAYS AS IDENTITY,
    nome_grupamento   VARCHAR(50)   NOT NULL,
    id_usuario        INTEGER       NULL,
    nome_musculo      VARCHAR(50)   NOT NULL,
    ativo             BOOLEAN       DEFAULT TRUE,

    
    CONSTRAINT pk_musculo
        PRIMARY KEY (id_musculo),
    
    CONSTRAINT uq_musculo
        UNIQUE (id_usuario, nome_grupamento, nome_musculo),

    CONSTRAINT fk_musculo_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),

    CONSTRAINT fk_musculo_grupamento
        FOREIGN KEY (nome_grupamento) REFERENCES grupamento(nome_grupamento) 
    );



CREATE TABLE exercicio(
    id_exercicio      INTEGER        GENERATED ALWAYS AS IDENTITY,
    id_musculo        INTEGER        NOT NULL,
    id_usuario        INTEGER        NULL,
    id_aparelho       INTEGER        NULL,
    nome_exercicio    VARCHAR(50)    NOT NULL,
    descricao         VARCHAR(120)   NULL,
    ativo             BOOLEAN       DEFAULT TRUE,


    CONSTRAINT pk_exercicio
        PRIMARY KEY (id_exercicio),

    CONSTRAINT uq_exercicio
        UNIQUE (id_usuario, id_musculo, id_aparelho, nome_exercicio),

    CONSTRAINT fk_exercicio_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),

    CONSTRAINT fk_exercicio_musculo
        FOREIGN KEY (id_musculo) REFERENCES musculo(id_musculo),

    CONSTRAINT fk_exercicio_aparelho
        FOREIGN KEY (id_aparelho) REFERENCES aparelho(id_aparelho)
    );


CREATE TABLE ficha_treino(
	id_ficha_treino         INTEGER       GENERATED ALWAYS AS IDENTITY,
	id_usuario              INTEGER       NOT NULL,
	nome_ficha_treino       VARCHAR(20)   NOT NULL,
	objetivo_ficha_treino   VARCHAR(50)   NOT NULL,
    ativo             BOOLEAN       DEFAULT TRUE,


	CONSTRAINT pk_ficha_treino
	    PRIMARY KEY (id_ficha_treino),

	CONSTRAINT uq_ficha_treino
	    UNIQUE (id_usuario, nome_ficha_treino),

	CONSTRAINT fk_ficha_treino_usuario
	    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    );



CREATE TABLE divisao_treino(
    divisao           VARCHAR(20)   NOT NULL,
    id_ficha_treino   INTEGER   NOT NULL,
    ativo             BOOLEAN       DEFAULT TRUE,


    CONSTRAINT pk_divisao_treino
        PRIMARY KEY (divisao, id_ficha_treino),

    CONSTRAINT fk_divisao_treino_ficha_treino
        FOREIGN KEY (id_ficha_treino) REFERENCES ficha_treino(id_ficha_treino)
);



CREATE TABLE relatorio_treino(
    id_relatorio_treino   INTEGER       GENERATED ALWAYS AS IDENTITY,
    id_ficha_treino       INTEGER       NOT NULL,
    data_relatorio        DATE          NOT NULL,
    divisao               VARCHAR(20)   NOT NULL,
    
    CONSTRAINT pk_relatorio_treino
        PRIMARY KEY (id_relatorio_treino),
        
    CONSTRAINT fk_relatorio_treino_divisao_treino
        FOREIGN KEY (id_ficha_treino, divisao) REFERENCES divisao_treino(id_ficha_treino, divisao)
);

CREATE TABLE divisao_exercicio(
    id_ficha_treino    INTEGER       NOT NULL,
    divisao            VARCHAR(20)       NOT NULL,
    id_exercicio       INTEGER       NOT NULL,
    ordem_execucao     INTEGER       NOT NULL,
    series             INTEGER       NOT NULL,
    repeticoes         VARCHAR(10)   NOT NULL,
    tecnica_avancada   VARCHAR(30)   NULL,
    descanso           INTEGER       NOT NULL,
    ativo             BOOLEAN       DEFAULT TRUE,


    CONSTRAINT pk_divisao_exercicio
        PRIMARY KEY (id_ficha_treino, divisao, id_exercicio, ordem_execucao),

    CONSTRAINT fk_divisao_exercicio_divisao_treino
        FOREIGN KEY (id_ficha_treino, divisao) REFERENCES divisao_treino(id_ficha_treino, divisao),

    CONSTRAINT fk_divisao_exercicio_exercicio
        FOREIGN KEY (id_exercicio) REFERENCES exercicio(id_exercicio)
);



CREATE TABLE serie_relatorio(
    id_relatorio_treino   INTEGER        NOT NULL,
    id_exercicio          INTEGER        NOT NULL,
    divisao               VARCHAR(20)        NOT NULL,
    id_ficha_treino       INTEGER        NOT NULL,
    ordem_execucao        INTEGER        NOT NULL,
    numero_serie          INTEGER        NOT NULL,
    repeticoes            VARCHAR(20)        NOT NULL,
    carga                 INTEGER        NOT NULL,
    observacao            VARCHAR(255)   NULL,

    CONSTRAINT pk_serie_relatorio
        PRIMARY KEY (id_relatorio_treino, id_exercicio, divisao, id_ficha_treino, numero_serie),

    CONSTRAINT fk_serie_relatorio_divisao_exercicio
        FOREIGN KEY (id_ficha_treino, divisao, id_exercicio, ordem_execucao) REFERENCES divisao_exercicio(id_ficha_treino, divisao, id_exercicio, ordem_execucao),

    CONSTRAINT fk_serie_relatorio_relatorio_treino
        FOREIGN KEY (id_relatorio_treino) REFERENCES relatorio_treino(id_relatorio_treino)
);

CREATE INDEX idx_grupamento_id_usuario ON grupamento(id_usuario);

CREATE INDEX id_username_usuario ON usuario(username);

CREATE INDEX id_email_usuario ON usuario(email);

CREATE INDEX idx_id_usuario_id_musculo_exercicio ON exercicio(id_usuario, id_musculo);

CREATE INDEX idx_id_musculo_exercicio ON exercicio(id_musculo);

CREATE INDEX idx_id_usuario_nome_grupamento_musculo ON musculo(id_usuario, nome_grupamento);

CREATE INDEX idx_id_usuario_nome_grupamento_aparelho ON aparelho(id_usuario, nome_grupamento);

CREATE INDEX idx_id_usuario_ficha_treino ON ficha_treino(id_usuario);

CREATE INDEX idx_id_ficha_treino_divisao_exercicio ON divisao_exercicio(id_ficha_treino);

CREATE INDEX idx_id_ficha_treino_id_relatorio_treino_serie_relatorio ON serie_relatorio(id_ficha_treino, id_relatorio_treino);
