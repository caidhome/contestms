from django.template import Library

register = Library()

@register.filter('level')
def level(value):
    levels = {'1': '国家级', '2': '省级', '3': '市级', '4': '校级', '5': '院级'}
    return levels[str(value)]

def checklang(value, liststr):
    lang_list = [item for item in liststr.split(';')]
    return value in lang_list

register.filter('level', level)
register.filter('checklang', checklang)