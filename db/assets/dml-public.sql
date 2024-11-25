-- Insertando datos en la tabla roles
INSERT INTO roles (role_name, created_at, updated_at)
VALUES 
    ('Admin', NOW(), NOW()),
    ('Teacher', NOW(), NOW()),
    ('Student', NOW(), NOW());

INSERT INTO permissions (id, name, description, created_at, updated_at) VALUES
    (1, 'create_faculties', 'Permission to create faculties', '2024-11-23 11:06:51.371', '2024-11-23 11:06:51.371'),
    (2, 'view_faculty', 'Permission to view a specific faculty', '2024-11-23 11:06:51.371', '2024-11-23 11:06:51.371'),
    (3, 'view_faculties', 'Permission to view the list of faculties', '2024-11-23 11:06:51.371', '2024-11-23 11:06:51.371'),
    (4, 'update_faculties', 'Permission to update faculties', '2024-11-23 11:06:51.371', '2024-11-23 11:06:51.371'),
    (5, 'delete_faculties', 'Permission to delete faculties', '2024-11-23 11:06:51.371', '2024-11-23 11:06:51.371'),
    (6, 'create_answers', 'Permission to create answers', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (7, 'view_answer', 'Permission to view a specific answer', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (8, 'view_answers', 'Permission to view the list of answers', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (9, 'update_answers', 'Permission to update answers', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (10, 'delete_answers', 'Permission to delete answers', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (11, 'create_evaluations', 'Permission to create evaluations', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (12, 'view_evaluation', 'Permission to view a specific evaluation', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (13, 'view_evaluations', 'Permission to view the list of evaluations', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (14, 'update_evaluations', 'Permission to update evaluations', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (15, 'delete_evaluations', 'Permission to delete evaluations', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (16, 'create_grading_matrix', 'Permission to create grading matrices', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (17, 'view_grading_matrix', 'Permission to view a specific grading matrix', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (18, 'view_grading_matrices', 'Permission to view the list of grading matrices', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (19, 'update_grading_matrix', 'Permission to update grading matrices', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (20, 'delete_grading_matrix', 'Permission to delete grading matrices', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (21, 'create_questions', 'Permission to create questions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (22, 'view_question', 'Permission to view a specific question', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (23, 'view_questions', 'Permission to view the list of questions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (24, 'update_questions', 'Permission to update questions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (25, 'delete_questions', 'Permission to delete questions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (26, 'create_role_permissions', 'Permission to create role permissions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (27, 'view_role_permission', 'Permission to view a specific role permission', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (28, 'view_role_permissions', 'Permission to view the list of role permissions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (29, 'update_role_permissions', 'Permission to update role permissions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (30, 'delete_role_permissions', 'Permission to delete role permissions', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (36, 'create_subjects', 'Permission to create subjects', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (37, 'view_subject', 'Permission to view a specific subject', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (38, 'view_subjects', 'Permission to view the list of subjects', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (39, 'update_subjects', 'Permission to update subjects', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (40, 'delete_subjects', 'Permission to delete subjects', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (41, 'create_users', 'Permission to create users', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (42, 'view_user', 'Permission to view a specific user', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (43, 'view_users', 'Permission to view the list of users', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (44, 'update_users', 'Permission to update users', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628'),
    (45, 'delete_users', 'Permission to delete users', '2024-11-23 11:41:18.628', '2024-11-23 11:41:18.628');


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
INSERT INTO public.answers (answer_description, id_evaluation, id_question, id_user, score, created_at, updated_at)
VALUES
-- Respuestas para la pregunta 1
('Sí', 1, 1, NULL, NULL, NOW(), NOW()),
('No', 1, 1, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 2
('Sí', 1, 2, NULL, NULL, NOW(), NOW()),
('No', 1, 2, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 3
('Sí', 2, 3, NULL, NULL, NOW(), NOW()),
('No', 2, 3, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 4
('Sí', 2, 4, NULL, NULL, NOW(), NOW()),
('No', 2, 4, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 5
('Sí', 2, 5, NULL, NULL, NOW(), NOW()),
('No', 2, 5, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 6
('Sí', 2, 6, NULL, NULL, NOW(), NOW()),
('No', 2, 6, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 7
('Sí', 2, 7, NULL, NULL, NOW(), NOW()),
('No', 2, 7, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 8
('Sí', 2, 8, NULL, NULL, NOW(), NOW()),
('No', 2, 8, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 9
('Sí', 2, 9, NULL, NULL, NOW(), NOW()),
('No', 2, 9, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 10
('Sí', 2, 10, NULL, NULL, NOW(), NOW()),
('No', 2, 10, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 11
('Sí', 3, 11, NULL, NULL, NOW(), NOW()),
('No', 3, 11, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 12
('Sí', 3, 12, NULL, NULL, NOW(), NOW()),
('No', 3, 12, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 13
('Sí', 3, 13, NULL, NULL, NOW(), NOW()),
('No', 3, 13, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 14
('Sí', 3, 14, NULL, NULL, NOW(), NOW()),
('No', 3, 14, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 15
('Sí', 3, 15, NULL, NULL, NOW(), NOW()),
('No', 3, 15, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 16
('Sí', 3, 16, NULL, NULL, NOW(), NOW()),
('No', 3, 16, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 17
('Sí', 3, 17, NULL, NULL, NOW(), NOW()),
('No', 3, 17, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 18
('Sí', 4, 18, NULL, NULL, NOW(), NOW()),
('No', 4, 18, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 19
('Sí', 4, 19, NULL, NULL, NOW(), NOW()),
('No', 4, 19, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 20
('Sí', 4, 20, NULL, NULL, NOW(), NOW()),
('No', 4, 20, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 21
('Sí', 4, 21, NULL, NULL, NOW(), NOW()),
('No', 4, 21, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 22
('Sí', 4, 22, NULL, NULL, NOW(), NOW()),
('No', 4, 22, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 23
('Sí', 4, 23, NULL, NULL, NOW(), NOW()),
('No', 4, 23, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 24
('Sí', 4, 24, NULL, NULL, NOW(), NOW()),
('No', 4, 24, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 25
('Sí', 5, 25, NULL, NULL, NOW(), NOW()),
('No', 5, 25, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 26
('Sí', 5, 26, NULL, NULL, NOW(), NOW()),
('No', 5, 26, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 27
('Sí', 5, 27, NULL, NULL, NOW(), NOW()),
('No', 5, 27, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 28
('Sí', 5, 28, NULL, NULL, NOW(), NOW()),
('No', 5, 28, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 29
('Sí', 5, 29, NULL, NULL, NOW(), NOW()),
('No', 5, 29, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 30
('Sí', 5, 30, NULL, NULL, NOW(), NOW()),
('No', 5, 30, NULL, NULL, NOW(), NOW()),
-- Respuestas para la pregunta 31
('Sí', 5, 31, NULL, NULL, NOW(), NOW()),
('No', 5, 31, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 32
('Sí', 6, 32, NULL, NULL, NOW(), NOW()),
('No', 6, 32, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 33
('Sí', 6, 33, NULL, NULL, NOW(), NOW()),
('No', 6, 33, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 34
('Sí', 6, 34, NULL, NULL, NOW(), NOW()),
('No', 6, 34, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 35
('Sí', 6, 35, NULL, NULL, NOW(), NOW()),
('No', 6, 35, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 36
('Sí', 6, 36, NULL, NULL, NOW(), NOW()),
('No', 6, 36, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 37
('Sí', 6, 37, NULL, NULL, NOW(), NOW()),
('No', 6, 37, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 38
('Sí', 6, 38, NULL, NULL, NOW(), NOW()),
('No', 6, 38, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 39
('Sí', 7, 39, NULL, NULL, NOW(), NOW()),
('No', 7, 39, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 40
('Sí', 7, 40, NULL, NULL, NOW(), NOW()),
('No', 7, 40, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 41
('Sí', 7, 41, NULL, NULL, NOW(), NOW()),
('No', 7, 41, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 42
('Sí', 7, 42, NULL, NULL, NOW(), NOW()),
('No', 7, 42, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 43
('Sí', 7, 43, NULL, NULL, NOW(), NOW()),
('No', 7, 43, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 44
('Sí', 7, 44, NULL, NULL, NOW(), NOW()),
('No', 7, 44, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 45
('Sí', 7, 45, NULL, NULL, NOW(), NOW()),
('No', 7, 45, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 46
('Sí', 8, 46, NULL, NULL, NOW(), NOW()),
('No', 8, 46, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 47
('Sí', 8, 47, NULL, NULL, NOW(), NOW()),
('No', 8, 47, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 48
('Sí', 8, 48, NULL, NULL, NOW(), NOW()),
('No', 8, 48, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 49
('Sí', 8, 49, NULL, NULL, NOW(), NOW()),
('No', 8, 49, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 50
('Sí', 8, 50, NULL, NULL, NOW(), NOW()),
('No', 8, 50, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 51
('Sí', 8, 51, NULL, NULL, NOW(), NOW()),
('No', 8, 51, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 52
('Sí', 8, 52, NULL, NULL, NOW(), NOW()),
('No', 8, 52, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 53
('Sí', 9, 53, NULL, NULL, NOW(), NOW()),
('No', 9, 53, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 54
('Sí', 9, 54, NULL, NULL, NOW(), NOW()),
('No', 9, 54, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 55
('Sí', 9, 55, NULL, NULL, NOW(), NOW()),
('No', 9, 55, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 56
('Sí', 9, 56, NULL, NULL, NOW(), NOW()),
('No', 9, 56, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 57
('Sí', 9, 57, NULL, NULL, NOW(), NOW()),
('No', 9, 57, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 58
('Sí', 9, 58, NULL, NULL, NOW(), NOW()),
('No', 9, 58, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 59
('Sí', 9, 59, NULL, NULL, NOW(), NOW()),
('No', 9, 59, NULL, NULL, NOW(), NOW()),

-- Respuestas para la pregunta 60
('Sí', 10, 60, NULL, NULL, NOW(), NOW()),
('No', 10, 60, NULL, NULL, NOW(), NOW());



-- Insertando datos en la tabla grading_matrix
INSERT INTO grading_matrix (id_subject, total_evaluations, total_score, recommendation, score, document, created_at, updated_at)
VALUES 
    (1, 10, 45.0, 'Good progress', 4.5, 'doc1.pdf', NOW(), NOW()),
    (2, 5, 18.5, 'Needs improvement', 3.7, 'doc2.pdf', NOW(), NOW()),
    (3, 8, 32.0, 'Excellent', 4.9, 'doc3.pdf', NOW(), NOW());
