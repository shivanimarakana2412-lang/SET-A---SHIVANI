-- ============================================================
-- queries.sql
-- SQL Dialect : SQLite 3
-- Run order   : after setup.sql, in the SAME database file
--               sqlite3 outputs/delivery.db < sql/queries.sql
-- delay_days  : MAX(actual_days - promised_days, 0)
-- ============================================================

.headers on
.mode csv

-- ------------------------------------------------------------
-- S2a — Total delay_days by service type (JOIN deliveries -> routes)
-- Returns: service_type, total_delay_days, ordered DESC
-- ------------------------------------------------------------
.once outputs/sql/s2a_delay_by_service_type.csv
SELECT
    r.service_type                                              AS service_type,
    SUM(MAX(d.actual_days - d.promised_days, 0))                AS total_delay_days
FROM deliveries d
JOIN routes r ON d.route_id = r.route_id
GROUP BY r.service_type
ORDER BY total_delay_days DESC;

-- ------------------------------------------------------------
-- S2b — Routes with significant delay (GROUP BY + HAVING > 8)
-- ------------------------------------------------------------
.once outputs/sql/s2b_routes_significant_delay.csv
SELECT
    d.route_id                                                  AS route_id,
    r.route                                                     AS route,
    SUM(MAX(d.actual_days - d.promised_days, 0))                AS total_delay_days
FROM deliveries d
JOIN routes r ON d.route_id = r.route_id
GROUP BY d.route_id, r.route
HAVING SUM(MAX(d.actual_days - d.promised_days, 0)) > 8
ORDER BY total_delay_days DESC;

-- ------------------------------------------------------------
-- S2c — Top two hubs by summed delay_days (ties broken alphabetically)
-- ------------------------------------------------------------
.once outputs/sql/s2c_top_hubs_by_delay.csv
SELECT
    hub,
    SUM(MAX(actual_days - promised_days, 0))                    AS total_delay_days
FROM deliveries
GROUP BY hub
ORDER BY total_delay_days DESC, hub ASC
LIMIT 2;

-- ------------------------------------------------------------
-- S3 — Data integrity check: every deliveries.route_id must match a
-- routes.route_id (LEFT JOIN deliveries -> routes; zero unmatched
-- keys expected)
-- ------------------------------------------------------------
.once outputs/sql/diagnostic_unmatched_keys.csv
SELECT
    d.record_id,
    d.route_id      AS deliveries_route_id,
    r.route_id       AS matched_routes_route_id
FROM deliveries d
LEFT JOIN routes r ON d.route_id = r.route_id
WHERE r.route_id IS NULL;
-- Expected result: 0 rows (empty file with header only) = zero unmatched keys.
