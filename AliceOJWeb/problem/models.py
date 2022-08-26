from django.db import models
from django.utils import timezone

from mdeditor.fields import MDTextField

from user.models import User


# Create your models here.


class Problem(models.Model):
    EASY = 0
    NORMAL = 1
    HARD = 2
    DIFFICULT_LEVEL = (
        (EASY, 'easy'),
        (NORMAL, 'normal'),
        (HARD, 'hard'),
    )
    title = models.CharField(max_length=32)
    description = MDTextField()
    difficult_level = models.PositiveIntegerField(choices=DIFFICULT_LEVEL, default=EASY)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.title


class Solution(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()
    cpu_time_limit = models.PositiveIntegerField(default=1000)
    real_time_limit = models.PositiveIntegerField(default=1000)
    memory_limit = models.PositiveIntegerField(default=65535*1024)
    # in = models.ManyToManyField(Problem)
    
    def __str__(self):
        return self.problem.title


class Answer(models.Model):
    # NOJUDGE = 0
    # JUDGING = 1
    # JUDGEDONE = 2

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    cpu_time = models.PositiveIntegerField(default=0)
    real_time = models.PositiveIntegerField(default=0)
    use_memory = models.PositiveIntegerField(default=0)
    judger_time = models.DateTimeField(default=timezone.now)

    message = models.TextField(null=True)
