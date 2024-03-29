CREATE DATABASE vacinapet;

-- public.tutor definition

-- Drop table

-- DROP TABLE public.tutor;

CREATE TABLE public.tutor (
	id serial4 NOT NULL,
	nome varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	telefone varchar(15) NULL,
	senha varchar(255) NOT NULL,
	CONSTRAINT tutor_pkey PRIMARY KEY (id)
);


-- public.pet definition

-- Drop table

-- DROP TABLE public.pet;

CREATE TABLE public.pet (
	id serial4 NOT NULL,
	tutor_id int4 NULL,
	nome varchar(255) NOT NULL,
	especie varchar(255) NULL,
	genero varchar(255) NULL,
	peso float4 NULL,
	idade int4 NULL,
	castrado bool NULL DEFAULT false,
	CONSTRAINT pet_pkey PRIMARY KEY (id),
	CONSTRAINT pet_tutor_id_fkey FOREIGN KEY (tutor_id) REFERENCES public.tutor(id)
);


-- public.vacina definition

-- Drop table

-- DROP TABLE public.vacina;

CREATE TABLE public.vacina (
	id serial4 NOT NULL,
	pet_id int4 NULL,
	nome varchar(255) NOT NULL,
	data_aplicacao date NOT NULL,
	prox_reforco date NOT NULL,
	lote varchar(255) NULL,
	CONSTRAINT vacina_pkey PRIMARY KEY (id),
	CONSTRAINT vacina_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pet(id)
);