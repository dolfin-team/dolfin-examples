# Personal Finance

A small bank-account model with two accounts, two transactions, and two flagging rules. It also shows how to declare a currency with `unitdef`.

## What's inside

- **`Account`**: a bank account with an owner, an `AccountType` (`Checking`, `Savings`, `Credit`) and a balance in cents.
- **`Transaction`**: a posting against an account. It has an amount in cents and an optional `amountQuantity`, which is a currency value such as `quantity(1200 USD)`.
- **`unitdef USD: scale 0.92 EUR`**: declares USD as a currency worth 0.92 EUR. EUR is built in.
- **`flag_large_transaction`**: marks any transaction over 100000 cents as a `LargeTransaction`.
- **`flag_overdrawn`**: marks any account with `overdrawn true` as an `OverdrawnAccount`.
- **Facts**: `checking` and `savings` accounts, plus the `rent` and `paycheck` transactions.

## Try it

- Run the query `large_transactions`. It lists large transactions and their accounts. `rent` and `paycheck` should both show up.
- Read `flag_overdrawn`. The `checking` account should be flagged because its `overdrawn` is `true`.

## Learn more

- `one of:` enumerations (`AccountType`, `TransactionType`)
- `unitdef` and `quantity(...)` for currencies
