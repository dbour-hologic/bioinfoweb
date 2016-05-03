from django.shortcuts import render
from .forms import SeqConvForm
from collections import Counter

def seq_tool(request):
	""" Sequence Conversion Main Logic
	"""

	seqForm = SeqConvForm()

	# Initialize dictionary for counting base pairs
	c = {} 

	if request.method == "POST":

		seqForm = SeqConvForm(request.POST)

		if seqForm.is_valid():

			origSeq = seqForm.cleaned_data['reverse_input'].upper()

			origSeqList = list(origSeq)
			c = Counter(origSeqList)

			totalbase = 0
			for key, value in c.iteritems():
				totalbase += value

			keyPairs = {"A":"T", "T":"A", "C":"G", "G":"C",
						"Y":"R", "R":"Y", "W":"S", "S":"W",
						"K":"M", "M":"K", "D":"H", "H":"D",
						"V":"B", "B":"V", "X":"X", "N":"N" }

			checkpoint = request.POST.get('submit')

			if checkpoint == "reverse":

				tooltype = "Reverse"
				seq = origSeq[::-1].upper()

			elif checkpoint == "complement":
				tooltype = "Complement"
				seq = ""

				for x in origSeq:
					seq += keyPairs[x]

			elif checkpoint == "reverse complement":

				tooltype = "Reverse Complement"
				seq = ""
				revSeq = origSeq[::-1]
				for x in revSeq:
					seq += keyPairs[x]

			elif checkpoint == "clear":

				tooltype = ""
				seq = ""
				origSeq = ""
				totalbase = ""
				c = ""
				seqForm = SeqConvForm()

			return render(request, 'seqconversion/seqconversion.html', {'formSeq':seq, 'origSeq':origSeq, 'tooltype':tooltype, 'c':dict(c), 'totalbase':totalbase, 'seqForm':seqForm})
	return render(request, 'seqconversion/seqconversion.html', {'seqForm': seqForm, 'c':dict(c) })

