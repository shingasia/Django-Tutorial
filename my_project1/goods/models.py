import uuid
from django.db import models
from django.forms import ModelForm
from datetime import datetime, timezone

# Create your models here.
class Book(models.Model):
    
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    # 판매기간
    sdate = models.DateTimeField(default=datetime.now())
    edate = models.DateTimeField(default=datetime(9999, 12, 31, 23, 59, 59, 999999))
    starpoint = models.FloatField(default=5.0) # 별점(5점 만점)
    author_email = models.EmailField(default=None) # 작가 이메일
    sell_url = models.URLField(default=None) # 구매링크
    
    def __str__(self):
        return F'이름: {self.name}'

# ===============================================================================================================================
# Django의 Field Types
# ===============================================================================================================================
# 1) AutoField                  ▶ 직접 사용할 필요는 없습니다. 달리 지정하지 않으면 기본 키(primary key) 필드가 모델에 자동으로 추가됩니다.
# 🔴 기본적으로 Django는  AppConfig.default_auto_field에서 앱별로 또는 DEFAULT_AUTO_FIELD 설정에서 전역적으로 지정된 타입을 사용하여 각 모델에 자동 증가 기본 키를 제공합니다.
# 2) BigAutoField               ▶ 1에서 9223372036854775807까지의 숫자에 맞도록 보장된다는 점을 제외하면 AutoField와 매우 유사한 64비트 정수입니다.
# 3) BigIntegerField            ▶ -9223372036854775808에서 9223372036854775807까지의 숫자에 맞도록 보장된다는 점을 제외하면 IntegerField와 매우 유사한 64비트 정수입니다. 이 필드의 기본 양식 위젯은 NumberInput입니다.
# 4) BinaryField                ▶ 원시(raw) 바이너리 데이터를 저장하는 필드입니다. 기본적으로 BinaryField는 editable을 False로 설정하며, 이 경우 django.forms.ModelForm에 포함될 수 없습니다.
# 5) BooleanField               ▶ True/False 필드. 이 필드의 기본 form 위젯은 CheckboxInput이거나 null=True인 NullBooleanSelect입니다.
# 6) CharField                  ▶ 텍스트 기반 값을 저장하는 필드입니다. 텍스트 양이 많으면 TextField를 사용하세요.
# 7) DateField                  ▶ Python에서 datetime.date 객체로 표현되는 날짜입니다. 기본 form 위젯은 DateInput입니다.
# 8) DateTimeField              ▶ Python에서 datetime.datetime 객체로 표현되는 날짜와 시간입니다. 기본 form 위젯은 DateTimeInput입니다.
# 9) DecimalField               ▶ Python에서 Decimal 객체로 표현되는 고정 정밀도(fixed-precision) 십진수입니다. 기본 form 위젯은 localize가 False인 경우 NumberInput이고 그렇지 않은 경우 TextInput입니다.
# 10) DurationField             ▶ 기간을 정하는 필드입니다. Python의 timedelta로 모델링되었습니다.
# 11) EmailField                ▶ EmailValidator를 사용하여 값이 유효한 이메일 주소인지 확인하는 CharField입니다.
# 12) FileField                 ▶ 파일 업로드 필드. 기본 FileSystemStorage를 사용하는 경우 FileField.upload_to 속성에 지정한 문자열 값이 MEDIA_ROOT 경로에 추가되어 업로드된 파일이 저장될 로컬 파일 시스템의 위치를 형성합니다.
# 13) FilePathField             ▶ 파일 시스템의 특정 디렉터리에 있는 파일 이름으로 제한되는 CharField입니다.
# 14) FloatField                ▶ Python에서 float 객체로 표현되는 부동 소수점(floating-point) 숫자입니다. 기본 form 위젯은 localize가 False인 경우 NumberInput이고 그렇지 않은 경우 TextInput입니다.
# 15) GeneratedField            ▶ 항상 해당 모델(model)의 다른 필드를 기반으로 계산되는 필드입니다. 이 필드는 데이터베이스 자체에서 관리되고 업데이트됩니다. 테이블 생성할 때 GENERATED ALWAYS 구문을 사용합니다.
# 16) GenericIPAddressField     ▶ 설명생략...
# 17) ImageField                ▶ FileField의 모든 속성과 메서드를 상속하지만 업로드된 개체가 유효한 이미지인지도 확인합니다. 이 필드의 기본 form 위젯은 ClearableFileInput입니다.
# 18) IntegerField              ▶ 정수 필드입니다. -2147483648부터 2147483647까지의 값은 Django가 지원하는 모든 데이터베이스에서 안전합니다. 기본 form 위젯은 localize가 False인 경우 NumberInput이고 그렇지 않은 경우 TextInput입니다.
# 19) JSONField                 ▶ JSON 인코딩 데이터를 저장하기 위한 필드입니다. Python 기본 형식(딕셔너리, 리스트, 문자열, 숫자, 부울, None)으로 표시됩니다.
# 20) PositiveBigIntegerField   ▶ PositiveIntegerField와 비슷하지만 범위가 0부터 9223372036854775807까지입니다.
# 21) PositiveIntegerField      ▶ IntegerField와 비슷하지만 범위가 0부터 2147483647까지입니다.
# 22) PositiveSmallIntegerField ▶ PositiveIntegerField와 비슷하지만 범위가 0부터 32767까지입니다.
# 23) SlugField                 ▶ 설명생략...
# 24) SmallAutoField            ▶ AutoField와 비슷하지만 범위가 1부터 32767까지입니다.
# 25) SmallIntegerField         ▶ IntegerField와 비슷하지만 범위가 -32768부터 32767까지입니다.
# 26) TextField                 ▶ 큰 텍스트 필드. 이 필의 기본 form 위젯은 Textarea입니다.
# 27) TimeField                 ▶ Python에서 datetime.time 객체로 표현되는 시간입니다. 이 필드의 기본 form 위젯은 TimeInput입니다.
# 28) URLField                  ▶ URLValidator에 의해 검증된 URL에 대한 CharField입니다. 이 필드의 기본 form 위젯은 URLInput입니다.
# 29) UUIDField                 ▶ UUID(Universally Unique IDentifier)를 저장하는 필드입니다. Python의 UUID 클래스를 사용합니다. 데이터베이스의 uuid 데이터타입 또는 char(32)에 저장됩니다.

# ===============================================================================================================================
# Relationship fields
# ===============================================================================================================================
# 1) ForeignKey
# 2) ManyToManyField
# 3) OneToOneField


# https://docs.djangoproject.com/en/5.0/ref/models/fields/#model-field-types

