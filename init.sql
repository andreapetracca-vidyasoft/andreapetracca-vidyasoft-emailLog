CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE email_enum AS ENUM ('RESERVE', 'RETURN');

CREATE TABLE emails (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_type email_enum NOT NULL,
    send_to TEXT NOT NULL,
    fields JSON NOT NULL DEFAULT '{}'::json,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

ALTER TABLE emails ADD CONSTRAINT email_check
CHECK (send_to ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$');

CREATE TYPE status_enum AS ENUM ('SENT', 'FAILED');

CREATE TABLE logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_id UUID NOT NULL,
    status status_enum NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),

    CONSTRAINT fk_email
        FOREIGN KEY (email_id)
        REFERENCES emails(id)
        ON DELETE CASCADE
);
