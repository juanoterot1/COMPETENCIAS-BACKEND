-- Insertando datos en la tabla roles
INSERT INTO roles (role_name, created_at, updated_at)
VALUES 
    ('Admin', NOW(), NOW()),
    ('Teacher', NOW(), NOW()),
    ('Student', NOW(), NOW());

-- Insertando datos en la tabla users
INSERT INTO users (username, password, full_name, phone, mail, role_id, dni, created_at, updated_at)
VALUES 
    ('jdoe', 'password123', 'John Doe', '555-1234', 'jdoe@example.com', 1, '12345678', NOW(), NOW()),
    ('asmith', 'password456', 'Alice Smith', '555-5678', 'asmith@example.com', 2, '87654321', NOW(), NOW()),
    ('bwhite', 'password789', 'Bob White', '555-8765', 'bwhite@example.com', 3, '11223344', NOW(), NOW());

-- Insertando datos en la tabla faculties
INSERT INTO faculties (name, created_at, updated_at)
VALUES 
    ('Engineering', NOW(), NOW()),
    ('Science', NOW(), NOW()),
    ('Arts', NOW(), NOW());

-- Insertando datos en la tabla subjects
INSERT INTO subjects (name, code, id_faculty, created_at, updated_at)
VALUES 
    ('Mathematics', 'MATH101', 1, NOW(), NOW()),
    ('Physics', 'PHYS101', 2, NOW(), NOW()),
    ('Literature', 'LIT101', 3, NOW(), NOW());

-- Insertando datos en la tabla evaluations
INSERT INTO evaluations (name, description, id_subject, id_faculty, id_user, status, created_at, updated_at)
VALUES 
    ('Midterm Exam', 'Midterm exam for Mathematics', 1, 1, 1, 'Pending', NOW(), NOW()),
    ('Final Exam', 'Final exam for Physics', 2, 2, 2, 'Scheduled', NOW(), NOW()),
    ('Essay', 'Literature essay evaluation', 3, 3, 3, 'Completed', NOW(), NOW());

-- Insertando datos en la tabla questions
INSERT INTO questions (name, value, id_evaluation, created_at, updated_at)
VALUES 
    ('Question 1', 5.0, 1, NOW(), NOW()),
    ('Question 2', 3.0, 1, NOW(), NOW()),
    ('Question 1', 4.0, 2, NOW(), NOW());

-- Insertando datos en la tabla answers
INSERT INTO answers (answer_description, id_evaluation, id_question, id_user, score, created_at, updated_at)
VALUES 
    ('Answer to Question 1', 1, 1, 1, 4.5, NOW(), NOW()),
    ('Answer to Question 2', 1, 2, 1, 3.0, NOW(), NOW()),
    ('Answer to Question 1', 2, 3, 2, 3.8, NOW(), NOW());

-- Insertando datos en la tabla grading_matrix
INSERT INTO grading_matrix (id_subject, total_evaluations, total_score, recommendation, score, document, created_at, updated_at)
VALUES 
    (1, 10, 45.0, 'Good progress', 4.5, 'doc1.pdf', NOW(), NOW()),
    (2, 5, 18.5, 'Needs improvement', 3.7, 'doc2.pdf', NOW(), NOW()),
    (3, 8, 32.0, 'Excellent', 4.9, 'doc3.pdf', NOW(), NOW());
