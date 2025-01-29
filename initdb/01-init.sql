-- Dodawanie użytkowników
INSERT INTO Uzytkownik (id, email, password) VALUES
    ('11111111-1111-1111-1111-111111111111', 'maja@example.com', 'maja'),
    ('22222222-2222-2222-2222-222222222222', 'anna.nowak@example.com', 'securepassword2');

-- Dodawanie zwierząt
INSERT INTO Zwierzeta (id, imie, typ, Uzytkownik_id) VALUES
    ('33333333-3333-3333-3333-333333333333', 'Burek', 'PIES', '11111111-1111-1111-1111-111111111111'),
    ('77777777-7777-7777-7777-777777777777', 'Rudzikkk', 'PIES', '11111111-1111-1111-1111-111111111111'),
    ('44444444-4444-4444-4444-444444444444', 'Mruczek', 'KOT', '22222222-2222-2222-2222-222222222222') ON CONFLICT (id) DO NOTHING;

-- Dodawanie ogłoszeń
INSERT INTO Ogloszenia (id, tresc, Uzytkownik_id, Zwierzeta_id, tytul) VALUES
    ('55555555-5555-5555-5555-555555555555', 'Sprzedam wesołego psa Burek. Idealny dla dzieci!', '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', 'Sprzedam psa'),
    ('66666666-6666-6666-6666-666666666666', 'Oddam kota Mruczka w dobre ręce. Uroczy i spokojny!', '22222222-2222-2222-2222-222222222222', '44444444-4444-4444-4444-444444444444', 'Oddam kota');
