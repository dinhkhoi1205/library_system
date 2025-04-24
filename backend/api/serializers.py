from django.contrib.auth.models import User
from rest_framework import serializers, request
from .models import Book, BorrowRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'published_date',
            'quantity',
            'available_copies',
            'is_available',
            'description',
            'cover_image'
        ]
        extra_kwargs = {
            'available_copies': {'read_only': True},  # Updated via borrow/return logic
            'cover_image': {'required': False}  # Optional field
        }

    def validate_quantity(self, value):
        """Ensure quantity is >= available_copies"""
        if value < self.instance.available_copies if self.instance else 0:
            raise serializers.ValidationError("Quantity cannot be less than available copies.")
        return value

    def get_is_available(self, obj):
        return obj.available_copies > 0


class BorrowRecordSerializer(serializers.ModelSerializer):
    # Include book details (nested representation)
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = [
            'id',
            'user',
            'book',
            'book_id',
            'borrow_date',
            'due_date',
            'return_date',
            'status',
        ]
        read_only_fields = [
            'borrow_date',
            'status',
            'due_date',
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        book_id = validated_data.pop("book_id")

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

        if book.available_copies <= 0:
            raise serializers.ValidationError("No copies available for borrowing.")

        book.available_copies -= 1
        book.save()

        return BorrowRecord.objects.create(
            user=user,
            book=book,
            **validated_data
        )


class BorrowRequestSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(pk=value)
            if book.available_copies <= 0:
                raise serializers.ValidationError("Book is not available.")
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book does not exist.")
        return value


class ReturnActionSerializer(serializers.Serializer):
    borrow_id = serializers.IntegerField()

    def validate_borrow_id(self, value):
        try:
            record = BorrowRecord.objects.get(pk=value)
            if record.status == 'RETURNED':
                raise serializers.ValidationError("This book was already returned")
        except BorrowRecord.DoesNotExist:
            raise serializers.ValidationError("Borrow record not found")
        return value
