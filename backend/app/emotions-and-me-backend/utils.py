from core.serializers import ProfileSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': ProfileSerializer(user, context={'request': request}).data
    }
