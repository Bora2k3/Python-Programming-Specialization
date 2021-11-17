import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from marshmallow import Schema, ValidationError, fields, post_load
from marshmallow.validate import Length, Range

from .models import Item, Review
from base64 import b64decode
from django.contrib.auth import authenticate


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=Length(1, 64))
    description = fields.Str(required=True, validate=Length(1, 1024))
    price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)

    @post_load
    def make(self, data):
        return Item(**data)


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
    text = fields.Str(required=True, validate=Length(1, 1024))

    @post_load
    def make(self, data):
        return Review(**data)


class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth is None:
            return HttpResponse('', status=401)
        auth_data = b64decode(auth).decode('ascii').split(':')
        login = auth_data[0]
        password = auth_data[1]
        user = authenticate(username=login, password=password)
        if user is None:
            return HttpResponse('', status=401)
        if not user.is_staff:
            return HttpResponse('', status=403)
        try:
            document = json.loads(request.body)
            schema = ItemSchema(strict=True)
            item = schema.load(document).data
            item.save()
        except (json.JSONDecodeError, ValidationError, AssertionError):
            return HttpResponse(status=400)
        data = {'id': item.pk}
        return JsonResponse(data, status=201)


class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            review = schema.load(document).data
            review.item = item
            review.save()
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except (json.JSONDecodeError, ValidationError):
            return HttpResponse(status=400)
        data = {'id': review.pk}
        return JsonResponse(data, status=201)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        schema = ItemSchema()
        data = schema.dump(item).data
        query = Review.objects.filter(item=item).order_by('-id')
        reviews = query[:5]
        schema = ReviewSchema(many=True)
        data['reviews'] = schema.dump(reviews).data
        return JsonResponse(data, status=200)
