--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: s_chat; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE s_chat (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    deleted boolean
);


ALTER TABLE s_chat OWNER TO postgres;

--
-- Name: s_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s_chat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s_chat_id_seq OWNER TO postgres;

--
-- Name: s_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s_chat_id_seq OWNED BY s_chat.id;


--
-- Name: s_chat_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE s_chat_user (
    id integer NOT NULL,
    chat_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE s_chat_user OWNER TO postgres;

--
-- Name: s_chat_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s_chat_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s_chat_user_id_seq OWNER TO postgres;

--
-- Name: s_chat_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s_chat_user_id_seq OWNED BY s_chat_user.id;


--
-- Name: s_community; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE s_community (
    cm_id integer NOT NULL,
    cm_alias character varying(255) NOT NULL,
    cm_name character varying(255) NOT NULL
);


ALTER TABLE s_community OWNER TO postgres;

--
-- Name: s_community_cm_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s_community_cm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s_community_cm_id_seq OWNER TO postgres;

--
-- Name: s_community_cm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s_community_cm_id_seq OWNED BY s_community.cm_id;


--
-- Name: s_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE s_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    chat_id integer NOT NULL,
    text text NOT NULL,
    data text,
    datetime timestamp without time zone DEFAULT now() NOT NULL,
    is_system boolean DEFAULT false NOT NULL
);


ALTER TABLE s_message OWNER TO postgres;

--
-- Name: s_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s_message_id_seq OWNER TO postgres;

--
-- Name: s_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s_message_id_seq OWNED BY s_message.id;


--
-- Name: s_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE s_user (
    usr_id integer NOT NULL,
    usr_email character varying(50),
    usr_password character varying(50),
    usr_firstname character varying(50) NOT NULL,
    usr_lastname character varying(50) NOT NULL,
    usr_photo character varying(255),
    usr_photo_s character varying(255)
);


ALTER TABLE s_user OWNER TO postgres;

--
-- Name: s_user_community; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE s_user_community (
    ucm_id integer NOT NULL,
    usr_id integer NOT NULL,
    cm_id integer NOT NULL,
    ucm_external_id character varying(255) NOT NULL,
    ucm_additional_data character varying(255)
);


ALTER TABLE s_user_community OWNER TO postgres;

--
-- Name: s_user_community_ucm_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s_user_community_ucm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s_user_community_ucm_id_seq OWNER TO postgres;

--
-- Name: s_user_community_ucm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s_user_community_ucm_id_seq OWNED BY s_user_community.ucm_id;


--
-- Name: s_user_role; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE s_user_role (
    usrr_id integer NOT NULL,
    usr_id integer NOT NULL,
    usrr_code character varying(255) NOT NULL
);


ALTER TABLE s_user_role OWNER TO postgres;

--
-- Name: s_user_role_usrr_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s_user_role_usrr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s_user_role_usrr_id_seq OWNER TO postgres;

--
-- Name: s_user_role_usrr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s_user_role_usrr_id_seq OWNED BY s_user_role.usrr_id;


--
-- Name: s_user_usr_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE s_user_usr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE s_user_usr_id_seq OWNER TO postgres;

--
-- Name: s_user_usr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE s_user_usr_id_seq OWNED BY s_user.usr_id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s_chat ALTER COLUMN id SET DEFAULT nextval('s_chat_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s_chat_user ALTER COLUMN id SET DEFAULT nextval('s_chat_user_id_seq'::regclass);


--
-- Name: cm_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s_community ALTER COLUMN cm_id SET DEFAULT nextval('s_community_cm_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s_message ALTER COLUMN id SET DEFAULT nextval('s_message_id_seq'::regclass);


--
-- Name: usr_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s_user ALTER COLUMN usr_id SET DEFAULT nextval('s_user_usr_id_seq'::regclass);


--
-- Name: ucm_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s_user_community ALTER COLUMN ucm_id SET DEFAULT nextval('s_user_community_ucm_id_seq'::regclass);


--
-- Name: usrr_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY s_user_role ALTER COLUMN usrr_id SET DEFAULT nextval('s_user_role_usrr_id_seq'::regclass);


--
-- Data for Name: s_chat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY s_chat (id, name, deleted) FROM stdin;
\.


--
-- Name: s_chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('s_chat_id_seq', 2, true);


--
-- Data for Name: s_chat_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY s_chat_user (id, chat_id, user_id) FROM stdin;
\.


--
-- Name: s_chat_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('s_chat_user_id_seq', 4, true);


--
-- Data for Name: s_community; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY s_community (cm_id, cm_alias, cm_name) FROM stdin;
1	fb	Facebook
2	vk	Vkontakte
\.


--
-- Name: s_community_cm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('s_community_cm_id_seq', 2, true);


--
-- Data for Name: s_message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY s_message (id, user_id, chat_id, text, data, datetime, is_system) FROM stdin;
\.


--
-- Name: s_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('s_message_id_seq', 8, true);


--
-- Data for Name: s_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY s_user (usr_id, usr_email, usr_password, usr_firstname, usr_lastname, usr_photo, usr_photo_s) FROM stdin;
\.


--
-- Data for Name: s_user_community; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY s_user_community (ucm_id, usr_id, cm_id, ucm_external_id, ucm_additional_data) FROM stdin;
\.


--
-- Name: s_user_community_ucm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('s_user_community_ucm_id_seq', 4, true);


--
-- Data for Name: s_user_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY s_user_role (usrr_id, usr_id, usrr_code) FROM stdin;
\.


--
-- Name: s_user_role_usrr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('s_user_role_usrr_id_seq', 1, false);


--
-- Name: s_user_usr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('s_user_usr_id_seq', 5, true);


--
-- Name: s_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY s_chat
    ADD CONSTRAINT s_chat_pkey PRIMARY KEY (id);


--
-- Name: s_chat_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY s_chat_user
    ADD CONSTRAINT s_chat_user_pkey PRIMARY KEY (id);


--
-- Name: s_community_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY s_community
    ADD CONSTRAINT s_community_pkey PRIMARY KEY (cm_id);


--
-- Name: s_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY s_message
    ADD CONSTRAINT s_message_pkey PRIMARY KEY (id);


--
-- Name: s_user_community_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY s_user_community
    ADD CONSTRAINT s_user_community_pkey PRIMARY KEY (ucm_id);


--
-- Name: s_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY s_user
    ADD CONSTRAINT s_user_pkey PRIMARY KEY (usr_id);


--
-- Name: s_user_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY s_user_role
    ADD CONSTRAINT s_user_role_pkey PRIMARY KEY (usrr_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

