from rest_framework.routers import SimpleRouter

from general.api.views import UserViewSet, PostViewSet, CommentViewSet, ReactionViewSet, ChatViewSet, MessageViewSet, FeedbackViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'posts', PostViewSet, basename="posts")
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'reaction', ReactionViewSet, basename='comments')
router.register(r'chats', ChatViewSet, basename='chats')
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'feedbacks', FeedbackViewSet, basename='feedbacks')
urlpatterns = router.urls
