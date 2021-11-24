def get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
       request.session.create()
       cart_id = request.session.session_key
    return cart_id
