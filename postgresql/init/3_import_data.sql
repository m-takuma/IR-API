--データベースの切り替え
\c api_dev

--companyのデータを入れる
\COPY companies FROM '/init/seed/01_company.csv' DELIMITER ',' CSV HEADER;

\COPY accounting_standards FROM '/init/seed/02_accounting_standard.csv' DELIMITER ',' CSV HEADER;

\COPY dei_industry_codes FROM '/init/seed/03_dei_industry_code.csv' DELIMITER ',' CSV HEADER;

\COPY period_types FROM '/init/seed/04_period_type.csv' DELIMITER ',' CSV HEADER;

\COPY fin_documents FROM '/init/seed/05_document.csv' DELIMITER ',' CSV HEADER;

\COPY account_labels FROM '/init/seed/06_account_label.csv' DELIMITER ',' CSV HEADER;

\COPY contexts FROM '/init/seed/07_context.csv' DELIMITER ',' CSV HEADER;

\COPY dimensions FROM '/init/seed/08_dimension.csv' DELIMITER ',' CSV HEADER;

\COPY fin_data FROM '/init/seed/09_fin_data(1).csv' DELIMITER ',' CSV HEADER;
\COPY fin_data FROM '/init/seed/09_fin_data(2).csv' DELIMITER ',' CSV HEADER;
\COPY fin_data FROM '/init/seed/09_fin_data(3).csv' DELIMITER ',' CSV HEADER;
\COPY fin_data FROM '/init/seed/09_fin_data(4).csv' DELIMITER ',' CSV HEADER;
\COPY fin_data FROM '/init/seed/09_fin_data(5).csv' DELIMITER ',' CSV HEADER;
\COPY fin_data FROM '/init/seed/09_fin_data(6).csv' DELIMITER ',' CSV HEADER;
\COPY fin_data FROM '/init/seed/09_fin_data(7).csv' DELIMITER ',' CSV HEADER;
