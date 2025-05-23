import paypalrestsdk.payments
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Comic, Cart, Order, Reviews, CustomerDetail
from .serializers import ComicSerializers, CartSerializer, OrderSerializer, ReviewsSerializer, CustomerDetailsSerializers, ComicUserSerializer

from .paypal import paypalrestsdk
# @     ()

@api_view(['GET'])
def getAllComics(request):
    comics = Comic.objects.all()
    serializer = ComicSerializers(comics, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getOneComic(request, pk_id):
    comic = Comic.objects.get(id=pk_id)
    allReviews = Reviews.objects.filter(reviews_on_comic=comic)
    serializer = ComicSerializers(comic)
    reviewSerializer = ReviewsSerializer(allReviews, many=True)
    return Response({'comic': serializer.data, 'reviews': reviewSerializer.data}, status=status.HTTP_200_OK)

# Cart Functionalities
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getCartItems(request):
    cartItems = Cart.objects.all()
    serializer = CartSerializer(cartItems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCartItem(request, itemID):
    try:
        cart_item = Cart.objects.get(id=itemID)
        cart_item.delete()
        return Response({'message': 'Cart item deleted successfully'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateCartItemQuantity(request, itemID):
    try:
        cartItem = Cart.objects.get(id=itemID)
        new_quantity = request.data.get('quantity')
        if new_quantity is None:
            return Response({'error':'Quantity value is missing Can not update quantity sorry'}, status=status.HTTP_400_BAD_REQUEST)
        cartItem.quantity = new_quantity
        cartItem.save()
        return Response({'message':'Quantity Updated successfully'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'error':'Item Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addToCart(request, comicID):
    try:
        comic = Comic.objects.get(pk=comicID)
    except Comic.DoesNotExist:
        return Response({'error':'Comic not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, product=comic)
        return Response({'message':'Item added to cart successfully', 'date':serializer.data}, status=status.HTTP_200_OK)
    return Response({'error':'Invalid data provided can not add item in cart', 'error_details':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
 
# Order Functionalities Start from Here
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getOrderList(request):
    try:
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response({'message':'fetched all orders', 'data':serializer.data}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'Error':'Order Does not found'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteOrderItem(request, ItemID):
    try:
        deleteMe = Order.objects.get(id=ItemID)
        deleteMe.delete()
        return Response({'message':'Order Deleted Successfully'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'Error':'Item Doest not exist'})
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def NewOrder(request, comicID, customerID):
    try:
        comic = Comic.objects.get(pk=comicID)
        customer = CustomerDetail.objects.get(pk=customerID)
    except Comic.DoesNotExist:
        return Response({'error':'Comic NOt Found', 'messaage':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, customer=customer, comic=comic)
        return Response({'message':'Order placed Successfully', 'data':serializer.data}, status=status.HTTP_200_OK)
    return Response({'error':'Unable to place Order Try Again','message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Customer Address Endpoint
def addCustomerAddress(request):
    serializer = CustomerDetailsSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message':'Address Added Successfully', 'data':serializer.data}, status=status.HTTP_200_OK)
    return Response({'error':'Unable To add Address', 'message': serializer.error}, status=status.HTTP_400_BAD_REQUEST)

# Review System start from here
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def PostUserReview(request, comic_id):
    try:
        comic = Comic.objects.get(pk=comic_id)
    except Comic.DoesNotExist:
        return Response({'error':'Comic Does not Exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReviewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, reviews_on_comic=comic)
        return Response({'message':'Review Posted successfully', 'data':serializer.data}, status=status.HTTP_200_OK)
    return Response({'error':'Unable post Review Try again', 'details':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateReview(request, comicID):
    try:
        comic = Comic.objects.get(pk=comicID)
    except Comic.DoesNotExist:
        return Response({'error':'Comic Not Found'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        review = Reviews.objects.get(user=request.user, reviews_on_comic=comic)
    except Reviews.DoesNotExist:
        return Response({'error':'Review not found for this comic by the current user'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ReviewsSerializer(review,data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'Review Update Successfully', 'data':serializer.data}, status=status.HTTP_200_OK)
    return Response({'error':'Invalid Data Provided', 'error_log':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
# PAYPAL PAYMENT SYSTEM
@api_view(['POST'])
def create_payment(resquest):
    payment = paypalrestsdk.Payment({
        "intent":"sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/api/execute_success_payment",
            "cancel_url": "http://localhost:8000/paypal/cancel"
        },
        "transactions":[{
            "amount":{
                "total": "10.00",
                "currency":"USD"
            },
            "description":"Testing Paypal payment integration"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return Response({"redirect_link":link.href}, status=status.HTTP_200_OK)
        return Response({"error":"Redirect url not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"message":"something is going wrong", "error":payment.error}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        return Response({"error": "Missing paymentId or PayerID"}, status=400)
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        return Response({"message": "Payment executed successfully"})
    else:
        return Response(payment.error, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def execute_success_payment(resquest):
    return Response({"message": "payment succedssfull"})

#USER AUTHENTICATION AND AUTHORIZATION
@api_view(['POST'])
def user_singup(request):
    serializer = ComicUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'User registered successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    token = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)
