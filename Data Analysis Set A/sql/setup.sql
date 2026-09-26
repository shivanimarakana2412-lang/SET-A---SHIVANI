-- ============================================================
-- setup.sql
-- SQL Dialect : SQLite 3 (tested on SQLite 3.4x; ships with Python's sqlite3 module)
-- Run order   : sqlite3 outputs/delivery.db < sql/setup.sql
--               sqlite3 outputs/delivery.db < sql/queries.sql
-- Purpose     : Create schema, load 12 clean fact rows + 4 lookup rows.
--               The 13th (exact duplicate, record_id 12) row from
--               data/raw/deliveries.csv is intentionally EXCLUDED at load
--               time, per exam rule.
-- ============================================================

DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS routes;

-- Lookup table: one row per route
CREATE TABLE routes (
    route_id      TEXT PRIMARY KEY,
    route         TEXT NOT NULL,
    service_type  TEXT NOT NULL
);

-- Fact table: one row per month-end route/hub delivery summary
-- Foreign key: deliveries.route_id -> routes.route_id
CREATE TABLE deliveries (
    record_id      INTEGER PRIMARY KEY,
    month          TEXT NOT NULL,      -- Jan / Feb / Mar (ordered text category)
    route_id       TEXT NOT NULL,
    hub            TEXT NOT NULL,
    promised_days  NUMERIC NOT NULL,
    actual_days    NUMERIC NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

PRAGMA foreign_keys = ON;

-- ---------- Load lookup data (4 rows) ----------
INSERT INTO routes (route_id, route, service_type) VALUES
('R1', 'Metro Link',      'Express'),
('R2', 'City Dash',       'Express'),
('R3', 'Highway Freight', 'Standard'),
('R4', 'Rural Feeder',    'Standard');

-- ---------- Load fact data (12 clean rows — duplicate record_id 12 excluded) ----------
INSERT INTO deliveries (record_id, month, route_id, hub, promised_days, actual_days) VALUES
(1,  'Jan', 'R1', 'Mumbai',  2, 2),
(2,  'Jan', 'R2', 'Chennai', 3, 4),
(3,  'Jan', 'R3', 'Delhi',   5, 8),
(4,  'Jan', 'R4', 'Mumbai',  6, 10),
(5,  'Feb', 'R1', 'Chennai', 2, 5),
(6,  'Feb', 'R2', 'Delhi',   3, 3),
(7,  'Feb', 'R3', 'Delhi',   5, 10),
(8,  'Feb', 'R4', 'Chennai', 6, 7),
(9,  'Mar', 'R1', 'Delhi',   2, 8),
(10, 'Mar', 'R2', 'Mumbai',  3, 5),
(11, 'Mar', 'R3', 'Chennai', 5, 5),
(12, 'Mar', 'R4', 'Mumbai',  6, 15);

-- Sanity check counts (visible when run interactively)
-- SELECT COUNT(*) AS route_rows     FROM routes;      -- expect 4
-- SELECT COUNT(*) AS delivery_rows  FROM deliveries;   -- expect 12
