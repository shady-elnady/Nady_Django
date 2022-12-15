from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from GraphQL.models import BaseModelName
from Product.models import Product

# Create your models here.


class  PharmaceuticalForm(BaseModelName):

    class Meta:
        verbose_name= _("Pharmaceutical Form")
        verbose_name_plural= _("Pharmaceutical Forms")


class EffectiveMaterial(BaseModelName):

    class Meta:
        verbose_name= _("Effective Material")
        verbose_name_plural= _("Effective Materials")


class Drug(Product):
    """
        Drugs Category:
            دستور تصنيف الأدوية الأمريكية
            وفقًا لدستور تصنيف الأدوية الأمريكية USP فإن الأدوية التي تصرف وفقًا لوصفة طبية تم تصنيفها إلى 48 قسم، وهذه التصنيفات هي:

            المسكنات ، بما في ذلك المواد الأفيونية وغير الأفيونية
            عقاقير مخدرة
            مضادات الجراثيم ، بما في ذلك المضادات الحيوية
            مضادات الاختلاج
            عوامل طب العيون
            وكلاء الأذن
            عوامل مضادات الذهان
            مضادات الاكتئاب
            مضادات السموم ومضادات السموم
            مضادات القيء
            مضادات الفطريات
            عوامل الجهاز التنفسي ، بما في ذلك مضادات الهيستامين وموسعات الشعب الهوائية
            العوامل المضادة للالتهابات ، بما في ذلك المسكنات
            وكلاء مضادات الصداع النصفي
            العوامل المضادة للوهن
            مضادات الجراثيم
            مضادات الأورام
            مضادات الطفيليات
            وكلاء مضاد مرض باركنسون
            مضادات الفيروسات ، بما في ذلك أدوية التهاب الكبد الوبائي سي والأدوية المضادة للفيروسات القهقرية
            عوامل مزيل القلق (مضادات القلق).
            عوامل هرمونية (الغدة الدرقية)
            مثبطات الهرمونات (الغدة الكظرية)
            مثبطات الهرمونات (جارات الدرقية)
            مثبطات الهرمونات (الغدة النخامية)
            مثبطات الهرمونات (الهرمونات الجنسية)
            مثبطات الهرمونات (الغدة الدرقية)
            وكلاء ثنائي القطب
            منظمات جلوكوز الدم ، بما في ذلك الأنسولين وأدوية السكري الأخرى
            منتجات الدم ، بما في ذلك مضادات التخثر
            عوامل القلب والأوعية الدموية ، بما في ذلك حاصرات بيتا ومثبطات الإنزيم المحول للأنجيوتنسين
            عوامل الجهاز العصبي المركزي ، بما في ذلك الأمفيتامينات
            وكلاء طب الأسنان والفم
            عوامل جلدية (جلدية)
            عامل استبدال الانزيم
            عوامل الجهاز الهضمي ، بما في ذلك حاصرات H2 ومثبطات مضخة البروتون
            عوامل الجهاز البولي التناسلي (المسالك البولية والتناسلية)
            عوامل هرمونية،  الغدة الكظرية
            عوامل هرمونية،  الغدة النخامية
            العوامل الهرمونية، البروستاجلاندين
            العوامل الهرمونية (الهرمونات الجنسية) ، بما في ذلك الإستروجين والتستوستيرون والستيرويدات الابتنائية
            العوامل المناعية ، بما في ذلك اللقاحات والأدوية المضادة للروماتيزم المعدلة للمرض (DMARDs)
            عوامل مرض التهاب الأمعاء
            عوامل أمراض العظام الأيضية
            المهدئات والمنومات
            مضادات الذهان
            مرخيات العضلات والهيكل العظمي
            المغذيات العلاجية والمعادن والإلكتروليتات
    """
    effective_material= models.ForeignKey(
        EffectiveMaterial,
        on_delete= models.CASCADE,
        related_name= _("Drugs"),
        verbose_name= _("Effective Material"),
    ) # الماده الفاعله
    pharmaceutical_form= models.ForeignKey(
        PharmaceuticalForm,
        on_delete= models.CASCADE,
        related_name= _("Drugs"),
        verbose_name= _("Pharmaceutical Form"),
    ) # الشكل الصيدلي
    for_child_pregnant= models.BooleanField(
        verbose_name= _("for Child Pregnant"),
    )
    trade_name= models.CharField(
        max_length= 25,
        unique= True,
        verbose_name= _("Trade Name"),
    ) # الاسم التجارى
    ## Override on Parent Class
    Product._meta.get_field('category').limit_choices_to= {"category_parent__isequ": "Drugs"},

    class Meta:
        verbose_name= _("Drug")
        verbose_name_plural= _("Drugs")

