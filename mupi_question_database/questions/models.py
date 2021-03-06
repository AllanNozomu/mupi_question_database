import datetime
from django.db import models
from mupi_question_database.users.models import User
from taggit.managers import TaggableManager

class Question(models.Model):
    LEVEL_CHOICES = (
        ('', 'Nenhuma opção'),
        ('E', 'Fácil'),
        ('M', 'Médio'),
        ('H', 'Difícil')
    )

    question_header = models.CharField(max_length=50)
    question_text = models.TextField()
    resolution = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=1, choices = LEVEL_CHOICES, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now_add=True)
    credit_cost = models.PositiveIntegerField(null=False, blank=False, default=0)

    tags = TaggableManager()
    #
    # class Meta:
    #     ordering = ['pk']

    def __str__(self):
        return u'QuestionId%d (%s) %s' % (self.pk, self.question_header ,self.question_text)


class Answer(models.Model):
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField()

    class Meta:
        ordering = ['question', 'pk']

    def __str__(self):
        return u'QuestionId: %d AnswerId: %d Correct: %s' % (
        self.question.pk, self.pk, ('Yes' if self.is_correct else 'No'))


class Question_List(models.Model):
    question_list_header = models.CharField('Nome da Lista', max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, through='QuestionQuestion_List', related_name='questions')
    create_date = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField('Lista privada')
    cloned_from = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return u'ListId: %d Header: %s' % (self.pk, self.question_list_header)


class QuestionQuestion_List(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_list = models.ForeignKey(Question_List, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        ordering = ['order']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit_balance = models.PositiveIntegerField(null=False, blank=True, default=0)
    avaiable_questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return u'Profile de %s' % (self.user.username)
