CREATE TABLE public.books (
	"book_id" serial NOT NULL,
	"book_title" varchar(255) NOT NULL,
	"total_pages" integer,
	"number_copy" integer NOT NULL,
	"genre_id" integer NOT NULL,
	"author_id" integer NOT NULL,
	CONSTRAINT "books_pk" PRIMARY KEY ("book_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.authors (
	"author_id" serial NOT NULL,
	"author_name" varchar(255) NOT NULL,
	CONSTRAINT "author_pk" PRIMARY KEY ("author_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.genres (
	"genre_id" serial NOT NULL ,
	"genre_name" varchar(255) NOT NULL,
	CONSTRAINT "genres_pk" PRIMARY KEY ("genre_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.user (
	"user_id" serial NOT NULL,
	"user_name" varchar(255) NOT NULL,
	"user_password" varchar(255) NOT NULL,
	CONSTRAINT "user_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.read_book (
	"read_id" serial NOT NULL,
	"user_id" integer NOT NULL,
	"book_id" integer NOT NULL,
	CONSTRAINT "read_book_pk" PRIMARY KEY ("read_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.favorite (
	"favorite_id" serial NOT NULL,
	"user_id" integer NOT NULL,
	"book_id" integer NOT NULL,
	CONSTRAINT "favorite_pk" PRIMARY KEY ("favorite_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.borrowing (
	"borrow_id" serial NOT NULL,
	"borrow_date" DATE NOT NULL,
	"user_id" integer NOT NULL,
	"book_id" integer NOT NULL,
	CONSTRAINT "borrowing_pk" PRIMARY KEY ("borrow_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.returnings (
	"return_id" serial NOT NULL,
	"return_date" DATE NOT NULL,
	"user_id" integer NOT NULL,
	"book_id" integer NOT NULL,
	CONSTRAINT "returnings_pk" PRIMARY KEY ("return_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE public.added_book (
	"added_id" serial NOT NULL,
	"book_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"added_date" DATE NOT NULL,
	CONSTRAINT "added_book_pk" PRIMARY KEY ("added_id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "books" ADD CONSTRAINT "books_fk0" FOREIGN KEY ("genre_id") REFERENCES "genres"("genre_id");
ALTER TABLE "books" ADD CONSTRAINT "books_fk1" FOREIGN KEY ("author_id") REFERENCES "authors"("author_id");




ALTER TABLE "read_book" ADD CONSTRAINT "read_book_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("user_id");
ALTER TABLE "read_book" ADD CONSTRAINT "read_book_fk1" FOREIGN KEY ("book_id") REFERENCES "books"("book_id");

ALTER TABLE "favorite" ADD CONSTRAINT "favorite_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("user_id");
ALTER TABLE "favorite" ADD CONSTRAINT "favorite_fk1" FOREIGN KEY ("book_id") REFERENCES "books"("book_id");

ALTER TABLE "borrowing" ADD CONSTRAINT "borrowing_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("user_id");
ALTER TABLE "borrowing" ADD CONSTRAINT "borrowing_fk1" FOREIGN KEY ("book_id") REFERENCES "books"("book_id");

ALTER TABLE "returnings" ADD CONSTRAINT "returnings_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("user_id");
ALTER TABLE "returnings" ADD CONSTRAINT "returnings_fk1" FOREIGN KEY ("book_id") REFERENCES "books"("book_id");

ALTER TABLE "added_book" ADD CONSTRAINT "added_book_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("book_id");
ALTER TABLE "added_book" ADD CONSTRAINT "added_book_fk1" FOREIGN KEY ("user_id") REFERENCES "user"("user_id");


