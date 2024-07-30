from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from .models import QuizRoom, Question

class QuizRoomForm(forms.ModelForm):
    class Meta:
        model = QuizRoom
        fields = ['room_name']

    def __init__(self, *args, **kwargs):
        super(QuizRoomForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('room_name')
        )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'score_per_question', 'time_allotted_per_question']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('text'),
            Field('option_a'),
            Field('option_b'),
            Field('option_c'),
            Field('option_d'),
            Field('correct_option'),
            Field('score_per_question'),
            Field('time_allotted_per_question'),
            ButtonHolder(
                Submit('add_question', 'Add Another Question', css_class='btn btn-secondary')
            )
        )
