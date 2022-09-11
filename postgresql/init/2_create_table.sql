--データベースの切り替え
\c api_dev
--企業の基本情報Tableを作成
CREATE TABLE companies (
  id SERIAL PRIMARY KEY, 
  jcn varchar UNIQUE NOT NULL,
  sec_code varchar UNIQUE,
  edinet_code varchar UNIQUE NOT NULL,
  name_jp varchar NOT NULL,
  name_eng varchar NOT NULL
);

--株式分割・併合の記録Tableを作成
CREATE TABLE stock_history (
  id SERIAL PRIMARY KEY,
  company_id bigint NOT NULL,
  activation_date date NOT NULL,
  ratio float NOT NULL,
  FOREIGN KEY (company_id) references companies(id)
);

--会計基準Tableを作成
CREATE TABLE accounting_standards (
  id SERIAL PRIMARY KEY,
  code varchar UNIQUE NOT NULL,
  name_jp varchar NOT NULL
);

--DEIの産業Tableを作成
CREATE TABLE dei_industry_codes (
  id SERIAL PRIMARY KEY,
  code varchar UNIQUE NOT NULL,
  name_jp varchar NOT NULL
);

--会計期間区分Tableを作成
CREATE TABLE period_types (
  id SERIAL PRIMARY KEY,
  code varchar UNIQUE NOT NULL,
  name_jp varchar NOT NULL
);

--有報などの提出書類の基本情報Tableを作成
CREATE TABLE fin_documents (
  id SERIAL PRIMARY KEY,
  document_uid varchar UNIQUE NOT NULL,
  current_fiscalyear_startdate date NOT NULL,
  current_fiscalyear_enddate date NOT NULL,
  current_period_enddate date NOT NULL,
  is_consolidated boolean NOT NULL,
  document_type varchar NOT NULL,
  company_id bigint NOT NULL,
  accounting_standard_id bigint NOT NULL,
  dei_industry_code_id bigint NOT NULL,
  period_type_id bigint NOT NULL,
  FOREIGN KEY (company_id) references companies(id),
  FOREIGN KEY (accounting_standard_id) references accounting_standards(id),
  FOREIGN KEY (dei_industry_code_id) references dei_industry_codes(id),
  FOREIGN KEY (period_type_id) references period_types(id)
);

--勘定科目Tableを作成
CREATE TABLE account_labels (
  id SERIAL PRIMARY KEY,
  qname varchar UNIQUE NOT NULL,
  name_jp varchar NOT NULL
);

--数値の計算期間、時点を定義したTableを作成
CREATE TABLE contexts (
  id SERIAL PRIMARY KEY,
  code varchar UNIQUE NOT NULL,
  name_jp varchar NOT NULL
);

--BS/PL/CF等を定義したTableを作成
CREATE TABLE dimensions (
  id SERIAL PRIMARY KEY,
  code varchar UNIQUE NOT NULL,
  name_jp varchar NOT NULL
);

--数値データTableを作成
CREATE TABLE fin_data (
  id SERIAL PRIMARY KEY,
  document_id bigint NOT NULL,
  account_label_id bigint NOT NULL,
  context_id bigint NOT NULL,
  dimension_id bigint NOT NULL,
  ammount float NOT NULL,
  is_consolidated boolean NOT NULL,
  FOREIGN KEY (document_id) references fin_documents(id),
  FOREIGN KEY (account_label_id) references account_labels(id),
  FOREIGN KEY (context_id) references contexts(id),
  FOREIGN KEY (dimension_id) references dimensions(id)
);