# coding: utf8

from django.db import models
import uuid
# import fdb


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return u'journal/%s/%s/%s' % (filename[:1], filename[2:3], filename)


class Message(models.Model):
    number = models.CharField('№ служебной записки', max_length=50)
    data = models.DateField('Дата публикации')
    description = models.TextField(max_length=150)
    count = models.IntegerField('Всего страниц', null=True)
    user_adr = models.CharField(max_length=50)
    user_ins = models.CharField(max_length=50)
    comment = models.TextField(max_length=150)

    def __str__(self):
        # con = fdb.connect(
        #     dsn='/home/kirill/PycharmProjects/kalugaenergo/journal/test.fdb',
        #     user='sysdba', password='masterkey'
        #     )
        # cur = con.cursor()
        # cur.execute("select count(*) from ts_point")
        # return self.number + str(cur.fetchall())
        return self.number

    def __unicode__(self):
        return u"%s" % self.__str__()

    def get_count(self):
        return self.document_set.count()

    def get_path_file(self):
        return Document.objects.get(message=self.id).file


class Document(models.Model):
    message = models.ForeignKey(Message, null=True)
    title = models.CharField('Наименование файла', max_length=150, null=True)
    file = models.FileField('Документ', null=True, upload_to=get_file_path, blank=True)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super

    def __unicode__(self):
        return u"%s" % self.__str__

    @property
    def __str__(self):
        return self.title
