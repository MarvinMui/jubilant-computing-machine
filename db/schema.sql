CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    hostname TEXT,
    ip_address TEXT,
    os TEXT,
    assigned_user TEXT,
--    encryption BOOLEAN,
    location TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    mfa_enabled BOOLEAN,
    last_login TIMESTAMP,
    status TEXT
);

CREATE TABLE IF NOT EXISTS apps (
    app_id TEXT PRIMARY KEY,
    name TEXT,
    type TEXT,
    owner TEXT,
    usage_count INTEGER
);

-- Relationship tables
CREATE TABLE IF NOT EXISTS user_device (
    user_id TEXT,
    device_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE IF NOT EXISTS user_app (
    user_id TEXT,
    app_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (app_id) REFERENCES apps(app_id)
);
