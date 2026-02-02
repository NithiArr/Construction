# Outstanding Logic Update & Vendor Analytics Project Filter

## ✅ **Changes Made:**

###  **1. Outstanding Logic Fixed**

**What Changed:**
- Only **CREDIT** purchases now count as outstanding
- **CASH, UPI, BANK** purchases are considered already paid

**Files Modified:**
- `dashboard_api.py`

**Updates in 4 locations:**

#### A. Main Dashboard KPIs (Lines 68-90)
```python
# Only CREDIT purchases count as outstanding
total_credit_purchases = sum([
    float(e.amount) for p in projects for e in p.expenses
    if e.category == 'Material Purchase' and e.payment_mode == 'CREDIT'
])

# CASH/UPI/BANK purchases are already paid
vendor_outstanding = total_credit_purchases - total_vendor_payments
```

#### B. Status-wise Analysis (Lines 135-152)
```python
# CREDIT Material purchases only (outstanding)
credit_purchases = sum([
    float(e.amount) for e in project.expenses
    if e.category == 'Material Purchase' and e.payment_mode == 'CREDIT'
])

vendor_outstanding = credit_purchases - vendor_payments
```

#### C. Project Details (Lines 178-201)
```python
# CREDIT Material purchases only (outstanding)
credit_purchases = sum([
    float(e.amount) for e in project.expenses
    if e.category == 'Material Purchase' and e.payment_mode == 'CREDIT'
])

vendor_outstanding = credit_purchases - vendor_payments_made
```

#### D. Vendor Summary (Lines 240-255)
```python
# Total CREDIT purchases only (outstanding)
total_credit_purchases = sum([
    float(e.amount) for e in vendor.expenses
    if e.payment_mode == 'CREDIT'
])

# Outstanding = Only CREDIT purchases minus payments
outstanding = total_credit_purchases - total_paid
```

#### E. Owner Dashboard Project Details (Lines 341-411)
```python
total_credit_purchases_amount = 0  # Only CREDIT purchases

# In the loop:
if expense.payment_mode == 'CREDIT':
    total_credit_purchases_amount += float(expense.amount)

# Calculate outstanding:
vendor_outstanding = total_credit_purchases_amount - total_vendor_payments
```

---

### **2. Vendor Analytics - Project Filter Added ✅**

**What Changed:**
- Added dropdown to filter vendor purchases by project
- Both Purchase History and Material Summary filter together
- Clean UI with "All Projects" as default

**Files Modified:**
- `templates/vendor_analytics.html`

**Features:**
1. **Project Filter Dropdown** (Line 47-54)
   - Located above Purchase History table
   - Auto-populated with unique project names from vendor purchases
   - "All Projects" option to show everything

2. **JavaScript Changes:**
   - Stores `allPurchases` and `currentVendorId` globally
   - Auto-populates project dropdown when modal opens
   - `filterByProject()` function filters both tables
   - Separate `renderPurchaseHistory()` and `renderMaterialSummary()` functions

---

## 🔧 **Backend API Update Needed:**

The vendor material summary endpoint needs one small update to support project filtering:

### **File: `dashboard_api.py`** (Line ~295-326)

**Add these lines after line 298:**

```python
def get_vendor_material_summary(vendor_id):
    """Get material-wise summary for a vendor (optionally filtered by project)"""
    from flask import request  # ADD THIS
    
    vendor = company_filter(Vendor.query).filter_by(vendor_id=vendor_id).first_or_404()
    
    # Get optional project filter from query parameter  # ADD THIS
    project_name = request.args.get('project', None)  # ADD THIS
    
    # Aggregate by material
    material_data = {}
    
    for expense in vendor.expenses:
        # Filter by project if specified  # ADD THIS
        if project_name and expense.project.name != project_name:  # ADD THIS
            continue  # ADD THIS
            
        # Check items (ExpenseItems)
        for item in expense.items:
            # ... rest of the code stays the same
```

---

## 📊 **Impact:**

### **Before:**
```
All purchases (CASH/UPI/BANK/CREDIT) = Outstanding
Outstanding - Vendor Payments = Final Outstanding
```

**Example:**
- ₹10 Lakh purchases (₹6L CASH, ₹4L CREDIT)
- ₹2L vendor payments made
- Outstanding shown: ₹8L ❌ (Wrong! CASH already paid)

### **After:**
```
Only CREDIT purchases = Outstanding
Outstanding - Vendor Payments = Final Outstanding
```

**Example:**
- ₹10 Lakh purchases (₹6L CASH, ₹4L CREDIT)
- ₹2L vendor payments made
- Outstanding shown: ₹2L ✅ (Correct! Only CREDIT minus payments)

---

## 🎯 **Testing:**

### **Test Outstanding Logic:**
1. Go to Dashboard
2. Check "Outstanding Payables" KPI
3. Should only show CREDIT purchases minus payments

### **Test Vendor Analytics Filter:**
1. Go to Vendor Analytics
2. Click "View Details" on any vendor
3. See "Filter by Project" dropdown
4. Select a project
5. Both Purchase History and Material Summary should filter

---

## 🚀 **Next Steps:**

1. ✅ Outstanding logic updated in 5 places
2. ✅ Vendor analytics UI updated with project filter
3. ⚠️ **Manual step needed**: Update the backend API (see code above)
4. 🔄 Restart server to apply changes
5. ✅ Push to GitHub

---

## 📝 **Business Logic Summary:**

**Purchases Payment Types:**

| Type | Considered | Appears in Outstanding |
|------|-----------|----------------------|
| **CREDIT** | Unpaid (credit/loan) | ✅ YES |
| **CASH** | Already paid | ❌ NO |
| **UPI** | Already paid | ❌ NO |  
| **BANK** | Already paid | ❌ NO |

**Formula:**
```
Vendor Outstanding = CREDIT Purchases - Vendor Payments Made
```

This matches real-world accounting where:
- CASH/UPI/BANK = Immediate payment
- CREDIT = Pay later (accounts payable)
