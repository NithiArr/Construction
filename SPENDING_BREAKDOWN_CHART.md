# Spending Breakdown Pie Chart - Project Details

## 🎯 New Feature Added

A **Spending Breakdown by Category** pie chart has been added to the Project Details Modal, showing exactly where your money was spent across different categories and subcategories.

---

## 📊 What It Shows

This chart visualizes **Total Spent (100%)** broken down by:
- **Material Purchase Subcategories** (Steel, Cement, Bricks, etc.)
- **Regular Expense Categories/Subcategories** (Labor, Equipment, Transportation, etc.)

---

## 💡 Example

### **Project: Skyline Tower**
**Total Spent:** ₹13,00,000 (100%)

**Breakdown:**
```
Steel:           ₹4,50,000  (34.6%)  🔴
Cement:          ₹2,50,000  (19.2%)  🟠
Labor:           ₹2,00,000  (15.4%)  🟢
Bricks:          ₹1,50,000  (11.5%)  🔵
Equipment Rental:₹1,00,000  (7.7%)   🟣
Transportation:  ₹80,000    (6.2%)   🌸
Sand:            ₹70,000    (5.4%)   🐦
```

---

## 🎨 Visual Layout

```
┌─── 📊 Spending Breakdown by Category ─────────────┐
│                                                    │
│  ┌──────────────┐  ┌──────────────────────────┐  │
│  │              │  │  Category Breakdown      │  │
│  │              │  │  ┌────────────────────┐  │  │
│  │   Pie Chart  │  │  │ 🔴 Steel          │  │  │
│  │              │  │  │    ₹4,50,000      │  │  │
│  │ (Interactive)│  │  │    (34.6%)        │  │  │
│  │              │  │  ├────────────────────┤  │  │
│  │              │  │  │ 🟠 Cement         │  │  │
│  │              │  │  │    ₹2,50,000      │  │  │
│  │              │  │  │    (19.2%)        │  │  │
│  │              │  │  ├────────────────────┤  │  │
│  │              │  │  │ 🟢 Labor          │  │  │
│  │              │  │  │    ₹2,00,000      │  │  │
│  │              │  │  │    (15.4%)        │  │  │
│  └──────────────┘  │  └────────────────────┘  │  │
│                    │  (Scrollable legend)      │  │
│                    └──────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

---

## 🔍 How It Works

### **Data Collection:**

1. **Material Purchases** → Grouped by `subcategory`
   ```
   Steel Bars:    ₹3,00,000
   Steel Plates:  ₹1,50,000
   ────────────────────────
   Total Steel:   ₹4,50,000
   ```

2. **Regular Expenses** → Grouped by `subcategory` or `category`
   ```
   Labor - Skilled:    ₹1,20,000
   Labor - Unskilled:  ₹80,000
   ─────────────────────────────
   Total Labor:        ₹2,00,000
   ```

### **Calculation:**
```python
total_spent = material_purchases + regular_expenses = 100%

Each category % = (category_amount / total_spent) × 100
```

---

## 🎯 Key Features

### **1. Dynamic Color Assignment**
- Up to 10 different colors
- Each category gets a unique color
- Cycles if more than 10 categories

### **2. Custom Legend Panel**
- Shows all categories with amounts
- Displays percentage for each
- Color-coded boxes match pie slices
- **Scrollable** if many categories

### **3. Interactive Tooltips**
- Hover over pie slices
- See exact amount and percentage
- Real-time interaction

### **4. Automatic Categorization**
- Uses `subcategory` from materials
- Uses `subcategory` or `category` from expenses
- Falls back to "Materials" or "Other" if missing

---

## 📈 Use Cases

### **Scenario 1: Material Cost Analysis**
**Question:** "Which material is costing us the most?"

**Chart Shows:**
```
Steel:  34.6%  ← Biggest expense!
Cement: 19.2%
Bricks: 11.5%
```
**Action:** Negotiate better rates for steel

---

### **Scenario 2: Labor vs Material Ratio**
**Question:** "Are we spending more on labor or materials?"

**Chart Shows:**
```
Materials: 70% (Steel + Cement + Bricks + Sand)
Labor:     15%
Equipment:  7.7%
Other:      7.3%
```
**Insight:** Material-heavy project

---

### **Scenario 3: Cost Optimization**
**Question:** "Where can we cut costs?"

**Chart Shows:**
```
Equipment Rental: 7.7%  ← Consider purchasing instead?
Transportation:   6.2%  ← Optimize delivery schedules?
```
**Action:** Identify optimization opportunities

---

## 🎨 Chart Characteristics

### **Colors (10 Palette):**
1. 🔴 Red
2. 🟠 Orange
3. 🟢 Green
4. 🔵 Blue
5. 🟣 Purple
6. 🌸 Pink
7. 🐦 Teal
8. 🟧 Amber
9. 🟩 Lime
10. 🟪 Violet

### **Legend Features:**
- Color box indicator
- Category name (bold)
- Amount in ₹ with percentage
- Card-style background
- Responsive layout

---

## 📍 Where to Find It

**Navigation:**
1. Go to **Projects** page
2. Click **"View Details"** on any project
3. Scroll down to **"📊 Spending Breakdown by Category"**
4. Located after the Budget Breakdown chart

---

## 💰 Example Breakdown

### **Project: Green Valley Apartments**
**Total Spent: ₹45,00,000**

| Category | Amount | % | Color |
|----------|--------|---|-------|
| Steel | ₹12,00,000 | 26.7% | 🔴 Red |
| Cement | ₹8,00,000 | 17.8% | 🟠 Orange |
| Labor - Skilled | ₹7,00,000 | 15.6% | 🟢 Green |
| Bricks | ₹5,00,000 | 11.1% | 🔵 Blue |
| Labor - Unskilled | ₹4,00,000 | 8.9% | 🟣 Purple |
| Equipment | ₹3,50,000 | 7.8% | 🌸 Pink |
| Sand | ₹2,50,000 | 5.6% | 🐦 Teal |
| Transportation | ₹2,00,000 | 4.4% | 🟧 Amber |
| Electrical | ₹1,00,000 | 2.2% | 🟩 Lime |

---

## 🔧 Technical Details

### **Data Sources:**
- **Purchase History:** Material purchases with subcategories
- **Expenses:** Regular expenses with categories/subcategories

### **API Field Used:**
```javascript
purchase_history[].subcategory  // Material categories
expenses[].subcategory          // Expense subcategories
expenses[].category             // Fallback if no subcategory
```

### **Chart Type:**
- Chart.js Pie Chart
- No default legend (custom HTML legend)
- Responsive and interactive

---

## 📊 Benefits

### **1. Know Where Money Goes**
See exact breakdown of spending by category

### **2. Identify Top Expenses**
Largest slices = biggest costs

### **3. Compare Categories**
Materials vs Labor vs Equipment at a glance

### **4. Track Spending Patterns**
Understand project cost structure

### **5. Make Informed Decisions**
Data-driven cost optimization

---

## 🎯 Summary

The **Spending Breakdown Chart** provides a clear visual answer to:

**"Where did all my project money go?"**

Instead of scrolling through transaction tables, you get an **instant visual breakdown** of:
- Which materials cost the most
- Labor expenses
- Equipment and other costs
- Exact percentages and amounts

**Perfect for:**
- Quick financial reviews
- Cost analysis
- Budget planning for future projects
- Stakeholder presentations

---

## 🚀 Next Steps

### **Optional Enhancements:**
1. **Drill-down:** Click category to see individual transactions
2. **Comparison:** Compare spending across multiple projects
3. **Export:** Download chart as image
4. **Filters:** Toggle categories on/off to focus on specific areas

---

**The chart updates automatically as you add new purchases and expenses!** 📈
