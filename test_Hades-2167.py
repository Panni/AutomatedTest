from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pytest


class TestHades2167:
    def setup_class(self):
        self.url = 'https://newkf-test.topchitu.com/callback.shtml?top_appkey=12090519&top_parameters=c3ViX3Rhb2Jhb191c2VyX25pY2s9sMK25LzSys7Tw8a3xuy9orXqJnRzPTE0Njg2MzY5MzA0NDQmdmlzaXRvcl9pZD0xMDA3MjczNzMmdmlzaXRvcl9uaWNrPbDCtuS80srO08PGt8bsvaK16g%3D%3D&top_session=6100308ba2bcefc817ffc15338f8e2c29ef13a18a4e6d23100727373&timestamp=2016-07-16+10%3A42%3A10&agreement=true&agreementsign=12090519-23224472-436003520-F10E5819E2EBDEEABA333BA5B2C8C1CE&top_sign=zqTm5BN1%2FJpUM2JL6J%2FsMg%3D%3D'
        self.wwMenu = ['汇总', '询单', '下单', '付款', '协助服务', '客单价分析', '成功率分析', '工作量分析', '分时接待分析', '接待压力分析', '议价能力分析',
                       '退款情况分析',
                       '退款率分析', '中差评分析', '值班情况分析', 'E客服评价分析', '商品咨询分析', '商品推荐分析', '商品销售分析']
        self.shopMenu = ['汇总', '询单', '下单', '协助服务', '客单价分析', '成功率分析', '工作量分析', '分时接待分析', '接待压力分析', '中差评分析', '退款情况分析',
                         '退款率分析',
                         '邮费分析']

        self.dr = webdriver.Firefox()
        self.dr.get(self.url)

    def teardown_class(self):
        self.dr.quit()

    # 验证店铺绩效所有页面，快捷时间下拉框都无“最近1天(延）”选项
    def test_shop(self):
        self.dr.find_element_by_xpath('//a[text()="店铺绩效"]').click()
        shopPage = ''
        flag = False;

        for sub in self.shopMenu:

            self.dr.find_element_by_link_text(sub).click()
            try:
                quickTime = self.dr.find_element_by_xpath('//div[text()="快捷时间"]')
            except NoSuchElementException:
                continue

            quickTime.click()
            ul = self.dr.find_element_by_xpath('//div[text()="快捷时间"]/../ul')
            numLi = ul.find_elements_by_tag_name('li')
            if (len(numLi) == 7):
                flag=True
                shopPage = shopPage + '\t' + sub

        #assert flag == False

        try:
            assert flag == False
        except AssertionError:
            print("店铺绩效以下页面测试不通过：\n"+shopPage)

    # 验证客服绩效下，部分页面快捷时间下拉框有延迟项
    def test_ww(self):
        self.dr.find_element_by_xpath('//a[text()="客服绩效"]').click()
        rightPage = '汇总询单下单协助服务成功率分析';# 应只有这些页面快捷时间下拉框，才有“最近延迟（1天）”
        wwPage = ''

        for sub in self.wwMenu:

            self.dr.find_element_by_link_text(sub).click()
            try:
                quickTime = self.dr.find_element_by_xpath('//div[text()="快捷时间"]')
            except NoSuchElementException:
                continue

            quickTime.click()
            ul = self.dr.find_element_by_xpath('//div[text()="快捷时间"]/../ul')
            numLi = ul.find_elements_by_tag_name('li')
            if (len(numLi) == 7):
                wwPage += sub

        assert wwPage == rightPage
