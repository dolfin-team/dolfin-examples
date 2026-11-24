# Library Lending

A small model of a library: books, authors, members and the loans that connect them. It shows how Dolfin describes data, derives new facts with a rule, and asks questions with a query.

## What's inside

- **`LoanStatus`**: a fixed list of loan states (`ACTIVE`, `RETURNED`, `OVERDUE`, `LOST`).
- **`Author`** and **`Book`**: a book has an ISBN, a title and one or more authors.
- **`Member`**: a person with a card number and a `loanLimit`.
- **`Loan`**: one member borrowing one book, with a status and dates.
- **Facts**: `tolkien`, `hobbit`, `alice` and `hobbitLoan` give a tiny working example.
- **`flag_classic`**: a rule that tags books published before 1970 as `ClassicBook`.
- **`overdue_loans`**: a query that lists loans with status `OVERDUE`.

## Try it

- Read `flag_classic`. `hobbit` (1937) becomes a `ClassicBook` automatically.
- Run `overdue_loans`. It returns nothing, because `hobbitLoan` is `ACTIVE`. Change its status to `OVERDUE` and run it again.

## Learn more

- `one of:` enumerations (`LoanStatus`)
- `optional`, `one` and `some` properties (`some Author` means one or more)
- Rules with `match:` and `then:`
