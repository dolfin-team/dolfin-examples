# S012: Name not defined by import

This project refers to a name in an imported namespace that the import does not define. The name is a typo.

## The mistake

`package.dlf` imports the FOAF vocabulary:

```dolfin
import <http://xmlns.com/foaf/0.1/> from <https://xmlns.com/foaf/spec/index.rdf>
```

`model.dlf` then uses `foaf:Agentx`. FOAF has `foaf:Agent`, but not `foaf:Agentx`:

```dolfin
prefix <http://xmlns.com/foaf/0.1/> as foaf

concept Gadget:
  sub foaf:Agentx
```

## What the checker says

The checker should report that `foaf:Agentx` is not defined by the import. To check the name, it needs the import lock. Without the lock, `radeau check` only warns:

```
warning: import <http://xmlns.com/foaf/0.1/>: no lock in .dolfin/imports/; export the import lock from Agrafe
```

Export the lock from Agrafe to see the real S012 diagnostic.

## How to fix it

Use a name that the imported vocabulary defines:

```dolfin
concept Gadget:
  sub foaf:Agent
```
