# Loans — showcase queries

Paste into the SPARQL tab of the public project.

## 1. Who lent to whom

```sparql
PREFIX l: <https://www.dolfin.fr/showcase/loans/loans#>
SELECT ?lender ?borrower WHERE {
  ?a l:lends ?b ; l:name ?lender .
  ?b l:name ?borrower .
} ORDER BY ?lender ?borrower
```

## 2. Who owes whom (rule `owes_lender`)

```sparql
PREFIX l: <https://www.dolfin.fr/showcase/loans/loans#>
SELECT ?debtor ?creditor WHERE {
  ?d l:owes ?c ; l:name ?debtor .
  ?c l:name ?creditor .
} ORDER BY ?debtor ?creditor
```

## 3. Each loan, with its amount and note

Each `lends` bracket is one `Loan` link node, tied to its edge by the
`lends_source` / `lends_target` roles:

```sparql
PREFIX l: <https://www.dolfin.fr/showcase/loans/loans#>
SELECT ?lender ?borrower ?amount ?note WHERE {
  ?loan a l:Loan ; l:lends_source ?a ; l:lends_target ?b ; l:amount ?amount .
  OPTIONAL { ?loan l:note ?note }
  ?a l:name ?lender .
  ?b l:name ?borrower .
} ORDER BY DESC(?amount)
```

With `rdf_version "1.2"` the link is a reifier of the asserted edge instead:

```sparql
PREFIX l: <https://www.dolfin.fr/showcase/loans/loans#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?lender ?borrower ?amount ?note WHERE {
  ?loan rdf:reifies <<( ?a l:lends ?b )>> ; l:amount ?amount .
  OPTIONAL { ?loan l:note ?note }
  ?a l:name ?lender .
  ?b l:name ?borrower .
} ORDER BY DESC(?amount)
```

## 4. Each loan by pair, in Dolfin

`query loans_by_pair` (`queries.dlf`) writes query 3 with an annotation
bracket, the same in both `rdf_version`s:

```dolfin
query loans_by_pair:
  ?a a loans.Person
    name ?lender
    lends ?b [amount ?amount]
  ?b name ?borrower
```

## 5. Who lent more than 50 to whom (rule `generous_lender`)

```sparql
PREFIX l: <https://www.dolfin.fr/showcase/loans/loans#>
SELECT ?lender ?borrower WHERE {
  ?a l:generousTo ?b ; l:name ?lender .
  ?b l:name ?borrower .
} ORDER BY ?lender ?borrower
```
