def tokml(queryset, stream):
    stream.write("<kml><Document><name>Troggle output</name>")
    for instance in queryset:
        stream.write(instance.kmlPlacemark())
    stream.write("</Document></kml>")

