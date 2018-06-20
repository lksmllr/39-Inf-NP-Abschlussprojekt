DROP TABLE IF EXISTS thinClients;

CREATE TABLE thinClients (
  id CHAR(12) PRIMARY KEY,
  latest_heartbeat TIMESTAMP NOT NULL,
  cpu CHAR(24) NOT NULL,
  gpu CHAR(24) NOT NULL,
  ram_in_gb INTEGER NOT NULL
);
