from django.db import models

class Book(models.Model):
    author = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Branch (models.Model):
    BranchName = models.CharField(max_length=100)
    BranchAddress = models.CharField(max_length=200)
    BranchCity = models.CharField(max_length=100)
    BranchState = models.CharField(max_length=100)
    BranchZip = models.CharField(max_length=20)
    BranchPhone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.BranchName} - {self.BranchCity}, {self.BranchState}"

class Inventory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('book', 'branch')

    def __str__(self):
        return f"{self.book.title} at {self.branch.BranchName} - {self.quantity} copies"