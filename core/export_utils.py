"""
Excel export utilities for project data
"""
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from core.models import Project
from finance.models import Expense, Payment, ClientPayment, ExpenseItem
from django.db.models import Sum


def apply_header_style(cell):
    """Apply consistent header styling"""
    cell.font = Font(bold=True, color="FFFFFF", size=11)
    cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )


def apply_currency_format(ws, col_letter, start_row, end_row):
    """Apply currency format to a column"""
    for row in range(start_row, end_row + 1):
        cell = ws[f'{col_letter}{row}']
        cell.number_format = '₹#,##0.00'


def auto_adjust_column_width(ws):
    """Auto-adjust column widths based on content"""
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width


@login_required
def export_project_to_excel(request, project_id):
    """Export complete project data to Excel with multiple sheets"""
    try:
        project = Project.objects.get(project_id=project_id, company=request.user.company)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    
    # Create workbook
    wb = Workbook()
    wb.remove(wb.active)  # Remove default sheet
    
    # Get all data
    expenses = Expense.objects.filter(project=project)
    payments = Payment.objects.filter(project=project)
    client_payments = ClientPayment.objects.filter(project=project)
    
    # Calculate KPIs
    material_purchases = expenses.filter(expense_type='Material Purchase')
    regular_expenses = expenses.filter(expense_type='Regular Expense')
    
    total_material = material_purchases.aggregate(Sum('amount'))['amount__sum'] or 0
    total_regular = regular_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_spent = float(total_material) + float(total_regular)
    
    total_vendor_payments = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    outstanding_payables = float(total_material) - float(total_vendor_payments)
    
    total_client_payments = client_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    budget_utilized_pct = (total_spent / float(project.budget) * 100) if project.budget > 0 else 0
    
    # ============================================
    # SHEET 1: Project Summary & KPIs
    # ============================================
    ws_summary = wb.create_sheet("Project Summary")
    
    # Project header
    ws_summary['A1'] = f"PROJECT FINANCIAL REPORT"
    ws_summary['A1'].font = Font(bold=True, size=16, color="1F4E78")
    ws_summary.merge_cells('A1:D1')
    
    ws_summary['A2'] = f"Project: {project.name}"
    ws_summary['A2'].font = Font(bold=True, size=14)
    ws_summary.merge_cells('A2:D2')
    
    ws_summary['A3'] = f"Export Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    ws_summary['A3'].font = Font(italic=True)
    ws_summary.merge_cells('A3:D3')
    
    # KPIs section
    row = 5
    ws_summary[f'A{row}'] = "FINANCIAL OVERVIEW"
    ws_summary[f'A{row}'].font = Font(bold=True, size=12, color="FFFFFF")
    ws_summary[f'A{row}'].fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
    ws_summary.merge_cells(f'A{row}:D{row}')
    
    row += 1
    kpis = [
        ["Total Budget", f"₹{float(project.budget):,.2f}"],
        ["Total Spent", f"₹{total_spent:,.2f}"],
        ["Budget Utilized", f"{budget_utilized_pct:.1f}%"],
        ["Amount Remaining", f"₹{(float(project.budget) - total_spent):,.2f}"],
        ["", ""],
        ["Material Purchases", f"₹{float(total_material):,.2f}"],
        ["Regular Expenses", f"₹{float(total_regular):,.2f}"],
        ["Vendor Payments Made", f"₹{float(total_vendor_payments):,.2f}"],
        ["Outstanding Payables", f"₹{outstanding_payables:,.2f}"],
        ["", ""],
        ["Client Payments Received", f"₹{float(total_client_payments):,.2f}"],
    ]
    
    for kpi_name, kpi_value in kpis:
        ws_summary[f'A{row}'] = kpi_name
        ws_summary[f'B{row}'] = kpi_value
        if kpi_name:
            ws_summary[f'A{row}'].font = Font(bold=True)
        row += 1
    
    auto_adjust_column_width(ws_summary)
    
    # ============================================
    # SHEET 2: Purchase History (with items)
    # ============================================
    ws_purchases = wb.create_sheet("Purchase History")
    
    headers = ['Date', 'Vendor', 'Invoice No.', 'Category', 'Item Name', 'Quantity', 'Unit', 'Unit Price', 'Total Price', 'Payment Mode']
    for col, header in enumerate(headers, 1):
        cell = ws_purchases.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    row = 2
    for expense in material_purchases:
        items = ExpenseItem.objects.filter(expense=expense)
        if items.exists():
            for item in items:
                ws_purchases[f'A{row}'] = expense.expense_date.strftime('%d/%m/%Y')
                ws_purchases[f'B{row}'] = expense.vendor.name if expense.vendor else 'N/A'
                ws_purchases[f'C{row}'] = expense.invoice_number or '-'
                ws_purchases[f'D{row}'] = expense.category or 'N/A'
                ws_purchases[f'E{row}'] = item.item_name
                ws_purchases[f'F{row}'] = float(item.quantity)
                ws_purchases[f'G{row}'] = item.measuring_unit
                ws_purchases[f'H{row}'] = float(item.unit_price)
                ws_purchases[f'I{row}'] = float(item.total_price)
                ws_purchases[f'J{row}'] = expense.payment_mode
                row += 1
        else:
            # Purchase without items
            ws_purchases[f'A{row}'] = expense.expense_date.strftime('%d/%m/%Y')
            ws_purchases[f'B{row}'] = expense.vendor.name if expense.vendor else 'N/A'
            ws_purchases[f'C{row}'] = expense.invoice_number or '-'
            ws_purchases[f'D{row}'] = expense.category or 'N/A'
            ws_purchases[f'E{row}'] = '-'
            ws_purchases[f'F{row}'] = '-'
            ws_purchases[f'G{row}'] = '-'
            ws_purchases[f'H{row}'] = '-'
            ws_purchases[f'I{row}'] = float(expense.amount)
            ws_purchases[f'J{row}'] = expense.payment_mode
            row += 1
    
    # Apply currency formatting
    if row > 2:
        apply_currency_format(ws_purchases, 'H', 2, row - 1)
        apply_currency_format(ws_purchases, 'I', 2, row - 1)
    
    # Add totals row
    if row > 2:
        ws_purchases[f'H{row}'] = "TOTAL:"
        ws_purchases[f'H{row}'].font = Font(bold=True)
        ws_purchases[f'I{row}'] = f"=SUM(I2:I{row-1})"
        ws_purchases[f'I{row}'].font = Font(bold=True)
        ws_purchases[f'I{row}'].number_format = '₹#,##0.00'
    
    ws_purchases.auto_filter.ref = f"A1:J{row}"
    auto_adjust_column_width(ws_purchases)
    
    # ============================================
    # SHEET 3: Regular Expenses
    # ============================================
    ws_expenses = wb.create_sheet("Regular Expenses")
    
    headers = ['Date', 'Category', 'Description', 'Amount', 'Payment Mode']
    for col, header in enumerate(headers, 1):
        cell = ws_expenses.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    row = 2
    for expense in regular_expenses:
        ws_expenses[f'A{row}'] = expense.expense_date.strftime('%d/%m/%Y')
        ws_expenses[f'B{row}'] = expense.category or 'N/A'
        ws_expenses[f'C{row}'] = expense.description or '-'
        ws_expenses[f'D{row}'] = float(expense.amount)
        ws_expenses[f'E{row}'] = expense.payment_mode
        row += 1
    
    if row > 2:
        apply_currency_format(ws_expenses, 'D', 2, row - 1)
        # Add totals row
        ws_expenses[f'C{row}'] = "TOTAL:"
        ws_expenses[f'C{row}'].font = Font(bold=True)
        ws_expenses[f'D{row}'] = f"=SUM(D2:D{row-1})"
        ws_expenses[f'D{row}'].font = Font(bold=True)
        ws_expenses[f'D{row}'].number_format = '₹#,##0.00'
    
    ws_expenses.auto_filter.ref = f"A1:E{row}"
    auto_adjust_column_width(ws_expenses)
    
    # ============================================
    # SHEET 4: Vendor Payments
    # ============================================
    ws_payments = wb.create_sheet("Vendor Payments")
    
    headers = ['Date', 'Vendor', 'Amount', 'Payment Mode', 'Invoice Reference']
    for col, header in enumerate(headers, 1):
        cell = ws_payments.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    row = 2
    for payment in payments:
        ws_payments[f'A{row}'] = payment.payment_date.strftime('%d/%m/%Y')
        ws_payments[f'B{row}'] = payment.vendor.name if payment.vendor else 'N/A'
        ws_payments[f'C{row}'] = float(payment.amount)
        ws_payments[f'D{row}'] = payment.payment_mode
        ws_payments[f'E{row}'] = payment.expense.invoice_number if payment.expense else '-'
        row += 1
    
    if row > 2:
        apply_currency_format(ws_payments, 'C', 2, row - 1)
        # Add totals row
        ws_payments[f'B{row}'] = "TOTAL:"
        ws_payments[f'B{row}'].font = Font(bold=True)
        ws_payments[f'C{row}'] = f"=SUM(C2:C{row-1})"
        ws_payments[f'C{row}'].font = Font(bold=True)
        ws_payments[f'C{row}'].number_format = '₹#,##0.00'
    
    ws_payments.auto_filter.ref = f"A1:E{row}"
    auto_adjust_column_width(ws_payments)
    
    # ============================================
    # SHEET 5: Client Payments
    # ============================================
    ws_client = wb.create_sheet("Client Payments")
    
    headers = ['Date', 'Amount', 'Payment Mode', 'Reference Number', 'Remarks']
    for col, header in enumerate(headers, 1):
        cell = ws_client.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    row = 2
    for cp in client_payments:
        ws_client[f'A{row}'] = cp.payment_date.strftime('%d/%m/%Y')
        ws_client[f'B{row}'] = float(cp.amount)
        ws_client[f'C{row}'] = cp.payment_mode
        ws_client[f'D{row}'] = cp.reference_number or '-'
        ws_client[f'E{row}'] = cp.remarks or '-'
        row += 1
    
    if row > 2:
        apply_currency_format(ws_client, 'B', 2, row - 1)
        # Add totals row
        ws_client[f'A{row}'] = "TOTAL:"
        ws_client[f'A{row}'].font = Font(bold=True)
        ws_client[f'B{row}'] = f"=SUM(B2:B{row-1})"
        ws_client[f'B{row}'].font = Font(bold=True)
        ws_client[f'B{row}'].number_format = '₹#,##0.00'
    
    ws_client.auto_filter.ref = f"A1:E{row}"
    auto_adjust_column_width(ws_client)
    
    # ============================================
    # Generate response
    # ============================================
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"{project.name.replace(' ', '_')}_Export_{datetime.now().strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb.save(response)
    return response


@login_required
def export_expenses_to_excel(request):
    """Export regular expenses to Excel with optional filtering"""
    
    # Get filter parameters
    project_id = request.GET.get('project')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    category = request.GET.get('category')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Regular Expenses"
    
    # Header
    headers = ['Date', 'Project', 'Category', 'Amount', 'Payment Mode', 'Description']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    # Base query
    expenses = Expense.objects.filter(
        company=request.user.company,
        expense_type='Regular Expense'
    ).select_related('project')
    
    # Apply filters & build filename parts
    filename_parts = ["Expenses"]
    
    if project_id:
        expenses = expenses.filter(project_id=project_id)
        try:
            p_name = Project.objects.get(project_id=project_id).name
            filename_parts.append(p_name.replace(' ', '_'))
        except Project.DoesNotExist:
            pass
            
    if category:
        expenses = expenses.filter(category=category)
        filename_parts.append(category.replace(' ', '_'))
        
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            expenses = expenses.filter(expense_date__gte=date_from)
            filename_parts.append(f"from_{date_from_str}")
        except ValueError:
            pass
            
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            expenses = expenses.filter(expense_date__lte=date_to)
            filename_parts.append(f"to_{date_to_str}")
        except ValueError:
            pass
            
    expenses = expenses.order_by('-expense_date')
    
    # Add data rows
    row = 2
    for expense in expenses:
        ws[f'A{row}'] = expense.expense_date.strftime('%d/%m/%Y')
        ws[f'B{row}'] = expense.project.name if expense.project else 'N/A'
        ws[f'C{row}'] = expense.category or 'N/A'
        ws[f'D{row}'] = float(expense.amount)
        ws[f'E{row}'] = expense.payment_mode
        ws[f'F{row}'] = expense.description or '-'
        row += 1
    
    # Apply formatting
    if row > 2:
        apply_currency_format(ws, 'D', 2, row - 1)
        # Add totals row
        ws[f'C{row}'] = "TOTAL:"
        ws[f'C{row}'].font = Font(bold=True)
        ws[f'D{row}'] = f"=SUM(D2:D{row-1})"
        ws[f'D{row}'].font = Font(bold=True)
        ws[f'D{row}'].number_format = '₹#,##0.00'
    
    ws.auto_filter.ref = f"A1:F{row}"
    auto_adjust_column_width(ws)
    
    # Generate response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    # Construct filename
    filename_str = "_".join(filename_parts) + f"_Export_{datetime.now().strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename_str}"'
    
    wb.save(response)
    return response


@login_required
def export_purchases_to_excel(request):
    """Export material purchases with optional filtering"""
    
    # Get filter parameters
    project_id = request.GET.get('project')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    vendor_id = request.GET.get('vendor')
    category = request.GET.get('category')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Material Purchases"
    
    # Header
    headers = ['Date', 'Project', 'Vendor', 'Invoice No.', 'Category', 'Item Name', 'Quantity', 'Unit', 'Unit Price', 'Total Price', 'Payment Mode']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    # Base query
    purchases = Expense.objects.filter(
        company=request.user.company,
        expense_type='Material Purchase'
    ).select_related('project', 'vendor')
    
    # Apply filters & build filename parts
    filename_parts = ["Purchases"]
    
    if project_id:
        purchases = purchases.filter(project_id=project_id)
        try:
            p_name = Project.objects.get(project_id=project_id).name
            filename_parts.append(p_name.replace(' ', '_'))
        except Project.DoesNotExist:
            pass

    if vendor_id:
        purchases = purchases.filter(vendor_id=vendor_id)
        try:
            # Assuming vendor is imported, if not use string filter
            pass # Keep filename simple for now
        except:
             pass

    if category:
        purchases = purchases.filter(category=category)
        filename_parts.append(category.replace(' ', '_'))
        
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            purchases = purchases.filter(expense_date__gte=date_from)
            filename_parts.append(f"from_{date_from_str}")
        except ValueError:
            pass
            
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            purchases = purchases.filter(expense_date__lte=date_to)
            filename_parts.append(f"to_{date_to_str}")
        except ValueError:
            pass
            
    purchases = purchases.order_by('-expense_date')
    
    # Add data rows
    row = 2
    for purchase in purchases:
        items = ExpenseItem.objects.filter(expense=purchase)
        if items.exists():
            for item in items:
                ws[f'A{row}'] = purchase.expense_date.strftime('%d/%m/%Y')
                ws[f'B{row}'] = purchase.project.name if purchase.project else 'N/A'
                ws[f'C{row}'] = purchase.vendor.name if purchase.vendor else 'N/A'
                ws[f'D{row}'] = purchase.invoice_number or '-'
                ws[f'E{row}'] = purchase.category or 'N/A'
                ws[f'F{row}'] = item.item_name
                ws[f'G{row}'] = float(item.quantity)
                ws[f'H{row}'] = item.measuring_unit
                ws[f'I{row}'] = float(item.unit_price)
                ws[f'J{row}'] = float(item.total_price)
                ws[f'K{row}'] = purchase.payment_mode
                row += 1
        else:
            # Purchase without items
            ws[f'A{row}'] = purchase.expense_date.strftime('%d/%m/%Y')
            ws[f'B{row}'] = purchase.project.name if purchase.project else 'N/A'
            ws[f'C{row}'] = purchase.vendor.name if purchase.vendor else 'N/A'
            ws[f'D{row}'] = purchase.invoice_number or '-'
            ws[f'E{row}'] = purchase.category or 'N/A'
            ws[f'F{row}'] = '-'
            ws[f'G{row}'] = '-'
            ws[f'H{row}'] = '-'
            ws[f'I{row}'] = '-'
            ws[f'J{row}'] = float(purchase.amount)
            ws[f'K{row}'] = purchase.payment_mode
            row += 1
    
    # Apply formatting
    if row > 2:
        apply_currency_format(ws, 'I', 2, row - 1)
        apply_currency_format(ws, 'J', 2, row - 1)
        # Add totals row
        ws[f'I{row}'] = "TOTAL:"
        ws[f'I{row}'].font = Font(bold=True)
        ws[f'J{row}'] = f"=SUM(J2:J{row-1})"
        ws[f'J{row}'].font = Font(bold=True)
        ws[f'J{row}'].number_format = '₹#,##0.00'
    
    ws.auto_filter.ref = f"A1:K{row}"
    auto_adjust_column_width(ws)
    
    # Generate response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    filename_str = "_".join(filename_parts) + f"_Export_{datetime.now().strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename_str}"'
    
    wb.save(response)
    return response


@login_required
def export_vendor_payments_to_excel(request):
    """Export vendor payments to Excel with filtering"""
    
    # Get filter parameters
    project_id = request.GET.get('project')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    vendor_id = request.GET.get('vendor')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Vendor Payments"
    
    # Header
    headers = ['Date', 'Project', 'Vendor', 'Amount', 'Payment Mode', 'Remarks', 'Invoice Reference']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    # Base query
    payments = Payment.objects.filter(
        company=request.user.company
    ).select_related('project', 'vendor', 'expense')
    
    # Apply filters & build filename parts
    filename_parts = ["Vendor_Payments"]
    
    if project_id:
        payments = payments.filter(project_id=project_id)
        try:
            p_name = Project.objects.get(project_id=project_id).name
            filename_parts.append(p_name.replace(' ', '_'))
        except Project.DoesNotExist:
            pass
            
    if vendor_id:
        payments = payments.filter(vendor_id=vendor_id)
        
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            payments = payments.filter(payment_date__gte=date_from)
            filename_parts.append(f"from_{date_from_str}")
        except ValueError:
            pass
            
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            payments = payments.filter(payment_date__lte=date_to)
            filename_parts.append(f"to_{date_to_str}")
        except ValueError:
            pass
            
    payments = payments.order_by('-payment_date')
    
    # Add data rows
    row = 2
    for payment in payments:
        ws[f'A{row}'] = payment.payment_date.strftime('%d/%m/%Y')
        ws[f'B{row}'] = payment.project.name if payment.project else 'N/A'
        ws[f'C{row}'] = payment.vendor.name if payment.vendor else 'N/A'
        ws[f'D{row}'] = float(payment.amount)
        ws[f'E{row}'] = payment.payment_mode
        ws[f'F{row}'] = payment.remarks or '-'
        ws[f'G{row}'] = payment.expense.invoice_number if payment.expense else '-'
        row += 1
    
    # Apply formatting
    if row > 2:
        apply_currency_format(ws, 'D', 2, row - 1)
        # Add totals row
        ws[f'C{row}'] = "TOTAL:"
        ws[f'C{row}'].font = Font(bold=True)
        ws[f'D{row}'] = f"=SUM(D2:D{row-1})"
        ws[f'D{row}'].font = Font(bold=True)
        ws[f'D{row}'].number_format = '₹#,##0.00'
    
    ws.auto_filter.ref = f"A1:G{row}"
    auto_adjust_column_width(ws)
    
    # Generate response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    filename_str = "_".join(filename_parts) + f"_Export_{datetime.now().strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename_str}"'
    
    wb.save(response)
    return response


@login_required
def export_client_payments_to_excel(request):
    """Export client payments to Excel with filtering"""
    
    # Get filter parameters
    project_id = request.GET.get('project')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Client Payments"
    
    # Header
    headers = ['Date', 'Project', 'Amount', 'Payment Mode', 'Reference Number', 'Remarks']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        apply_header_style(cell)
    
    # Base query
    payments = ClientPayment.objects.filter(
        company=request.user.company
    ).select_related('project')
    
    # Apply filters & build filename parts
    filename_parts = ["Client_Payments"]
    
    if project_id:
        payments = payments.filter(project_id=project_id)
        try:
            p_name = Project.objects.get(project_id=project_id).name
            filename_parts.append(p_name.replace(' ', '_'))
        except Project.DoesNotExist:
            pass
            
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            payments = payments.filter(payment_date__gte=date_from)
            filename_parts.append(f"from_{date_from_str}")
        except ValueError:
            pass
            
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            payments = payments.filter(payment_date__lte=date_to)
            filename_parts.append(f"to_{date_to_str}")
        except ValueError:
            pass
            
    payments = payments.order_by('-payment_date')
    
    # Add data rows
    row = 2
    for payment in payments:
        ws[f'A{row}'] = payment.payment_date.strftime('%d/%m/%Y')
        ws[f'B{row}'] = payment.project.name if payment.project else 'N/A'
        ws[f'C{row}'] = float(payment.amount)
        ws[f'D{row}'] = payment.payment_mode
        ws[f'E{row}'] = payment.reference_number or '-'
        ws[f'F{row}'] = payment.remarks or '-'
        row += 1
    
    # Apply formatting
    if row > 2:
        apply_currency_format(ws, 'C', 2, row - 1)
        # Add totals row
        ws[f'B{row}'] = "TOTAL:"
        ws[f'B{row}'].font = Font(bold=True)
        ws[f'C{row}'] = f"=SUM(C2:C{row-1})"
        ws[f'C{row}'].font = Font(bold=True)
        ws[f'C{row}'].number_format = '₹#,##0.00'
    
    ws.auto_filter.ref = f"A1:F{row}"
    auto_adjust_column_width(ws)
    
    # Generate response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    filename_str = "_".join(filename_parts) + f"_Export_{datetime.now().strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename_str}"'
    
    wb.save(response)
    return response
