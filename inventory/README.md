# Inventory

A small e-commerce model: products in a warehouse, customers, and orders. Rules automatically flag products that need restocking.

## What's inside

- **`Product`**: a sellable item with a price, stock level (`quantityOnHand`) and `reorderThreshold`.
- **`Warehouse`**: where stock is held (`mainWarehouse`, in Newark).
- **`Customer`** and **`Order`**: an order has a customer, a status and one or more `items`.
- **`OrderStatus`**: a fixed list of stages: `PENDING`, `PAID`, `SHIPPED`, `DELIVERED`, `CANCELLED`.
- **`flag_low_stock`**: a rule marking any product at or below its reorder threshold as `LowStockProduct`.
- **`flag_out_of_stock`**: a rule marking products with zero units as `OutOfStockProduct`.

## Try it

- Read the facts `mechanicalKeyboard` (4 on hand, threshold 10) and `usbCable` (0 on hand, threshold 20). Both should be flagged low on stock. `usbCable` should also be flagged out of stock.
- Run the query `pending_orders_by_warehouse`. It lists pending orders and the warehouse each item ships from. The only sample order, `order1001`, is `PAID`, so expect no rows until you add a pending one.

## Learn more

- `one of:` enumerations (`OrderStatus`)
- Rules with a comparison filter: `quantityOnHand [ <= ?_threshold ]`
