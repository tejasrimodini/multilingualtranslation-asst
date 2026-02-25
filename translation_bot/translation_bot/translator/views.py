import json
import urllib.request
import urllib.parse
import urllib.error
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import TranslationHistory, LANGUAGE_CHOICES


def index(request):
    recent_translations = TranslationHistory.objects.all()[:10]
    total_translations = TranslationHistory.objects.count()
    total_characters = sum(t.character_count for t in TranslationHistory.objects.all())
    
    languages_used = TranslationHistory.objects.values_list('target_language', flat=True).distinct().count()

    context = {
        'languages': LANGUAGE_CHOICES,
        'recent_translations': recent_translations,
        'stats': {
            'total_translations': total_translations,
            'total_characters': total_characters,
            'languages_used': languages_used,
        }
    }
    return render(request, 'translator/index.html', context)


def translate_text_google(text, target_lang, source_lang='auto'):
    """Use Google Translate unofficial API."""
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': source_lang,
            'tl': target_lang,
            'dt': 't',
            'q': text,
        }
        full_url = url + '?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(full_url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        translated = ''
        for item in data[0]:
            if item[0]:
                translated += item[0]
        
        detected = None
        if source_lang == 'auto' and len(data) > 2 and data[2]:
            detected = data[2]
        
        return translated, detected
    except Exception as e:
        return None, str(e)


@csrf_exempt
@require_http_methods(["POST"])
def translate(request):
    try:
        body = json.loads(request.body)
        text = body.get('text', '').strip()
        target_lang = body.get('target_language', 'es')
        source_lang = body.get('source_language', 'auto')

        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)

        if len(text) > 5000:
            return JsonResponse({'error': 'Text too long (max 5000 characters)'}, status=400)

        translated_text, detected = translate_text_google(text, target_lang, source_lang)

        if translated_text is None:
            return JsonResponse({'error': f'Translation failed: {detected}'}, status=500)

        # Save to history
        history = TranslationHistory.objects.create(
            source_text=text,
            translated_text=translated_text,
            source_language=source_lang,
            target_language=target_lang,
            detected_language=detected,
        )

        lang_dict = dict(LANGUAGE_CHOICES)
        return JsonResponse({
            'translated_text': translated_text,
            'detected_language': detected,
            'detected_language_name': lang_dict.get(detected, detected) if detected else None,
            'target_language_name': lang_dict.get(target_lang, target_lang),
            'character_count': len(text),
            'history_id': history.id,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def batch_translate(request):
    """Translate text to multiple languages at once."""
    try:
        body = json.loads(request.body)
        text = body.get('text', '').strip()
        target_languages = body.get('target_languages', [])
        source_lang = body.get('source_language', 'auto')

        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        if not target_languages:
            return JsonResponse({'error': 'No target languages provided'}, status=400)
        if len(target_languages) > 10:
            return JsonResponse({'error': 'Max 10 languages at once'}, status=400)

        lang_dict = dict(LANGUAGE_CHOICES)
        results = []

        for lang in target_languages:
            translated, detected = translate_text_google(text, lang, source_lang)
            if translated:
                results.append({
                    'language': lang,
                    'language_name': lang_dict.get(lang, lang),
                    'translated_text': translated,
                })
                TranslationHistory.objects.create(
                    source_text=text,
                    translated_text=translated,
                    source_language=source_lang,
                    target_language=lang,
                    detected_language=detected if source_lang == 'auto' else None,
                )

        return JsonResponse({'results': results, 'source_text': text})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def history(request):
    translations = TranslationHistory.objects.all()[:50]
    lang_dict = dict(LANGUAGE_CHOICES)
    return JsonResponse({
        'history': [
            {
                'id': t.id,
                'source_text': t.source_text[:100],
                'translated_text': t.translated_text[:100],
                'source_language': t.source_language,
                'target_language': t.target_language,
                'target_language_name': lang_dict.get(t.target_language, t.target_language),
                'detected_language': t.detected_language,
                'created_at': t.created_at.strftime('%Y-%m-%d %H:%M'),
                'character_count': t.character_count,
            }
            for t in translations
        ]
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def clear_history(request):
    count, _ = TranslationHistory.objects.all().delete()
    return JsonResponse({'deleted': count})
