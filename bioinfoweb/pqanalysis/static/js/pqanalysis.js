// DataTable library for organization of results
$(document).ready(function() {
	$("#pqupload").validate({
		rules: {
			'file[]': {
				required: true,
				extension: 'csv|tsv|lis|LIS'
			},
			'analysis_id': {
				required: true,
				alphanumeric:true,
				rangelength:[1,99]
			},
			'submitter': {
				required: true,
				rangelength:[1,99]
			}
		},
		messages: {
			'file[]': {
				required: true,
				extension: "Please upload valid file format."
			}
		}
	});
});
