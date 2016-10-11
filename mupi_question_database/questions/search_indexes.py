from haystack import indexes
from .models import Question
import datetime

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True,use_template=True)
    author = indexes.CharField(model_attr='author')
    create_date = indexes.DateTimeField(model_attr='create_date')
    level = indexes.CharField(model_attr='level')
    text_auto = indexes.EdgeNgramField(model_attr='question_text')

    def get_model(self):
        return Question
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(create_date__lte=datetime.datetime.now())