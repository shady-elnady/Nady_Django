from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from djongo.models import ArrayReferenceField
import pytz

from Facility.models import MobileNetWork
from GraphQL.models import BaseModelImage, BaseModelName, BaseModelNative, BaseModelSVG
from Entity.models import Entity
from Payment.models import Currency
from Language.models import Language


# Create your models here.


class Country(BaseModelNative, BaseModelSVG):
    ## https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes
    class Continents(models.TextChoices):
        AF = "AF", _("Africa")
        AS = "AS", _("Asia")
        EU = "EU", _("Europe")
        NA = "NA", _("North America")
        OC = "OC", _("Oceania")
        SA = "SA", _("South America")
        AN = "AN", _("Antarctica")

    ALL_TIMEZONES = sorted((item, item) for item in pytz.all_timezones)

    continent = models.CharField(
        max_length= 2,
        choices= Continents.choices,
        verbose_name= _("Continent Name"),
    )
    capital = models.OneToOneField(
        to="City",
        on_delete= models.CASCADE,
        related_name= _("Capital To +"),
        verbose_name= _("Capital"),
    )
    flag_emoji = models.CharField(
        max_length= 5,
        null= True,
        blank= True,
        verbose_name= _("Flag Emoji"),
    )
    currency = models.ForeignKey(
        Currency,
        on_delete= models.CASCADE,
        related_name= _("Countries"),
        verbose_name= _("Currency"),
    )
    languages = models.ManyToManyField(
        Language,
        related_name= _("Countries"),
        verbose_name= _("languages"),
    )
    tel_code = models.CharField(
        max_length= 3,
        null= True,
        blank= True,
        verbose_name= _("Telphone Code"),
    )
    time_zones= models.CharField(
        max_length= 32,
        null= True,
        blank= True,
        choices= ALL_TIMEZONES,
        verbose_name= _("Time Zones"),
    )

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

        # def get_absolute_url(self):
        #     return reverse("_detail", kwargs={"pk": self.pk})



class Governorate(BaseModelNative):  # المحافظه
    ## https://en.wikipedia.org/wiki/ISO_3166-2:EG
    tel_code = models.CharField(
        max_length= 3,
        blank= True,
        null= True,
        unique= True,
        verbose_name= _("Telephone Code"),
    )
    country = models.ForeignKey(
        Country,
        on_delete= models.CASCADE,
        related_name= _("Governorates"),
        verbose_name= _("Country"),
    )

    class Meta:
        verbose_name = _("Governorate")
        verbose_name_plural = _("Governorates")


class City(BaseModelNative):
    country = models.ForeignKey(
        Country,
        on_delete= models.CASCADE,
        related_name= _("Cities"),
        verbose_name= _("Country"),
    )
    governorate = models.ForeignKey(
        Governorate,
        on_delete= models.CASCADE,
        related_name= _("Cities"),
        verbose_name= _("Governorate"),
    )
    
    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Region(BaseModelNative):
    city = models.ForeignKey(
        City,
        on_delete= models.CASCADE,
        related_name= _("Regions"),
        verbose_name= _("City"),
    )

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class Street(BaseModelNative):
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name= _("Streets"),
        verbose_name= _("Region"),
    )

    class Meta:
        verbose_name = _("Street")
        verbose_name_plural = _("Streets")


class CommunicationWay(PolymorphicModel):
    owner = models.ForeignKey(
        Entity,
        on_delete= models.CASCADE,
        related_name= _("Special_Communication_Ways"),
        verbose_name= _("Owner"),
    )
    @property
    def slug(self):
        return slugify(f"{self.pk}")

    def __str__(self):
        return f"{self.pk}"

    def __decode__(self):
        return f"{self.pk}"
    
    # def get_absolute_url(self):
    #     return reverse("Vegetable:vegetable_detail", args=[self.slug])

    class Meta:
        verbose_name = _("Communication Way")
        verbose_name_plural = _("Communication Ways")


class Phone(CommunicationWay):
    country_code = models.ForeignKey(
        Country,
        on_delete= models.CASCADE,
        related_name= _("Phones"),
        verbose_name= _("Country Code"),
    )
    rest_number = models.CharField(max_length=7, verbose_name=_("Phone Number"))

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")


class LandPhone(Phone):
    governorate_code = models.ForeignKey(
        Governorate,
        to_field="tel_code",
        on_delete=models.CASCADE,
        related_name= _("LandPhones"),
        verbose_name= _("Governorate Code"),
    )

    @property
    def number(self):
        return f"{self.country_code.tel_code}{self.governorate_code.tel_code}{self.rest_number}"

    class Meta:
        verbose_name = _("Land Phone")
        verbose_name_plural = _("Land Phones")


class Address(BaseModelNative, CommunicationWay):
    street = models.ForeignKey(
        Street,
        on_delete= models.CASCADE,
        related_name= _("Address"),
        verbose_name= _("Street"),
    )    
    neighbors = ArrayReferenceField(
        to= Entity,
        # model_form_class=NeighborForm,
    )
    # TODO Location Google Maps
    location = models.CharField(
        max_length= 100,
        verbose_name= _("Location"),
    )  # add Lat and Lang for Google Maps

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Address")


class SocialMedia(BaseModelImage):
    is_email = models.BooleanField(
        verbose_name=_("is E-Mail"),
    )

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Medias")


class SocialCommunication(BaseModelName, CommunicationWay):
    social_media = models.ForeignKey(
        SocialMedia,
        on_delete=models.CASCADE,
        verbose_name=_("Social Media"),
    )

    class Meta:
        verbose_name = _("Social Communication")
        verbose_name_plural = _("Social Communications")


class EMail(CommunicationWay):
    e_mail = models.EmailField(
        max_length= 200,
        primary_key= True,
        verbose_name= _("E-Mail"),
    )
    server = models.ForeignKey(
        SocialMedia,
        null= True,
        blank= True,
        limit_choices_to= {'is_email': True},
        on_delete= models.CASCADE,
        related_name= _("E-Mails +"),
        verbose_name= _("Server"),
    )
    socila_media = models.ManyToManyField(
        SocialMedia,
        verbose_name= _("Social Medias"),
    )

    @property
    def slug(self):
        return slugify(f"{self.e_mail}")

    def __str__(self):
        return f"{self.e_mail}"

    def __decode__(self):
        return f"{self.e_mail}"

    class Meta:
        verbose_name = _("EMail")
        verbose_name_plural = _("EMails")



class Mobile(Phone):
    netWork_code = models.ForeignKey(
        MobileNetWork,
        on_delete= models.CASCADE,
        related_name= _("Mobiles"),
        verbose_name= _("NetWork Code"),
    )
    socila_media = models.ManyToManyField(
        SocialMedia,
        verbose_name= _("Social Medias"),
    )
    has_cach= models.BooleanField(
        default= False,
        verbose_name= _("has Cach"),
    )

    @property
    def number(self):
        return (
            f"{str(self.country_code.tel_code)}{str(self.netWork_code.tel_code)}{str(self.rest_number)}"
        )

    class Meta:
        verbose_name = _("Mobile")
        verbose_name_plural = _("Mobiles")



# TODO API FOR COUNTRIES
# https://restcountries.com/#api-endpoints-v3
""" 
    {
        "name": {
            "common": "Egypt",
            "official": "Arab Republic of Egypt",
            "nativeName": {
                "ara": {
                    "official": "جمهورية مصر العربية",
                    "common": "مصر"
                }
            }
        },
        "tld": [
            ".eg",
            ".مصر"
        ],
        "cca2": "EG",
        "ccn3": "818",
        "cca3": "EGY",
        "cioc": "EGY",
        "independent": true,
        "status": "officially-assigned",
        "unMember": true,
        "currencies": {
            "EGP": {
                "name": "Egyptian pound",
                "symbol": "£"
            }
        },
        "idd": {
            "root": "+2",
            "suffixes": [
                "0"
            ]
        },
        "capital": [
            "Cairo"
        ],
        "altSpellings": [
            "EG",
            "Arab Republic of Egypt"
        ],
        "region": "Africa",
        "subregion": "Northern Africa",
        "languages": {
            "ara": "Arabic"
        },
        "translations": {
            "ara": {
                "official": "جمهورية مصر العربية",
                "common": "مصر"
            },
            "ces": {
                "official": "Egyptská arabská republika",
                "common": "Egypt"
            },
            "cym": {
                "official": "Gweriniaeth Arabaidd yr Aifft",
                "common": "Yr Aifft"
            },
            "deu": {
                "official": "Arabische Republik Ägypten",
                "common": "Ägypten"
            },
            "est": {
                "official": "Egiptuse Araabia Vabariik",
                "common": "Egiptus"
            },
            "fin": {
                "official": "Egyptin arabitasavalta",
                "common": "Egypti"
            },
            "fra": {
                "official": "République arabe d'Égypte",
                "common": "Égypte"
            },
            "hrv": {
                "official": "Arapska Republika Egipat",
                "common": "Egipat"
            },
            "hun": {
                "official": "Egyiptomi Arab Köztársaság",
                "common": "Egyiptom"
            },
            "ita": {
                "official": "Repubblica araba d'Egitto",
                "common": "Egitto"
            },
            "jpn": {
                "official": "エジプト·アラブ共和国",
                "common": "エジプト"
            },
            "kor": {
                "official": "이집트 아랍 공화국",
                "common": "이집트"
            },
            "nld": {
                "official": "Arabische Republiek Egypte",
                "common": "Egypte"
            },
            "per": {
                "official": "جمهوری عربی مصر",
                "common": "مصر"
            },
            "pol": {
                "official": "Arabska Republika Egiptu",
                "common": "Egipt"
            },
            "por": {
                "official": "República Árabe do Egipto",
                "common": "Egito"
            },
            "rus": {
                "official": "Арабская Республика Египет",
                "common": "Египет"
            },
            "slk": {
                "official": "Egyptská arabská republika",
                "common": "Egypt"
            },
            "spa": {
                "official": "República Árabe de Egipto",
                "common": "Egipto"
            },
            "swe": {
                "official": "Arabrepubliken Egypten",
                "common": "Egypten"
            },
            "urd": {
                "official": "مصری عرب جمہوریہ",
                "common": "مصر"
            },
            "zho": {
                "official": "阿拉伯埃及共和国",
                "common": "埃及"
            }
        },
        "latlng": [
            27,
            30
        ],
        "landlocked": false,
        "borders": [
            "ISR",
            "LBY",
            "PSE",
            "SDN"
        ],
        "area": 1002450,
        "demonyms": {
            "eng": {
                "f": "Egyptian",
                "m": "Egyptian"
            },
            "fra": {
                "f": "Égyptienne",
                "m": "Égyptien"
            }
        },
        "flag": "🇪🇬",
        "maps": {
            "googleMaps": "https://goo.gl/maps/uoDRhXbsqjG6L7VG7",
            "openStreetMaps": "https://www.openstreetmap.org/relation/1473947"
        },
        "population": 102334403,
        "gini": {
            "2017": 31.5
        },
        "fifa": "EGY",
        "car": {
            "signs": [
                "ET"
            ],
            "side": "right"
        },
        "timezones": [
            "UTC+02:00"
        ],
        "continents": [
            "Africa"
        ],
        "flags": {
            "png": "https://flagcdn.com/w320/eg.png",
            "svg": "https://flagcdn.com/eg.svg"
        },
        "coatOfArms": {
            "png": "https://mainfacts.com/media/images/coats_of_arms/eg.png",
            "svg": "https://mainfacts.com/media/images/coats_of_arms/eg.svg"
        },
        "startOfWeek": "sunday",
        "capitalInfo": {
            "latlng": [
                30.05,
                31.25
            ]
        },
        "postalCode": {
            "format": "#####",
            "regex": "^(\\d{5})$"
        }
    }
"""
