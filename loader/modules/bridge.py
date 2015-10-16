# -*- coding: utf-8 -*-
import urllib, mimetypes, json, hashlib

class File(object):
    def __init__(self,grantname,filename,site,link,dumpname,kind):
        '''
        Class that define a simple file object, that can be doc, pdf, etc.
        It requires a grant name, stored filename and a site id for the 
        link, dump filename. A kind of link is needed
        '''
        self.grantname = grantname
        self.filename = filename
        self.site = site
        self.link = link
        self.kind = kind
        self.text = ''
        self.dumpname = dumpname
        self._import()
    
    def store(self):
        self.analyse()
        self.code()
        self.save()
    
    def save(self):
        _var = dict(name=self.grantname,url=self.site,
            description=self.text,
            link=self.link,kind=self.kind)
        try:
            old = json.load(open(self.dumpname))
            old.append(_var)
        except:
            old = [_var]
        try:
            with open(self.dumpname, "w") as dump:
                json.dump(old,dump)
        except:
            raise #IOError("Error saving file")

    def code(self):
        try:
            self.text = self.text.encode("utf-8")
        except:
            try:
            	self.text = self.text.decode("utf-8")
            except: 
                self.text = self.text.decode("latin1")
    
class Docx(File):
    def _import(self):
        from docx import opendocx, getdocumenttext
        self.opendocx = opendocx
        self.getdocumenttext = getdocumenttext
    
    def analyse(self):
        try:
            document = self.opendocx(self.filename)
        except:
            raise #IOError("Not a valid file")
        
        try:
            totxtlist = self.getdocumenttext(document)
        except:
            raise #IOError("Error getting file contents")
                
        self.text = '\n\n'.join(totxtlist)

class Doc(File):
    def _import(self):
        from subprocess import check_output
        self.check_output = check_output
    
    def analyse(self):
        try:
            self.text = self.check_output(["catdoc", self.filename])
        except:
            raise #IOError("Error getting file contents")

class Pdf(File):
    def _import(self):
        from subprocess import check_output
        self.check_output = check_output
    
    def analyse(self):
        try:
            # pdf = self.check_output(["pdftotext", self.filename])
            self.text = self.check_output(["pdftotext", self.filename])
            # self.te
        # except CalledProcessError as (errno, strerror):
        except:
            # print "PDFEncryptionError in {2} CalledProcessError({0}): {1}".format(errno, strerror,self.link)
            raise

class Html(File):
    def _import(self):
        from pdfkit import from_url
        from subprocess import check_output
        self.check_output = check_output
        self.from_url = from_url
    
    def analyse(self):
        try:
            pdf = hashlib.md5(self.link).hexdigest()+'.pdf'
            self.from_url(str(self.link),pdf)
        except:
            raise #IOError("Error getting pdf file from url")
        try:
            # self.text = self.check_output(["pdf2txt.py", pdf])
            self.text = self.check_output(["pdftotext", pdf])
        except:
            raise #IOError("Error getting file contents")

class Text(File):
    def _import(self):
        pass
    def analyse(self):
        pass

def saveit(grantname, uri,site,filename,kind,text):
    '''
    This function gets a grant name, uri and a site id from crawler and 
    gets the file and dump filename. A grant kind is needed too.
    The text field enable get a field automatically
    '''
    def get():
        try:
            return urllib.urlretrieve(uri)
        except:
            raise #IOError("Error saving file to filesystem")

    item = get()
    name = item[0]
    fext = item[1].getheader('Content-Disposition') or ''

    if text:
        mime = mimetypes.guess_type(text)[0]
    else:
        mime = mimetypes.guess_type(name)[0]

    print item[0]
    if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in [mime, item[1].type] \
            or '.docx' in fext:
        choose = Docx(grantname, name,site,uri,filename,kind)
    elif 'application/msword' in [mime, item[1].type] \
            or '.doc' in fext:
        choose = Doc(grantname, name,site,uri,filename,kind)
    elif 'application/pdf' in [mime, item[1].type] \
            or '.pdf' in fext:
        choose = Pdf(grantname, name,site,uri,filename,kind)
    elif item[1].type == 'text/html' and not text:
        choose = Html(grantname,name,site,uri,filename,kind)
    elif not mime and text:
        choose = Text(grantname,name,site,uri,filename,kind)
        choose.text = text
    else:
        raise IOError("Error finding mimetype from file: "+str(mime))
    
    choose.store()

#saveit('grandtest','http://localhost:8000/teste.doc','teste','teste.json',1)
#saveit('docxtest','http://localhost:8000/teste.docx','testex','testex.json',1)
#saveit('pdftest','http://localhost:8000/simple1.pdf','testepdf','testepdf.json',1)
#saveit('htmlpdftest','http://www.google.com.br','testepdf','testehtmlpdf.json',1)
#saveit('texttest','http://www.google.com.br','testetext','testetext.json',1,'lalallalala')
