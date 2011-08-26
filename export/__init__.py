def tokml(queryset, stream):
    stream.write("<kml><Document><name>Troggle output</name>")
    for instance in queryset:
        res=instance.kmlPlacemark()
	print res
	stream.write(instance.kmlPlacemark())
    stream.write("</Document></kml>")
    stream.close()

