from django.contrib import admin
from .models import Product_Details, Comment,Message,Cart


class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'available', 'quantity', 'item_type', 'created_at')  # Fields shown in list view
    list_filter = ('available', 'item_type', 'created_at')  # Filters in sidebar
    search_fields = ('product_name', 'details')  # Searchable fields
    readonly_fields = ('created_at',)  # Make created_at read-only
    list_editable = ('price', 'available', 'quantity')  # Allow editing in list view
    ordering = ('-created_at',)  # Sort by newest first
    fieldsets = (
        ("Basic Information", {'fields': ('product_name', 'details')}),
        ("Pricing & Availability", {'fields': ('price', 'available', 'quantity', 'item_type')}),
        ("Metadata", {'fields': ('created_at',)}),
    )

admin.site.register(Product_Details, ProductDetailsAdmin)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'item_type', 'short_message', 'comm_date')  # Display key fields in list view
    list_filter = ('comm_date', 'item_type')  # Filters on sidebar
    search_fields = ('username__username', 'item_type__product_name', 'message')  # Searchable fields
    ordering = ('-comm_date',)  # Newest comments first
    readonly_fields = ('comm_date',)  # Make comment date read-only
    fieldsets = (
        ("User & Product", {'fields': ('username', 'item_type')}),
        ("Comment Details", {'fields': ('message', 'comm_date')}),
    )

    def short_message(self, obj):
        """Show a short preview of the message in the list view."""
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message Preview"

admin.site.register(Comment, CommentAdmin)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'short_message', 'message_date')  # Display key fields in list view
    list_filter = ('message_date',)  # Filters messages by date
    search_fields = ('user_name__username', 'email', 'message')  # Search by username, email, or message
    ordering = ('-message_date',)  # Newest messages appear first
    readonly_fields = ('message_date',)  # Make the message date read-only
    fieldsets = (
        ("User Information", {'fields': ('user_name', 'email')}),
        ("Message Details", {'fields': ('message', 'message_date')}),
    )

    def short_message(self, obj):
        """Show a short preview of the message in the list view."""
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message Preview"

admin.site.register(Message, MessageAdmin)



class CartAdmin(admin.ModelAdmin):
    list_display = ('username', 'product', 'quantity', 'ordered_date', 'reach_date')  
    list_filter = ('ordered_date', 'reach_date')  
    search_fields = ('username__username', 'product__product_name')  
    ordering = ('-ordered_date',)

admin.site.register(Cart, CartAdmin)