from datetime import timezone

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from api.models import Book, BorrowRecord
from rest_framework import generics, viewsets, status
from api.serializers import UserSerializer, BookSerializer, BorrowRecordSerializer, ReturnActionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'genre']

    def get_queryset(self):
        queryset = Book.objects.all()
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        return queryset


class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        book_id = request.data.get("book_id")

        try:
            # Fetch the book
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already borrowed this book and hasn't returned it yet
        if BorrowRecord.objects.filter(user=user, book=book, status="BORROWED").exists():
            return Response({"detail": "You have already borrowed this book and not returned it yet."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if there are available copies of the book
        if book.available_copies <= 0:
            return Response({"detail": "No available copies."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a borrow record and decrease available copies by 1
        borrow_record = BorrowRecord.objects.create(user=user, book=book)
        book.available_copies -= 1
        book.save()

        return Response({"detail": "Book borrowed successfully."}, status=status.HTTP_201_CREATED)

class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReturnActionSerializer(data=request.data)
        if serializer.is_valid():
            borrow_id = serializer.validated_data['borrow_id']
            record = BorrowRecord.objects.get(id=borrow_id)

            record.return_date = timezone.now()
            record.status = 'RETURNED'
            record.book.available_copies += 1
            record.book.save()
            record.save()

            return Response({"detail": "Book returned successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBorrowedBooksView(generics.ListAPIView):
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRecord.objects.filter(user=self.request.user, status='BORROWED')