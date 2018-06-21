DROP TABLE IF EXISTS thinClients;

CREATE TABLE thinClients (
  id CHAR(12) PRIMARY KEY,
  latest_heartbeat TEXT,
  cpu CHAR(24),
  gpu CHAR(24),
  ram_in_gb INTEGER
);
