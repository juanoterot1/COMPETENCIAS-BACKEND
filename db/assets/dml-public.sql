-- Insertar en la tabla roles
INSERT INTO roles (role_name, created_at, updated_at) 
VALUES ('Admin', NOW(), NOW()), 
       ('Student', NOW(), NOW()), 
       ('Teacher', NOW(), NOW());

-- Insertar en la tabla users
INSERT INTO users (username, password, full_name, phone, mail, id_role, created_at, updated_at) 
VALUES ('admin_user', 'adminpassword', 'Admin User', '123456789', 'admin@example.com', 1, NOW(), NOW()),
       ('jdoe', 'studentpassword', 'John Doe', '987654321', 'jdoe@example.com', 2, NOW(), NOW()),
       ('tteacher', 'teacherpassword', 'Tom Teacher', '654987321', 'tteacher@example.com', 3, NOW(), NOW());

-- Insertar en la tabla faculties
INSERT INTO faculties (name, created_at, updated_at) 
VALUES ('Engineering', NOW(), NOW()), 
       ('Arts', NOW(), NOW());

-- Insertar en la tabla subjects
INSERT INTO subjects (name, code, id_faculty, created_at, updated_at) 
VALUES ('Math', 'MATH101', 1, NOW(), NOW()),
       ('History', 'HIST101', 2, NOW(), NOW());

-- Insertar en la tabla evaluations
INSERT INTO evaluations (name, description, id_subject, id_faculty, id_user, status, created_at, updated_at) 
VALUES ('Midterm Math', 'Midterm exam for Math 101', 1, 1, 3, 'Pending', NOW(), NOW()), 
       ('Final History', 'Final exam for History 101', 2, 2, 3, 'Completed', NOW(), NOW());

-- Insertar en la tabla questions
INSERT INTO questions (name, value, id_evaluation, created_at, updated_at) 
VALUES ('Question 1 Math', 10.0, 1, NOW(), NOW()), 
       ('Question 2 Math', 15.0, 1, NOW(), NOW()), 
       ('Question 1 History', 20.0, 2, NOW(), NOW());

-- Insertar en la tabla answers
INSERT INTO answers (answer_description, id_evaluation, id_question, id_user, score, created_at, updated_at) 
VALUES ('Answer 1 for Math', 1, 1, 2, 8.0, NOW(), NOW()), 
       ('Answer 2 for Math', 1, 2, 2, 13.0, NOW(), NOW()), 
       ('Answer 1 for History', 2, 3, 2, 18.0, NOW(), NOW());

-- Insertar en la tabla grading_matrix
INSERT INTO grading_matrix (id_subject, total_evaluations, total_score, recommendation, score, document, created_at, updated_at) 
VALUES (1, 2, 100.0, 'Pass', 80.0, 'grade_document_1.pdf', NOW(), NOW()), 
       (2, 1, 100.0, 'Pass', 85.0, 'grade_document_2.pdf', NOW(), NOW());
