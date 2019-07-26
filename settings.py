"""
Django settings for red_fox project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@*9m@s@(sh9djf)b7z8xs6@@&o@mo-_)fgn^p*ng97%a#j)*re'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'InstagramCrawler',
    'SpotifyCrawler',
    'TwitterCrawler'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'red_fox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'red_fox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


INSTAGRAM_USER_NAME = "insta@gmail.com"
INSTAGRAM_PASSWORD = "insta"

LINKEDIN_USER_NAME ="linkedin@gmail.com"
LINKEDIN_PASSWORD= "linkedin"

TWITTER_CONSUMER_KEY = ' '
TWITTER_CONSUMER_SECRET = ' '
TWITTER_ACCESS_TOKEN_KEY = '  '
TWITTER_ACCESS_TOKEN_SECRET = ' '
GET_TWEET_COUNT = 1000

ELASTIC_SEARCH_DATABASE_NAME = "redfox"
ELASTIC_SEARCH_NLTK_NAME="nltk"
ELASTIC_SEARCH_USER_DATABASE = "redfox_users"
ELASTIC_SEARCH_HOST ="0.0.0.0"
SPOTIFY_CLIENT_ID= " "
SPOTIFY_CLIENT_SECRET= " "
# Kafka conf.
KAFKA_HOST = "localhost"
KAFKA_PORT = "9092"
KAFKA_API_VERSION = (0, 10, 0)
KAFKA_CONNECTION_URL = '{host}:{port}'.format(host=KAFKA_HOST, port=KAFKA_PORT)

HEADER={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/72.0.3626.119 Safari/537.36"}


treebank_dict= {"CC":"Coordinating conjunction",
"CD":"Cardinal number",
"DT":"Determiner",
"EX":"Existential there",
"FW":"Foreign word",
"IN":"Preposition or subordinating conjunction",
"JJ":"Adjective",
"JJR":"Adjective, comparative",
"JJS":"Adjective, superlative",
"LS":"List item marker",
"MD":"Modal",
"NN":"Noun, singular or mass",
"NNS":"Noun, plural",
"NNP":"Proper noun, singular",
"NNPS":"Proper noun, plural",
"PDT":"Predeterminer",
"POS":"Possessive ending",
"PRP":"Personal pronoun",
"PRP$":"Possessive pronoun",
"RB":"Adverb",
"RBR":"Adverb, comparative",
"RBS":"Adverb, superlative",
"RP":"Particle",
"SYM":"Symbol",
"TO":"to",
"UH":"Interjection",
"VB":"Verb, base form",
"VBD":"Verb, past tense",
"VBG":"Verb, gerund or present participle",
"VBN":"Verb, past participle",
"VBP":"Verb, non-3rd person singular present",
"VBZ":"Verb, 3rd person singular present",
"WDT":"Wh-determiner",
"WP":"Wh-pronoun",
"WP$":"Possessive wh-pronoun",
"WRB":"Wh-adverb",
"$":None
}