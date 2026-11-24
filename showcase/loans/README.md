# Loans Between Friends

Who lent how much to whom? Each loan is an edge between two people that carries its own data: an amount and an optional note.

## What's inside

- **`Person`**: someone with a `name`.
- **`Loan`**: the link behind each `lends` edge. Alice can lend to Bob twice, and each loan keeps its own amount.
- **`lends`**: a property from lender to borrower, with a required `amount` and an optional `note`. Its inverse is `borrowsFrom`.
- **`vouchesFor`**: another annotated edge, with an optional `since` date. There is at most one per pair.
- **`owes`**: derived by rule `owes_lender`. If A lends to B, then B owes A.
- **`generousTo`**: derived by rule `generous_lender`. It holds when a single loan is over 50.0.
- **Facts**: `alice`, `bob` and `carol`, with four loans between them.

## Try it

- Run query `loans_by_pair` to see each loan with its lender, borrower and amount.
- Run `generous` to see who lent more than 50. Then read rule `generous_lender`.
- Run `loan_amounts` to read amounts straight off the `Loan` links.

```dolfin
?lender lends ?borrower [amount [ > 50.0]]
```

The bracket after `lends` filters on the loan's own `amount`.

## Learn more

- Reified properties (`via Loan`) put data on an edge.
- Rules can read edge annotations in brackets.
