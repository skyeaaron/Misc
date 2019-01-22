# -*- coding: utf-8 -*-
import re

class Provider:
    """ class for provider names
    so they can be split, sorted into study arm,
    matched to other providers, assigned id/study arm
    based on matches, etc. """
    def __init__(self, og_name, prov_id = None, study_arm = None):
        self.og_name = og_name
        self.id = prov_id
        self.study_arm = study_arm
        self.matches = set()
        self.set_split_name(self.og_name)
        
    def __repr__(self):
        return "<Provider og_name:%s split_name: %s id:%s study_arm:%s matches:%s>" % (self.og_name, self.split_name, self.id, self.study_arm, str(self.matches))
    
    def set_split_name(self, input_name):
        new_name = input_name.replace('INACTIVE', '')
        new_name = new_name.replace('HOSPITALIST', '')
        self.split_name = set(word for word in re.split(r'[, ]', new_name) if word!= '')
        return None
        
    def match_prov(self, prov2):
        """ look for at least 2 matching terms in the split_names """
        if len(self.split_name & prov2.split_name) >= 2:
            self.matches = self.matches | {prov2.og_name}
            return True
        else:
            return False
      
    def classify(self, prov2):
        """ set id and/or study_arm based on prov2
            set id to borrow from prov2 if prov2.id is bigger (whoops)
            set study arm to borrow from prov2 so long as study arm is not
            intervention. does not overwrite Intervention with Control or None"""
        if self.id is None:
            self.id = prov2.id
        elif self.id < prov2.id:
            self.id = prov2.id
        if self.study_arm != "Intervention" and prov2.study_arm is not None:
            self.study_arm = prov2.study_arm
        return None
        
    def reclassify(self, prov2):
        """ if there is a match with prov2:
            reset id to borrow from prov2 if prov2.id is smaller
            set study arm to borrow from prov2 so long as study arm is not
            intervention. do not overwrite intervention with control or None"""
        if self.match_prov(prov2):
            if self.id is None:
                self.id = prov2.id
            elif self.id > prov2.id:
                self.id = prov2.id
            else:
                pass
            if self.study_arm != "Intervention":
                self.study_arm = prov2.study_arm
            else:
                pass
        return None
    

#prov1 = Provider('Aaron, SkyeINACTIVE', 4, 'Control')
#print(prov1)
#prov2 = Provider('Aaron, Skye P.', 6, 'Intervention')
#print(prov2)
#prov1.reclassify(prov2)
#print(prov1)
#prov3 = Provider('Aaron Skye', 6, 'Intervention')
#print(prov3)
#prov1.reclassify(prov3)
#print(prov1)
#prov4 = Provider('Aaron Skye', 3, 'Control')
#print(prov4)
#prov1.reclassify(prov4)
#print(prov1)
