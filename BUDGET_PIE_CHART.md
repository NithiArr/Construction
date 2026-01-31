# Budget Breakdown Pie Chart - Project Details

## 🎯 Feature Added

A **Budget Breakdown Pie Chart** has been added to the **Project Details Modal** (View Project page).

---

## 📊 What It Shows

The pie chart visualizes how the **Total Project Budget** is allocated:

### **3 Slices:**

1. **🟢 Paid to Vendors** (Green)
   - Vendor payments already made
   - Cash that has left your account

2. **🟠 Vendor Outstanding** (Orange)  
   - Material purchases made but not yet paid
   - What you still owe vendors

3. **🔵 Remaining Budget** (Blue)
   - Budget not yet spent
   - Available for future expenses

---

## 💡 Example

### **Project: Skyline Tower**
- **Total Budget:** ₹15,00,000

**Breakdown:**
```
Paid to Vendors:      ₹6,00,000  (40%)  🟢
Vendor Outstanding:   ₹4,00,000  (26.7%) 🟠
Remaining Budget:     ₹5,00,000  (33.3%) 🔵
```

**Pie Chart:**
```
      🟢 Paid
     ____40%____
    /           \
🔵  |  BUDGET   | 🟠
33.3% |₹15,00,000| 26.7%
Remaining|        |Outstanding
    \_________/
```

---

## 📐 How It's Calculated

### **1. Paid to Vendors**
```python
paid = total_vendor_payments
```
Sum of all vendor payments made for this project

### **2. Vendor Outstanding**
```python
outstanding = total_material_purchases - total_vendor_payments
```
Materials purchased but not yet paid

### **3. Remaining Budget**
```python
remaining = budget - total_spent
```
Where `total_spent = material_purchases + regular_expenses`

---

## 🎨 Visual Design

### **Chart Features:**
- **Responsive**: Adjusts to modal size
- **Interactive Tooltips**: Hover to see exact amounts and percentages
- **Color-Coded**: Easy to understand at a glance
- **Legend Below Chart**: Clear labels with values

### **Summary Stats Below Chart:**
```
┌─────────────────┬──────────────────────┬─────────────────┐
│ Paid to Vendors │  Vendor Outstanding  │ Remaining Budget│
│   ₹6,00,000     │      ₹4,00,000       │   ₹5,00,000     │
└─────────────────┴──────────────────────┴─────────────────┘
```

---

## 📍 Where to Find It

**Navigation:**
1. Go to **Projects** page
2. Click **"View Details"** on any project
3. See the pie chart after the 3 KPI cards

**Modal Structure:**
```
┌─ Project Details Modal ─────────────────────────┐
│                                                  │
│  [Total Spent] [Total Received] [Vendor Outstanding]
│                                                  │
│  ┌── 💰 Budget Breakdown ──────────────────┐   │
│  │                                          │   │
│  │         [Pie Chart]                      │   │
│  │                                          │   │
│  │  [Paid] [Vendor Outstanding] [Remaining]│   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  Purchase History...                             │
│  Vendor Payments...                              │
│  Expenses...                                     │
└──────────────────────────────────────────────────┘
```

---

## 🚀 Benefits

### **1. Instant Visual Understanding**
- See budget allocation at a glance
- No mental math required

### **2. Financial Health Check**
- Large "Remaining Budget" slice = Good  
- Large "Vendor Outstanding" slice = Pay attention to cash flow

### **3. Payment Planning**
- Know exactly how much you owe vendors
- Plan when to make payments

### **4. Budget Monitoring**
- Track if you're on budget
- Remaining budget shows spending capacity

---

## 🔍 Use Cases

### **Scenario 1: Check Payment Obligations**
**Question:** "How much do I need to pay vendors soon?"

**Look at:** 🟠 Orange slice (Vendor Outstanding)

---

### **Scenario 2: Plan Additional Expenses**
**Question:** "Can I afford to buy more materials?"

**Look at:** 🔵 Blue slice (Remaining Budget)

---

### **Scenario 3: Review Cash Outflow**
**Question:** "How much have I actually paid so far?"

**Look at:** 🟢 Green slice (Paid to Vendors)

---

## 📊 Example Scenarios

### **Healthy Project:**
```
Paid:        40% 🟢
Outstanding: 20% 🟠
Remaining:   40% 🔵
```
✅ Good balance, enough budget left

---

### **High Outstanding:**
```
Paid:        30% 🟢
Outstanding: 50% 🟠  ← Need to pay vendors soon!
Remaining:   20% 🔵
```
⚠️ Large vendor payables - plan cash flow

---

### **Over Budget:**
```
Paid:        60% 🟢
Outstanding: 45% 🟠
Remaining:   -5% 🔵  ← Negative!
```
🔴 Spent more than budget - need more funds

---

## 🎯 Summary

The Budget Breakdown Pie Chart provides a **visual snapshot** of your project's financial status:

- **Where money went** (Paid)
- **Where money will go** (Outstanding)  
- **What's left** (Remaining)

All in one easy-to-understand chart! 📈

**Perfect for:**
- Quick financial reviews
- Stakeholder presentations
- Payment planning
- Budget monitoring
