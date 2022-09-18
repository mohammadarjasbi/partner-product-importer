import json
import xmltodict

from common.utils.logger import getLogger

logger = getLogger("XML Partner Product Transformer")


class XMLPartnerProductTransformer:

    """
    this class is responsible for convert XML data to JSON data and Map them into desired JSON format.

    """

    def __init__(
        self,
        xml_data: str,
        xml_element_namespace="nsx:",
        xml_root_element="items",
        xml_item_element="item",
    ):
        self.json_data = self.__xml_to_json(xml_data)
        self.xml_element_namespace = xml_element_namespace
        self.root_element_key = self.xml_element_namespace + xml_root_element
        self.item_element_key = self.xml_element_namespace + xml_item_element
        self.transformed_product_items = []

    def __xml_to_json(self, xml_data: str):
        return xmltodict.parse(xml_data)

    def __get_attribute(self, data: dict, attribute_key: str):
        return data.get(self.xml_element_namespace + attribute_key)

    def __get_image_url_by_number(self, image_list: list, image_number: int):
        for image_item in image_list:
            if image_item.get("@type") == str(image_number):
                return image_item.get("@url")

    def __product_image_transformer(self, product_images: dict):

        """
        this specific function have responsibility to get image attributes and map them into proper order
        'cause we need return Null for missing image values in JSON data
        """

        image_list = self.__get_attribute(product_images, "image")
        transformed_image_dict = {}
        max_image_number = max(
            int(image_item.get("@type")) for image_item in image_list
        )

        for image_number in range(1, max_image_number + 1):
            image_key = f"image_{image_number}"
            transformed_image_dict[image_key] = self.__get_image_url_by_number(
                image_list, image_number
            )

        return transformed_image_dict

    def __product_price_transformer(self, product_prices: dict):
        price_list = self.__get_attribute(product_prices, "price")
        transformed_price_list = []

        for price_item in price_list:
            transformed_price_list.append(
                {
                    "currency": self.__get_attribute(price_item, "currency"),
                    "value": self.__get_attribute(price_item, "value"),
                }
            )

        return transformed_price_list

    def __product_item_transformer(self, product_item: dict):
        return {
            "product_id": product_item.get("@id"),
            "product_category": self.__get_attribute(product_item, "category"),
            "product_description": self.__get_attribute(product_item, "description"),
            "product_images": self.__product_image_transformer(
                self.__get_attribute(product_item, "images"),
            ),
            "prices": self.__product_price_transformer(
                self.__get_attribute(product_item, "prices"),
            ),
        }

    def transform(self):
        product_items = self.json_data.get(self.root_element_key).get(
            self.item_element_key
        )
        product_transform_counter = 0
        for product_item in product_items:
            try:
                transformed_item = self.__product_item_transformer(product_item)
                self.transformed_product_items.append(transformed_item)
                product_transform_counter += 1
            except Exception as e:
                logger.error(
                    f"Failed to transform item: {json.dumps(product_item)}, error: {e}"
                )

        logger.info(
            f"{product_transform_counter}/{len(product_items)} products transformed successfully"
        )

    def get_json(self):
        return self.transformed_product_items
