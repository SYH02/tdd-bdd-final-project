######################################################################
# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
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
######################################################################

# spell: ignore Rofrano jsonify restx dbname
"""
Product Store Service with UI
"""
from flask import jsonify, request, abort
from flask import url_for  # noqa: F401 pylint: disable=unused-import
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import app


######################################################################
# H E A L T H   C H E C K
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


######################################################################
# H O M E   P A G E
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# C R E A T E   A   N E W   P R O D U C T
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")

    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product = Product()
    product.deserialize(data)
    product.create()
    app.logger.info("Product with new id [%s] saved!", product.id)

    message = product.serialize()

    #
    # Uncomment this line of code once you implement READ A PRODUCT
    #
    # location_url = url_for("get_products", product_id=product.id, _external=True)
    location_url = "/"  # delete once READ is implemented
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# L I S T   A L L   P R O D U C T S
######################################################################

#
# PLACE YOUR CODE TO LIST ALL PRODUCTS HERE
#

######################################################################
# R E A D   A   P R O D U C T
######################################################################

#
# PLACE YOUR CODE HERE TO READ A PRODUCT
#

######################################################################
# U P D A T E   A   P R O D U C T
######################################################################

#
# PLACE YOUR CODE TO UPDATE A PRODUCT HERE
#

######################################################################
# D E L E T E   A   P R O D U C T
######################################################################


#
# PLACE YOUR CODE TO DELETE A PRODUCT HERE
#

def get_product(product_id):
    """
    Retrieves a single Product

    This endpoint will return a Product based on it's id
    """

    app.logger.info("Request to Retrieve a product with id [%s]", product_id)

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.name)
    return product.serialize(), status.HTTP_200_OK


def test_update_product_with_factory(self):
    """Tests updating a product using ProductFactory and asserts changes"""
    # Create a product with the factory
    created_product = ProductFactory()
    response = self.client.post(BASE_URL, json=created_product.serialize())
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Get the created product ID
    product_id = response.get_json()["id"]

    # Prepare updated data with a different description
    updated_data = {
        "name": created_product.name,  # Keep name the same
        "description": "This is a completely new description!",
        "price": created_product.price,  # Keep price the same
        "available": created_product.available,  # Keep availability the same
        "category": created_product.category.id,  # Keep category the same
    }

    # Send the PUT request with updated data
    response = self.client.put(f"{BASE_URL}/{product_id}", json=updated_data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Verify the description has been updated
    updated_product = response.get_json()
    self.assertEqual(updated_product["description"], updated_data["description"])

######

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Updates a product with the provided data.

    Args:
        product_id (int): The ID of the product to be updated.

    Returns:
        tuple: A tuple containing the updated product data (as JSON) and the HTTP status code (200 OK on success).

    Raises:
        HTTPException: A 404 Not Found exception if the product with the provided ID is not found.
        HTTPException: A 415 Unsupported Media Type exception if the request content type is not application/json.
    """

    # Validate content type
    check_content_type("application/json")

    # Find the product by ID
    product = Product.query.get(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with ID {product_id} not found.")

    # Extract and validate update data (optional)
    update_data = request.get_json()
    # You can add validation logic here if needed

    # Update product attributes
    product.update(update_data)

    # Save changes
    db.session.commit()

    # Return the updated product data
    return product.serialize(), status.HTTP_200_OK





def test_delete_product(self):
    """Tests deleting a product and verifies successful deletion.

    This test creates multiple products, deletes the first one,
    and verifies that:
        * The deletion request returns a 204 No Content status code.
        * No data is returned in the response.
        * A subsequent GET request for the deleted product returns a 404 Not Found.
        * The total product count is reduced by 1.
    """

    # Create multiple products
    initial_count = self.get_product_count()
    created_products = self._create_products(5)

    # Select the first product for deletion
    product_to_delete = created_products[0]

    # Send the delete request
    response = self.client.delete(f"{BASE_URL}/{product_to_delete.id}")

    # Assert response status and data
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(len(response.data), 0)

    # Verify deletion by GET request
    response = self.client.get(f"{BASE_URL}/{product_to_delete.id}")
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Verify product count reduction
    new_count = self.get_product_count()
    self.assertEqual(new_count, initial_count - 1)

#########

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Deletes a product with the provided ID.

    Args:
        product_id (int): The ID of the product to be deleted.

    Returns:
        tuple: An empty response body and the HTTP status code (204 No Content on success).

    Raises:
        HTTPException: A 404 Not Found exception if the product with the provided ID is not found.
    """

    # Find the product by ID
    product = Product.query.get(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with ID {product_id} not found.")

    # Delete the product
    product.delete()
    db.session.commit()

    # Return empty response with No Content status
    return "", status.HTTP_204_NO_CONTENT





def test_get_product_list(self):
  """Tests retrieving a list of all products.

  This test creates several products and then sends a GET request to
  the `/products` endpoint. It verifies that:
    * The request returns a 200 OK status code.
    * The response data contains a list of products.
    * The number of products in the response matches the number created.
  """

  # Create multiple products
  created_products = self._create_products(5)

  # Send the GET request to list all products
  response = self.client.get(BASE_URL)

  # Assert response status and data format
  self.assertEqual(response.status_code, status.HTTP_200_OK)
  data = response.get_json()
  self.assertIsInstance(data, list)

  # Verify the number of products matches what was created
  self.assertEqual(len(data), len(created_products))

###########

@app.route("/products", methods=["GET"])
def get_all_products():
  """Retrieves and returns a list of all products.

  Returns:
      tuple: A tuple containing the list of serialized product data 
             and the HTTP status code (200 OK).
  """

  # Fetch all products from the database
  products = Product.query.all()

  # Convert products to serialized data (JSON format)
  serialized_products = [product.serialize() for product in products]
  
  # Return the list of products and success status
  return serialized_products, status.HTTP_200_OK





def test_get_products_by_name(self):
  """Tests retrieving products filtered by name.

  This test creates several products with different names, then sends a GET request to
  the `/products` endpoint with a name query parameter. It verifies that:
    * The request returns a 200 OK status code.
    * The response data contains a list of products.
    * The number of products in the response matches the number with the specified name.
    * All products in the response have the expected name.
  """

  # Create products with different names
  products = self._create_products(5, with_unique_names=True)

  # Select a product name for filtering
  test_name = products[0].name

  # Construct the URL with the query parameter
  url = f"{BASE_URL}?name={quote_plus(test_name)}"

  # Send the GET request to list products by name
  response = self.client.get(url)

  # Assert response status and data format
  self.assertEqual(response.status_code, status.HTTP_200_OK)
  data = response.get_json()
  self.assertIsInstance(data, list)

  # Verify the number of products matches the expected count
  expected_count = sum(1 for p in products if p.name == test_name)
  self.assertEqual(len(data), expected_count)

  # Verify all products have the specified name
  for product in data:
    self.assertEqual(product["name"], test_name)

########

@app.route("/products", methods=["GET"])
def get_products_by_name_or_all():
  """Retrieves and returns products filtered by name (if provided), 
  otherwise returns all products.

  Returns:
      tuple: A tuple containing the list of serialized product data 
             and the HTTP status code (200 OK).
  """

  # Get the name parameter from the query string (if any)
  name = request.args.get("name")

  if name:
    # Filter products by name if a name is provided
    products = Product.query.filter_by(name=name).all()
  else:
    # Fetch all products if no name is specified
    products = Product.query.all()

  # Convert products to serialized data (JSON format)
  serialized_products = [product.serialize() for product in products]
  
  # Return the list of products and success status
  return serialized_products, status.HTTP_200_OK





def test_get_products_by_category(self):
  """Tests retrieving products filtered by category.

  This test creates several products with different categories, then sends a GET request to
  the `/products` endpoint with a category query parameter. It verifies that:
    * The request returns a 200 OK status code.
    * The response data contains a list of products.
    * The number of products in the response matches the number with the specified category.
    * All products in the response have the expected category name.
  """

  # Create products with different categories
  products = self._create_products(10, with_unique_categories=True)

  # Select a product category for filtering
  test_category = products[0].category

  # Construct the URL with the query parameter
  url = f"{BASE_URL}?category={test_category.name}"

  # Send the GET request to list products by category
  response = self.client.get(url)

  # Assert response status and data format
  self.assertEqual(response.status_code, status.HTTP_200_OK)
  data = response.get_json()
  self.assertIsInstance(data, list)

  # Verify the number of products matches the expected count
  expected_count = sum(1 for p in products if p.category == test_category)
  self.assertEqual(len(data), expected_count)

  # Verify all products have the specified category name
  for product in data:
    self.assertEqual(product["category"], test_category.name)

###########

@app.route("/products", methods=["GET"])
def get_products_by_name_category_or_all():
  """Retrieves and returns products filtered by name (if provided), 
  category (if provided), otherwise returns all products.

  Returns:
      tuple: A tuple containing the list of serialized product data 
             and the HTTP status code (200 OK).
  """

  # Get the name parameter from the query string (if any)
  name = request.args.get("name")

  # Get the category parameter from the query string (if any)
  category_name = request.args.get("category")

  if name:
    # Filter products by name if a name is provided (handled in previous logic)
    pass
  elif category_name:
    # Filter products by category if a category is provided
    try:
      # Attempt to convert category name to the corresponding enum value
      category_value = getattr(Category, category_name.upper())
      products = Product.query.filter_by(category=category_value).all()
    except AttributeError:
      # Handle the case where the provided category name doesn't exist 
      abort(status.HTTP_400_BAD_REQUEST, f"Invalid category: {category_name}")
  else:
    # Fetch all products if no name or category is specified
    products = Product.query.all()

  # Convert products to serialized data (JSON format)
  serialized_products = [product.serialize() for product in products]
  
  # Return the list of products and success status
  return serialized_products, status.HTTP_200_OK




def test_get_products_by_availability(self):
  """Tests retrieving products filtered by availability.

  This test creates a mix of available and unavailable products, then sends a GET request to
  the `/products` endpoint with an availability query parameter. It verifies that:
    * The request returns a 200 OK status code.
    * The response data contains a list of products.
    * The number of products in the response matches the number with the specified availability.
    * All products in the response have the expected availability.
  """

  # Create products with a mix of availability
  products = self._create_products(10, with_mixed_availability=True)

  # Separate products based on availability
  available_products = [p for p in products if p.available]
  unavailable_products = [p for p in products if not p.available]

  # Test filtering by available products
  availability_value = "true"
  url = f"{BASE_URL}?available={availability_value}"
  response = self.client.get(url)

  # Assert response status and data format
  self.assertEqual(response.status_code, status.HTTP_200_OK)
  data = response.get_json()
  self.assertIsInstance(data, list)

  # Verify the number of products matches the expected count
  expected_count = len(available_products)
  self.assertEqual(len(data), expected_count)

  # Verify all products have the expected availability
  for product in data:
    self.assertEqual(product["available"], True)

  # (Optional) Test filtering by unavailable products (add similar logic)

################

@app.route("/products", methods=["GET"])
def get_products_by_name_category_availability_or_all():
  """Retrieves and returns products filtered by name (if provided), 
  category (if provided), availability (if provided), otherwise returns all products.

  Returns:
      tuple: A tuple containing the list of serialized product data 
             and the HTTP status code (200 OK).
  """

  # Get the name parameter from the query string (if any)
  name = request.args.get("name")

  # Get the category parameter from the query string (if any)
  category_name = request.args.get("category")

  # Get the availability parameter from the query string (if any)
  availability_str = request.args.get("available")

  if name:
    # Filter products by name if a name is provided (handled in previous logic)
    pass
  elif category_name:
    # Filter products by category if a category is provided (handled in previous logic)
    pass
  elif availability_str:
    # Filter products by availability if an availability parameter is provided
    try:
      # Convert availability string to a boolean value (case-insensitive)
      available_value = availability_str.lower() in ["true", "yes", "1"]
      products = Product.query.filter_by(available=available_value).all()
    except ValueError:
      # Handle the case where the provided availability string is invalid
      abort(status.HTTP_400_BAD_REQUEST, f"Invalid availability value: {availability_str}")
  else:
    # Fetch all products if no name, category, or availability is specified
    products = Product.query.all()

  # Convert products to serialized data (JSON format)
  serialized_products = [product.serialize() for product in products]
  
  # Return the list of products and success status
  return serialized_products, status.HTTP_200_OK







