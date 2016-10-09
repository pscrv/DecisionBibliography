 
    
if __name__ == "__main__":
    import os
    import django 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DecisionBibliography.settings')  
    django.setup()

    from app.models import DecisionBibliographyModel

    objects = DecisionBibliographyModel.objects.all()
    for obj in objects:
        if obj.DecisionLanguage == "DE":
            obj.Link = obj.LinkDE
        if obj.DecisionLanguage == "EN":
            obj.Link = obj.LinkEN
        if obj.DecisionLanguage == "FR":
            obj.Link = obj.LinkFR
        obj.save()
    x = 1


