BEGIN;

-- 1) Cria 20 usuários profissionais
INSERT INTO users (id, name, email, password, role, cpf, phone, cep, uf, city, address, created_at, updated_at) VALUES
(1,  'Profissional 1',  'professional1@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '49501618900', '11900000001', '01001000', 'SP', 'São Paulo',        'Endereço 1',  now(), now()),
(2,  'Profissional 2',  'professional2@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '54964427455', '11900000002', '01001000', 'RJ', 'Rio de Janeiro',  'Endereço 2',  now(), now()),
(3,  'Profissional 3',  'professional3@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '37612779625', '11900000003', '01001000', 'MG', 'Belo Horizonte', 'Endereço 3',  now(), now()),
(4,  'Profissional 4',  'professional4@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '63077480603', '11900000004', '01001000', 'BA', 'Salvador',       'Endereço 4',  now(), now()),
(5,  'Profissional 5',  'professional5@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '60385742398', '11900000005', '01001000', 'RS', 'Porto Alegre',  'Endereço 5',  now(), now()),
(6,  'Profissional 6',  'professional6@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '51538386500', '11900000006', '01001000', 'SC', 'Florianópolis', 'Endereço 6',  now(), now()),
(7,  'Profissional 7',  'professional7@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '16568557986', '11900000007', '01001000', 'PR', 'Curitiba',      'Endereço 7',  now(), now()),
(8,  'Profissional 8',  'professional8@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '13843959544', '11900000008', '01001000', 'CE', 'Fortaleza',     'Endereço 8',  now(), now()),
(9,  'Profissional 9',  'professional9@example.com',  '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '32821394039', '11900000009', '01001000', 'SP', 'São Paulo',        'Endereço 9',  now(), now()),
(10, 'Profissional 10', 'professional10@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '46071291518', '11900000010', '01001000', 'RJ', 'Rio de Janeiro',  'Endereço 10', now(), now()),
(11, 'Profissional 11', 'professional11@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '36963146926', '11900000011', '01001000', 'MG', 'Belo Horizonte', 'Endereço 11', now(), now()),
(12, 'Profissional 12', 'professional12@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '57924312307', '11900000012', '01001000', 'BA', 'Salvador',       'Endereço 12', now(), now()),
(13, 'Profissional 13', 'professional13@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '23698662094', '11900000013', '01001000', 'RS', 'Porto Alegre',  'Endereço 13', now(), now()),
(14, 'Profissional 14', 'professional14@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '87113771947', '11900000014', '01001000', 'SC', 'Florianópolis', 'Endereço 14', now(), now()),
(15, 'Profissional 15', 'professional15@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '97414715647', '11900000015', '01001000', 'PR', 'Curitiba',      'Endereço 15', now(), now()),
(16, 'Profissional 16', 'professional16@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '85329784107', '11900000016', '01001000', 'CE', 'Fortaleza',     'Endereço 16', now(), now()),
(17, 'Profissional 17', 'professional17@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '76016863530', '11900000017', '01001000', 'SP', 'São Paulo',        'Endereço 17', now(), now()),
(18, 'Profissional 18', 'professional18@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '39103853977', '11900000018', '01001000', 'RJ', 'Rio de Janeiro',  'Endereço 18', now(), now()),
(19, 'Profissional 19', 'professional19@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '30450111288', '11900000019', '01001000', 'MG', 'Belo Horizonte', 'Endereço 19', now(), now()),
(20, 'Profissional 20', 'professional20@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'professional', '48820500213', '11900000020', '01001000', 'BA', 'Salvador',       'Endereço 20', now(), now());

-- Ajusta a sequence
SELECT setval(pg_get_serial_sequence('users','id'), 21, true);


-- Exemplo para um dos perfis:
INSERT INTO professional_profiles (user_id, bio, category, profissional_identification, services, price, only_online, only_presential, rating, num_reviews, start_hour, end_hour, available_days_of_week, created_at, updated_at)
VALUES
(1, 'Profissional 1 com vasta experiência.', 'doctor', 'PID0001', 'Serviço1A,Serviço1B', 110.00, true, false, 0, 0, '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday', now(), now());
-- repita de 1 a 10 com diferentes dias e horários se quiser.
-- 1) Cria 20 usuários profissionais
INSERT INTO professional_profiles (user_id, bio, category, profissional_identification, services, price, only_online, only_presential, rating, num_reviews, start_hour, end_hour, available_days_of_week, created_at, updated_at) VALUES
(2,  'Profissional 2 com vasta experiência.',  'nutritionist',         'PID0002',  'Serviço2A,Serviço2B',    120.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(3,  'Profissional 3 com vasta experiência.',  'psychologist',         'PID0003',  'Serviço3A,Serviço3B',    130.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(4,  'Profissional 4 com vasta experiência.',  'physician',            'PID0004',  'Serviço4A,Serviço4B',    140.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(5,  'Profissional 5 com vasta experiência.',  'personal_trainer',     'PID0005',  'Serviço5A,Serviço5B',    150.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(6,  'Profissional 6 com vasta experiência.',  'physiotherapist',      'PID0006',  'Serviço6A,Serviço6B',    160.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(7,  'Profissional 7 com vasta experiência.',  'occupational_therapy', 'PID0007',  'Serviço7A,Serviço7B',    170.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(8,  'Profissional 8 com vasta experiência.',  'elderly_care',         'PID0008',  'Serviço8A,Serviço8B',    180.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(9,  'Profissional 9 com vasta experiência.',  'doctor',               'PID0009',  'Serviço9A,Serviço9B',    190.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(10, 'Profissional 10 com vasta experiência.', 'nutritionist',         'PID0010',  'Serviço10A,Serviço10B',  200.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(11, 'Profissional 11 com vasta experiência.', 'psychologist',         'PID0011',  'Serviço11A,Serviço11B',  210.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(12, 'Profissional 12 com vasta experiência.', 'physician',            'PID0012',  'Serviço12A,Serviço12B',  220.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(13, 'Profissional 13 com vasta experiência.', 'personal_trainer',     'PID0013',  'Serviço13A,Serviço13B',  230.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(14, 'Profissional 14 com vasta experiência.', 'physiotherapist',      'PID0014',  'Serviço14A,Serviço14B',  240.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(15, 'Profissional 15 com vasta experiência.', 'occupational_therapy', 'PID0015',  'Serviço15A,Serviço15B',  250.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(16, 'Profissional 16 com vasta experiência.', 'elderly_care',         'PID0016',  'Serviço16A,Serviço16B',  260.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(17, 'Profissional 17 com vasta experiência.', 'doctor',               'PID0017',  'Serviço17A,Serviço17B',  270.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(18, 'Profissional 18 com vasta experiência.', 'nutritionist',         'PID0018',  'Serviço18A,Serviço18B',  280.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(19, 'Profissional 19 com vasta experiência.', 'psychologist',         'PID0019',  'Serviço19A,Serviço19B',  290.00, true,  false, 0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now()),
(20, 'Profissional 20 com vasta experiência.', 'physician',            'PID0020',  'Serviço20A,Serviço20B',  300.00, false, true,  0, 0,  '08:00', '17:00', 'monday,tuesday,wednesday,thursday,friday',now(), now());
  
-- 3) Cria 3 usuários pacientes
INSERT INTO users (id, name, email, password, role, cpf, phone, cep, uf, city, address, created_at, updated_at) VALUES
(22, 'Paciente 1', 'paciente1@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'patient', '497.790.600-49', '11900000021', '01001000', 'SP', 'São Paulo', 'Rua A, 123', now(), now()),
(23, 'Paciente 2', 'paciente2@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'patient', '273.043.470-40', '11900000022', '01001000', 'RJ', 'Rio de Janeiro', 'Rua B, 456', now(), now()),
(24, 'Paciente 3', 'paciente3@example.com', '$2a$10$/dgH.llg0qmT513u/n1fVO2fTlRSXAOQEw4KF4PRywya.VU4mJkQu', 'patient', '676.136.200-85', '11900000023', '01001000', 'MG', 'Belo Horizonte', 'Rua C, 789', now(), now());

SELECT setval(pg_get_serial_sequence('users','id'), 24, true);

-- 4) Cria 3 agendamentos
INSERT INTO appointments (patient_id, professional_id, start_time, end_time, status, created_at, updated_at) VALUES
(22, 1, '2025-08-12 09:00:00', '2025-08-12 10:00:00', 'pending', now(), now()),
(23, 2, '2025-08-13 14:00:00', '2025-08-13 15:00:00', 'pending', now(), now()),
(24, 3, '2025-08-14 11:00:00', '2025-08-14 12:00:00', 'pending', now(), now());

COMMIT;

