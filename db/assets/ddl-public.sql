CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR,
    password VARCHAR,
    full_name VARCHAR,
    phone VARCHAR,
    mail VARCHAR,
    role_id INTEGER,
    dni VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE faculties (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    code VARCHAR,
    id_faculty INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (id_faculty) REFERENCES faculties(id)
);

CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR,
    id_subject INTEGER,
    id_faculty INTEGER,
    id_user INTEGER,
    status VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (id_subject) REFERENCES subjects(id),
    FOREIGN KEY (id_faculty) REFERENCES faculties(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    value FLOAT,
    id_evaluation INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (id_evaluation) REFERENCES evaluations(id)
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    answer_description VARCHAR,
    id_evaluation INTEGER,
    id_question INTEGER,
    id_user INTEGER,
    score FLOAT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (id_evaluation) REFERENCES evaluations(id),
    FOREIGN KEY (id_question) REFERENCES questions(id),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

CREATE TABLE grading_matrix (
    id SERIAL PRIMARY KEY,
    id_subject INTEGER,
    total_evaluations INTEGER,
    total_score FLOAT,
    recommendation VARCHAR,
    score FLOAT,
    document VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (id_subject) REFERENCES subjects(id)
);
