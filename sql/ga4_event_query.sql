WITH total_interacoes_por_usuario_futuro AS (
  SELECT
    events.user_pseudo_id AS id_usuario,
    COUNT(events.event_name) AS total_interacoes
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` events
  WHERE PARSE_DATE("%Y%m%d", events.event_date) BETWEEN "2021-01-01" AND "2021-02-01"
  AND events.event_name IN UNNEST(["page_view", "view_search_results", "view_item_list", "select_item", "select_promotion", "add_to_cart", "begin_checkout"])
  GROUP BY events.user_pseudo_id
),
metricas_por_usuario AS (
  SELECT 
    events.user_pseudo_id AS id_usuario,
    COUNT(events.user_pseudo_id) AS total_pedidos,
    ROUND(SUM(events.ecommerce.purchase_revenue_in_usd), 2) AS receita_total_em_usd,
    ROUND(SUM(events.ecommerce.purchase_revenue_in_usd) / COUNT(events.user_pseudo_id), 2) AS ticket_medio_em_usd,
    PARSE_DATE("%Y%m%d", MIN(events.event_date)) AS data_primeiro_pedido,
    PARSE_DATE("%Y%m%d", MAX(events.event_date)) AS data_ultimo_pedido,
    DATE_DIFF(DATE("2021-01-01"), PARSE_DATE("%Y%m%d", MAX(events.event_date)), DAY) AS recencia_dias,
    DATE_DIFF(DATE("2021-01-01"), PARSE_DATE("%Y%m%d", MIN(events.event_date)), DAY) AS dias_desde_primeiro_pedido,
    DATE_DIFF(PARSE_DATE("%Y%m%d", MAX(events.event_date)), PARSE_DATE("%Y%m%d", MIN(events.event_date)), DAY) AS tempo_relacionamento_dias,
    SUM(
      (
        SELECT
          SUM(item.quantity)
          FROM UNNEST(events.items) AS item
      )
    ) AS total_itens_comprados
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` events
  WHERE events.event_name = "purchase"
  AND PARSE_DATE("%Y%m%d", events.event_date) <= "2020-12-31"
  GROUP BY events.user_pseudo_id
  ORDER BY tempo_relacionamento_dias DESC
),
metricas_interacoes_por_usuario AS (
  SELECT
    events.user_pseudo_id AS id_usuario,
    COUNT(events.event_name) AS total_interacoes,
    COUNTIF(events.event_name = "page_view") AS total_interacoes_page_view,
    COUNTIF(events.event_name = "view_search_results") AS total_interacoes_view_search_results,
    COUNTIF(events.event_name = "view_item_list") AS total_interacoes_view_item_list,
    COUNTIF(events.event_name = "select_item") AS total_interacoes_select_item,
    COUNTIF(events.event_name = "select_promotion") AS total_interacoes_select_promotion,
    COUNTIF(events.event_name = "add_to_cart") AS total_interacoes_add_to_cart,
    COUNTIF(events.event_name = "begin_checkout") AS total_interacoes_begin_checkout,
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 14 DAY AND DATE("2020-12-31") - INTERVAL 0 DAY
    ) AS total_interacoes_quinzena_4,
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 29 DAY AND DATE("2020-12-31") - INTERVAL 15 DAY
      ) AS total_interacoes_quinzena_3, 
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 44 DAY AND DATE("2020-12-31") - INTERVAL 30 DAY
      ) AS total_interacoes_quinzena_2, 
    COUNTIF(
      PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 59 DAY AND DATE("2020-12-31") - INTERVAL 45 DAY
      ) AS total_interacoes_quinzena_1, 
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` events
  WHERE PARSE_DATE("%Y%m%d", events.event_date) BETWEEN DATE("2020-12-31") - INTERVAL 59 DAY AND DATE("2020-12-31") - INTERVAL 0 DAY
  AND events.event_name IN UNNEST(["page_view", "view_search_results", "view_item_list", "select_item", "select_promotion", "add_to_cart", "begin-checkout"])
  GROUP BY events.user_pseudo_id
)
SELECT 
  DISTINCT events.user_pseudo_id AS id_usuario,
  events.device.category AS dispositivo,
  events.platform AS meio_acesso,
  events.traffic_source.medium AS meio_trafego,
  events.traffic_source.source AS fonte_trafego,
  metricas_por_usuario.total_pedidos AS total_pedidos,
  metricas_por_usuario.receita_total_em_usd AS receita_total_em_usd,
  metricas_por_usuario.ticket_medio_em_usd AS ticket_medio_em_usd,
  metricas_por_usuario.data_primeiro_pedido AS data_primeiro_pedido,
  metricas_por_usuario.data_ultimo_pedido AS data_ultimo_pedido,
  metricas_por_usuario.recencia_dias AS recencia_dias,
  metricas_por_usuario.dias_desde_primeiro_pedido AS dias_desde_primeiro_pedido,
  metricas_por_usuario.tempo_relacionamento_dias AS tempo_relacionamento_dias,
  IF (metricas_por_usuario.total_itens_comprados IS NULL, 0, metricas_por_usuario.total_itens_comprados) AS total_itens_comprados,
  metricas_interacoes_por_usuario.total_interacoes AS total_interacoes,
  metricas_interacoes_por_usuario.total_interacoes_page_view AS total_interacoes_page_view,
  metricas_interacoes_por_usuario.total_interacoes_view_search_results AS total_interacoes_view_search_results,
  metricas_interacoes_por_usuario.total_interacoes_view_item_list AS total_interacoes_view_item_list,
  metricas_interacoes_por_usuario.total_interacoes_select_item AS total_interacoes_select_item,
  metricas_interacoes_por_usuario.total_interacoes_select_promotion AS total_interacoes_select_promotion,
  metricas_interacoes_por_usuario.total_interacoes_add_to_cart AS total_interacoes_add_to_cart,
  metricas_interacoes_por_usuario.total_interacoes_begin_checkout AS total_interacoes_begin_checkout,
  metricas_interacoes_por_usuario.total_interacoes_quinzena_1 AS total_interacoes_quinzena_1,
  metricas_interacoes_por_usuario.total_interacoes_quinzena_2 AS total_interacoes_quinzena_2,
  metricas_interacoes_por_usuario.total_interacoes_quinzena_3 AS total_interacoes_quinzena_3,
  metricas_interacoes_por_usuario.total_interacoes_quinzena_4 AS total_interacoes_quinzena_4,
  IF (total_interacoes_por_usuario_futuro.total_interacoes IS NULL, 1, 0) AS churn
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` events
LEFT JOIN metricas_por_usuario ON metricas_por_usuario.id_usuario = events.user_pseudo_id
LEFT JOIN metricas_interacoes_por_usuario ON metricas_interacoes_por_usuario.id_usuario = events.user_pseudo_id
LEFT JOIN total_interacoes_por_usuario_futuro ON total_interacoes_por_usuario_futuro.id_usuario = events.user_pseudo_id
WHERE events.event_name = "purchase"
AND PARSE_DATE("%Y%m%d", events.event_date) <= "2020-12-31"
ORDER BY total_itens_comprados DESC