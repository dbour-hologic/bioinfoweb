from django import forms
import django.forms.extras.widgets;

""" Fields for accepting inputs for the Melting 5 Wrapper 
The fields are generated individually in the templates for 
formatting purposes """
class MeltForm(forms.Form):

	hybridChoices = (
		("dnadna", "DNA:DNA"),
		("rnadna", "RNA:DNA"),
		("dnarna", "DNA:RNA"),
		("rnarna", "RNA:RNA"),
		("mrnarna", "2-O-Methyl-RNA:RNA"),
	)

	meltSeq = forms.CharField(widget=forms.Textarea(attrs={'data-bind':'event:{keyup: readArray()}' ,'maxlength':'59', 'rows':'4', 'cols':'60', 'id':'seq'}))
	hybridType = forms.CharField(widget=forms.Select(choices=hybridChoices, attrs={'id':'hybridType'}))
	oligoConc = forms.CharField(widget=forms.TextInput(attrs={'size':'4', 'id':'oligoConc'}))
	sodiumConc = forms.CharField(widget=forms.TextInput(attrs={'size':'4', 'id':'sodiumConc'}))
	magConc = forms.CharField(widget=forms.TextInput(attrs={'size':'4', 'id':'magConc'}))
