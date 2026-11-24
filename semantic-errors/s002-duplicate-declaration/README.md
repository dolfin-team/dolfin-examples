# S002: Duplicate declaration

This project declares the same concept, `Book`, twice on purpose.

## The mistake

```dolfin
concept Book

concept Book
```

## What the checker says

`radeau check` reports an error at `model.dlf:3:1`:

```
error[S002]: duplicate declaration `Book`
```

## How to fix it

Declare each name once. Delete the second line, or rename it if you meant a different concept.

```dolfin
concept Book
```
