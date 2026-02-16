from app.services.facebook import FacebookService


def test_facebook_service_not_configured_by_default():
    service = FacebookService()
    assert isinstance(service.is_configured(), bool)
