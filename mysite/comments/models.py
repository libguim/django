from django.db import models
from django.contrib.auth.models import User

from posts.models import Posts

# 댓글 모델
class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name="게시글",
                             related_name="post_comments")
    content = models.TextField(verbose_name="내용")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자",
                                   null=True, blank=True, related_name="comments_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="수정자",
                                   null=True, blank=True, related_name="comments_updated_by")
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        db_table = 'comments'
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"

    def __str__(self):
        return self.content