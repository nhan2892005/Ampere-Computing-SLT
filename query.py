Q3_TEMP0 = """
    SELECT
        w.id,
        f.name          AS facility,
        p.name          AS product,
        p.category_name AS category,
        s.name          AS supplier,
        w.quantity      AS import_quantity,
        COALESCE(c.quantity, 0) AS order_quantity,
        w.import_date,
        w.exp_date,
        c.order_date,
        :ref_date       AS ref_date
    FROM warehouse w
    JOIN facility f ON f.id = w.facility_id
    JOIN product  p ON p.id = w.product_id
    JOIN supplier s ON s.id = p.supplier_id
    LEFT JOIN consumption c
        ON  c.facility_id = w.facility_id
        AND c.product_id  = w.product_id
        AND c.order_date <= w.exp_date
        AND c.order_date > (
            SELECT COALESCE(MAX(w2.exp_date), '1900-01-01')
            FROM warehouse w2
            WHERE w2.facility_id = w.facility_id
              AND w2.product_id  = w.product_id
              AND w2.exp_date    < w.exp_date
        )
"""

Q3_TEMP1 = """
    SELECT
        id, facility, product, category, supplier,
        import_quantity,
        SUM(order_quantity) AS total_order,
        import_date, exp_date, ref_date,
        CASE WHEN exp_date < ref_date
             THEN 0
             ELSE import_quantity - SUM(order_quantity)
        END AS remain_quantity,
        CASE WHEN exp_date < ref_date
             THEN import_quantity - SUM(order_quantity)
             ELSE 0
        END AS overdue_quantity
    FROM temp0
    GROUP BY id, facility, product, category, supplier,
             import_quantity, import_date, exp_date, ref_date
"""

Q3_FINAL_SQL  = f"""
WITH temp0 AS ({Q3_TEMP0}),
temp1 AS ({Q3_TEMP1}),
aggregated AS (
    SELECT
        facility, product, supplier,
        MIN(id)              AS first_id,
        SUM(remain_quantity) AS remain_quantity,
        SUM(overdue_quantity) AS overdue_quantity,
        CASE WHEN SUM(remain_quantity) < 100 THEN 'Yes' ELSE 'No' END AS need_import
    FROM temp1
    GROUP BY facility, product, supplier
)
SELECT facility, product, supplier, remain_quantity, overdue_quantity, need_import
FROM aggregated
ORDER BY first_id;
"""