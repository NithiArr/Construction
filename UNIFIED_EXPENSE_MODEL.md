# Unified Expense Model - Quick Guide

## Overview
The database now uses a **unified Expense table** that handles both regular expenses and material purchases.

## How It Works

### Database Structure
**Table:** `expense`

All expenses (both regular and material purchases) are stored in this single table with the following key fields:

| Field | Description | Example Values |
|-------|-------------|----------------|
| `category` | Type of expense | 'Regular Expense' or 'Material Purchase' |
| `subcategory` | Detailed classification | 'Steel', 'Cement', 'Labor', 'Transportation' |
| `vendor_id` | Vendor reference (nullable) | Used for Material Purchases |
| `invoice_number` | Invoice reference (nullable) | Used for Material Purchases |
| `amount` | Total amount | Amount in currency |
| `payment_mode` | Payment method | 'CASH', 'BANK', 'UPI', 'CREDIT' |

### Material Purchases
When you add a purchase:
- **Category**: Automatically set to `'Material Purchase'`
- **Subcategory**: **Required** - Specify the material type (e.g., 'Steel', 'Cement', 'Electrical')
- **Vendor**: Required - Link to vendor
- **Invoice Number**: Invoice reference
- **Items**: Stored in `expense_item` table (quantity, unit price, total)

**Example:**
```
Category: Material Purchase
Subcategory: Steel Bars
Vendor: Steel Suppliers Ltd
Invoice: INV-2025-001
Items: 
  - Steel Bars (12mm): 1000 kg @ ₹450 = ₹4,50,000
  - Steel Plates: 50 units @ ₹1000 = ₹50,000
Total: ₹5,00,000
```

### Regular Expenses
When you add an expense:
- **Category**: Set to `'Regular Expense'`
- **Subcategory**: Optional - Specify expense type (e.g., 'Skilled Labor', 'Crane Rental')
- **Vendor**: Not required
- **No items** - Just a single amount

**Example:**
```
Category: Regular Expense
Subcategory: Skilled Labor
Amount: ₹1,50,000
Payment Mode: BANK
Description: Monthly wages for masons
```

## UI Changes

### Purchases Page
- New **"Material Category"** field - specify the type of material (Steel, Cement, etc.)
- This appears in the form and in the table listing
- **Required field** when creating a purchase

### Expenses Page
- Already has **Category** and **Subcategory** fields
- Subcategory is optional for regular expenses

## API Behavior

### Purchases API (`/api/purchases`)
- **GET**: Returns `Expense` records where `category='Material Purchase'`
- **POST**: Creates an `Expense` with `category='Material Purchase'` + items
- Field mapping:
  - `purchase_id` → `expense_id` (for backward compatibility)
  - `invoice_date` → `expense_date`
  - `payment_type` → `payment_mode`

### Expenses API (`/api/expenses`)
- **GET**: Returns `Expense` records where `category='Regular Expense'`
- **POST**: Creates an `Expense` with `category='Regular Expense'`

## Benefits of This Structure

1. **Simplified Database**: One table instead of two
2. **Flexible Classification**: Subcategory allows detailed tracking
3. **Consistent Reporting**: All expenses in one place for KPIs
4. **Easier Queries**: Single table to query for all project spending

## Migration Notes

- Old database file: `construction.db`
- New database file: `construction_v2.db` ✅
- Data has been re-seeded with the new structure
- All helper scripts updated to use the new database

## Subcategory Examples

### Material Purchases
- Steel Bars
- Cement
- Bricks
- Electrical Cables
- Plumbing Materials
- Paint
- Hardware

### Regular Expenses
- Skilled Labor
- Unskilled Labor
- Equipment Rental
- Transportation
- Site Supervision
- Safety Equipment
- Utilities
- Miscellaneous
