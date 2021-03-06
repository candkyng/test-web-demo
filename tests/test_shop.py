import pytest

from data.shop_data import ShopData
from pages.homepage import Homepage
from testutil.base_class import BaseClass


class TestPhoneShop(BaseClass):

    @pytest.fixture(params=ShopData.get_data_all())
    def data_e2e(self, request):
        return request.param

    def test_e2e(self, data_e2e):
        log = self.get_logger()
        self.log_testdata_info(log, data_e2e)

        # Test Data
        products_to_buy = [x.strip() for x in str(data_e2e['products']).split(',')]
        search_destination = data_e2e['search_country']
        ship_to_destination = data_e2e['country']
        success_message_expected = ShopData.SUCCESS_MSG_EXPECTED

        # Steps and Assertions
        homepage = Homepage(self.driver, self.test_url)
        homepage.goto()
        product_page = homepage.click_shop_button()
        product_page.add_products_to_cart(products_to_buy)
        assert product_page.get_checkout_number() == len(products_to_buy)

        cart_page = product_page.click_checkout_button()
        products_in_cart = cart_page.get_products()
        product_names_in_cart = [p.name for p in products_in_cart]
        assert product_names_in_cart == products_to_buy

        product_totals_in_cart = [p.total for p in products_in_cart]
        assert sum(product_totals_in_cart) == cart_page.get_total()

        checkout_page = cart_page.click_checkout_button()
        checkout_page.enter_destination(search_destination)
        checkout_page.select_destination_from_dropdown(ship_to_destination)
        assert ship_to_destination == checkout_page.get_destination()

        checkout_page.click_agree_condition()
        checkout_page.click_purchase_button()
        assert success_message_expected in checkout_page.get_success_text()
