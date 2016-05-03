from django import forms

class SeqConvForm(forms.Form):
	reverse_input = forms.CharField(
		label="",
		widget=forms.TextInput(
			attrs={
				'style':'text-transform:uppercase;',
				'size':'80',
				'id':'seqField'
				}
			)
		)