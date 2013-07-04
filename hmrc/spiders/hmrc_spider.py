import re
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.utils.url import canonicalize_url, parse_url


from hmrc.items import HmrcItem

IGNORED_EXTENSIONS = [
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a',

    # office suites
    #'xls', 'ppt', 'doc', 'docx', 'odt', 'ods', 'odg', 'odp',

    # other
    'css', #'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar',
]

def my_canonicalize_url(url):
    url = canonicalize_url(url)
    scheme, netloc, path, params, query, fragment = parse_url(url)
    # case sensitivity
    path = path.lower()
    # www.hmrc.gov.uk and hmrc.gov.uk are the same
    if netloc == 'hmrc.gov.uk':
        netloc = 'www.hmrc.gov.uk'
    # Fix manuals links with multiple slashes
    path = re.sub(r'^/+', '/', path)
    # Fix customs.hmrc with session tokens in path (!?)
    if params and path.endswith('.portal'):
        params = ''
    url = urlparse.urlunparse((scheme, netloc, path, params, query, fragment))
    return url

class CanonicalizingLinkExtractor(SgmlLinkExtractor):

    def _link_allowed(self, link):
        allowed = SgmlLinkExtractor._link_allowed(self, link)
        if allowed and self.canonicalize:
            link.url = my_canonicalize_url(link.url)
        return allowed

class HmrcSpider(CrawlSpider):
    name = "hmrc"
    allowed_domains = ["hmrc.gov.uk"]
    start_urls = [
        "http://www.hmrc.gov.uk/////sa/index.htm",
        "http://www.hmrc.gov.uk/practitioners/index.shtml",
        "http://www.hmrc.gov.uk/individuals/index.shtml",
        "http://www.hmrc.gov.uk/menus/contactus.shtml",
        "http://www.hmrc.gov.uk/online/index.htm",
        "http://www.hmrc.gov.uk/vat/index.htm",
        "http://www.hmrc.gov.uk/employers/index.shtml",
        "http://www.hmrc.gov.uk/sa/file-online.htm",
        "http://www.hmrc.gov.uk/incometax/index.htm",
        "http://www.hmrc.gov.uk/taxcredits/index.htm",
        "http://www.hmrc.gov.uk/allforms.shtml",
        "http://www.hmrc.gov.uk/paye/index.htm",
        "http://www.hmrc.gov.uk/selfemployed/index.shtml",
        "http://www.hmrc.gov.uk/news/index.htm",
        "http://www.hmrc.gov.uk/sa/forms/content.htm",
        "http://www.hmrc.gov.uk/sa/your-tax-return.htm",
        "http://www.hmrc.gov.uk/employers/epa.htm",
        "http://www.hmrc.gov.uk/jobs/index.htm",
        "http://www.hmrc.gov.uk/businesses/index.shtml",
        "http://www.hmrc.gov.uk/paye/new-services.htm",
        "http://www.hmrc.gov.uk/taxcredits/who-qualifies.htm",
        "http://www.hmrc.gov.uk/incometax/tax-right.htm",
        "http://www.hmrc.gov.uk/taxcredits/entitlement.htm",
        "http://www.hmrc.gov.uk/saemployees/fagsa100.shtml",
        "http://www.hmrc.gov.uk/thelibrary/manuals.htm",
        "http://www.hmrc.gov.uk/pbr2008/index.htm",
        "http://www.hmrc.gov.uk/businesses/tmacorporate-tax.shtml",
        "http://www.hmrc.gov.uk/thelibrary/rates.htm",
        "http://www.hmrc.gov.uk/pbr2008/measure1.htm",
        "http://www.hmrc.gov.uk/childbenefit/who-qualifies.htm",
        "http://www.hmrc.gov.uk/individuals/tmanational-insurance.shtml",
        "http://www.hmrc.gov.uk/childbenefit/online.htm",
        "http://www.hmrc.gov.uk/ctsa/index.htm",
        "http://www.hmrc.gov.uk/individuals/fgcategories_individuals.shtml",
        "http://www.hmrc.gov.uk/individuals/",
        "http://www.hmrc.gov.uk/incometax/refund-reclaim.htm",
        "http://www.hmrc.gov.uk/individuals/moreiwt.shtml#individuals",
        "http://www.hmrc.gov.uk/childbenefit/claiming.htm",
        "http://www.hmrc.gov.uk/individuals/moretma.shtml#individuals",
        "http://www.hmrc.gov.uk/pensionschemes/online/online-splash.htm",
        "http://www.hmrc.gov.uk/childbenefit/index.htm",
        "http://www.hmrc.gov.uk/menus/aboutmenu.htm",
        "http://www.hmrc.gov.uk/agents/forms.htm",
        "http://www.hmrc.gov.uk/employers/rates_and_limits.htm",
        "http://www.hmrc.gov.uk/taxcredits/do-you-qualify.htm",
        "http://www.hmrc.gov.uk/individuals/faq.htm",
        "http://www.hmrc.gov.uk/childbenefit/payments.htm",
        "http://www.hmrc.gov.uk/taxcredits/claiming.htm",
        "http://www.hmrc.gov.uk/agents/contacting.htm",
        "http://www.hmrc.gov.uk/howtopay/menu.htm",
        "http://www.hmrc.gov.uk/pensioners/index.htm",
        "http://www.hmrc.gov.uk/calcs/paye.htm",
        "http://www.hmrc.gov.uk/nav/index.htm",
        "http://www.hmrc.gov.uk/businesses/tmastarting-up-in-business.shtml",
        "http://www.hmrc.gov.uk/selfemployed/",
        "http://www.hmrc.gov.uk/sa/payments-refunds.htm",
        "http://www.hmrc.gov.uk/thelibrary/",
        "http://www.hmrc.gov.uk/newemployers/index.shtml",
        "http://www.hmrc.gov.uk/thelibrary/publications.htm",
        "http://www.hmrc.gov.uk/contractors/",
        "http://www.hmrc.gov.uk/incometax/intro-income-tax.htm",
        "http://www.hmrc.gov.uk/cto/forms3.htm",
        "http://www.hmrc.gov.uk/agents/authorisation.htm",
        "http://www.hmrc.gov.uk/employers/",
        "http://www.hmrc.gov.uk/sa/self-emp-part.htm",
        "http://www.hmrc.gov.uk/paye/exb.htm",
        "http://www.hmrc.gov.uk/",
        "http://www.hmrc.gov.uk/leaflets/cgtfs1.htm",
        "http://www.hmrc.gov.uk/employers/moretma.shtml#employers",
        "http://www.hmrc.gov.uk/taxcredits/changes-home-work.htm",
        "http://www.hmrc.gov.uk/vat/vat-registering.htm",
        "http://www.hmrc.gov.uk/taxcredits/calculator.htm",
        "http://www.hmrc.gov.uk/security/spoofs.htm",
        "http://www.hmrc.gov.uk/so/index.htm",
        "http://www.hmrc.gov.uk/calcs/nice.htm",
        "http://www.hmrc.gov.uk/vat/vat-introduction.htm",
        "http://www.hmrc.gov.uk/paye/intro-register.htm",
        "http://www.hmrc.gov.uk/childbenefit/aged-16-over.htm",
        "http://www.hmrc.gov.uk/childbenefit/changes-to-report.htm",
        "http://www.hmrc.gov.uk/cgt/index.htm",
        "http://www.hmrc.gov.uk/forms/sa102.pdf",
        "http://www.hmrc.gov.uk/taxcredits/forms-leaflets.htm",
        "http://www.hmrc.gov.uk/calcs/cars.htm",
        "http://www.hmrc.gov.uk/incometax/tax-codes.htm",
        "http://www.hmrc.gov.uk/vat/vat-ret-pay-ref.htm",
        "http://www.hmrc.gov.uk/selfemployed/fagsa103.shtml",
        "http://www.hmrc.gov.uk/childbenefit/change-circs.htm",
        "http://www.hmrc.gov.uk/pbr2008/personal-tax.htm",
        "http://www.hmrc.gov.uk/incometax/allowance-relief.htm",
        "http://www.hmrc.gov.uk/employers/moreiwt.shtml#employers",
        "http://www.hmrc.gov.uk/businesses/iwtregister-a-new-business.shtml",
        "http://www.hmrc.gov.uk/vat/vat-sales-purchases.htm",
        "http://www.hmrc.gov.uk/cis/cis-intro.htm",
        "http://www.hmrc.gov.uk/businesses/moretma.shtml#businesses",
        "http://www.hmrc.gov.uk/cto/iht/tnrb.htm",
        "http://www.hmrc.gov.uk/charities/index.htm",
        "http://www.hmrc.gov.uk/employers/fgcategories_employers.shtml",
        "http://www.hmrc.gov.uk/sa/help-using-online.htm",
        "http://www.hmrc.gov.uk/paye/exb-intro.htm",
        "http://www.hmrc.gov.uk/paye/statutorypayements.htm",
        "http://www.hmrc.gov.uk/paye/payments.htm",
        "http://www.hmrc.gov.uk/ctsa/guide.htm",
        "http://www.hmrc.gov.uk/faqs/nicqc1.htm#5",
        "http://www.hmrc.gov.uk/childbenefit/forms.htm",
        "http://www.hmrc.gov.uk/individuals/fgcat-taxback.shtml",
        "http://www.hmrc.gov.uk/vat/ret-complete.htm",
        "http://www.hmrc.gov.uk/employers/fagp46.shtml",
        "http://www.hmrc.gov.uk/employers/fagp45.shtml",
        "http://www.hmrc.gov.uk/paye/statutorypayments-ssp.htm",
        "http://www.hmrc.gov.uk/pensionsschemes/index.shtml",
        "http://www.hmrc.gov.uk/incometax/report-changes.htm",
        "http://www.hmrc.gov.uk/paye/splash.htm",
        "http://www.hmrc.gov.uk/vat/reg-vat.htm",
        "http://www.hmrc.gov.uk/taxcredits/payments.htm",
        "http://www.hmrc.gov.uk/cto/customerguide/page1.htm",
        "http://www.hmrc.gov.uk/pbr2008/business-payment.htm",
        "http://www.hmrc.gov.uk/cto/iht.htm",
        "http://www.hmrc.gov.uk/paye/intro.htm",
        "http://www.hmrc.gov.uk/guidance/cgt-introduction.pdf",
        "http://www.hmrc.gov.uk/paye/exb-stepbystep.htm",
        "http://www.hmrc.gov.uk/leaflets/menu.htm",
        "http://www.hmrc.gov.uk/individuals/fgcat-claimingarepayment.shtml",
        "http://www.hmrc.gov.uk/paye/onlinefiling-understanding.htm",
        "http://www.hmrc.gov.uk/nonresidents/",
        "http://www.hmrc.gov.uk/agents/started.htm",
        "http://www.hmrc.gov.uk/paye/statutorypayments-smp.htm",
        "http://www.hmrc.gov.uk/paye/newemployees.htm",
        "http://www.hmrc.gov.uk/businesses/iwtfile-our-corporate-tax-return-and-accounts.shtml",
        "http://www.hmrc.gov.uk/dealingwith/reporting-changes.htm",
        "http://www.hmrc.gov.uk/vat/vat-account-choose.htm",
        "http://www.hmrc.gov.uk/menus/help.htm",
        "http://www.hmrc.gov.uk/pensioners/approaching.htm",
        "http://www.hmrc.gov.uk/taxcredits/renewing-claim.htm",
        "http://www.hmrc.gov.uk/dealingwith/complain.htm",
        "http://www.hmrc.gov.uk/cto/customerguide/page15.htm",
        "http://www.hmrc.gov.uk/rates/menu.htm",
        "http://www.hmrc.gov.uk/taxcredits/if-things-go-wrong.htm",
        "http://www.hmrc.gov.uk/childbenefit/question.htm",
        "http://www.hmrc.gov.uk/employers/orderline.htm",
        "http://www.hmrc.gov.uk/demo/",
        "http://www.hmrc.gov.uk/payetaxpayers/",
        "http://www.hmrc.gov.uk/businesses/fgcategories_businesses.shtml",
        "http://www.hmrc.gov.uk/employers/faq.htm",
        "http://www.hmrc.gov.uk/pensioners/paying.htm",
        "http://www.hmrc.gov.uk/vat/vat-change-reg-details.htm",
        "http://www.hmrc.gov.uk/tools/childbenefit/chbcalc.htm",
        "http://www.hmrc.gov.uk/agents/news.htm",
        "http://www.hmrc.gov.uk/thelibrary/vat.htm",
        "http://www.hmrc.gov.uk/paye/intro-takingon.htm",
        "http://www.hmrc.gov.uk/forms/ca6855.pdf",
        "http://www.hmrc.gov.uk/vat/vat-international.htm",
        "http://www.hmrc.gov.uk/paye/statutorypayments-calcsmp.htm",
        "http://www.hmrc.gov.uk/working/employed.htm",
        "http://www.hmrc.gov.uk/worksheets/sa108-notes.pdf",
        "http://www.hmrc.gov.uk/graduate/index.htm",
        "http://www.hmrc.gov.uk/consultations/index.htm",
        "http://www.hmrc.gov.uk/bst/index.htm",
        "http://www.hmrc.gov.uk/manuals/CG1manual/",
        "http://www.hmrc.gov.uk/paye/statutorypayments-calcssp.htm",
        "http://www.hmrc.gov.uk/childbenefit/parents.htm",
        "http://www.hmrc.gov.uk/paye/onlinefiling.htm",
        "http://www.hmrc.gov.uk/paye/yearround.htm",
        "http://www.hmrc.gov.uk/businesses/faq.htm",
        "http://www.hmrc.gov.uk/cis/getting-started.htm",
        "http://www.hmrc.gov.uk/incometax/arrive-leave-uk.htm",
        "http://www.hmrc.gov.uk/pdfs/2002_03/capital_gains/sa108_notes.pdf",
        "http://www.hmrc.gov.uk/families/",
        "http://www.hmrc.gov.uk/paye/exb-reporting.htm",
        "http://www.hmrc.gov.uk/practitioners/tools-more.shtml",
        "http://www.hmrc.gov.uk/students/",
        "http://www.hmrc.gov.uk/calcs/esi.htm",
        "http://www.hmrc.gov.uk/saemployees/",
        "http://www.hmrc.gov.uk/pensioners/pension.htm",
        "http://www.hmrc.gov.uk/vat/vat-problems.htm",
        "http://www.hmrc.gov.uk/childbenefit/wrong-claim.htm",
        "http://www.hmrc.gov.uk/migrantworkers/index.htm",
        "http://www.hmrc.gov.uk/employers/fagp11-03.shtml",
        "http://www.hmrc.gov.uk/howtopay/corporation_tax.htm",
        "http://www.hmrc.gov.uk/newbusinesses/iwtset-up-as-a-limited-company.shtml",
        "http://www.hmrc.gov.uk/ctsa/returns.htm",
        "http://www.hmrc.gov.uk/calcs/stat-calcs.htm",
        "http://www.hmrc.gov.uk/sa/appeals.htm",
        "http://www.hmrc.gov.uk/employers/fagp11d-03.shtml",
        "http://www.hmrc.gov.uk/cis/returns-records-con.htm",
        "http://www.hmrc.gov.uk/sa/forms/net-07-08.htm",
        "http://www.hmrc.gov.uk/cis/pay-cis.htm",
        "http://www.hmrc.gov.uk/vat/vat-keeping-records.htm",
        "http://www.hmrc.gov.uk/employers/fagp9x-03.shtml",
        "http://www.hmrc.gov.uk/employers/epa-basicrate.htm",
        "http://www.hmrc.gov.uk/vat/account-flat.htm",
        "http://www.hmrc.gov.uk/employers-bulletin/index.htm",
        "http://www.hmrc.gov.uk/cto/pa.htm",
        "http://www.hmrc.gov.uk/about/foi.htm",
        "http://www.hmrc.gov.uk/cto/glossary.htm",
        "http://www.hmrc.gov.uk/cto/practitioners.htm",
        "http://www.hmrc.gov.uk/howtopay/inheritance.htm",
        "http://www.hmrc.gov.uk/calcs/stc.htm",
        "http://www.hmrc.gov.uk/cgt/disposal.htm",
        "http://www.hmrc.gov.uk/rates/cgt.htm",
        "http://www.hmrc.gov.uk/comment/index.htm",
        "http://www.hmrc.gov.uk/paye/statutorypayments-spp.htm",
        "http://www.hmrc.gov.uk/menus/help-technical.htm",
        "http://www.hmrc.gov.uk/thelibrary/legislation.htm",
        "http://www.hmrc.gov.uk/cto/online.htm",
        "http://www.hmrc.gov.uk/newbusinesses/",
        "http://www.hmrc.gov.uk/paye/onlinefiling-deadlines.htm",
        "http://www.hmrc.gov.uk/agents/news-agents.htm",
        "http://www.hmrc.gov.uk/employers/fagp46car_02.shtml",
        "http://www.hmrc.gov.uk/paye/daytoday.htm",
        "http://www.hmrc.gov.uk/employers/iwtcalculate-a-deemed-payment.shtml",
        "http://www.hmrc.gov.uk/calcs/nicd.htm",
        "http://www.hmrc.gov.uk/pensioners/reducing.htm",
        "http://www.hmrc.gov.uk/vat/vat-agents.htm",
        "http://www.hmrc.gov.uk/cis/forms-sheet-gloss.htm",
        "http://www.hmrc.gov.uk/pensioners/claiming.htm",
        "http://www.hmrc.gov.uk/calcs/ccin.htm",
        "http://www.hmrc.gov.uk/partnerships/",
        "http://www.hmrc.gov.uk/employers/stoppress.htm",
        "http://www.hmrc.gov.uk/payeonline/online-filing2008.htm#100taxfree",
        "http://www.hmrc.gov.uk/news/hartnett-poynter-icc.htm",
        "http://www.hmrc.gov.uk/contactus/special-needs.htm",
        "http://www.hmrc.gov.uk/cgt/faqs-cgt-reform.htm",
        "http://www.hmrc.gov.uk/pensioners/understanding.htm",
        "http://www.hmrc.gov.uk/childbenefit/customer-update.htm",
        "http://www.hmrc.gov.uk/employers/payefunding.htm",
        "http://www.hmrc.gov.uk/vat/vat-consumers.htm",
        "http://www.hmrc.gov.uk/families/fagch2.shtml",
        "http://www.hmrc.gov.uk/paye/endtaxyear.htm",
        "http://www.hmrc.gov.uk/paye/endtaxyear-p14.htm",
        "http://www.hmrc.gov.uk/cgt/cgt-recent-developments.pdf",
        "http://www.hmrc.gov.uk/vat/vat-charities.htm",
        "http://www.hmrc.gov.uk/cis/ensure-you-comply.htm",
        "http://www.hmrc.gov.uk/cto/iht/whatsnew.htm",
        "http://www.hmrc.gov.uk/employers/fagssp2.shtml",
        "http://www.hmrc.gov.uk/budget2007/index.htm",
        "http://www.hmrc.gov.uk/migrantworkers/migrantworkers-release.htm",
        "http://www.hmrc.gov.uk/taxon/bank.htm",
        "http://www.hmrc.gov.uk/sa/trustees-charities.htm",
        "http://www.hmrc.gov.uk/demo/organisation/index.html",
        "http://www.hmrc.gov.uk/agents/index.htm",
        "http://www.hmrc.gov.uk/so/dar/dar-search.htm",
        "http://www.hmrc.gov.uk/calcs/mrr.htm",
        "http://www.hmrc.gov.uk/agents/yoursay.htm",
        "http://www.hmrc.gov.uk/podcasts/index.htm",
        "http://www.hmrc.gov.uk/sa/who-has-died.htm",
        "http://www.hmrc.gov.uk/ebu/psu.htm",
        "http://www.hmrc.gov.uk/employers/diary.htm",
        "http://www.hmrc.gov.uk/businesses/tmarandd-tax-credits.shtml",
        "http://www.hmrc.gov.uk/working/index.htm",
        "http://www.hmrc.gov.uk/trusts/",
        "http://www.hmrc.gov.uk/about/accessibility.htm",
        "http://www.hmrc.gov.uk/pensioners/passing.htm",
        "http://www.hmrc.gov.uk/largecompanies/",
        "http://www.hmrc.gov.uk/thelibrary/research.htm",
        "http://www.hmrc.gov.uk/cgt/cg34.htm",
        "http://www.hmrc.gov.uk/paye/statutorypayments-calcspp.htm",
        "http://www.hmrc.gov.uk/largecompanies/tmalarge-business-office.shtml",
        "http://www.hmrc.gov.uk/paye/forms-publications.htm",
        "http://www.hmrc.gov.uk/employers/talk.htm",
        "http://www.hmrc.gov.uk/budget/index.htm",
        "http://www.hmrc.gov.uk/paye/more-tools.htm",
        "http://www.hmrc.gov.uk/cto/iht/northernrock-qa.htm",
        "http://www.hmrc.gov.uk/about/new-penalties/",
        "http://www.hmrc.gov.uk/cymraeg/index.htm",
        "http://www.hmrc.gov.uk/cgt/entre-relief-en.pdf",
        "http://www.hmrc.gov.uk/working/casual.htm",
        "http://www.hmrc.gov.uk/carter/compulsory-deadlines.htm",
        "http://www.hmrc.gov.uk/employers/emp-form.htm",
        "http://www.hmrc.gov.uk/sa/forms/net-05-06.htm#cgt",
        "http://www.hmrc.gov.uk/cgt/entre-faqs.htm",
        "http://www.hmrc.gov.uk/taxon/index.htm",
        "http://www.hmrc.gov.uk/library.htm",
        "http://www.hmrc.gov.uk/dealingwith/appeals.htm",
        "http://www.hmrc.gov.uk/working/self-employed.htm",
        "http://www.hmrc.gov.uk/menus/links.htm",
        "http://www.hmrc.gov.uk/enq/index.htm",
        "http://www.hmrc.gov.uk/demo/organisation/corporation-tax/file-a-return/page1.html",
        "http://www.hmrc.gov.uk/pensioners/paying-retire.htm",
        "http://www.hmrc.gov.uk/sa/pension-scheme.htm",
        "http://www.hmrc.gov.uk/charities/charities-search.htm",
        "http://www.hmrc.gov.uk/terms/",
        "http://www.hmrc.gov.uk/pensionschemes/tax-simp-forms.htm",
        "http://www.hmrc.gov.uk/cymraeg/sa/index.htm",
        "http://www.hmrc.gov.uk/dealingwith/index.htm",
        "http://www.hmrc.gov.uk/cgt/entre-relief-draft.pdf",
        "http://www.hmrc.gov.uk/working/forms.htm",
        "http://www.hmrc.gov.uk/calcs/r85/",
        "http://www.hmrc.gov.uk/payinghmrc/index.htm",
        "http://www.hmrc.gov.uk/cto/heritage.htm",
        "http://www.hmrc.gov.uk/paye/onlinefiling-register.htm",
        "http://www.hmrc.gov.uk/incometax/relief-charity.htm",
        "http://www.hmrc.gov.uk/stats/update_calendar/enquiry_2.htm",
        "http://www.hmrc.gov.uk/individuals/moretma.shtml#pensioners",
        "http://www.hmrc.gov.uk/cgt/cgt-reform-draft.pdf",
        "http://www.hmrc.gov.uk/online/service-availability.htm",
        "http://www.hmrc.gov.uk/carter/sa-deadlines.htm",
        "http://www.hmrc.gov.uk/paye/intro-choosing.htm",
        "http://www.hmrc.gov.uk/cis/lb-pub-nonuk.htm",
        "http://www.hmrc.gov.uk/cgt/archive.htm",
        "http://www.hmrc.gov.uk/working/first-job.htm",
        "http://www.hmrc.gov.uk/taxon/uk.htm",
        "http://www.hmrc.gov.uk/comment/wcp-feedback.htm",
        "http://www.hmrc.gov.uk/taxon/savings.htm",
        "http://www.hmrc.gov.uk/eis/index.htm",
        "http://www.hmrc.gov.uk/tdsi/key-info.htm",
        "http://www.hmrc.gov.uk/pensioners/help.htm",
        "http://www.hmrc.gov.uk/worksheets/2007/sa108-notes.pdf",
        "http://www.hmrc.gov.uk/local/index.htm",
        "http://www.hmrc.gov.uk/cto/index.htm",
        "http://www.hmrc.gov.uk/calcs/r85/index.htm",
        "http://www.hmrc.gov.uk/contactus/staustellform.htm",
        "http://www.hmrc.gov.uk/payinghmrc/vat.htm",
        "http://www.hmrc.gov.uk/tools/inheritancetax/interest-rate-calculator.htm",
        "http://www.hmrc.gov.uk/copyright/",
        "http://www.hmrc.gov.uk/carter/managing.htm",
        "http://www.hmrc.gov.uk/paye/statutorypayments-sap.htm",
        "http://www.hmrc.gov.uk/cgt/cgt-reform-en.pdf",
        "http://www.hmrc.gov.uk/pensioners/approaching-notify.htm",
        "http://www.hmrc.gov.uk/businesses/fageis1.shtml",
        "http://www.hmrc.gov.uk/taxon/foreign.htm",
        "http://www.hmrc.gov.uk/cis/changes-report.htm",
        "http://www.hmrc.gov.uk/casc/index.htm",
        "http://www.hmrc.gov.uk/working/work-out-emp-self-emp.htm",
        "http://www.hmrc.gov.uk/individuals/moreiwt.shtml#pensioners",
        "http://www.hmrc.gov.uk/rewrite/index.htm",
        "http://www.hmrc.gov.uk/paye/daytoday-completing.htm",
        "http://www.hmrc.gov.uk/forms/ca6855.pdf",
        "http://www.hmrc.gov.uk/incometax/contact-hmrc.htm",
        "http://www.hmrc.gov.uk/worksheets/2006/sa108-notes.pdf",
        "http://www.hmrc.gov.uk/about/supplying.htm",
        "http://www.hmrc.gov.uk/about/privacy.htm",
        "http://www.hmrc.gov.uk/online/availability-software.htm",
        "http://www.hmrc.gov.uk/employers/moretma.shtml#newemployers",
        "http://www.hmrc.gov.uk/pensioners/reducing-allowances.htm",
        "http://www.hmrc.gov.uk/sa/forms/net-06-07.htm",
        "http://www.hmrc.gov.uk/shareschemes/sip-info-employees.rtf",
        "http://www.hmrc.gov.uk/incometax/appeal.htm",
        "http://www.hmrc.gov.uk/employers/moreiwt.shtml#newemployers",
        "http://www.hmrc.gov.uk/specialist/esc.pdf",
        "http://www.hmrc.gov.uk/carter/employer-deadlines.htm",
        "http://www.hmrc.gov.uk/employers/first_steps.htm",
        "http://www.hmrc.gov.uk/cgt/negligible_list.htm",
        "http://www.hmrc.gov.uk/cgt/pibs.htm",
        "http://www.hmrc.gov.uk/shareschemes/shares-valuation.htm",
        "http://www.hmrc.gov.uk/working/company-cars.htm",
        "http://www.hmrc.gov.uk/about/trp.htm",
        "http://www.hmrc.gov.uk/taxon/sale-shares.htm",
        "http://www.hmrc.gov.uk/paye/statutorypayments-calcsap.htm",
        "http://www.hmrc.gov.uk/working/tips-bonuses.htm",
        "http://www.hmrc.gov.uk/menus/legalmenu.htm",
        "http://www.hmrc.gov.uk/cgt/gilts-list.htm",
        "http://www.hmrc.gov.uk/carter/tax-agents.htm",
        "http://www.hmrc.gov.uk/heritage/index.htm",
        "http://www.hmrc.gov.uk/dealingwith/dealing-with.htm",
        "http://www.hmrc.gov.uk/carter/get-ready.htm",
        "http://www.hmrc.gov.uk/isa/index.htm",
        "http://www.hmrc.gov.uk/practitioners/sop.pdf",
        "http://www.hmrc.gov.uk/cgt/monthly-savings-schemes.htm",
        "http://www.hmrc.gov.uk/payinghmrc/corporationtax.htm",
        "http://www.hmrc.gov.uk/bst/map.htm",
        "http://www.hmrc.gov.uk/contactus/orderlines.htm",
    ]

    rules = (
        Rule(CanonicalizingLinkExtractor(deny=(r'TellAFriend',),
                                         deny_extensions=IGNORED_EXTENSIONS),
             callback='parse_page',
             follow=True),
    )


    def parse_page(self, response):
        try:
            hxs = HtmlXPathSelector(response)

        except AttributeError:
            # Not an HTML document: PDF/DOC or similar
            item = HmrcItem()
            item['url'] = response.url
            return item

        try:
            title = hxs.select('//title/text()').extract()[0]
        except IndexError:
            title = '[none]'
        try:
            desc = hxs.select('//meta[@name="description"]/@content').extract()[0]
        except IndexError:
            desc = '[none]'
        try:
            head = hxs.select('//h1/text()').extract()[0]
        except IndexError:
            try:
                head = hxs.select('//h2/text()').extract()[0]
            except IndexError:
                try:
                    head = hxs.select('//h2/text()').extract()[0]
                except IndexError:
                    head = '[none]'

        item = HmrcItem()
        item['url'] = response.url
        item['title'] = title
        item['desc'] = desc
        item['head'] = head

        return item
