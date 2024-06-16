from mongoengine import connect, Document, StringField, disconnect, BooleanField, IntField, DictField, ListField
import json

class Testcase(Document):

    inclusionmethod     = StringField( null=False, blank=False )
    difference          = StringField( null=False, blank=False )
    filetype            = StringField( null=False, blank=False )
    browser             = StringField( null=False, blank=False )

    # the state of the resource to be included
    includee_state      = BooleanField( )

    # from which config this test case was created
    testsuite           = StringField()

    length              = IntField()
    duration            = StringField()
    time                = StringField()
    logs                = StringField()

    diff_results         = DictField()
    url                  = StringField()
    diff_tags            = ListField()

    def switch_state(self):
        self.includee_state = not self.includee_state
        self.save()

    def getName(self):
        return f"{self.inclusionmethod}/{self.difference}/{self.filetype}/{self.browser}"

    def __repr__(self):
        return f"<Diff {self.getName()}>"

    meta = {
        'indexes': [
             { 'fields': ['inclusionmethod', 'difference', 'filetype', 'browser'], 'unique': True },
             { 'fields': ['-time'] },
             { 'fields': ['-length']},
             { 'fields': ['-inclusionmethod']},
             { 'fields': ['-difference']},
             { 'fields': ['-filetype']},
             { 'fields': ['-browser']}
        ],
        'ordering': ['-time'],
        'auto_create_index': True,
    }

class elementgroup(Document):
    url                 = StringField()
    state               = StringField()
    browser             = StringField()
    response            = StringField()
    resources = DictField()


class browsers(Document):
    name = StringField(required=True)

class differences(Document):
    name = StringField(required=True)
    response0 = DictField(required=True)
    response1 = DictField(required=True)

class inclusionmethods(Document):
    name = StringField(required=True)
    template = StringField(required=True)


class filetypes(Document):
    name=StringField(required=True)
    contenttype=StringField(required=True)
    filetemplate=StringField(required=True)


class site_detection_results(Document):
    url=StringField(required=True)
    results=ListField(required=True)

    def to_json(self):
        return {
            "_id": str(self.pk),
            "url": self.url,
            "results": self.results,
        }

    def get_results(self):
        return json.dumps(self.results)

class testtemplate(Document):
    test_name=StringField(required=True)
    test_category=StringField()
    test_description=StringField()
    test_file=StringField(required=True)
    test_timeout=IntField()
    test_needswindow=StringField()
    def to_json(self):
        return {
            "_id": str(self.pk),
            "test_name": self.test_name,
            "test_category": self.test_category,
            "test_description": self.test_description,
            "test_file": self.test_file,
            "test_timeout": self.test_timeout,
            "test_needswindow": self.test_needswindow
        }
