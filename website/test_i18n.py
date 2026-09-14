"""End-to-end regression coverage for URL-selected public languages."""
import gettext
import re
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree

from django.conf import settings
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from .seo import PUBLIC_PAGE_ROUTES


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class MultilingualTests(TestCase):
    def setUp(self):
        self.language = translation.override('zh')
        self.language.__enter__()
        self.addCleanup(self.language.__exit__, None, None, None)

    def payload(self, language):
        return {
            'identity': 'company', 'organization_name': 'Example',
            'consultation_direction': 'business_market_entry',
            'subject': 'Europe project', 'message': 'Please contact us.',
            'name': 'Example User', 'email': 'sender@example.com', 'phone': '',
            'preferred_language': language, 'privacy_consent': 'on', 'website': '',
        }

    def test_root_always_redirects_to_chinese(self):
        for language in ('zh', 'fr', 'en'):
            self.client.cookies['django_language'] = language
            response = self.client.get('/', HTTP_ACCEPT_LANGUAGE=language)
            self.assertRedirects(response, '/zh/', fetch_redirect_response=False)
            self.assertNotIn('django_language', response.cookies)

    def test_all_public_pages_have_translations_and_valid_internal_links(self):
        visited = set()
        for language, html_lang in [('zh', 'zh-Hans'), ('fr', 'fr'), ('en', 'en')]:
            with translation.override(language):
                for name in PUBLIC_PAGE_ROUTES:
                    with self.subTest(language=language, page=name):
                        translation.activate(language)
                        response = self.client.get(reverse(name))
                        self.assertEqual(response.status_code, 200)
                        self.assertContains(response, f'<html lang="{html_lang}">')
                        self.assertEqual(response.headers['Content-Language'], language)
                        self.assertNotIn('django_language', response.cookies)
                        content = response.content.decode()
                        self.assertEqual(content.count('<h1'), 1)
                        self.assertNotIn('{% ', content)
                        self.assertNotIn('语言版本预留', content)
                        if language != 'zh':
                            # Chinese is intentional in the brand and language autonym only.
                            checked = re.sub(r'<!--.*?-->', '', content, flags=re.S)
                            checked = checked.replace('艾克斯咨询', '').replace('中文', '')
                            self.assertIsNone(re.search(r'[\u4e00-\u9fff]', checked))
                        for href in re.findall(r'href="([^"?#]+)', content):
                            if not href.startswith('/') or href.startswith('/static/') or href in visited:
                                continue
                            visited.add(href)
                            self.assertEqual(self.client.get(href, follow=True).status_code, 200, href)

    def test_representative_translated_content(self):
        for language, nav, hero, label in [
            ('fr', 'Entreprises', 'Votre partenaire en stratégie', 'Adresse e-mail'),
            ('en', 'Business', 'Your Strategy and Execution Partner', 'Email Address'),
        ]:
            response = self.client.get(f'/{language}/')
            self.assertContains(response, nav)
            self.assertContains(response, hero)
            self.assertContains(self.client.get(f'/{language}/contact/'), label)

    def test_switcher_preserves_logical_page_and_query_without_cookie(self):
        for source, suffix in [('zh', 'business/market-entry/'), ('fr', 'about/')]:
            response = self.client.get(f'/{source}/{suffix}?source=menu')
            links = response.context['language_switch_urls']
            self.assertEqual({item['url'] for item in links}, {
                f'/{language}/{suffix}?source=menu' for language in ('zh', 'fr', 'en')
            })
            for item in links:
                self.assertNotIn('django_language', self.client.get(item['url']).cookies)
            self.assertContains(response, f'hreflang="{ "zh-Hans" if source == "zh" else source }" aria-current="page"')

    def test_language_dropdown_is_single_item_before_contact(self):
        response = self.client.get('/en/about/')
        header = response.content.decode().split('</header>', 1)[0]

        self.assertEqual(header.count('class="language-menu"'), 1)
        self.assertEqual(header.count('data-language-menu-toggle'), 1)
        self.assertIn('<span>Language</span>', header)
        self.assertNotIn('language-switcher', header)
        self.assertLess(
            header.index('class="language-menu"'),
            header.index('href="/en/contact/"'),
        )
        for language, url in [
            ('zh-Hans', '/zh/about/'),
            ('fr', '/fr/about/'),
            ('en', '/en/about/'),
        ]:
            self.assertIn(
                f'href="{url}" lang="{language}" hreflang="{language}"',
                header,
            )

    @override_settings(SITE_URL='https://www.acoeursconsulting.com', SITE_NOINDEX=False)
    def test_canonical_and_alternates_on_every_logical_page(self):
        for language in ('zh', 'fr', 'en'):
            with translation.override(language):
                for name in PUBLIC_PAGE_ROUTES:
                    path = reverse(name)
                    response = self.client.get(path + '?source=test')
                    self.assertContains(response, f'<link rel="canonical" href="https://www.acoeursconsulting.com{path}">')
                    self.assertContains(response, f'<meta property="og:url" content="https://www.acoeursconsulting.com{path}">')
                    for target, tag in [('zh', 'zh-Hans'), ('fr', 'fr'), ('en', 'en'), ('zh', 'x-default')]:
                        with translation.override(target):
                            alternate = reverse(name)
                        self.assertContains(response, f'<link rel="alternate" hreflang="{tag}" href="https://www.acoeursconsulting.com{alternate}">')

    @override_settings(SITE_URL=None)
    def test_unconfigured_origin_uses_relative_alternates(self):
        response = self.client.get('/fr/about/')
        self.assertNotContains(response, 'rel="canonical"')
        self.assertContains(response, 'hreflang="en" href="/en/about/"')

    def test_infrastructure_routes_are_not_prefixed(self):
        for name, path in [('health', '/health/'), ('robots', '/robots.txt'), ('sitemap', '/sitemap.xml')]:
            with translation.override('fr'):
                self.assertEqual(reverse(name), path)
            self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.client.get('/fr/health/').status_code, 404)
        self.assertEqual(self.client.post('/i18n/setlang/').status_code, 404)

    @override_settings(SITE_URL='https://www.acoeursconsulting.com', SITE_NOINDEX=False)
    def test_sitemap_contains_all_39_urls_and_robots_allows_languages(self):
        response = self.client.get('/sitemap.xml')
        tree = ElementTree.fromstring(response.content)
        urls = {node.text for node in tree.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
        expected = set()
        for language in ('zh', 'fr', 'en'):
            with translation.override(language):
                expected.update('https://www.acoeursconsulting.com' + reverse(name) for name in PUBLIC_PAGE_ROUTES)
        self.assertEqual(urls, expected)
        robots = self.client.get('/robots.txt')
        self.assertNotContains(robots, 'Disallow: /fr/')
        self.assertNotContains(robots, 'Disallow: /en/')

    def test_legacy_redirects_preserve_language(self):
        targets = {
            'personal_residency_family': ('personal', ''),
            'personal_property_wealth': ('personal', ''),
            'personal_cross_border_tax_risk': ('personal', ''),
            'consultation': ('contact', ''),
            'case_listed_company_france': ('home', '#case-title'),
        }
        for language in ('zh', 'fr', 'en'):
            with translation.override(language):
                for source, (target, fragment) in targets.items():
                    self.assertRedirects(self.client.get(reverse(source)), reverse(target) + fragment, status_code=301, fetch_redirect_response=False)

    def test_contact_defaults_and_validation_follow_page_language(self):
        for language, name_error, invalid_email in [
            ('zh', '请填写您的姓名。', '请输入有效的电子邮箱地址。'),
            ('fr', 'Veuillez indiquer votre nom.', 'Veuillez saisir une adresse e-mail valide.'),
            ('en', 'Please enter your name.', 'Please enter a valid email address.'),
        ]:
            path = f'/{language}/contact/'
            response = self.client.get(path)
            self.assertEqual(response.context['form']['preferred_language'].value(), language)
            response = self.client.post(path, {**self.payload(language), 'name': '', 'email': 'invalid'})
            self.assertContains(response, name_error)
            self.assertContains(response, invalid_email)
            self.assertEqual(response.context['form']['preferred_language'].value(), language)
            self.assertContains(response, f'href="/{language}/privacy/"')

    @override_settings(CONTACT_RECIPIENT_EMAIL='info@acoeursconsulting.com', DEFAULT_FROM_EMAIL='Acoeurs Consulting <info@acoeursconsulting.com>')
    def test_contact_success_preserves_language_and_internal_email(self):
        for language in ('zh', 'fr', 'en'):
            response = self.client.post(f'/{language}/contact/', self.payload(language))
            self.assertRedirects(response, f'/{language}/contact/?submitted=1', fetch_redirect_response=False)
            self.assertNotIn('django_language', response.cookies)
            message = mail.outbox[-1]
            self.assertEqual(message.to, ['info@acoeursconsulting.com'])
            self.assertEqual(message.from_email, settings.DEFAULT_FROM_EMAIL)
            self.assertEqual(message.reply_to, ['sender@example.com'])
            self.assertIn('身份：企业或机构', message.body)
            self.assertIn('欧洲市场进入与战略', message.subject)
        self.assertEqual(len(mail.outbox), 3)

    def test_contact_allows_another_communication_language(self):
        response = self.client.post('/fr/contact/', self.payload('en'))
        self.assertRedirects(response, '/fr/contact/?submitted=1', fetch_redirect_response=False)
        self.assertIn('沟通语言：English', mail.outbox[-1].body)

    def test_contact_failure_is_localized_and_keeps_values(self):
        for language, error in [('zh', '信息暂时未能发送'), ('fr', 'Votre message n’a pas pu être envoyé'), ('en', 'Your message could not be sent')]:
            with patch('website.views.send_contact_email', side_effect=RuntimeError('test failure')):
                with self.assertLogs('website.views', level='ERROR'):
                    response = self.client.post(f'/{language}/contact/', self.payload(language))
            self.assertContains(response, error)
            self.assertContains(response, 'sender@example.com')
            self.assertEqual(response.context['current_step'], 3)
            self.assertTrue(response.context['send_failed'])
            self.assertEqual(response.wsgi_request.path, f'/{language}/contact/')

    def test_url_language_overrides_browser_and_existing_language_cookie(self):
        self.client.cookies['django_language'] = 'en'
        response = self.client.get('/fr/contact/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertContains(response, '<html lang="fr">')
        self.assertEqual(response.context['form']['preferred_language'].value(), 'fr')
        self.assertNotIn('django_language', response.cookies)

    @override_settings(DEBUG=False)
    def test_existing_error_pages_follow_language(self):
        for language, phrase in [('zh', '页面未找到'), ('fr', 'Page introuvable'), ('en', 'Page Not Found')]:
            response = self.client.get(f'/{language}/missing-page/')
            self.assertEqual(response.status_code, 404)
            self.assertIn(phrase, response.content.decode())
            self.assertTemplateUsed(response, '404.html')

    def test_compiled_catalogs_contain_no_empty_public_translations(self):
        for language in ('fr', 'en'):
            with (Path(settings.BASE_DIR) / 'locale' / language / 'LC_MESSAGES' / 'django.mo').open('rb') as stream:
                catalog = gettext.GNUTranslations(stream)
            self.assertGreater(len(catalog._catalog), 900)
            self.assertTrue(all(value for key, value in catalog._catalog.items() if key))
