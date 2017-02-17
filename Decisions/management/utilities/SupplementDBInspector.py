from Decisions.models import DecisionSupplementaryModel

def count():
    return DecisionSupplementaryModel.objects.count()