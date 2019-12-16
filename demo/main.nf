process foo{
	echo true
	input:
	val x from params.message

	"""
	echo ${x}
	"""
}