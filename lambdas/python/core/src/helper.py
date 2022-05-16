# Queries
header = """-- QUERY ENCABEZADO --

SELECT a.account_id, a.contact_first_name || ' ' || a.contact_last_name AS "titular", a.email, c.cvu, u.cuil, u.documentid
    FROM  public.tb_ar_cvu c INNER JOIN public.tb_ar_core_accounts a 
        ON a.account_id = c.account_id
            INNER JOIN public.tb_ar_core_users u ON u.user_name = a.user_name
            WHERE u.documentid = '{DNI}'; -- DNI DEL USUARIO A BUSCAR --
    """

debits ="""SELECT t.*, t.amount AS "debito", 0.0 AS "credito" 
    FROM public.tb_ar_core_transactions t 
        INNER JOIN public.tb_ar_configs_params p ON p.value_2 = t.transaction_type 
            WHERE t.status = 'AUTHORIZED'
            AND t.transaction_date > '{FROM_DATE}' --FECHA DESDE--
            AND t.transaction_date <= '{TO_DATE}' --FECHA HASTA (INCLUSIVE) --
            AND p.param_type = 'transaction_type'
            AND p.value_3 = 'TRUE'
            AND	t.account_from = '{ACCOUNT_ID}' --IDENTIFICADOR DE CUENTA--
UNION

SELECT t.*,  0.0 AS "debito", t.amount AS "credito"
    FROM public.tb_ar_core_transactions t 
        INNER JOIN public.tb_ar_configs_params p ON p.value_2 = t.transaction_type 
            WHERE t.status = 'AUTHORIZED'
            AND t.transaction_date > '{FROM_DATE}' --FECHA DESDE--
            AND t.transaction_date <= '{TO_DATE}' --FECHA HASTA (INCLUSIVE)--
            AND p.param_type = 'transaction_type'
            AND t.transaction_type != 'USER_TO_USER'
            AND	t.account_from = '{ACCOUNT_ID}' --IDENTIFICADOR DE CUENTA--
            AND p.value_3 = 'FALSE';
    """
