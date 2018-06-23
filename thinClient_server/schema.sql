DROP TABLE IF EXISTS thinClients;

CREATE TABLE thinClients (
  id CHAR(12) PRIMARY KEY,
  latest_heartbeat CHAR(24),
  cpu CHAR(24),
  ram_in_gb INTEGER,
  gpu CHAR(24),
  alive INTEGER
);
