from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField("포스트 제목", max_length=100) # verbose_name="포스트 제목"은 admin 페이지에서 데이터 등록시 좌측에 설명란으로 표시된다.
    content = models.TextField("포스트 내용")
    
    def __str__(self):
        return self.title

class Comment(models.Model): # N방향의 모델 (Comment)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True) # 1방향의 모델 (Post)
    content = models.TextField("댓글 내용")
    
    def __str__(self):
        # return F'{self.post.title}의 댓글 (ID : {self.id})'
        return (
            F'{self.post.title}의 댓글 (ID : {self.id})' if self.post is not None else F'부모 게시글이 없는 떠돌이 댓글입니다. (ID : {self.id})'
        )


'''
🔴 Related objects (add, create, remove, clear, set) 메서드에 대한 예제
# ===========================================================================================================================
# 새 댓글 추가
# add(*objs, bulk=True, through_defaluts=None)
# - bulk=False를 사용하여 저장되지 않은 객체를 인수로 전달할 수 있습니다.
# ===========================================================================================================================

# 방법1
first_post = Post.objects.all()[0]
new_comment1 = Comment.objects.create(content = "새 댓글1", post = first_post)
new_comment2 = Comment.objects.create(content = "새 댓글2", post = first_post)
new_comment3 = Comment.objects.create(content = "새 댓글3", post = first_post)
new_comment4 = Comment.objects.create(content = "새 댓글4", post = first_post)

# 방법2
new_comment5 = Comment(content = '새 댓글5', post = first_post)
new_comment5.save()

Comment(content = '댓글1', post = None).save() # ForeignKey(..., null = True) 일때 None으로 지정 가능
Comment(content = '댓글2', post = None).save()
Comment(content = '댓글3', post = None).save()
Comment(content = '댓글4', post = None).save()

# 방법3 (이미 등록된 댓글을 FK로 연결)
first_post.comment_set.add(Comment.objects.get(id = 1))
Post.objects.get(id = 1).comment_set.add(Comment.objects.get(id = 2))

# 방법4 (아직 저장되지 않은 새 댓글을 INSERT 하고 FK로 연결 -> None 이어도 id=1인 Post와 연결된다.)
Post.objects.get(id = 1).comment_set.add(
    Comment(content = 'NEW 댓글1', post = None),
    Comment(content = 'NEW 댓글2', post = None),
    Comment(content = 'NEW 댓글3', post = None),
    bulk=False
)

first_post.comment_set.count() # 댓글 추가 후 개수 확인
first_post.comment_set.values() # QuerySet 으로 확인

# ===========================================================================================================================
# 댓글 삭제
# remove(*objs, bulk=True)
# clear(bulk=True)
# ✅ ForeignKey를 NULL로 업데이트 합니다. 그래서 ForeignKey(null = True)인 경우에만 사용할 수 있습니다.
# 연관 필드를 None(NULL)로 설정할 수 없는 경우 객체를 다른 객체에 add하지 않고는 관계에서 제거할 수 없습니다.
# ✅ clear() 모든 하위 항목의 ForeignKey를 NULL로 업데이트합니다. remove()와 마찬가지로 ForeignKey(null = True)인 경우에만 사용할 수 있습니다.
# ===========================================================================================================================

# 방법1 (진짜 DELETE 쿼리)
first_post.comment_set.get(id = 7).delete()

# 방법2 (DELETE 쿼리가 아닌 FK를 NULL로 바꿔서 관계를 끊음)
Post.objects.get(id = 1).comment_set.remove(Comment.objects.get(id = 1))

# 방법3 (인수로 전달된 댓글들의 FK를 NULL로 설정)
Post.objects.get(id = 1).comment_set.remove(
    Comment(id = 5, content = 'NEW 댓글1', post = Post.objects.get(id = 1)),
    Comment(id = 6, content = 'NEW 댓글2', post = Post.objects.get(id = 1)),
    Comment(id = 7, content = 'NEW 댓글3', post = Post.objects.get(id = 1)),
    bulk=False
)

# 방법1
Post.objects.get(id = 1).comment_set.clear()
# 방법2
Post(id = 1).comment_set.clear(bulk=False)

# ===========================================================================================================================
# 댓글 갱신
# set(objs, bulk=True, clear=False, through_defaults=None)
# clear=True를 지정하면 인수로 넘겨준 데이터 외 나머지는 ForeignKey를 NULL로 설정하여 연결을 해제합니다.
# ===========================================================================================================================

# 방법1 (지정한 댓글들의 content가 수정되고, FK도 다시 Post(id = 1)와 연결된다)
Post.objects.get(id = 1).comment_set.set([
    Comment(id = 1, content = '홀수댓글', post = None),
    Comment(id = 3, content = '홀수댓글', post = None),
    Comment(id = 5, content = '홀수댓글', post = None),
    Comment(id = 7, content = '홀수댓글', post = None),
], bulk=False)

# 방법2 (지정한 댓글들의 content가 수정되고, FK도 다시 Post(id = 1)와 연결된다 나머지 댓글은 전부 FK가 NULL로 설정된다.)
Post.objects.get(id = 1).comment_set.set([
    Comment(id = 1, content = '홀수댓글 외 전부 연결 해제', post = None),
    Comment(id = 3, content = '홀수댓글 외 전부 연결 해제', post = None),
    Comment(id = 5, content = '홀수댓글 외 전부 연결 해제', post = None),
    Comment(id = 7, content = '홀수댓글 외 전부 연결 해제', post = None),
], bulk=False, clear=True)

# 방법3 (지정한 댓글들의 FK 연결이 설정되고, 나머지 기존 데이터들은 FK가 NULL로 설정된다.)
Post.objects.get(id = 1).comment_set.set([
    Comment.objects.get(id = 2),
    Comment.objects.get(id = 4),
    Comment.objects.get(id = 6),
], clear=True)


# https://django.readthedocs.io/en/stable/ref/models/relations.html
# https://docs.djangoproject.com/en/5.0/ref/models/relations/
'''
