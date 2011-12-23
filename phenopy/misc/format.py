from markdown import Markdown
import markdown
import re

class CDATA(object):
    pass

def markdown_cdata_format(text, safe_mode=True):
    cdata = CDATA()
    
    # Markdown changed syntax - test which case will work
    #cdata.content =  Markdown(text, safe_mode = safe_mode).convert().encode('utf-8')
    cdata.content =  markdown.markdown(text, safe_mode = safe_mode).encode('utf-8')

    return cdata

def quote_markdown(text):
    return "\n".join( [ "> %s"%x for x in text.split('\n')] )

def quote_subject(text):
    m = re.match(r'^\[RE:\s*(\d+)\] +(.*)', text)
    if m:
        n = int(m.group(1)) + 1
        return "[RE:%d] %s"%(n, m.group(2))
    
    return "[RE:1] %s"%text
    
#    return "\n".join( [ "> %s"%x for x in text.split('\n')] )
