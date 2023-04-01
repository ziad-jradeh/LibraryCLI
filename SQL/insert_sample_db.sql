INSERT INTO authors (author_name)
VALUES
    ('Harper Lee'),
    ('F. Scott Fitzgerald'),
    ('George Orwell'),
    ('Jane Austen'),
    ('J.D. Salinger'),
    ('Mark Twain'),
    ('Herman Melville'),
    ('Mary Shelley'),
    ('Bram Stoker'),
    ('Charlotte Bronte'),
    ('Emily Bronte'),
    ('Oscar Wilde'),
    ('J.R.R. Tolkien'),
    ('Douglas Adams'),
    ('Aldous Huxley'),
    ('Gabriel Garcia Marquez'),
    ('William Faulkner'),
    ('Ernest Hemingway'),
    ('Alice Walker'),
    ('Toni Morrison'),
    ('Margaret Atwood'),
    ('Sylvia Plath'),
    ('Kurt Vonnegut');


INSERT INTO genres (genre_name)
VALUES
    ('Fiction'),
    ('Dystopian'),
    ('Adventure'),
    ('Gothic Horror'),
    ('Fantasy'),
    ('Science Fiction'),
    ('Magical Realism'),
    ('Historical Fiction');


INSERT INTO books (book_title, total_pages, number_copy, genre_id, author_id)
VALUES

  ('To Kill a Mockingbird', 281, 10, 1, 1),
  ('The Great Gatsby', 180, 8, 1, 2),
  ('1984', 328, 12, 2, 3),
  ('Animal Farm', 112, 6, 2, 3),
  ('Pride and Prejudice', 279, 9, 1, 4),
  ('Sense and Sensibility', 352, 7, 1, 4),
  ('The Catcher in the Rye', 277, 11, 1, 5),
  ('The Adventures of Huckleberry Finn', 366, 13, 1, 6),
  ('The Adventures of Tom Sawyer', 224, 9, 1, 6),
  ('Moby-Dick', 585, 5, 3, 7),
  ('Frankenstein', 280, 7, 4, 8),
  ('Dracula', 418, 9, 4, 9),
  ('Jane Eyre', 507, 8, 1, 10),
  ('Wuthering Heights', 353, 6, 1, 11),
  ('The Picture of Dorian Gray', 254, 5, 1, 12),
  ('The Hobbit', 310, 9, 5, 13),
  ('The Lord of the Rings', 1178, 4, 5, 13),
  ('The Hitchhiker''s Guide to the Galaxy', 215, 11, 6, 14),
  ('Brave New World', 311, 10, 2, 15),
  ('One Hundred Years of Solitude', 422, 8, 7, 16),
  ('The Sound and the Fury', 326, 6, 1, 17),
  ('As I Lay Dying', 267, 7, 1, 17),
  ('The Sun Also Rises', 251, 5, 1, 18),
  ('For Whom the Bell Tolls', 471, 9, 1, 18),
  ('The Old Man and the Sea', 127, 10, 1, 18),
  ('The Color Purple', 295, 8, 8, 19),
  ('Beloved', 321, 6, 8, 20),
  ('The Handmaid''s Tale', 311, 11, 2, 21),
  ('The Bell Jar', 288, 7, 1, 22),
  ('Slaughterhouse-Five', 215, 9, 1, 23),
  ('Cat''s Cradle', 287, 6, 6, 23);

iNSERT INTO public."user" (user_name, user_password) VALUES ('Elen', '123');
iNSERT INTO public."user" (user_name, user_password) VALUES ('Thom', '1');
iNSERT INTO public."user" (user_name, user_password) VALUES ('Mary', '2');

INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2020-01-01', 1, 2);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-02-04', 1, 5);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-02-04', 2, 7);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-02-04', 2, 9);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-02-04', 3, 11);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-02-04', 3, 12);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-01-01', 2, 2);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-01-01', 2, 5);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-01-01', 2, 11);
INSERT INTO public.borrowing (borrow_date, user_id, book_id) VALUES ('2022-01-01', 2, 12);


INSERT INTO public.returnings (return_date, user_id, book_id) VALUES ('2023-01-01', 2, 2);
INSERT INTO public.returnings (return_date, user_id, book_id) VALUES ('2023-01-01', 2, 5);
INSERT INTO public.returnings (return_date, user_id, book_id) VALUES ('2023-01-01', 2, 11);
INSERT INTO public.returnings (return_date, user_id, book_id) VALUES ('2023-01-01', 2, 12);

  

