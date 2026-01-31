# UI Terminology Fix - Outstanding

## Changes Made

### ✅ Fixed Terminology Across All Templates

The term "Balance" has been replaced with "**Outstanding**" to accurately represent **vendor payables** (money we owe to vendors).

---

## Updated Files

### 1. **vendor_analytics.html** ✅
**Purchase History Table Header:**
- ❌ Before: `Balance`  
- ✅ After: `Outstanding`

**What it shows:** How much money we still owe to each vendor for their invoices.

---

### 2. **owner_dashboard.html** ✅

**KPI Card:**
- ❌ Before: `Outstanding` (ambiguous)
- ✅ After: `Vendor Outstanding` with helper text "What we owe vendors"

**Table Column:**
- Shows `vendor_outstanding` per project
- **Bold formatting** to emphasize vendor payables

---

### 3. **projects.html** ✅

**Financial Summary Card:**
- ❌ Before: `Outstanding` (ambiguous)
- ✅ After: `Vendor Outstanding` with helper text "What we owe vendors"

**Purchase History Table:**
- ❌ Before: `Balance`  
- ✅ After: `Outstanding`

**Data Source:**
- Now correctly uses `financial_summary.vendor_outstanding`

---

## Terminology Clarity

### Vendor Outstanding (Payables)
**What we owe to vendors**

```
Example:
- Purchased materials worth ₹5,00,000  
- Paid to vendor ₹2,50,000  
- Outstanding = ₹2,50,000 (we still owe them this)
```

**Visible in:**
- Owner Dashboard → "Vendor Outstanding" KPI
- Owner Dashboard → Project table "Outstanding" column  
- Vendor Analytics → "Outstanding" column
- Project Details Modal → "Vendor Outstanding" card
- Project Details Modal → Purchase History "Outstanding" column

---

### Client Outstanding (Receivables)
**What clients owe to us**

```
Example:
- Total project cost ₹13,00,000  
- Client paid ₹80,00,000  
- Client Outstanding = -₹67,00,000 (they overpaid, or we're in profit)
```

**Currently:** Not displayed in UI (backend calculates but not shown)

---

## Visual Improvements

1. **Added Helper Text** on cards:
   - "What we owe vendors" below Vendor Outstanding
   - Small, secondary text for clarity

2. **Bold Formatting** on critical amounts:
   - Vendor Outstanding values are **bolded** in tables
   - Makes it easier to spot important payables

3. **Consistent Column Names**:
   - All "Balance" → "Outstanding"
   - Reduces confusion across different views

---

## Business Impact

### Before (Confusing ❌)
```
Outstanding: ₹4,00,000
```
*Is this what vendors owe us or what we owe vendors?*

### After (Clear ✅)
```
Vendor Outstanding: ₹4,00,000
What we owe vendors
```
*Crystal clear!*

---

## Next Steps (Optional Enhancements)

### 1. Add Client Outstanding to UI
Show "Client Outstanding" (receivables) alongside "Vendor Outstanding":

```
[Vendor Outstanding]    [Client Outstanding]
₹4,00,000              ₹3,00,000
What we owe vendors     What clients owe us
```

### 2. Cash Flow Indicator
Compare the two:
- If Vendor Outstanding > Client Outstanding = 🔴 Cash outflow needed
- If Client Outstanding > Vendor Outstanding = 🟢 Healthy position

### 3. Aging Reports
Break down outstanding by age:
- 0-30 days
- 31-60 days
- 60+ days (overdue)

---

## Summary

All instances of "Balance" in purchase history and payment tables have been changed to **"Outstanding"** to clearly communicate **vendor payables**.

The UI now makes it unmistakably clear:
- **Vendor Outstanding** = What you owe vendors
- Every instance is labeled consistently
- Helper text provides additional clarity

✅ **The terminology is now aligned with standard accounting practices!**
