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
