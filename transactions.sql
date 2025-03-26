CREATE TABLE transactions (
    id UUID PRIMARY KEY NOT NULL,
    amount DECIMAL NOT NULL,
    currency VARCHAR(3) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL,
    gateway_transaction_id VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- Crear índices para mejorar las consultas de búsqueda
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_customer_email ON transactions(customer_email);
CREATE INDEX idx_transactions_customer_name ON transactions(customer_name);
CREATE INDEX idx_transactions_gateway_transaction_id ON transactions(gateway_transaction_id);