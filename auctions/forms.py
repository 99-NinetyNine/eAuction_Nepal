from location_field.forms.plain import PlainLocationField

class Address(forms.Form):
    city = forms.CharField()
    location = PlainLocationField(based_fields=['city'],
                                  initial='-22.2876834,-49.1607606')