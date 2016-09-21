// DataTable library for organization of results
$(document).ready(function() {

	$.validator.addMethod("alphaonly", function(value, element) {
		return this.optional(element) || /^[a-z0-9]+$/i.test(value);
	}),

	$("#pqupload").validate({
		rules: {
			'analysis_id': {
				required: true,
				alphaonly:true,
				rangelength:[1,99]
			},
			'submitter': {
				required: true,
				rangelength:[1,99]
			}
		},
		messages: {
			'analysis_id': 'Only letters and numbers allowed.'
		}
	});
});
