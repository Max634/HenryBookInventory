from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Sum
from .models import Book, Branch, Inventory

# Home view - Dashboard with statistics
def home(request):
    total_books = Book.objects.count()
    total_branches = Branch.objects.count()
    total_inventory = Inventory.objects.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_items = Inventory.objects.filter(quantity__lt=5).count()
    
    recent_books = Book.objects.order_by('-id')[:5]
    
    context = {
        'total_books': total_books,
        'total_branches': total_branches,
        'total_inventory': total_inventory,
        'low_stock_items': low_stock_items,
        'recent_books': recent_books,
    }
    return render(request, 'core/home.html', context)

# Book views
def book_list(request):
    search_query = request.GET.get('search', '')
    books = Book.objects.all()
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    return render(request, 'core/book_list.html', {
        'books': books,
        'search_query': search_query
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    inventory_items = Inventory.objects.filter(book=book).select_related('branch')
    return render(request, 'core/book_detail.html', {
        'book': book,
        'inventory_items': inventory_items
    })

def book_create(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        url = request.POST.get('url', '')
        price = request.POST.get('price')
        
        if author and title and price:
            book = Book.objects.create(
                author=author,
                title=title,
                description=description,
                url=url,
                price=price
            )
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('core:book_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'core/book_form.html', {'action': 'Create'})

def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.author = request.POST.get('author')
        book.title = request.POST.get('title')
        book.description = request.POST.get('description', '')
        book.url = request.POST.get('url', '')
        book.price = request.POST.get('price')
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('core:book_detail', book_id=book.id)
    
    return render(request, 'core/book_form.html', {
        'book': book,
        'action': 'Edit'
    })

def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('core:book_list')
    
    return render(request, 'core/book_confirm_delete.html', {'book': book})

# Branch views
def branch_list(request):
    search_query = request.GET.get('search', '')
    branches = Branch.objects.all()
    
    if search_query:
        branches = branches.filter(
            Q(BranchName__icontains=search_query) | 
            Q(BranchCity__icontains=search_query) |
            Q(BranchState__icontains=search_query)
        )
    
    return render(request, 'core/branch_list.html', {
        'branches': branches,
        'search_query': search_query
    })

def branch_detail(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    inventory_items = Inventory.objects.filter(branch=branch).select_related('book')
    total_books = inventory_items.aggregate(total=Sum('quantity'))['total'] or 0
    
    return render(request, 'core/branch_detail.html', {
        'branch': branch,
        'inventory_items': inventory_items,
        'total_books': total_books
    })

def branch_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        phone = request.POST.get('phone')
        
        if name and address and city and state:
            branch = Branch.objects.create(
                BranchName=name,
                BranchAddress=address,
                BranchCity=city,
                BranchState=state,
                BranchZip=zip_code,
                BranchPhone=phone
            )
            messages.success(request, f'Branch "{branch.BranchName}" created successfully!')
            return redirect('core:branch_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'core/branch_form.html', {'action': 'Create'})

def branch_edit(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.method == 'POST':
        branch.BranchName = request.POST.get('name')
        branch.BranchAddress = request.POST.get('address')
        branch.BranchCity = request.POST.get('city')
        branch.BranchState = request.POST.get('state')
        branch.BranchZip = request.POST.get('zip')
        branch.BranchPhone = request.POST.get('phone')
        branch.save()
        
        messages.success(request, f'Branch "{branch.BranchName}" updated successfully!')
        return redirect('core:branch_detail', branch_id=branch.id)
    
    return render(request, 'core/branch_form.html', {
        'branch': branch,
        'action': 'Edit'
    })

def branch_delete(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.method == 'POST':
        branch_name = branch.BranchName
        branch.delete()
        messages.success(request, f'Branch "{branch_name}" deleted successfully!')
        return redirect('core:branch_list')
    
    return render(request, 'core/branch_confirm_delete.html', {'branch': branch})

# Inventory views
def inventory_list(request):
    search_query = request.GET.get('search', '')
    inventory_items = Inventory.objects.select_related('book', 'branch').all()
    
    if search_query:
        inventory_items = inventory_items.filter(
            Q(book__title__icontains=search_query) |
            Q(book__author__icontains=search_query) |
            Q(branch__BranchName__icontains=search_query)
        )
    
    return render(request, 'core/inventory_list.html', {
        'inventory_items': inventory_items,
        'search_query': search_query
    })

def inventory_create(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        branch_id = request.POST.get('branch')
        quantity = request.POST.get('quantity')
        
        if book_id and branch_id and quantity:
            book = get_object_or_404(Book, id=book_id)
            branch = get_object_or_404(Branch, id=branch_id)
            
            inventory, created = Inventory.objects.get_or_create(
                book=book,
                branch=branch,
                defaults={'quantity': quantity}
            )
            
            if not created:
                inventory.quantity = int(inventory.quantity) + int(quantity)
                inventory.save()
                messages.success(request, f'Updated quantity for "{book.title}" at {branch.BranchName}')
            else:
                messages.success(request, f'Added "{book.title}" to {branch.BranchName} inventory')
            
            return redirect('core:inventory_list')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    books = Book.objects.all()
    branches = Branch.objects.all()
    
    return render(request, 'core/inventory_form.html', {
        'books': books,
        'branches': branches,
        'action': 'Add'
    })

def inventory_edit(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            inventory.quantity = quantity
            inventory.save()
            messages.success(request, f'Updated inventory for "{inventory.book.title}"')
            return redirect('core:inventory_list')
        else:
            messages.error(request, 'Please enter a valid quantity.')
    
    return render(request, 'core/inventory_edit.html', {
        'inventory': inventory,
        'action': 'Edit'
    })

def inventory_delete(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    
    if request.method == 'POST':
        book_title = inventory.book.title
        branch_name = inventory.branch.BranchName
        inventory.delete()
        messages.success(request, f'Removed "{book_title}" from {branch_name} inventory')
        return redirect('core:inventory_list')
    
    return render(request, 'core/inventory_confirm_delete.html', {'inventory': inventory})

def inventory_by_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    inventory_items = Inventory.objects.filter(branch=branch).select_related('book')
    
    return render(request, 'core/inventory_by_branch.html', {
        'branch': branch,
        'inventory_items': inventory_items
    })
