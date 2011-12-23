

CREATE SEQUENCE account_pk_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE account (
    id          integer  PRIMARY KEY DEFAULT nextval('account_pk_seq'::regclass) NOT NULL,
    login       character varying(30) UNIQUE NOT NULL,
    passwd_hash character varying(34) NOT NULL,
    passwd_salt character(10) NOT NULL
);

