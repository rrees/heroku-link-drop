import hashlib

def name_or_url(link):
	if hasattr(link, 'name') and link.name:
		return link.name

	return link.url

def md5(link):
	if not link:
		return ''
	return hashlib.md5(link).hexdigest()

all_filters = {
	'name_or_url': name_or_url,
	'md5': md5,
}