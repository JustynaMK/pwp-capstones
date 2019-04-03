class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("Email address for " + self.name + " has been updated.")

    def __repr__(self):
        return "User " + self.name + ", email: " + self.email + ", books read: " + str(len(self.books.keys()))

    def __eq__(self, other_user):
        if other_user.email == self.email:
            if other_user.name == self.name:
                return True

    def read_book(self, book, rating=None):
        self.books.update({book: rating})

    def get_average_rating(self):
        sum_rating = 0
        count_rating = 0
        for rating in self.books.values():
            if rating is not None:
                sum_rating += rating
                count_rating += 1
        return sum_rating/count_rating


class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("ISBN for " + self.title + " has been updated to " + str(self.isbn))

    def add_rating(self, rating):
        if rating in range(0, 5):
            self.ratings.append(rating)
        else:
            print("Invalid Rating. Must be a number between 0 and 4.")

    def __eq__(self, other_book):
        if other_book.title == self.title:
            if other_book.isbn == self.isbn:
                return True

    def get_average_rating(self):
        sum_rating = 0
        count_rating = 0
        for rating in self.ratings:
            if rating is not None:
                sum_rating += rating
                count_rating += 1
        return sum_rating/count_rating

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return self.title + " by " + self.author


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title + ", a " + self.level + " manual on " + self.subject


class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.unique_isbn = []

    def __repr__(self):
        return "Welcome! We currently have " + str(len(self.users)) + " users and " \
               + str(len(self.books)) + " books in our database."

    def create_book(self, title, isbn):
        # make sure that books have unique ISBNs
        if isbn in self.unique_isbn:
            print("We already have this book in our database! ISBN: " + str(isbn))
        else:
            self.unique_isbn.append(isbn)
            print("Book '" + title + "' has been added.")
            return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        # make sure that books have unique ISBNs
        if isbn in self.unique_isbn:
            print("We already have this book in our database! ISBN: " + str(isbn))
        else:
            self.unique_isbn.append(isbn)
            print("Book '" + title + "' has been added.")
            return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        # make sure that books have unique ISBNs
        if isbn in self.unique_isbn:
            print("We already have this book in our database! ISBN: " + str(isbn))
        else:
            self.unique_isbn.append(isbn)
            print("Book '" + title + "' has been added.")
            return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            user = self.users.get(email)
            user.read_book(book, rating)
            if rating is not None:
                book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] += 1
            else:
                self.books[book] = 1
            # print("Book '" + book.title + "' has been added to email: " \
            # + email + ". Current count: " + str(self.books[book]))
        else:
            print("No user with email " + email + "!")

    def add_user(self, name, email, user_books=None):
        # error testing - this user already exists
        if email in self.users.keys():
            print("We already have " + email + " in our database!")
        # make sure that an email address is valid
        elif '@' not in email:
            print("Invalid email address! " + email)
        else:
            new_user = User(name, email)
            self.users.update({email: new_user})
            if user_books is not None:
                for book in user_books:
                    self.add_book_to_user(book, email)
            # print("User " + name + ", email: " + email + ", added to the database.")

    # Some Additional Analysis Methods for TomeRater
    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        max_value = 0
        most_read = ""
        for book_title, book_value in self.books.items():
            if book_value > max_value:
                max_value = book_value
                most_read = book_title
        return "The most read book is: '" + str(most_read) + "', our users read it " + str(max_value) + " times!"
        # to be adjusted - print book title

    def highest_rated_book(self):
        score = 0
        for book in self.books.keys():
            # print(str(book.get_average_rating()))
            if book.get_average_rating() > score:
                score = book.get_average_rating()
        return "The highest rated book is: '" + str(book) + "' with an average rating: " + str(score)

    def most_positive_user(self):
        score = 0
        winning_user = ""
        for user in self.users.values():
            # print(user.email + " - " + str(user.get_average_rating()))
            if user.get_average_rating() > score:
                score = user.get_average_rating()
                winning_user = user
        return "The most positive user is: " + winning_user.get_email() + " with an average rating: " + str(score)

    # A few more analysis methods:

    def get_n_most_read_books(self, n):
        # top_n_books = {}
        if n > len(self.books):
            return "Whoa! We do not have " + str(n) + " books in our database."
        else:
            for book in sorted(list(self.books.values()))[:3]:
                return book

    def get_n_most_prolific_readers(self, n):
        if n > len(self.users):
            return "Whoa! We do not have " + str(n) + " users in our database."
        else:
            for user in sorted(list(self.users.items()))[:3]:
                return type(self.users.items())