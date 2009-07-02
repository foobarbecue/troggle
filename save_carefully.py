import logging

def save_carefully(objectType, lookupAttribs={}, nonLookupAttribs={}):
    """Looks up instance using lookupAttribs and carries out the following:
            -if instance does not exist in DB: add instance to DB, return (new instance, True)
            -if instance exists in DB and was modified using Troggle: do nothing, return (existing instance, False)
            -if instance exists in DB and was not modified using Troggle: overwrite instance, return (instance, False)
            
        The checking is accomplished using Django's get_or_create and the new_since_parsing boolean field
        defined in core.models.TroggleModel.
    
    """
    
    instance, created=objectType.objects.get_or_create(defaults=nonLookupAttribs, **lookupAttribs)

    if not created and not instance.new_since_parsing:
        for k, v in nonLookupAttribs.items(): #overwrite the existing attributes from the logbook text (except date and title)
            setattr(instance, k, v)
        instance.save()
    
    if created:
        logging.info(unicode(instance)+u' was just added to the database for the first time. \n')
    
    if not created and instance.new_since_parsing:
        logging.info(unicode(instance)+" has been modified using Troggle, so the current script left it as is. \n")

    if not created and not instance.new_since_parsing:
        logging.info(unicode(instance)+" existed in the database unchanged since last parse. It was overwritten by the current script. \n")
    return (instance, created)