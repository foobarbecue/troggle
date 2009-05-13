def save(objectType, lookupAttribs={}, nonLookupAttribs={}):

    instance, created=objectType.objects.get_or_create(defaults=nonLookupAttribs, **lookupAttribs)

    if not created and not instance.new_since_parsing:
        for k, v in nonLookupAttribs.items(): #overwrite the existing attributes from the logbook text (except date and title)
            setattr(instance, k, v)
        instance.save()
    
    return instance