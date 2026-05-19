from .models import SiteSettings, SliderImage

def global_data(request):
    return {
        'site_settings': SiteSettings.objects.first(),
        'sliders': SliderImage.objects.filter(is_active=True)
    }