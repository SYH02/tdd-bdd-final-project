# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #
    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None

        # Save the product using SQLAlchemy
        db.session.add(product)
        db.session.commit()

        self.assertIsNotNone(product.id)

        found_product = Product.query.get(product.id)  # Use query.get for SQLAlchemy

        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.id = None
        product.save()
        self.assertIsNotNone(product.id)

        # Update product description
        product.description = "testing"
        original_id = product.id

        # Save the updated product using SQLAlchemy
        db.session.add(product)
        db.session.commit()

        # Assert updated properties
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "testing")

        # Fetch updated product
        fetched_product = Product.query.get(product.id)

        # Assert fetched product has updated description
        self.assertEqual(fetched_product.description, "testing")


    def test_delete_a_product(self):
        """It should Delete a Product"""

        product = ProductFactory()
        product.save()

        # Verify product creation
        all_products = Product.objects.all()
        self.assertEqual(len(all_products), 1)

        # Delete the product
        product.delete()

        # Verify product deletion
        all_products = Product.objects.all()
        self.assertEqual(len(all_products), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""

        self.assertEqual(len(Product.all()), 0)

        products = [ProductFactory() for _ in range(5)]
        for product in products:
            product.save()

        self.assertEqual(len(Product.all()), 5)


    def test_find_by_name(self):
        """It should Find a Product by Name"""

        products = ProductFactory.create_batch(5)

        # Save each product explicitly
        for product in products:
            product.save()

        # Get the name of the first product
        name = products[0].name

        # Count occurrences of the name
        count = len([product for product in products if product.name == name])

        # Find products by name
        found_products = Product.find_by_name(name)

        # Assert count and names
        self.assertEqual(len(found_products), count)
        for product in found_products:
            self.assertEqual(product.name, name)


    def test_find_by_availability(self):
        """It should Find Products by Availability"""

        products = ProductFactory.create_batch(10)
        for product in products:
            product.save()

        available = products[0].available
        count = len([product for product in products if product.available == available])

        found_products = Product.find_by_availability(available)

        self.assertEqual(len(found_products), count)
        for product in found_products:
            self.assertEqual(product.available, available)

    def test_find_by_category(self):
        """It should Find Products by Category"""

        # Create a batch of products
        products = ProductFactory.create_batch(10)

        # Save products to the database
        for product in products:
            product.save()

        # Get the category of the first product
        category = products[0].category

        # Count occurrences of the category
        category_count = len([product for product in products if product.category == category])

        # Find products by category
        found_products = Product.find_by_category(category)

        # Assert count and categories
        self.assertEqual(len(found_products), category_count)
        for product in found_products:
            self.assertEqual(product.category, category)


    def test_find_by_category(self):
        """It should Find Products by Category"""

        # Create a batch of products
        products = ProductFactory.create_batch(10)

        # Save products to the database
        for product in products:
            product.save()

        # Get the category of the first product
        category = products[0].category

        # Count occurrences of the category
        category_count = len([product for product in products if product.category == category])

        # Find products by category
        found_products = Product.find_by_category(category)

        # Assert count and categories
        self.assertEqual(len(found_products), category_count)
        for product in found_products:
            self.assertEqual(product.category, category)
