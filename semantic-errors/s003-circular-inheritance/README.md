# S003: Circular inheritance

Two concepts, `Novel` and `Story`, each declare the other as their parent.

## The mistake

```dolfin
concept Novel:
  sub Story

concept Story:
  sub Novel
```

A concept cannot be its own ancestor. Here `Novel` inherits from `Story`, which inherits from `Novel`, and so on forever.

## What the checker says

```
error[L/semantic/circular-sub]: Circular inheritance detected for concept 'Novel'
  --> ./model.dlf:3:1
```

## How to fix it

Keep only one direction. A novel is a kind of story, so remove `sub Novel` from `Story`:

```dolfin
concept Novel:
  sub Story

concept Story:
```
