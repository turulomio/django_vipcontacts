from vipcontacts.models import Person, Mail, MailType
import vobject
from django.utils import timezone

class VCard:
    def __init__(self, filename):
        self.filename=filename
        try:
            self._vcard=self._load()
            self._loaded=True
        except:
            self._loaded=False
            
    def isLoaded(self):
#        if hasattr(self, "_card") is False:
#            return False
        return self._loaded

    def _load(self):
        vcard=None
        with open(self.filename) as source_file:
            vcard=vobject.readOne(source_file.read())
        return vcard

    def name(self):
        return self._vcard.n.value.given
#        list_n=self._vcard.n.value.split(" ")
#        if len(list_n)==0:
#            return ""
#        elif len(list_n)==1:
#            return self._vcard.n.value
#        else:
#            return self._vcard.n.value[0]
        
    def surname(self):
#        list_n=self._vcard.n.value.split(" ")
        return self._vcard.n.value.additional
#        if len(list_n)<2:
#            return ""
#        else:
#            return self._vcard.n.value[1]
    def surname2(self):
        return self._vcard.n.value.family
#        list_n=self._vcard.n.value.split(" ")
#        if len(list_n)<3:
#            return ""
#        else:
#            return self._vcard.n.value[2]
            
    def birthday(self):
        try:
            return self._vcard.bday.value[:10]
        except:
            return None

    ## Return mail and vipcontacts types
    def mails(self):
        r=[]
        if not 'email' in self._vcard.contents:
            return []
        for o in self._vcard.contents['email']:
            if not "TYPE" in o.params:
                r.append((o.value,  MailType.Other))
            elif o.params["TYPE"]==['HOME']:
                r.append((o.value,  MailType.Personal))
            elif o.params["TYPE"]==['PREF', 'HOME']:
                r.append((o.value,  MailType.Personal))
            elif o.params["TYPE"]==['WORK']:
                r.append((o.value,  MailType.Work))
            elif o.params["TYPE"]==['PREF', 'WORK']:
                r.append((o.value,  MailType.Work))
            elif o.params["TYPE"]==['PREF']:
                r.append((o.value,  MailType.Personal))
            elif o.params["TYPE"]==['TYPE']:
                r.append((o.value,  MailType.Other))
            else:
                print(f"  - Mail type missing: {o.params['TYPE']}")
                r.append((o.value,  MailType.Other))
            
        return r

    def phones(self):
        r=[]
        for o in self._vcard.contents['tel']:
            r.append((o.value, o.name, o.params))
        return r



def import_in_vipcontacts(filename):
    vcard=VCard(filename)
    print(f"Trying {filename}:")
    if vcard.isLoaded() is False:
        return f"  - ERROR LOADING {filename}"
    person=Person(name=vcard.name(), surname=vcard.surname(), surname2=vcard.surname2(),  gender=0, birth=vcard.birthday())
    person.save()
    print (f"  - {person}")
    
    for mail,  type_ in vcard.mails():
        mail=Mail(dt_update=timezone.now(), mail=mail,  retypes=type_,  person=person)
        mail.save()
        print (f"  - {mail}")
  
    return person
        
